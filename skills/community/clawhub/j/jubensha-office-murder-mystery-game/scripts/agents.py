#!/usr/bin/env python3
"""角色代理层：真实 LLM 版 + 确定性 Mock 版。

接口一致，game.py 不关心背后是哪一个：

    router(text, phase_name, actions)          -> dict
    answer(char, questions, log)               -> str
    plan_asks(char, targets, quota, log)       -> {target: [{"q","based_on"}]}
    vote(char, others, log)                    -> str
"""

from __future__ import annotations

import re

# 推理禁令：AI 只陈述与提问，不下结论
BAN_PATTERNS = [
    "所以你在撒谎",
    "所以他在撒谎",
    "你在撒谎",
    "他在撒谎",
    "凶手是",
    "时间对不上",
    "对不上",
    "明显是",
    "说明是你",
    "就是凶手",
]

FORBIDDEN_RULE = "【禁止】\n- 禁止说「所以你在撒谎」「凶手是某某」「你们俩的时间对不上」\n- 禁止做跨人物的推理比对\n你只能：陈述你知道的事、提出疑问、回避、否认。"

ANSWER_SYS = """你是{name}，{role}。你正在被其他角色询问。

【规则】{lie_rule}

【你知道的事实】（照实回答）
{public}

【你不想主动说的】（被追问可以说，但绝不主动提）
{private}

【禁止透露】（一旦出现即视为失败）
{forbidden}

{ban}

【最近对话】
{log}

【要求】第一人称，口语，逐条回答，每条 1–2 句。不要复述本条规则，不要说“根据我的设定”。"""

PLAN_SYS = """你是{name}。现在是人类发言之后的空档，你可以主动向其他人提问。

【你可以问的人】{targets}
【每人上限】本轮每人最多 {cap} 个问题；没有疑问就给空数组
【判断依据】你的每个问题都必须基于【你自己掌握的信息】
【提问姿势】只问“对方”的经历；**不要把“我做过什么”写进问句**
  ✅「你 17:40 推门进去时，屋里灯亮着吗？」
  ❌「我 17:40 推门进去看到灯亮着，你当时在哪？」
【建议】通常 0–2 个问题就够，问题越精准越有价值
【正例】“你 17:50 那通电话，背景里有没有什么声音？”
【反例】“你到底有没有杀人？”

{ban}

【最近对话】
{log}

【你应该基于的事实】
{public}

输出 JSON（只输出 JSON）：
{{"目标名": [{{"q": "一句话", "based_on": "你依据的那条信息"}}]}}"""

ROUTER_SYS = """把侦探的一句话解析成结构化动作，只输出 JSON。

当前阶段：{phase}
可用动作：{actions}
场上角色：{names}
可搜查地点：{places}

动作格式：
- {{"type":"ask","target":"角色名","question":"侦探原话"}}
- {{"type":"search","target":"地点名"}}
- {{"type":"search_body","target":"角色名"}}
- {{"type":"drill","target":"地点名","item":"线索名","subtarget":"角色名"}}   # 可选
- {{"type":"confront","a":"角色名","b":"角色名","topic":"对质主题"}}
- {{"type":"vote","target":"角色名"}}
- {{"type":"pass"}}     # 结束本轮，让 AI 说话（如“轮到你们了”“我没问题了”）
- {{"type":"next"}}     # 推进到下一阶段（如“进入投票阶段”）

无法判断时用 {{"type":"ask","target":"<默认第一个角色>","question":"<原话>"}}。"""

VOTE_SYS = """你是{name}。基于你掌握的信息和上面的讨论，你投票。
只能投 {others} 之一，不能投自己。

【你知道的事实】
{public}

【最近对话】
{log}

输出 JSON（只输出 JSON）：{{"vote": "名字"}}"""


def _tail(log: list[dict], n: int = 20) -> str:
    rows = log[-n:]
    if not rows:
        return "（暂无）"
    return "\n".join(f"{r['speaker']}：{r['text']}" for r in rows)


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items) if items else "- （无）"


def has_ban(text: str) -> str | None:
    for pat in BAN_PATTERNS:
        if pat in text:
            return pat
    return None


# ---------------------------------------------------------------- 真实 LLM


