"""
留言非语 — Mock 演示脚本

模拟完整对话流程，不需要真实 API Key。
预设了一个"职场委屈 + 自我欺骗"的典型用户对话，
完整走一遍：开场 → 对话 → 第5轮分析切换 → 退出人格画像。
"""

import asyncio
import sys
import io
import os
import time
import json

# 强制 UTF-8 输出
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.counselors import COUNSELORS

# ─────────────────────────────────────────────
#  预设的 Mock 对话脚本
#  模拟一个典型用户：被领导打压、嘴上说想辞职但一直没行动
# ─────────────────────────────────────────────

MOCK_CONVERSATION = [
    {
        "user": "我最近工作压力很大，感觉领导总是针对我。",
        "counselor": "静水",
        "reply": "针对你，具体是哪些事让你有这种感觉？",
    },
    {
        "user": "他开会的时候经常当着所有人的面否定我的方案，但对其他人就没这样。",
        "counselor": "静水",
        "reply": "其他人的方案被否定时，是什么样的？",
    },
    {
        "user": "也有被否定，但没有我这么频繁。我觉得我可能就是比较倒霉。",
        "counselor": "静水",
        "reply": '你刚才说领导「总是针对你」，现在又说是「比较倒霉」——这两种解释，你自己更信哪个？',
    },
    {
        "user": "…我不知道。可能两个都有吧。我太累了，有时候想干脆辞了算了。",
        "counselor": "静水",
        "reply": '这个「干脆辞了」的念头出现多久了？',
    },
    {
        "user": "快一年了。但是现在经济形势不好，我又没存什么钱，就一直拖着。",
        "counselor": "静水",
        "reply": "（后台分析中...）",  # 第5轮触发分析
        "analysis_trigger": True,
        "analysis_result": {
            "expression_style": {"score": 4, "observation": '倾向于内敛，情绪通过「累了」「倒霉」等淡化词表达'},
            "locus_of_control": {"score": 3, "observation": '初期归因于领导，压力下迅速转为「倒霉」自我消解'},
            "conflict_pattern": {"score": 2, "observation": "典型回避型，一年内想法从未转化为行动"},
            "self_awareness": {"score": 5, "observation": "有觉察但还在两套解释之间摇摆"},
            "emotional_regulation": {"score": 3, "observation": '在压抑，用「不确定」「可能」等词软化真实感受'},
            "attachment_style": {"type": "焦虑型", "observation": "担心外部环境（经济/存款）作为不行动的挡箭牌"},
            "change_readiness": {"score": 3, "observation": "嘴上说想辞职，实际上找了很多理由留下"},
            "recommended_counselor": "烈风",
            "counselor_reason": "用户在「想走/不走」这个点上已经绕了一年，是典型的自我欺骗循环，需要被直接点破",
            "personality_summary": '一个清楚知道自己不快乐、但用「现实理由」给自己的不行动找合理化的人。真正的问题不是要不要辞职，而是为什么一年后还在同一个位置反复问这个问题。'
        },
        "reply_after_analysis": '一年。你在这个「想辞」和「不辞」之间来回了整整一年。',
    },
    {
        "user": "是啊…感觉自己很没用，连辞职这件事都做不到。",
        "counselor": "烈风",
        "reply": '等一下。辞职没做到，是因为「没用」？还是因为你根本就不想辞？',
    },
    {
        "user": "我当然想辞，只是条件不允许。",
        "counselor": "烈风",
        "reply": "「条件不允许」这句话你说了多少次了？一年里，这些条件有变好过吗？",
    },
    {
        "user": "没有，反而更差了。",
        "counselor": "烈风",
        "reply": "所以条件只会越来越差——那你在等什么？",
    },
]

PERSONALITY_SUMMARY = """
一个清楚知道自己不快乐、但用「现实理由」给自己的不行动找合理化的人。

真正的问题不是要不要辞职，
而是为什么一年后还在同一个位置反复问这个问题。

核心模式：回避型冲突处理 × 外部归因 × 焦虑型依恋

这三个叠在一起的结果，是一个人可以在一个让自己痛苦的处境里待很久很久，
同时一直告诉自己「只是还没到时机」。
"""

