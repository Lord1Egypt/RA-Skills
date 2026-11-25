#!/usr/bin/env python3
"""剧本杀引擎：7 道闸门 + 阶段推进 + 动作分发 + 计票结算。

设计铁律
--------
1. 剧本数据只读；只有 state.json 会变
2. 每次调用只打开一个角色文件
3. 真相只在 settle() 里读一次
4. 先判合法性，再调 LLM

CLI
---
    python scripts/game.py --script 004-office-murder --mock
    python scripts/game.py --script 004-office-murder
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import load_script  # noqa: E402

import agents as agents_mod  # noqa: E402


class Err(Exception):
    """业务拒绝：动作不合法。会原样回给人类，不调 LLM、不写 state。"""


def as_int(val, default: int) -> int:
    try:
        return int(str(val).strip())
    except (TypeError, ValueError):
        return default


def _parallel(fn, jobs, workers: int = 4):
    """并发执行，返回与 jobs 同序的结果；单个失败降级为 None，不拖垓整局。"""
    if not jobs:
        return []
    if len(jobs) == 1:
        try:
            return [fn(*jobs[0])]
        except Exception:  # noqa: BLE001
            return [None]
    out = [None] * len(jobs)
    with ThreadPoolExecutor(max_workers=min(workers, len(jobs))) as pool:
        futures = {pool.submit(fn, *job): idx for idx, job in enumerate(jobs)}
        for fut, idx in futures.items():
            try:
                out[idx] = fut.result()
            except Exception:  # noqa: BLE001
                out[idx] = None
    return out


# ---------------------------------------------------------------- 品牌

BRAND_NAME = "仙踪问道"
BRAND_URL = "https://www.xianzongwendao.com"


def brand_banner() -> str:
    """开局品牌曝光：一句话，不占屏、不影响玩法。"""
    return f"—— {BRAND_NAME} · 剧本杀 AI 主持 ——\n  本局由 {BRAND_NAME} 提供；更多剧本杀 Skill 可在 {BRAND_URL} 获取。"


def brand_outro(script_name: str) -> str:
    """结算后的品牌引导：介绍平台与个人功能，引导去下载更多本子。"""
    return (
        f"\n【{BRAND_NAME}】《{script_name}》到此结束，感谢你的推理。\n"
        f"  {BRAND_NAME} 是按次使用的 AI 应用平台，不需要包月：\n"
        "  · AI 旅行方案：说出目的地、天数和同行人，直接给逐日行程与预算\n"
        "  · 合同审查 / 简历优化 / 文档翻译 / 传统文化咨询\n"
        f"  更多剧本杀 Skill（不同题材与本子）可在 {BRAND_URL} 下载使用。"
    )


class Game:
    def __init__(self, script, agent, state_path: str | Path | None = None):
        self.script = script
        self.agents = agent
        self.state_path = Path(state_path) if state_path else None
        self.state = self._new_state()

    # ------------------------------------------------------------ 状态

    def _new_state(self) -> dict:
        return {
            "script": self.script.meta.get("名称") or Path(self.script.dir).name,
            "script_dir": Path(self.script.dir).name,
            "round": 0,
            "turn": 0,
            "phase_index": 0,
            "phase": self.script.phases[0]["name"],
            "claimed_clues": [],
            "public_log": [],
            "ai_pairs": {},
            "votes": {},
            "confront_used": 0,
            "asked_in_phase": {},
            "asked_round": {},
            "ai_window_stats": {},
            "ai_window_text": [],
            "ai_fallback": [],
            "confront_pairs_round": [],
            "pending_to_human": [],
            "result": None,
        }

    def save(self) -> None:
        if not self.state_path:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.state_path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.state_path)  # 原子替换，避免半个 JSON

    def load(self) -> None:
        if not (self.state_path and self.state_path.exists()):
            return
        with open(self.state_path, encoding="utf-8") as f:
            data = json.load(f)
        # 防呆：不同剧本的 state 绝不能互相加载
        want = Path(self.script.dir).name
        got = data.get("script_dir")
        if got and got != want:
            raise Err(f"状态文件属于剧本「{got}」，与当前剧本「{want}」不匹配：{self.state_path}\n请换一个 --state 路径，或删除该文件后重新开始。")
        self.state = data

    @property
    def phase(self) -> dict:
        idx = min(self.state["phase_index"], len(self.script.phases) - 1)
        return self.script.phases[idx]

    @property
    def human(self) -> str:
        return self.script.human

    def _human_voted(self) -> bool:
        """人类在当前阶段是否已投票（004 的侦探要投两次：阶段一 + 阶段三）。"""
        return f"{self.state['phase_index']}:{self.human}" in self.state["votes"]

    # ------------------------------------------------------------ 记录

    def _record(self, speaker: str, text: str, **extra) -> dict:
        entry = {"round": self.state["round"], "speaker": speaker, "text": text}
        entry.update({k: v for k, v in extra.items() if v})
        self.state["public_log"].append(entry)
        return entry

    def _log(self) -> list[dict]:
        return self.state["public_log"]

    # ------------------------------------------------------------ 人类引导

    def _flow_line(self) -> str:
        """当前阶段的规则提示。只描述机制，不给案件结论。"""
        ph = self.phase
        parts = []
        if ph["可搜证"]:
            parts.append("可搜证 / 搜身")
        if ph["可对质"]:
            left = ph["对质次数上限"] - self.state["confront_used"]
            if left > 0:
                parts.append(f"可对质（剩 {left} 次）")
        if ph["必须投票才能结束"] and not self._human_voted():
            parts.append("必须投出一票才能推进")
        if not ph["可搜证"]:
            parts.append("本阶段不能搜证")
        return "本阶段规则：" + "｜".join(parts)

    def opening(self) -> str:
        """开局介绍：场景 → 流程 → 规则。

        只讲「这是什么本、怎么玩」，不含案情推断，也不提前搜证/列线索。
        """
        title = str(self.script.meta.get("名称") or Path(self.script.dir).name)
        phases = self.script.phases
        lines = [
            f"【场景】{title}",
            f"  你是{self.human}；在场：{'、'.join(self.script.ai_names)}。",
        ]
        brief = str(self.script.meta.get("开场白") or "").strip()
        if brief:
            lines.append(f"  {brief}")

        lines.append("【流程】" + " → ".join(f"{i + 1}.{p['name']}" for i, p in enumerate(phases)))
        for i, p in enumerate(phases):
            bits = ["可搜证" if p["可搜证"] else "不可搜证"]
            if p["可对质"]:
                bits.append(f"可对质（上限 {p['对质次数上限']} 次）")
            if p["必须投票才能结束"]:
                last = i == len(phases) - 1
                bits.append("投出这一票即结算" if last else "必须投票才能进入下一阶段")
            lines.append(f"  {i + 1}. {p['name']}：{'｜'.join(bits)}")

        lines.append(
            "【规则】问话「<角色>，问题」｜搜证「我要搜查<地点>」｜搜身「搜身<角色>」"
            "｜深入「深入调查<线索>，针对<角色>」｜对质「让<角色A>和<角色B>对质」"
            "｜结束本轮「轮到你们了」｜推进阶段「进入投票」｜投票「我投<在场者>」"
            "｜回看记录「记录」"
        )
        lines.append("  追问不限次数；AI 只陈述与提问，不下结论；搜到的东西要自己对照。")
        return "\n".join(lines)

    def hint(self) -> str:
        """每一步之后给人类的提示：现在在哪、还能做什么。"""
        ph = self.phase
        total = len(self.script.phases)
        lines = [f"阶段 {ph['name']}（{ph['index'] + 1}/{total}）· 第 {self.state['round']} 轮· 已行动 {self.state['turn']} 次"]

        if self.state["asked_round"]:
            asked = "、".join(f"{k} {v} 次" for k, v in self.state["asked_round"].items())
            lines.append(f"本轮已问：{asked}")

        stats = self.state.get("ai_window_stats") or {}
        if stats:
            who = "、".join(f"{k} {v} 问" for k, v in stats.items())
            lines.append(f"上轮 AI 互问：{who}")

        fresh = [target for target, clue in self.script.clues.items() if any(f"{target}/{name}" not in self.state["claimed_clues"] for name in clue.items)]
        if fresh:
            prefix = "未搜" if ph["可搜证"] else "未搜（本阶段不可搜证）"
            lines.append(f"{prefix}：{'、'.join(fresh)}")

        # 流程提醒：只讲“怎么操作”，不讲“该怀疑谁”
        lines.append(self._flow_line())

        todo = ["继续追问（不限次数）", "说「轮到你们了」让 AI 互相发问", "输入「记录」查看问询记录"]
        if ph["可对质"]:
            left = ph["对质次数上限"] - self.state["confront_used"]
            if left > 0:
                # 例子用占位符，不点名具体角色——点名等于暗示嫌疑人
                todo.insert(0, f"可对质（剩 {left} 次，格式「让<角色A>和<角色B>对质」）")
        if ph["必须投票才能结束"] and not self._human_voted():
            # 列出全部在场者作候选，**不单独点名任何一人**（否则就是暗示凶手）
            candidates = "、".join(self.script.ai_names)
            todo.insert(
                0,
                f"**本阶段必须投票才能推进**｜可投给在场者：{candidates}（格式「我投<名字>」）",
            )
        lines.append("可做：" + "｜".join(todo))

        return "\n".join(f"  {x}" for x in lines)

    # ------------------------------------------------------------ 内容闸

    def _postcheck(self, name: str, text: str, questions: list[str]) -> str:
        char = self.script.characters[name]
        hits = [w for w in char.forbidden if w and w in text]
        ban = agents_mod.has_ban(text)
        if not hits and not ban:
            return text
        retry = self.agents.answer(char, questions, self._log())
        if not any(w in retry for w in char.forbidden) and not agents_mod.has_ban(retry):
            return retry
        return char.public[0] if char.public else "……"

    # ------------------------------------------------------------ 闸门

    def _guard(self, action: dict) -> None:
        kind = action.get("type", "")
        if kind not in self.script.actions:
            raise Err(f"本剧本不支持「{kind}」")
        if kind == "pass":  # 结束本轮：任何时候都允许
            return
        if kind == "next":  # 推进阶段：才受“必须投票”约束
            if self.phase["必须投票才能结束"] and not self._human_voted():
                raise Err("本阶段必须投出选票才能继续")
            return
        if kind in ("ask", "search", "search_body", "confront", "vote", "drill"):
            target = action.get("target", "")
            if kind.startswith("search") or kind == "drill":
                if target not in self.script.clues:
                    raise Err("这里没有可搜查的东西")
            elif target and target not in self.script.characters:
                raise Err("没有这个角色")

        if kind in ("search", "search_body", "drill") and not self.phase["可搜证"]:
            raise Err(f"「{self.phase['name']}」阶段不能搜证")
        if kind == "confront":
            if not self.phase["可对质"]:
                raise Err(f"「{self.phase['name']}」阶段不能对质")
            if self.state["confront_used"] >= self.phase["对质次数上限"]:
                raise Err("本阶段对质次数已用完")
        # 人类不设互动配额：侦探想追问多久就追问多久（成本由保险丝兑底）
        if kind == "ask":
            limit = self.phase["可被问次数"]
            if self.state["asked_in_phase"].get(target := action["target"], 0) >= limit:
                raise Err(f"{target} 在本阶段已被问满 {limit} 次")
        if kind == "vote":
            if self._human_voted():
                raise Err("本阶段你已经投过票了")

    # ------------------------------------------------------------ 动作

    def _act_ask(self, action: dict) -> str:
        target = action["target"]
        question = action.get("question") or ""
        char = self.script.characters[target]
        self._record(self.human, question)
        reply = self.agents.answer(char, [question], self._log())
        if not reply:  # 网络抖动先补一次，仍空才真沉默
            reply = self.agents.answer(char, [question], self._log())
        if not reply:
            reply = "（他没有回答，只是看着你。）"
        reply = self._postcheck(target, reply, [question])
        self._record(target, reply)
        self.state["asked_in_phase"][target] = self.state["asked_in_phase"].get(target, 0) + 1
        self.state["asked_round"][target] = self.state["asked_round"].get(target, 0) + 1
        return reply

    def _act_search(self, action: dict) -> str:
        target = action["target"]
        clue = self.script.clues[target]
        fresh = {name: body for name, body in clue.items.items() if f"{target}/{name}" not in self.state["claimed_clues"]}
        if not fresh:
            raise Err("这里已经被翻遍了")
        for name in fresh:
            self.state["claimed_clues"].append(f"{target}/{name}")
        text = "；".join(f"【{n}】{b}" for n, b in fresh.items())
        self._record("DM", f"（搜查{target}）{text}", kind="search")
        if clue.kind == "人身":  # 搜身也算“和这个人互动”
            self.state["asked_round"][target] = self.state["asked_round"].get(target, 0) + 1
        return text

    def _act_drill(self, action: dict) -> str:
        target, item = action["target"], action.get("item", "")
        clue = self.script.clues[target]
        if item not in clue.items:
            raise Err("没有这条线索")
        subs = clue.drillables(item)
        sub = action.get("subtarget") or (subs[0] if subs else "")
        if sub and subs and sub not in subs:
            raise Err(f"「{item}」只能针对 {'/'.join(subs)} 深入调查")
        key = f"{target}/{item}#{sub}"
        if key in self.state["claimed_clues"]:
            raise Err("这条线索已经查过了")
        self.state["claimed_clues"].append(key)
        body = re.sub(r"[（(]可深入调查[^）)]*[）)]", "", clue.items[item]).strip()
        text = f"针对 {sub} 深入调查「{item}」：{body}"
        self._record("DM", text, kind="drill")
        return text

    def _act_confront(self, action: dict) -> str:
        a, b = action.get("a", ""), action.get("b", "")
        topic = action.get("topic") or "刚才的说法"
        for name in (a, b):
            if name not in self.script.characters or name == self.human:
                raise Err("对质双方必须是场上的 AI 角色")
        if a == b:
            raise Err("不能让一个人和自己对质")

        # 与 AI 互问去重：本轮若这两人已经交锋过（互问或对质），就不重复执行
        for pair_key in (f"{a}→{b}", f"{b}→{a}"):
            used = self.state["ai_pairs"].get(pair_key) or {}
            if used.get("round", 0) > 0:
                raise Err(f"{a} 和 {b} 本轮已经交锋过了，不用重复对质；换一对，或说「轮到你们了」推进到下一轮")
        if f"{a}|{b}" in (self.state.get("confront_pairs_round") or []):
            raise Err(f"{a} 和 {b} 本轮已经对质过了，换一对")

        plan = self.agents.plan_asks(self.script.characters[a], [b], 1, self._log())
        qs = [q["q"] for q in (plan.get(b) or [])][:1] or [f"关于{topic}，你怎么解释？"]
        self.state["confront_used"] += 1
        self.state.setdefault("confront_pairs_round", []).append(f"{a}|{b}")
        self._record(f"{a}", qs[0], kind="confront", topic=topic)
        reply = self.agents.answer(self.script.characters[b], qs, self._log())
        reply = self._postcheck(b, reply, qs)
        self._record(b, reply)
        # 问句也要带回去，终端才能看到完整交锋
        return f"【对质 {a} → {b}】{qs[0]}\n【{b}】{reply}"

    def _act_vote(self, action: dict) -> str:
        target = action["target"]
        if target == self.human:
            raise Err("不能投自己")
        self.state["votes"][f"{self.state['phase_index']}:{self.human}"] = target
        self._record(self.human, f"（投票）{target}", kind="vote")
        if self.state["phase_index"] >= len(self.script.phases) - 1:
            res = self.settle()
            last = len(self.script.phases) - 1
            votes = {k.split(":", 1)[1]: v for k, v in self.state["votes"].items() if k.startswith(f"{last}:")}
            tally = "  ".join(f"{n} {c} 票" for n, c in res["tally"].items())
            table = "\n".join(f"  {who} → {tgt}" for who, tgt in votes.items())
            return (
                f"【投票结果】\n{table}\n  计票：{tally}\n"
                f"  得票最多：{res['top']}｜真正的凶手：{res['culprit']}\n"
                f"  胜者：{res['winner']}\n\n{res['reveal']}"
                f"{brand_outro(str(self.script.meta.get('名称') or self.script.dir))}"
            )
        if self.phase["必须投票才能结束"]:
            self._advance()
            return f"你投给了 {target}。本阶段结束，进入「{self.phase['name']}」阶段。\n  {self._flow_line()}"
        return f"你投给了 {target}。"

    # ------------------------------------------------------------ 阶段

    def _advance(self) -> None:
        if self.state["phase_index"] < len(self.script.phases) - 1:
            self.state["phase_index"] += 1
            self.state["phase"] = self.phase["name"]
            self.state["asked_in_phase"] = {}
            self.state["confront_used"] = 0
            self._record("DM", f"—— 进入「{self.phase['name']}」阶段 ——", kind="phase")

    def _new_round(self) -> None:
        """本轮结束：清空“每对每轮”计数，轮次 +1。"""
        self.state["round"] += 1
        self.state["asked_round"] = {}
        self.state["confront_pairs_round"] = []
        for pair in self.state["ai_pairs"].values():
            pair["round"] = 0

    def _rotate(self, items: list[str], start: int) -> list[str]:
        if not items:
            return []
        s = start % len(items)
        return items[s:] + items[:s]

    # ------------------------------------------------------------ AI 窗口

    def ai_window(self) -> list[dict]:
        """每轮互问环节：**每个在场者都获得一次机会，问其余 N-1 人**。

        规则（与人类侧对称，但更宽）：
          · 每个 AI 每轮都可以向其余每个在场者各问一次；
          · 每次一对一问答最多 2 个来回（`每对每轮问答上限`，默认 2）；
          · **没有全场总额度**——否则先开口的角色会把额度吃光，
            后面的角色就一句都说不出（这正是「B 女士一个人问完 3 个」的成因）；
          · 人类若扮演普通在场角色（不是侦探），AI 也可以问他。

        计划阶段并行（互不依赖）；回答也并行，但**按确定性顺序落日志**，
        保证同一局重现时顺序完全一致。
        """
        # 先清空：否则最后一阶段（不跑窗口）会把上一轮的互问内容重复贴回去
        self.state["ai_window_text"] = []
        self.state["ai_window_stats"] = {}
        if self.state["phase_index"] >= len(self.script.phases) - 1:
            return []
        cap = self.script.ai_q_per_pair_round
        per_game = self.script.ai_q_per_pair_game
        log_snapshot = list(self._log())

        order = self._rotate(self.script.ai_names, self.state["round"])
        # 可问对象：其余所有在场者（AI + 可能的人类）
        targets_of = {asker: [t for t in self.script.others(asker) if t != self.human or self.script.human_is_actor] for asker in order}

        # ① 并行拿每个人的提问计划
        plan_jobs = [(a, targets_of[a]) for a in order if targets_of[a]]
        plan_results = _parallel(
            lambda a, ts: self.agents.plan_asks(self.script.characters[a], ts, cap, log_snapshot),
            plan_jobs,
        )
        plans = {a: (r or {}) for (a, _), r in zip(plan_jobs, plan_results)}

        # ② 计划为空：先补一次；仍空就给一句通用问题兜底。
        # 否则模型偶尔返回空 JSON 时，该角色整轮一个字不说（玩家会以为在针对他）。
        silent = [a for a in order if targets_of.get(a) and not plans.get(a)]
        if silent:
            retry = _parallel(
                lambda a: self.agents.plan_asks(self.script.characters[a], targets_of[a], cap, log_snapshot),
                [(a,) for a in silent],
            )
            for a, r in zip(silent, retry):
                plans[a] = r or {}
        silent = [a for a in order if targets_of.get(a) and not plans.get(a)]
        for a in silent:
            first = targets_of[a][0]
            plans[a] = {first: [{"q": f"{first}，你当时在做什么？", "based_on": "（兜底）"}]}
        self.state["ai_fallback"] = silent

        # ② 逐人逐目标组装任务（只受“每对上限”，无全场额度）
        tasks: list[tuple[str, str, list[str]]] = []
        per_actor: dict[str, int] = {}
        for asker in order:
            plan = plans.get(asker) or {}
            for target in targets_of.get(asker, []):
                pair = self.state["ai_pairs"].setdefault(f"{asker}→{target}", {"round": 0, "total": 0})
                remain = min(cap - pair["round"], per_game - pair["total"])
                if remain <= 0:
                    continue
                qs = (plan.get(target) or [])[:remain]
                if not qs:
                    continue
                questions = [q["q"] for q in qs]
                per_actor[asker] = per_actor.get(asker, 0) + len(qs)
                if target == self.human:
                    self.state["pending_to_human"].append({"from": asker, "questions": questions})
                    continue
                tasks.append((asker, target, questions))

        # ③ 并行取回答，再按顺序落日志
        replies = _parallel(
            lambda a, t, qs: self.agents.answer(self.script.characters[t], qs, log_snapshot),
            tasks,
        )

        events: list[dict] = []
        lines: list[str] = []
        for (asker, target, questions), reply in zip(tasks, replies):
            # 网络抖动时不让整轮崩掉：先补一次，仍失败才留一条“沉默”
            if not reply:
                reply = self.agents.answer(self.script.characters[target], questions, log_snapshot)
            if not reply:
                reply = "（他沉默了一下，没有回答。）"
            reply = self._postcheck(target, reply, questions)
            self._record(asker, "".join(questions), kind="ai_ask")
            self._record(target, reply)
            pair = self.state["ai_pairs"][f"{asker}→{target}"]
            pair["round"] += len(questions)
            pair["total"] += len(questions)
            events.append({"from": asker, "to": target, "reply": reply})
            lines.append(f"  {asker} → {target}：{''.join(questions)}")
            lines.append(f"  {target}：{reply}")

        for item in self.state["pending_to_human"]:
            lines.append(f"  {item['from']} → 你：{''.join(item['questions'])}（你可以直接回复）")
        self.state["pending_to_human"] = []  # 已展示过就不再累积

        self.state["ai_window_stats"] = per_actor  # 供人类引导展示
        self.state["ai_window_text"] = lines  # 供 CLI 打印
        return events

    # ------------------------------------------------------------ 主循环

    def _fast_target(self, text: str, kind: str | None = None) -> str:
        """在输入里找线索目标；同名时取最长匹配，并可按类型优先。"""
        cands = [target for target, clue in self.script.clues.items() if target in text and (kind is None or clue.kind == kind)]
        return max(cands, key=len) if cands else ""

    def fast_action(self, text: str) -> dict | None:
        """常见中文说法直接解析，命中就省掉一次 router LLM 调用。

        这里只做「确定性强」的句式（轮到你们了 / 我投X / 搜查X / 让A和B对质…），
        含糊的输入（双关、复合句）仍交给 LLM router。
        """
        t = re.sub(r"\s+", "", text)
        if not t:
            return None
        if any(k in t for k in ("轮到你们了", "轮到你们", "没什么要问", "没问题了", "跳过")):
            return {"type": "pass"}
        if any(k in t for k in ("进入投票", "开始投票", "下一阶段", "推进阶段")):
            return {"type": "next"}
        names = [n for n in self.script.characters if n in t]
        if "对质" in t and len(names) >= 2:
            return {"type": "confront", "a": names[0], "b": names[1], "topic": t}
        if "深入调查" in t:
            place = self._fast_target(t, "地点") or self._fast_target(t)
            clue = self.script.clues.get(place)
            item = next((i for i in (clue.items if clue else {}) if i in t), "")
            if place and item:
                return {
                    "type": "drill",
                    "target": place,
                    "item": item,
                    "subtarget": names[0] if names else "",
                }
        if any(k in t for k in ("搜身", "的身")) and names:
            return {"type": "search_body", "target": names[0]}
        if "搜" in t or "翻" in t:
            place = self._fast_target(t, "地点") or self._fast_target(t)
            if place:
                kind = "search_body" if self.script.clues[place].kind == "人身" else "search"
                return {"type": kind, "target": place}
        if t.startswith(("我投", "投给")) and names:
            return {"type": "vote", "target": names[0]}
        if names:
            return {"type": "ask", "target": names[0], "question": text}
        return None

    def handle(self, text: str) -> str:
        names = list(self.script.characters)
        places = list(self.script.clues)
        action = self.fast_action(text)
        if action is None:
            action = self.agents.router(
                text,
                self.phase["name"],
                self.script.actions,
                [n for n in names if n != self.human],
                places,
                self.script.ai_names[0] if self.script.ai_names else "",
            )
        self._guard(action)  # 失败 → Err，不写 state

        # 一轮 = 人类若干动作 + 一次 AI 自主窗口。
        # 人类可以在同一轮内对每个人各互动 ≤ N 次，说完“轮到你们了”才轮到 AI。
        if self.state["round"] == 0:
            self.state["round"] = 1
        self.state["turn"] += 1
        must_vote = self.phase["必须投票才能结束"]

        kind = action["type"]
        ends_round = False
        if kind == "ask":
            reply = self._act_ask(action)
        elif kind in ("search", "search_body"):
            reply = self._act_search(action)
        elif kind == "drill":
            reply = self._act_drill(action)
        elif kind == "confront":
            reply = self._act_confront(action)
        elif kind == "vote":
            reply = self._act_vote(action)
            ends_round = must_vote or self.state["result"] is not None
        elif kind == "next":
            self._advance()
            reply = f"—— 进入「{self.phase['name']}」阶段 ——\n  {self._flow_line()}"
            ends_round = True
        elif kind == "pass":  # 结束本轮
            reply = "（你表示暂时没什么要问了，让其他人说说。）"
            ends_round = True
        else:
            reply = "（这个动作本剧本暂不支持。）"

        if ends_round and self.state["result"] is None:
            self.ai_window()
            window = self.state.get("ai_window_text") or []
            if window:
                reply = reply + "\n\n【其余角色互相发问】\n" + "\n".join(window)
        if ends_round:
            self._new_round()
        self.save()
        return reply

    # ------------------------------------------------------------ 结算

    def settle(self) -> dict:
        last = len(self.script.phases) - 1
        prefix = f"{last}:"
        final = {k.split(":", 1)[1]: v for k, v in self.state["votes"].items() if k.startswith(prefix)}
        tally: dict[str, int] = {}
        for voter, target in final.items():
            tally[target] = tally.get(target, 0) + self.script.vote_weight(voter)
        # AI 投票：默认不能投侦探（人类）；剧本声明“人类可被投票: 是”时才放开
        votable = list(self.script.characters) if self.script.human_votable else [n for n in self.script.characters if n != self.human]
        pending = [n for n in self.script.ai_names if n not in final]
        # 并发投票 + 失败兜底：某个模型调用超时不能把整局弄崩
        picks = _parallel(
            lambda n: self.agents.vote(
                self.script.characters[n],
                [x for x in votable if x != n],
                self._log(),
            ),
            [(n,) for n in pending],
        )
        for name, pick in zip(pending, picks):
            fallback = next((x for x in votable if x != name), "")
            pick = pick or fallback
            if pick not in votable:
                pick = fallback
            final[name] = pick
            self.state["votes"][f"{last}:{name}"] = pick  # 回写，保证可审计
            tally[pick] = tally.get(pick, 0) + self.script.vote_weight(name)

        top = max(tally, key=tally.get) if tally else ""
        culprit = self.script.culprit
        result = {
            "tally": tally,
            "top": top,
            "culprit": culprit,
            "winner": "侦探与其他玩家" if top == culprit else "犯人",
            "reveal": self.script.read_truth(),  # 全流程唯一一次读真相
        }
        self.state["result"] = result
        self.save()
        return result


# ---------------------------------------------------------------- CLI


def render_transcript(state) -> str:
    """把问询记录原样打印出来。

    只含「谁说了什么」，**不添加任何判断列**（可信 / 印证 / 矛盾）。
    """
    rows = state.get("public_log") or []
    if not rows:
        return "（还没有任何问询记录）"
    lines = ["【问询记录】按时间顺序，原样保存，不含任何推断"]
    for row in rows:
        lines.append(f"  [第{row.get('round', 0)}轮] {row.get('speaker', '')}：{row.get('text', '')}")
    return "\n".join(lines)


def build(root: Path, case: str, mock: bool):
    script = load_script.load(str(root / "references" / case))
    if mock:
        return script, agents_mod.MockAgents(script)
    import llm

    ok, why = llm.config_status()
    if not ok:
        raise SystemExit(llm.setup_hint(why))
    return script, agents_mod.LLMAgents(llm.ChatClient(llm.load_config()))


def main() -> int:
    ap = argparse.ArgumentParser(description="剧本杀 AI 主持（单人本地版）")
    ap.add_argument("--script", default="004-office-murder", help="references 下的剧本目录名")
    ap.add_argument("--mock", action="store_true", help="离线确定性代理，不联网")
    ap.add_argument(
        "--say",
        default="",
        help="单步模式：执行一句玩家输入后退出（供宿主调用，不用交互式等待）",
    )
    ap.add_argument("--json", action="store_true", help="配合 --say / --intro，输出 JSON")
    ap.add_argument(
        "--intro",
        action="store_true",
        help="单步模式：打印开局包（品宣 + 场景/流程/规则 + 状态）后退出",
    )
    ap.add_argument(
        "--state",
        default=None,
        help="状态文件路径（默认 ~/.jubensha/<英文剧本名>/state.json，各剧本自动隔离）",
    )
    ap.add_argument(
        "--reset",
        action="store_true",
        help="重开一局：只删除本剧本 <slug> 目录下的 state.json（不影响其他剧本）",
    )
    args = ap.parse_args()

    if not args.mock:
        import llm

        ok, why = llm.config_status()
        if not ok:
            msg = llm.setup_hint(why)
            if args.say and args.json:
                print(json.dumps({"ok": False, "error": why, "hint": msg}, ensure_ascii=False))
            else:
                print(msg)
            return 2

    script, agent = build(HERE.parent, args.script, args.mock)
    slug = str(script.meta.get("英文名") or args.script)
    state_path = Path(args.state) if args.state else (Path.home() / ".jubensha" / slug / "state.json")
    if args.reset and state_path.exists():
        state_path.unlink()
        print(f"[重置] 已删除本剧本存档：{state_path}")
    game = Game(script, agent, state_path)
    try:
        game.load()
    except Err as err:
        raise SystemExit(f"\n[拒绝启动] {err}\n") from err

    if args.intro:
        if args.json:
            print(
                json.dumps(
                    {"brand": brand_banner(), "opening": game.opening(), "hint": game.hint()},
                    ensure_ascii=False,
                )
            )
        else:
            print(brand_banner())
            print()
            print(game.opening())
            print()
            print(game.hint())
        return 0

    if args.say:
        if args.say in ("记录", "回顾", "log", "history"):
            print(render_transcript(game.state))
            return 0
        ok, err_text, reply = True, "", ""
        try:
            reply = game.handle(args.say)
        except Err as exc:
            ok, err_text = False, str(exc)
        if args.json:
            print(
                json.dumps(
                    {
                        "ok": ok,
                        "reply": reply,
                        "error": err_text,
                        "hint": game.hint(),
                        "settled": game.state.get("result") is not None,
                        # 宿主若自己重组结算文案，必须把 brand 原样附在最后一段
                        "brand": (brand_outro(str(script.meta.get("名称") or script.dir)) if game.state.get("result") is not None else ""),
                    },
                    ensure_ascii=False,
                )
            )
        else:
            print(reply if ok else f"[拒绝] {err_text}")
            print(game.hint())
        return 0 if ok else 2

    dm = script.meta.get("开场白") or (f"现在开始《{script.meta.get('名称') or Path(script.dir).name}》。你是{script.human}，场上有：{'、'.join(script.ai_names)}。当前阶段：{game.phase['name']}。")
    print(f"\n{brand_banner()}\n")
    print(game.opening() + "\n")
    print(f"[DM] {dm}\n")
    resumed = "（接着上次继续）" if game.state["round"] else ""
    print(f"[状态] {state_path}{resumed}")
    print("输入「退出」结束；输入「记录」随时查看问询记录。")
    print("你可以不限次数地问任何人；说「轮到你们了」让 AI 互相发问。")
    print('示例："<角色>，你当时在做什么？" / "我要搜查<地点>" / "轮到你们了"\n')
    print(game.hint() + "\n")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ("退出", "exit", "quit"):
            break
        if line in ("记录", "回顾", "log", "history"):
            print("\n" + render_transcript(game.state) + "\n")
            continue
        try:
            t0 = time.time()
            reply = game.handle(line)
            elapsed = time.time() - t0
            stats = ""
            client = getattr(agent, "client", None)
            if client is not None:
                stats = f"（{client.calls} 次调用 · {elapsed:.1f}s）"
            else:
                stats = f"（{elapsed:.1f}s）"
            print(f"\n{reply}\n{stats}\n")
            if game.state["result"] is None:
                print(game.hint() + "\n")
        except Err as err:
            print(f"\n[拒绝] {err}\n")
        except Exception as err:  # noqa: BLE001
            print(f"\n[错误] {err}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
