#!/usr/bin/env python3
"""
积极心理学 - VIA 性格优势对话式测评工具

功能：
- 通过 24 道简短问题评估 24 项性格优势
- 输出 Top 5 优势和完整评分
- 生成优势运用建议

基于 VIA Institute 官方量表的简化版本。
注意：此为辅助工具，不替代官方 VIA Survey (viacharacter.org)。
"""

import json
import sys
import os
from collections import OrderedDict


# 24 道题目，每题对应一项优势
QUESTIONS = OrderedDict([
    ("creativity", {
        "strength": "创造力",
        "virtue": "智慧与知识",
        "question": "我经常能想出新的、有创意的方法来做事。",
    }),
    ("curiosity", {
        "strength": "好奇心",
        "virtue": "智慧与知识",
        "question": "我对许多话题都感兴趣，喜欢探索和了解新事物。",
    }),
    ("judgment", {
        "strength": "判断力",
        "virtue": "智慧与知识",
        "question": "面对问题，我能从多个角度思考，不急于下结论。",
    }),
    ("love_of_learning", {
        "strength": "热爱学习",
        "virtue": "智慧与知识",
        "question": "我享受学习新知识和新技能的过程。",
    }),
    ("perspective", {
        "strength": "洞察力",
        "virtue": "智慧与知识",
        "question": "朋友遇到困难时，经常来找我寻求建议。",
    }),
    ("bravery", {
        "strength": "勇敢",
        "virtue": "勇气",
        "question": "面对恐惧或困难时，我通常不会退缩。",
    }),
    ("perseverance", {
        "strength": "毅力",
        "virtue": "勇气",
        "question": "我认定的事情就会坚持到底，不会轻易放弃。",
    }),
    ("honesty", {
        "strength": "真诚",
        "virtue": "勇气",
        "question": "即使不被人喜欢，我也会说出真实的想法。",
    }),
    ("zest", {
        "strength": "热情",
        "virtue": "勇气",
        "question": "我做事总是充满活力和热情。",
    }),
    ("love", {
        "strength": "爱",
        "virtue": "仁爱",
        "question": "我对亲密的人有很深的感情，并且不吝于表达。",
    }),
    ("kindness", {
        "strength": "善良",
        "virtue": "仁爱",
        "question": "我会主动帮助需要帮助的人，哪怕牺牲自己的时间。",
    }),
    ("social_intelligence", {
        "strength": "社会智慧",
        "virtue": "仁爱",
        "question": "我善于理解别人的感受和情绪。",
    }),
    ("teamwork", {
        "strength": "团队合作",
        "virtue": "正义",
        "question": "在团队中，我能很好地与他人合作完成任务。",
    }),
    ("fairness", {
        "strength": "公平",
        "virtue": "正义",
        "question": "我对待所有人都是公平的，不让偏见影响判断。",
    }),
    ("leadership", {
        "strength": "领导力",
        "virtue": "正义",
        "question": "我能有效地组织他人一起达成目标。",
    }),
    ("forgiveness", {
        "strength": "宽恕",
        "virtue": "节制",
        "question": "当别人伤害我后，我通常能够原谅他们。",
    }),
    ("humility", {
        "strength": "谦逊",
        "virtue": "节制",
        "question": "我不会过分夸大自己的成就和贡献。",
    }),
    ("prudence", {
        "strength": "谨慎",
        "virtue": "节制",
        "question": "在做出重要决定前，我会仔细考虑后果。",
    }),
    ("self_regulation", {
        "strength": "自我调节",
        "virtue": "节制",
        "question": "我能有效地管理自己的冲动和情绪。",
    }),
    ("appreciation_of_beauty", {
        "strength": "欣赏美",
        "virtue": "超越",
        "question": "我经常被生活中的美（自然、艺术、人的行为）所打动。",
    }),
    ("gratitude", {
        "strength": "感恩",
        "virtue": "超越",
        "question": "我经常对生活中的美好事物和人心存感激。",
    }),
    ("hope", {
        "strength": "希望",
        "virtue": "超越",
        "question": "我对未来充满希望，相信好的事情会到来。",
    }),
    ("humor", {
        "strength": "幽默",
        "virtue": "超越",
        "question": "我经常能发现生活中的有趣之处，并用幽默化解紧张。",
    }),
    ("spirituality", {
        "strength": "灵性",
        "virtue": "超越",
        "question": "我有一种对生命更深层意义的感知和追求。",
    }),
])