# ─────────────────────────────────────────────
#  演示主程序
# ─────────────────────────────────────────────

def print_slow(text, delay=0.03):
    """模拟打字机效果输出"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_separator(char="-", width=50):
    print(char * width)

async def run_demo():
    print()
    print("=" * 50)
    print("  留 言 非 语  [MOCK 演示模式]")
    print("  —— 不是治愈你，而是让你看见自己")
    print("=" * 50)
    print()
    print("  ⚡ 此为预设脚本演示，展示完整对话流程")
    print("  ⚡ 包含：咨询师切换 + 后台人格分析机制")
    print_separator()
    print()

    await asyncio.sleep(0.5)

    # 开场白
    print_slow("[静水]: 你好。今天想聊些什么？")
    print()
    await asyncio.sleep(1)

    current_counselor = "静水"

    for i, turn in enumerate(MOCK_CONVERSATION):
        # 显示用户输入
        print_separator("·", 30)
        print(f"你: {turn['user']}")
        await asyncio.sleep(0.5)

        # 检查是否触发分析
        if turn.get("analysis_trigger"):
            print()
            print("  ┌─ [系统] 第5轮触发后台人格分析...")
            await asyncio.sleep(0.3)
            print("  │  分析维度：表达风格 / 归因方式 / 冲突模式 / 自我觉察...")
            await asyncio.sleep(0.8)

            result = turn["analysis_result"]
            print(f"  │  推荐切换：{result['recommended_counselor']}")
            print(f"  │  原因：{result['counselor_reason']}")
            await asyncio.sleep(0.3)
            print("  └─ [系统] 分析完成，人设切换中...")
            print()
            await asyncio.sleep(0.5)

            # 切换咨询师
            old_counselor = current_counselor
            current_counselor = result["recommended_counselor"]
            print(f"  ※ （切换：{old_counselor} → {current_counselor}）")
            print()
            await asyncio.sleep(0.3)

            reply = turn["reply_after_analysis"]
        else:
            reply = turn["reply"]
            current_counselor = turn["counselor"]

        # 显示咨询师回复
        print(f"[{current_counselor}]: ", end='', flush=True)
        print_slow(reply, delay=0.025)
        print()
        await asyncio.sleep(0.8)

    # 用户退出
    print_separator("·", 30)
    print("你: /quit")
    print()
    await asyncio.sleep(0.5)

    print("再见。希望你比来的时候更了解自己一点。")
    print()
    await asyncio.sleep(0.5)

    # 显示人格画像
    print("=" * 50)
    print("  你的人格画像")
    print("=" * 50)
    print()

    for line in PERSONALITY_SUMMARY.strip().split('\n'):
        print_slow(line.strip() if line.strip() else "", delay=0.02)
        if not line.strip():
            await asyncio.sleep(0.3)

    print()
    print_separator()

    # 显示详细分析数据
    print()
    print("  [调试] 后台分析的完整数据（/status 命令会显示这个）：")
    print()
    analysis = MOCK_CONVERSATION[4]["analysis_result"]
    dimensions = [
        ("表达风格", analysis["expression_style"]["score"], analysis["expression_style"]["observation"]),
        ("归因方式", analysis["locus_of_control"]["score"], analysis["locus_of_control"]["observation"]),
        ("冲突模式", analysis["conflict_pattern"]["score"], analysis["conflict_pattern"]["observation"]),
        ("自我觉察", analysis["self_awareness"]["score"], analysis["self_awareness"]["observation"]),
        ("情绪调节", analysis["emotional_regulation"]["score"], analysis["emotional_regulation"]["observation"]),
        ("改变意愿", analysis["change_readiness"]["score"], analysis["change_readiness"]["observation"]),
    ]

    for name, score, obs in dimensions:
        bar = "█" * score + "░" * (10 - score)
        print(f"  {name:6}  [{bar}] {score:2}/10  {obs}")

    att = analysis["attachment_style"]
    print(f"  {'依恋模式':6}  [{att['type']:^12}]       {att['observation']}")

    print()
    print("=" * 50)
    print("  演示结束。接入真实 API Key 后可体验完整版本。")
    print("=" * 50)
    print()


if __name__ == "__main__":
    asyncio.run(run_demo())
