#!/usr/bin/env python3
"""火一五小红书写作训练 — 把"写"当成可练习的肌肉。

为什么需要练习
==============
看再多模板也写不好，得动手。这个脚本提供两种训练：

1. **`prompt`** — 命题练习
   助手给你一个主题 + 一个公式 + 一个场景约束，你写一条标题或一段开头。
   写完跑 `practice.py grade` 给你打分 + 对照参考。

2. **`rewrite`** — 改写训练
   助手随机抽一段"反面教材"（或你过往得分低的笔记片段），让你改写。
   提交后对比你的版本和"AI 默认改法"，告诉你为什么哪种好。

3. **`drill`** — 题库训练
   把所有命题串成一个题库（每天 1 题），可批量回顾历史成绩。

记录在 `~/.xiaohongshu/profile/practice.jsonl`。

用法
----

    # 出 1 道命题
    python3 practice.py prompt

    # 提交答案
    python3 practice.py grade --task-id 5 --answer "你的标题或段落"

    # 改写训练
    python3 practice.py rewrite

    # 看历史
    python3 practice.py history --days 30
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore  # noqa: E402
from xhs_writer import (  # noqa: E402
    Draft,
    generate_titles,
    score_post,
    score_title,
)


# ---------- 命题题库 ----------


_PRACTICE_PROMPTS = [
    {"topic": "干皮护肤", "persona": "30+ 干皮女生", "constraint": "标题 ≤ 22 字，使用 T2 公式（痛点共情）"},
    {"topic": "副业", "persona": "互联网打工人", "constraint": "首段 3 行，必须命中 '代入式提问' 钩子"},
    {"topic": "通勤", "persona": "上班族", "constraint": "用 T11 故事开场，标题以 '上周' 开头"},
    {"topic": "减脂餐", "persona": "微胖", "constraint": "标题 + 首 50 字，无 emoji，靠文字钩子"},
    {"topic": "Notion 模板", "persona": "学生党", "constraint": "T6 福利免费公式，标题不能用 '最/唯一/第一'"},
    {"topic": "护肤避雷", "persona": "敏感肌", "constraint": "T3 反差冲突，要有 '我以为...结果...'"},
    {"topic": "亲子绘本", "persona": "新手妈妈", "constraint": "T10 步骤指南，副标题写 '3 步'"},
    {"topic": "断舍离", "persona": "出租屋住户", "constraint": "T1 数字对比，限制 18 字"},
    {"topic": "面试自我介绍", "persona": "应届生", "constraint": "T5 身份代入，避开 '最强/保过'"},
    {"topic": "周末独处", "persona": "i 人", "constraint": "T7 时间节点 + 故事感"},
]


_REWRITE_BAD_SAMPLES = [
    {
        "bad": "100% 有效！秋冬最强护肤大法，绝对让你皮肤变好！",
        "issues": ["100%", "最强", "绝对", "无具体方法"],
        "good_hint": "把'绝对/最强'换成'我亲测 3 个月'，给 3 个具体步骤。",
    },
    {
        "bad": "宝子们我跟你说真的，这个东西真的太好用了，不买真的会后悔，都给我冲！！！",
        "issues": ["营销味", "无信息量", "诱导购买"],
        "good_hint": "把'冲'改成具体使用细节 + 适合谁不适合谁。",
    },
    {
        "bad": "副业月入 3 万的方法，加我 vx 私信领",
        "issues": ["导流站外", "夸大收益"],
        "good_hint": "改成'我自己副业 3 个月的真实流水 + 几条踩坑'，不导流。",
    },
    {
        "bad": "护肤其实很简单，按部就班就行，没什么难的。",
        "issues": ["首段无钩子", "无具体场景", "信息密度低"],
        "good_hint": "把'按部就班'改成具体场景：'你是不是也每天早晨手忙脚乱涂 5 层？其实只要...'",
    },
]


# Allen 实战对照：贾维斯陷阱（5 维差距）改写训练
_JARVIS_REWRITE_SAMPLES = [
    {
        "bad": "你是不是也每天累成狗，连周末都不知道怎么过？\n\n建议你：\n1. 早点起床\n2. 出门散步\n3. 远离手机",
        "issues": ["开头挖痛点", "引导建议动作", "我在说话"],
        "good_hint": "重新定义周末（不是用来恢复元气的）+ 展示画面（有人在追日出 / 有人在阳台坐了一下午）+ 让真实用户说话。",
        "allen_dimensions": ["开头", "引导", "角色"],
    },
    {
        "bad": "30+ 干皮女生为什么总是脸又紧又起皮？我推荐你一定要学会这 5 个步骤！",
        "issues": ["开头挖痛点", "我在说话", "教做型"],
        "good_hint": "重新定义干皮（不是缺水，是失衡）+ 展示有人在做（一个 38 岁姐姐三个月没用面霜...）+ 不教做。",
        "allen_dimensions": ["开头", "角色", "结尾"],
    },
    {
        "bad": "想看更多副业内容的扣 1，过 100 我就更下一篇！希望大家都能找到自己的副业",
        "issues": ["运营口吻", "教做型结尾"],
        "good_hint": "邀请语换朋友凑过来：'你呢，你那 8 小时之外是怎么过的'。结尾让读者感觉被珍视：'不论你副业是为了赚钱还是只为了证明自己有别的活法 — 都很对'。",
        "allen_dimensions": ["语气", "结尾"],
    },
]


def cmd_rewrite_jarvis(args: argparse.Namespace) -> int:
    """贾维斯陷阱改写训练：给一段攻略型文案，让你改成范本型。"""
    store = ProfileStore()
    history = load_practice(store)
    task_id = len(history) + 1
    sample = random.choice(_JARVIS_REWRITE_SAMPLES)

    entry = {
        "task_id": task_id,
        "kind": "rewrite-jarvis",
        "issued_at": dt.datetime.now().isoformat(timespec="seconds"),
        "bad": sample["bad"],
        "issues": sample["issues"],
        "allen_dimensions": sample["allen_dimensions"],
        "good_hint": sample["good_hint"],
        "answer": "",
        "score": None,
    }
    append_practice(store, entry)

    print(f"🎯 贾维斯陷阱改写训练 #{task_id}\n")
    print("原文（攻略型 — 教读者怎么做）：")
    print(f"  > {sample['bad']}\n")
    print(f"命中陷阱维度：{', '.join(sample['allen_dimensions'])}")
    print(f"具体问题：{', '.join(sample['issues'])}\n")
    print("改写要求：")
    print("  • 把'教读者怎么做' → 改成'展示什么样的人已经在做'")
    print("  • 至少改掉 2 个命中的陷阱维度\n")
    print(f"提示：{sample['good_hint']}\n")
    print(f"提交：python3 scripts/practice.py grade --task-id {task_id} --answer '你的改写'")
    print()
    print("（参考 data/allen_method.md 末尾「实战对照：贾维斯陷阱」章节）")
    return 0


# ---------- 存储 ----------


def practice_log_path(store: ProfileStore) -> Path:
    return store.root / "practice.jsonl"


def append_practice(store: ProfileStore, entry: Dict[str, Any]) -> None:
    p = practice_log_path(store)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_practice(store: ProfileStore) -> List[Dict[str, Any]]:
    p = practice_log_path(store)
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


# ---------- 子命令 ----------


def cmd_prompt(args: argparse.Namespace) -> int:
    store = ProfileStore()
    history = load_practice(store)
    task_id = len(history) + 1
    prompt = random.choice(_PRACTICE_PROMPTS)

    entry = {
        "task_id": task_id,
        "kind": "prompt",
        "issued_at": dt.datetime.now().isoformat(timespec="seconds"),
        "topic": prompt["topic"],
        "persona": prompt["persona"],
        "constraint": prompt["constraint"],
        "answer": "",
        "score": None,
    }
    append_practice(store, entry)
    print(f"📝 命题练习 #{task_id}\n")
    print(f"  主题约束 : {prompt['topic']}")
    print(f"  目标读者 : {prompt['persona']}")
    print(f"  写作约束 : {prompt['constraint']}\n")
    print(f"提交答案：")
    print(f"  python3 scripts/practice.py grade --task-id {task_id} --answer '你的回答'")
    return 0


def cmd_grade(args: argparse.Namespace) -> int:
    store = ProfileStore()
    history = load_practice(store)
    if args.task_id < 1 or args.task_id > len(history):
        print(f"❌ task_id 无效（{args.task_id}）", file=sys.stderr)
        return 1
    task = history[args.task_id - 1]
    answer = args.answer.strip()
    if not answer:
        print("❌ 答案为空", file=sys.stderr)
        return 1

    # 简单判分：如果答案像"标题"（短）→ 用 score_title；否则按 score_post 当正文
    if len(answer) < 35 and "\n" not in answer:
        s, issues, suggestions = score_title(answer)
        score = int(s * 10)
        breakdown = {"title": s}
        # 给参考标题
        ref = generate_titles(task["topic"], persona=task["persona"], formulas=["T2", "T3"], n_each=1)
        ref_text = " / ".join(t["title"] for t in ref)
    else:
        ps = score_post("(your-title)" if len(answer) > 35 else answer, answer, [])
        score = ps.total
        breakdown = ps.breakdown
        suggestions = ps.suggestions
        ref_text = "（用 brainstorm.py 看更完整的参考骨架）"

    # 更新记录
    task["answer"] = answer
    task["score"] = score
    task["graded_at"] = dt.datetime.now().isoformat(timespec="seconds")
    history[args.task_id - 1] = task
    # 全量 rewrite（小数据量可接受）
    p = practice_log_path(store)
    with p.open("w", encoding="utf-8") as f:
        for h in history:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")

    # 输出
    print(f"📊 命题 #{args.task_id} 评分：{score}/100")
    print(f"   主题：{task['topic']}    约束：{task['constraint']}")
    print(f"   你的回答：{answer[:80]}{'...' if len(answer) > 80 else ''}")
    print()
    if breakdown:
        for k, v in breakdown.items():
            print(f"   {k:<14} {'█' * v}{'░' * (10 - v)} {v}/10")
        print()
    if suggestions:
        print("💡 改进建议：")
        for s in suggestions[:5]:
            print(f"   • {s}")
        print()
    print(f"📚 参考写法：{ref_text}")
    return 0


def cmd_rewrite(args: argparse.Namespace) -> int:
    store = ProfileStore()
    history = load_practice(store)
    task_id = len(history) + 1
    sample = random.choice(_REWRITE_BAD_SAMPLES)

    entry = {
        "task_id": task_id,
        "kind": "rewrite",
        "issued_at": dt.datetime.now().isoformat(timespec="seconds"),
        "bad": sample["bad"],
        "issues": sample["issues"],
        "good_hint": sample["good_hint"],
        "answer": "",
        "score": None,
    }
    append_practice(store, entry)

    print(f"🔧 改写练习 #{task_id}\n")
    print(f"原文（反面教材）：")
    print(f"  > {sample['bad']}\n")
    print(f"已知问题：{', '.join(sample['issues'])}\n")
    print(f"提示：{sample['good_hint']}\n")
    print(f"提交：python3 scripts/practice.py grade --task-id {task_id} --answer '你的改写版本'")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    store = ProfileStore()
    history = load_practice(store)
    if not history:
        print("（还没练过题。从 `practice.py prompt` 或 `practice.py rewrite` 开始）")
        return 0

    cutoff = dt.datetime.now() - dt.timedelta(days=args.days)
    recent = [h for h in history if h.get("issued_at", "") >= cutoff.isoformat(timespec="seconds")]

    print(f"📚 最近 {args.days} 天练习：{len(recent)} 题")
    print()
    if recent:
        graded = [h for h in recent if h.get("score") is not None]
        if graded:
            avg = sum(h["score"] for h in graded) / len(graded)
            best = max(graded, key=lambda x: x["score"])
            print(f"  已评分 {len(graded)} 题，平均 {avg:.1f}，最高 {best['score']}")
            print(f"  最高分题目：#{best['task_id']} - {best.get('topic') or '改写'}")
            print()
        for h in recent[-10:]:
            tag = "📝" if h["kind"] == "prompt" else "🔧"
            score = h.get("score", "?")
            topic = h.get("topic") or h.get("bad", "")[:30]
            print(f"  {tag} #{h['task_id']} ({score}分) {topic}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="practice.py", description="小红书写作训练")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("prompt", help="出一道命题").set_defaults(func=cmd_prompt)
    sub.add_parser("rewrite", help="改写训练（通用反例）").set_defaults(func=cmd_rewrite)
    sub.add_parser("rewrite-jarvis", help="Allen 实战对照：贾维斯陷阱改写").set_defaults(
        func=cmd_rewrite_jarvis)

    pg = sub.add_parser("grade", help="提交答案 + 评分")
    pg.add_argument("--task-id", type=int, required=True)
    pg.add_argument("--answer", required=True)
    pg.set_defaults(func=cmd_grade)

    ph = sub.add_parser("history", help="查看练习历史")
    ph.add_argument("--days", type=int, default=30)
    ph.set_defaults(func=cmd_history)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
