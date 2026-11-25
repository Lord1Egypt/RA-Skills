#!/usr/bin/env python3
"""离线回归：用确定性 mock 代理跑通一局，不联网、不花钱。

覆盖验收标准：
  1. 角色可被质询，AI 回答不含「禁止透露」词
  2. 按地点搜证 + 重复搜告警 + 深入调查去重
  3. 阶段一必须投票才能进入阶段二
  4. 阶段一不能对质、阶段二可以
  5. 计票正确、真相只在结算时读出
  6. AI 之间自主互问，且受「每对每轮 4 问」约束

    python tests/run_offline.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import load_script  # noqa: E402
from game import Err, Game  # noqa: E402

import agents as agents_mod  # noqa: E402

CASE = ROOT / "references" / "004-office-murder"
PASS, FAIL = 0, 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok    {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}  {detail}")


def expect_err(label: str, fn, keyword: str = "") -> None:
    try:
        fn()
    except Err as err:
        check(label, keyword in str(err), f"实际: {err}")
        return
    check(label, False, "没有抛出 Err")


class LeakyAgents(agents_mod.MockAgents):
    """故意泄露禁透词的代理，用来验证内容闸。"""

    def answer(self, char, questions, log):
        if char.key == "C经理":
            return "我只是用石头摆件砸了他一下，真的很抱歉。"  # 命中 forbidden
        return super().answer(char, questions, log)


def main() -> int:
    script = load_script.load(str(CASE))

    print("\n[1] 结构校验")
    check("角色数 = 5", len(script.characters) == 5, str(list(script.characters)))
    check("AI 角色数 = 4", len(script.ai_names) == 4, str(script.ai_names))
    check("线索数 = 5", len(script.clues) == 5, str(list(script.clues)))
    check("阶段数 = 3", len(script.phases) == 3, str([p["name"] for p in script.phases]))
    check("犯人 = C经理", script.culprit == "C经理", script.culprit)
    check("侦探 2 票", script.vote_weight("侦探") == 2)
    check("每对每轮问答上限 = 2", script.ai_q_per_pair_round == 2, str(script.ai_q_per_pair_round))
    check("侦探不可被 AI 反向提问", script.human_is_actor is False, str(script.human_is_actor))
    check(
        "每个角色独占一个文件",
        len({c.path for c in script.characters.values()}) == 5,
    )

    print("\n[2] 人类不限次数（同一人可反复追问）")
    # 测试中间状态写在 ~/.jubensha/<slug>/test_state.json，绝不落到仓库或 /tmp；
    # 用独立文件名，避免覆盖玩家真实存档 state.json。
    slug = str(script.meta.get("英文名") or CASE.name)
    state_path = Path.home() / ".jubensha" / slug / "test_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    if state_path.exists():
        state_path.unlink()
    game = Game(script, agents_mod.MockAgents(script), state_path)

    reply = game.handle("A同事，你最后一次见到李无义是什么时候？")
    check("AI 有回答", bool(reply.strip()), reply)
    check("记录写入 public_log", len(game.state["public_log"]) >= 2)
    check("未结束本轮 → AI 还没说话", not game.state["ai_pairs"])

    game.handle("C经理，17:30到18:00你在哪里？")
    for i in range(5):
        game.handle(f"A同事，第{i + 2}个补充问题？")
    check(
        "同一人连问 6 次均放行",
        game.state["asked_round"].get("A同事") == 6,
        str(game.state["asked_round"]),
    )
    check("人类追问不会触发 AI 窗口", not game.state["ai_pairs"])

    print("\n[3] 结束本轮 → AI 自主窗口")
    game.handle("轮到你们了")
    asked = [e for e in game.state["public_log"] if e.get("kind") == "ai_ask"]
    check("AI 开始互问", bool(asked), str(len(asked)))
    check("轮次已推进", game.state["round"] >= 2, str(game.state["round"]))
    check(
        "每对每轮计数已清空",
        all(p["round"] == 0 for p in game.state["ai_pairs"].values()),
        str(game.state["ai_pairs"]),
    )
    # 关键：每个 AI 都要有机会开口，不能被先开口的人把额度吃光
    stats = game.state.get("ai_window_stats") or {}
    check(
        "所有 4 个 AI 本轮都需发言",
        len(stats) == len(script.ai_names),
        f"实际只说了: {stats}",
    )
    print("\n[3b] 互问内容可打印")
    window = game.state.get("ai_window_text") or []
    check("互问内容可打印到终端", bool(window), str(len(window)))
    check(
        "每对每轮问答不超过 2",
        all(p["round"] <= 2 for p in game.state["ai_pairs"].values()),
        str(game.state["ai_pairs"]),
    )

    print("\n[3c] 计划为空时仍要有人说话")

    class _NoPlan(agents_mod.MockAgents):
        def plan_asks(self, char, targets, quota, log):
            return {}

    gm_empty = Game(script, _NoPlan(script))
    gm_empty.handle(f"{script.ai_names[0]}，你当时在做什么？")
    gm_empty.handle("轮到你们了")
    stats_empty = gm_empty.state.get("ai_window_stats") or {}
    check(
        "空计划也覆盖全部 AI（不会只一个人发言）",
        len(stats_empty) == len(script.ai_names),
        str(stats_empty),
    )

    print("\n[4] 搜证 / 闸门")
    before_clues = set(game.state["claimed_clues"])
    before_log = len(game.state["public_log"])
    text = game.handle("我要搜查文件柜")
    new_clues = set(game.state["claimed_clues"]) - before_clues
    new_rows = len(game.state["public_log"]) - before_log
    check("搜到 50万现金", "50万现金" in text, text)
    check("线索已入账", "文件柜/50万现金" in game.state["claimed_clues"])
    check(
        "一次输入只搜一个地点（不替玩家多搜）",
        all(c.startswith("文件柜/") for c in new_clues),
        str(new_clues),
    )
    check("一次输入只产生一条记录", new_rows <= 1, f"新增 {new_rows} 条")
    expect_err("重复搜查被拒", lambda: game.handle("我要搜查文件柜"), "翻遍")
    expect_err("阶段一不能对质", lambda: game.handle("让A同事和C经理对质"), "不能对质")
    expect_err("不投票不能进下一阶段", lambda: game.handle("进入投票"), "必须投出选票")

    print("\n[5] 投票推进阶段")
    game.handle("我投C经理")
    check("阶段一投票后进入阶段二", game.phase["name"] == "讨论求证", game.phase["name"])

    print("\n[5b] 提示不点名暗示凶手")
    h = game.hint()
    check("提示列出全部在场者", all(n in h for n in script.ai_names), h)
    check(
        "提示里没有单独的投票示例点名",
        "我投C经理" not in h,
        h,
    )

    print("\n[6] 阶段二：对质 / 深入调查")
    out = game.handle("让A同事和C经理对质")
    check("对质有回应", bool(out.strip()), out)
    check("对质次数已计数", game.state["confront_used"] == 1)
    check("对质输出含问与答", "【对质" in out and "】" in out, out[:60])
    # 同一对再对质：本轮已交锋 / 或本轮互问已覆盖 → 应被拒
    expect_err(
        "同一对重复对质被拒",
        lambda: game.handle("让A同事和C经理对质"),
        "已经",
    )

    out = game.handle("深入调查办公桌的擦拭痕迹，针对A同事")
    check("深入调查成功", "A同事" in out or "擦拭" in out, out)
    expect_err(
        "重复深入调查被拒",
        lambda: game.handle("深入调查办公桌的擦拭痕迹，针对A同事"),
        "已经查过",
    )

    body = game.handle("搜一下A同事的身")
    check("人身搜查成功", "墨迹" in body or "袖口" in body, body)

    text_into_vote = game.handle("进入投票")
    check("阶段二可推进到投票", game.phase["name"] == "投票", game.phase["name"])
    check(
        "进入终局阶段不重复贴上一轮互问",
        "【其余角色互相发问】" not in text_into_vote,
        text_into_vote[:60],
    )

    print("\n[7] 结算")
    reveal = game.handle("我投C经理")
    result = game.state["result"]
    check("有结算结果", result is not None)
    check("得票最多 = C经理", result["top"] == "C经理", str(result["tally"]))
    check("人类胜利", result["winner"] == "侦探与其他玩家", result["winner"])
    check("真相已回放", "C经理" in reveal and len(reveal) > 100)
    check("结算末尾有品牌引导", "仙踪问道" in reveal, reveal[-80:])
    check(
        "计票含侦探 2 票",
        result["tally"].get("C经理", 0) >= 2,
        str(result["tally"]),
    )
    last_votes = {k.split(":", 1)[1]: v for k, v in game.state["votes"].items() if k.startswith(f"{len(script.phases) - 1}:")}
    check(
        "全员投票已落盘（含 4 个 AI）",
        len(last_votes) == 5,
        str(last_votes),
    )
    check(
        "AI 没有投侦探",
        all(v != script.human for k, v in last_votes.items() if k != script.human),
        str(last_votes),
    )

    print("\n[8] 内容闸：泄露禁透词")
    leak_game = Game(script, LeakyAgents(script))
    answer = leak_game._postcheck("C经理", "我只是用石头摆件砸了他一下，真的很抱歉。", ["你干了什么？"])
    check("禁透词被拦截重写", "石头摆件" not in answer, answer)

    print("\n[9] 推理禁令")
    banned = agents_mod.has_ban("所以你在撒谎，凶手是他。")
    check("推理结论被识别", banned is not None, str(banned))
    check("正常陈述不误判", agents_mod.has_ban("17:40 我看到他靠在椅子上。") is None)

    print("\n[10] 测试中间状态的落点")
    check("状态写在 ~/.jubensha/<slug>/ 下", state_path.parent == Path.home() / ".jubensha" / slug, str(state_path))
    check("测试用独立文件名，不覆盖真实存档", state_path.name == "test_state.json", state_path.name)
    check("仓库内未产生 .jubensha/", not (ROOT / ".jubensha").exists(), str(ROOT / ".jubensha"))
    if state_path.exists():
        state_path.unlink()
    check("测试结束后已清理中间状态", not state_path.exists(), str(state_path))

    print(f"\n通过 {PASS} 项，失败 {FAIL} 项")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