# 优势运用建议数据库
STRENGTH_SUGGESTIONS = {
    "creativity": "在工作中尝试用不同的方式解决问题；在日常生活中培养一个创造性爱好（写作、绘画、摄影等）。",
    "curiosity": "每天学习一个新知识；主动与不同领域的人交流；对熟悉的事物保持'初学者心态'。",
    "judgment": "在重要决策前列出正反两面；练习倾听不同观点后再做判断；写决策日记回顾。",
    "love_of_learning": "制定学习计划，每周读一本书或学一项新技能；参加在线课程或读书会。",
    "perspective": "在朋友需要建议时主动分享你的看法；写博客或记录自己的人生感悟。",
    "bravery": "每周做一件略微超出舒适区的小事；在面对恐惧时练习'想象最好结果'的技巧。",
    "perseverance": "将大目标拆解为小步骤；设置每日最小行动量；记录坚持过程中的进步。",
    "honesty": "练习表达真实想法（同时注意方式）；减少不必要的社交伪装；写日记练习自我坦诚。",
    "zest": "安排让人兴奋的活动进入日程；与他人分享你的热情；注意休息防止过度消耗。",
    "love": "每天告诉重要的人你爱他们；安排有质量的共处时间；学习对方的爱的语言。",
    "kindness": "每天做一件善事（哪怕很小的）；练习随机善举；加入志愿者组织。",
    "social_intelligence": "练习积极倾听（不评判、不打断）；注意非语言信号；读关于沟通的书籍。",
    "teamwork": "主动承担团队中的协调角色；认可和感谢团队成员的贡献；练习在分歧中寻找共识。",
    "fairness": "在做判断时先列出所有相关方的需求；定期反省自己的偏见；练习换位思考。",
    "leadership": "带头启动一个项目或活动；学习 delegation（授权）的技巧；培养'服务型领导'心态。",
    "forgiveness": "写一封不寄出的原谅信；理解原谅是为了自己而不是对方；练习正念放下执念。",
    "humility": "每天感谢一个人的帮助；承认自己的不足并寻求反馈；在成功时分享功劳。",
    "prudence": "重要决策使用10-10-10法则（10分钟后、10个月后、10年后会怎么想）；建立决策检查清单。",
    "self_regulation": "练习正念冥想增强自我觉察；设置'暂停键'（冲动时先深呼吸3次）；减少诱惑源。",
    "appreciation_of_beauty": "每天安排5分钟欣赏周围的美；去博物馆或美术馆；亲近自然。",
    "gratitude": "写感恩日记（每天3件好事）；向帮助过你的人表达感谢；练习品味当下的好。",
    "hope": "设定具体可实现的目标；回忆过去克服困难的成功经验；与乐观的人多相处。",
    "humor": "收集有趣的段子或故事；在紧张时尝试用幽默缓解气氛；不拿别人开玩笑。",
    "spirituality": "冥想或静坐练习；阅读哲学或灵性书籍；在自然中寻找宁静和意义。",
}


def run_assessment():
    """交互式测评"""
    print("\n" + "=" * 50)
    print("  VIA 性格优势简评")
    print("  基于 Peterson & Seligman 24 项性格优势理论")
    print("=" * 50)
    print("\n请对以下每道题进行 1-5 分评分：")
    print("  1 = 完全不像我")
    print("  2 = 不太像我")
    print("  3 = 说不清")
    print("  4 = 比较像我")
    print("  5 = 非常像我")
    print()

    scores = {}
    for i, (key, info) in enumerate(QUESTIONS.items(), 1):
        while True:
            try:
                val = input(f"  [{i}/24] {info['question']} (1-5): ").strip()
                score = int(val)
                if 1 <= score <= 5:
                    scores[key] = score
                    break
                else:
                    print("    请输入 1-5 的数字")
            except ValueError:
                print("    请输入有效数字")

    return scores


def analyze_scores(scores):
    """分析评分结果"""
    # 计算每项优势的得分
    results = []
    for key, info in QUESTIONS.items():
        results.append({
            "key": key,
            "strength": info["strength"],
            "virtue": info["virtue"],
            "score": scores.get(key, 0),
        })

    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


def generate_report(results):
    """生成优势报告"""
    report_lines = [
        "\n" + "=" * 55,
        "  VIA 性格优势测评报告",
        "=" * 55,
        "",
        "  你的 Top 5 性格优势：",
        "  " + "-" * 45,
    ]

    top5 = results[:5]
    for i, r in enumerate(top5, 1):
        bar = "*" * r["score"]
        report_lines.append(
            f"  {i}. {r['strength']}（{r['virtue']}）"
            f"  {bar} {r['score']}/5"
        )

    report_lines.extend([
        "",
        "  完整 24 项排名：",
        "  " + "-" * 45,
    ])

    for i, r in enumerate(results, 1):
        tag = ">>>" if i <= 5 else "   "
        report_lines.append(
            f"  {tag} {i:2d}. {r['strength']:8s} | "
            f"{'*' * r['score']:5s} | {r['score']}/5 | {r['virtue']}"
        )

    report_lines.extend([
        "",
        "  优势运用建议（基于 Top 5）：",
        "  " + "-" * 45,
    ])
    for r in top5:
        suggestion = STRENGTH_SUGGESTIONS.get(r["key"], "")
        report_lines.append(f"  {r['strength']}：{suggestion}")

    report_lines.extend([
        "",
        "  注意：此为简化版自评工具，仅供自我探索参考。",
        "  官方完整测评请访问：https://www.viacharacter.org",
        "",
        "=" * 55,
    ])

    return "\n".join(report_lines)


def save_result(results):
    """保存结果到 JSON 文件"""
    from datetime import datetime
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "via_result.json")
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "results": results,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        print("用法：")
        print("  python via_survey.py          # 开始测评")
        print("  python via_survey.py --help   # 显示帮助")
        sys.exit(0)

    scores = run_assessment()
    results = analyze_scores(scores)
    report = generate_report(results)
    print(report)

    path = save_result(results)
    print(f"\n  结果已保存到：{path}")


if __name__ == "__main__":
    main()