class LLMAgents:
    def __init__(self, client):
        self.client = client

    def router(self, text, phase_name, actions, names, places, default_target):
        sys = ROUTER_SYS.format(
            phase=phase_name,
            actions=", ".join(actions),
            names=", ".join(names),
            places=", ".join(places) or "（无）",
        )
        data = self.client.chat_json(
            [{"role": "system", "content": sys}, {"role": "user", "content": text}],
            schema_hint='{"type":"...","target":"..."}',
        )
        if not data.get("type"):
            return {"type": "ask", "target": default_target, "question": text}
        data.setdefault("question", text)
        return data

    def answer(self, char, questions, log):
        sys = ANSWER_SYS.format(
            name=char.key,
            role=char.role or "在场人员",
            lie_rule=("你可以说谎。必须守住上面的对外口径，不要自相矛盾。" if char.can_lie else "你不能说谎，但你可以隐瞒事实、可以只说一部分。"),
            public=_bullets(char.public),
            private=char.private or "（无）",
            forbidden=_bullets(char.forbidden),
            ban=FORBIDDEN_RULE,
            log=_tail(log),
        )
        user = "对方问你：\n" + "\n".join(f"· {q}" for q in questions) + "\n\n请直接用口语回答，不要输出序号、编号或“1.”这类前缀。"
        return self.client.chat([{"role": "system", "content": sys}, {"role": "user", "content": user}]).strip()

    def plan_asks(self, char, targets, quota, log):
        sys = PLAN_SYS.format(
            name=char.key,
            targets=", ".join(targets) or "（无人可问）",
            cap=quota,
            ban=FORBIDDEN_RULE,
            log=_tail(log),
            public=_bullets(char.public),
        )
        data = self.client.chat_json(
            [{"role": "system", "content": sys}, {"role": "user", "content": "请给出你的提问计划。"}],
            schema_hint='{"目标名":[{"q":"...","based_on":"..."}]}',
        )
        out: dict[str, list[dict]] = {}
        for name, qs in (data or {}).items():
            if name not in targets or not isinstance(qs, list):
                continue
            clean = [{"q": str(q.get("q", "")).strip(), "based_on": str(q.get("based_on", "")).strip()} for q in qs if isinstance(q, dict) and str(q.get("q", "")).strip()]
            if clean:
                out[name] = clean[:quota]
        return out

    def vote(self, char, others, log):
        sys = VOTE_SYS.format(
            name=char.key,
            others=", ".join(others),
            public=_bullets(char.public),
            log=_tail(log),
        )
        try:
            data = self.client.chat_json(
                [{"role": "system", "content": sys}, {"role": "user", "content": "请投票。"}],
                schema_hint='{"vote":"名字"}',
            )
        except Exception:  # 超时/限流 → 退化为顺序投票，不让整局崩
            return others[0] if others else ""
        pick = str(data.get("vote", "")).strip()
        if pick in others:
            return pick
        return others[0] if others else ""


# ---------------------------------------------------------------- Mock


class MockAgents:
    """确定性代理：不联网，用于离线测试与演示。

    行为规则（刻意简单，只用来验证引擎）：
      - 每个角色向"下一个"角色提 1 个问题，依据是自己公开口径的第一条
      - 回答 = 自己公开口径的第一条
      - 投票 = 剧本标注的犯人（这样人类只要投对就赢）
    """

    def __init__(self, script):
        self.script = script

    def router(self, text, phase_name, actions, names, places, default_target):
        if any(k in text for k in ("下一阶段", "进入投票", "开始投票", "进入下轮")):
            return {"type": "next"}

        if any(k in text for k in ("轮到你们", "结束本轮", "没什么", "跳过", "pass")):
            return {"type": "pass"}

        if "深入调查" in text:
            # 一句里可能同时出现地点和人名（"办公桌…针对A同事"），取**位置最靠前**的地点
            cands = [(text.find(p), p) for p in places if p in text]
            place = min(cands)[1] if cands else ""
            item = ""
            clue = self.script.clues.get(place)
            if clue:
                item = next((n for n in clue.items if n in text), "")
            sub = next((n for n in names if n in text), "")
            return {"type": "drill", "target": place, "item": item, "subtarget": sub}

        if "对质" in text:
            picked = [n for n in names if n in text]
            if len(picked) >= 2:
                return {"type": "confront", "a": picked[0], "b": picked[1], "topic": text}

        if any(k in text for k in ("搜", "翻", "查一下", "看看")):
            for place in places:
                if place in text:
                    if "身" in text:
                        return {"type": "search_body", "target": place}
                    return {"type": "search", "target": place}
            kind = "search_body" if "身" in text else "search"
            return {"type": kind, "target": (places[0] if places else "")}

        if any(k in text for k in ("投", "指认")):
            for name in names:
                if name in text:
                    return {"type": "vote", "target": name}
            return {"type": "vote", "target": names[0]}
        for name in names:
            if name in text:
                return {"type": "ask", "target": name, "question": text}
        return {"type": "ask", "target": default_target, "question": text}

    def answer(self, char, questions, log):
        base = char.public[0] if char.public else "我不清楚。"
        return base.rstrip("。") + "。"

    def plan_asks(self, char, targets, quota, log):
        if not targets or quota <= 0:
            return {}
        target = targets[0]
        based = char.public[0] if char.public else "我掌握的线索"
        return {target: [{"q": f"{target}，你当时在做什么？", "based_on": based}][:quota]}

    def vote(self, char, others, log):
        culprit = self.script.culprit
        if culprit in others:
            return culprit
        return others[0] if others else ""


def norm(text: str) -> str:
    return re.sub(r"\s+", "", text or "")
