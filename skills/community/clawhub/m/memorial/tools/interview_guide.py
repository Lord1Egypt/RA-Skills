#!/usr/bin/env python3
"""
interview_guide.py — 访谈问题生成器

支持两种模式：
  - 家人访谈（--role spouse/child/...）：问家人关于档案主人的问题
  - 本人访谈（--role self）：生前建档，直接问档案主人本人

用法：
  python interview_guide.py --meta ../memorials/grandpa_wang/meta.json --role spouse
  python interview_guide.py --name "爷爷" --birth 1938 --role child
  python interview_guide.py --name "奶奶" --birth 1940 --role self          # 生前建档
  python interview_guide.py --meta ../memorials/grandpa_wang/meta.json --all-roles
  python interview_guide.py --name "奶奶" --role self --sessions short      # 适合分次进行
"""

import argparse
import json
import os
from typing import Optional


# ── 问题库 ────────────────────────────────────────────────────────────────────

# 所有角色通用问题
UNIVERSAL_QUESTIONS = [
    "你第一次见到 {name} 是什么情景？",
    "在你心里，{name} 最大的特点是什么？用一两个词来形容。",
    "有没有一句话是 {name} 经常说的？",
    "有没有一件事，让你觉得很能代表 {name} 这个人？",
    "你最想让后辈记住 {name} 的哪一面？",
]

# 按关系类型的问题
ROLE_QUESTIONS = {
    "spouse": [  # 配偶
        "你们是怎么认识的？",
        "结婚后，{name} 在家里是什么角色——主要决策者，还是更多默默支持？",
        "{name} 表达爱意的方式是什么？说出来，还是做出来？",
        "你们有没有特别的习惯或仪式？比如固定一起做什么事。",
        "{name} 最让你感动的一件事是什么？",
        "{name} 最难相处的地方是什么？",
        "吵架的时候，{name} 一般是什么反应？",
        "晚年的 {name} 有什么变化？",
        "{name} 有没有说过什么遗憾，或者想做却没做的事？",
        "你最想对 {name} 说什么，但那时没说出口？",
    ],
    "child": [  # 子女
        "{name} 对你的教育方式是什么样的？严格，还是宽松？",
        "{name} 表达对你的爱是用说的，还是用做的？举个例子。",
        "你小时候最怕 {name} 什么？",
        "你长大后，对 {name} 的看法有没有变化？",
        "{name} 有没有让你觉得特别骄傲的时刻？",
        "{name} 在你最艰难的时候，是怎么支持你的？",
        "{name} 对你影响最深的一件事或一句话是什么？",
        "如果你能问 {name} 一个问题，你会问什么？",
    ],
    "grandchild": [  # 孙辈
        "你跟 {name} 最深的记忆是什么？",
        "{name} 会对你说什么——平时怎么跟你说话？",
        "{name} 喜欢跟你做什么事情？",
        "{name} 有没有给你讲过什么故事或者道理？",
        "{name} 在你眼里跟爸爸妈妈有什么不一样？",
    ],
    "sibling": [  # 兄弟姐妹
        "你们小时候是什么关系？亲近还是有些距离？",
        "{name} 在兄弟姐妹里是什么角色——老大的担当，还是有点特别？",
        "长大后，你们的关系怎么样？",
        "{name} 有没有为你做过让你特别感动的事？",
        "你们之间有没有特别的默契或者共同话题？",
    ],
    "friend": [  # 朋友
        "你们是什么时候、因为什么成为朋友的？",
        "{name} 在你眼里是什么样的人？",
        "你们一般在一起做什么？",
        "{name} 遇到困难的时候，是什么反应？",
        "{name} 有没有什么事是只有你知道的？",
    ],
    "colleague": [  # 同事/学生
        "{name} 工作/教学的风格是什么？",
        "{name} 最让同事/学生印象深刻的地方是什么？",
        "{name} 在工作上有什么原则是绝对不退让的？",
        "有没有一件工作上的事，让你觉得很能代表 {name}？",
        "{name} 如何对待比自己资历浅的人？",
    ],
}

# ── 本人访谈问题（生前建档模式）────────────────────────────────────────────────

# 问本人自己的问题，分5个模块，可整次或分次进行
SELF_QUESTIONS = {
    "origin": {  # 模块A：从哪里来
        "label": "从哪里来",
        "intro": "关于你的早年经历和成长背景",
        "questions": [
            "你是哪里人？小时候在哪里长大的？",
            "那时候的生活是什么样的？",
            "你记得的，关于你小时候最深的一件事是什么？",
            "你的父母是什么样的人？他们对你影响最大的是什么？",
            "你读书了吗？读到什么程度？那段时间对你意味着什么？",
            "你有兄弟姐妹吗？你们之间是什么关系？",
        ],
    },
    "journey": {  # 模块B：走过了什么
        "label": "走过了什么",
        "intro": "关于人生中的转折点和重大经历",
        "questions": [
            '你这辈子，有没有哪个时间节点，让你觉得"从那之后不一样了"？',
            "你做过的最重要的一个决定是什么？",
            "有没有一段特别难熬的时期？那时候你怎么撑过来的？",
            "你最骄傲的一件事是什么？",
            "有没有一件事，你当时觉得很难，但后来发现是好事？",
        ],
    },
    "values": {  # 模块C：在乎什么
        "label": "在乎什么",
        "intro": "关于价值观和人生哲学",
        "questions": [
            "你这辈子，最在乎的是什么？",
            "有没有什么事，是你觉得无论如何都不能做的？",
            "你觉得一个人怎么样才算活得好？",
            "有没有什么话或者道理，是你一直信的？",
            "你最想让我们记住你的哪一面？",
        ],
    },
    "family": {  # 模块D：关于家人
        "label": "关于家人",
        "intro": "关于你和家人之间的事",
        "questions": [
            "你对我们（家人）最想说的一句话是什么？",
            "你觉得自己做得最好的地方是什么？最遗憾的地方呢？",
            "有没有什么话，是你一直想说但没说出口的？",
            "你希望我们以后记住你什么？",
            "你觉得你给我们留下了什么？",
        ],
    },
    "legacy": {  # 模块E：留下什么
        "label": "留下什么",
        "intro": "关于这一生和想传递的东西",
        "questions": [
            "你这辈子，有没有什么事是很想做但一直没做的？",
            "如果让你对年轻时候的自己说一句话，你会说什么？",
            "有没有什么经历，是你觉得值得讲给孩子们听的？",
            "你最希望我们从你身上学到什么？",
            "有没有什么东西——不管是物件还是习惯——你希望我们好好保留？",
        ],
    },
}

# 根据年代为本人访谈添加历史相关问题
SELF_ERA_QUESTIONS = {
    "pre1945": [
        "你经历过战争年代吗？那时候你在哪里，在做什么？",
        "那段时间，你们家是怎么过的？",
    ],
    "1945_1965": [
        "你经历过三年困难时期吗？那时候是什么感受？",
        "文革的时候，你在哪里？那段时间对你影响大吗？",
    ],
    "1965_1980": [
        "改革开放对你的生活有什么影响？",
        '你年轻的时候，有没有什么机会让你觉得"时代变了"？',
    ],
}

# 基于年代的追加问题
ERA_QUESTIONS = {
    "pre1945": [  # 1945前出生
        "{name} 有没有讲过战争年代的事？",
        "{name} 对于当年经历过的困难，是怎么看的？",
    ],
    "1945_1965": [  # 1945-1965出生
        "{name} 有没有提过文革或者那个年代的事情？",
        "{name} 对于物质方面（节俭/浪费）有什么特别的态度？",
    ],
    "1965_1980": [  # 1965-1980出生
        "{name} 有没有聊过改革开放对 ta 的影响？",
        "{name} 年轻时有没有什么经历特别影响了 ta？",
    ],
}


# ── 问题生成 ──────────────────────────────────────────────────────────────────

def get_era_key(birth_year: Optional[int]) -> Optional[str]:
    """根据出生年份返回年代键。"""
    if not birth_year:
        return None
    if birth_year < 1945:
        return "pre1945"
    elif birth_year < 1965:
        return "1945_1965"
    elif birth_year < 1980:
        return "1965_1980"
    return None


def generate_questions(
    name: str,
    role: str,
    birth_year: Optional[int] = None,
    occupation: Optional[str] = None,
) -> list[str]:
    """生成访谈问题列表。"""
    questions = []

    # 通用问题
    questions.extend(UNIVERSAL_QUESTIONS)

    # 角色特定问题
    role_qs = ROLE_QUESTIONS.get(role, [])
    questions.extend(role_qs)

    # 年代相关问题
    era_key = get_era_key(birth_year)
    if era_key:
        questions.extend(ERA_QUESTIONS.get(era_key, []))

    # 职业相关（如果是教师，使用 colleague 里的学生问题）
    if occupation and ("教师" in occupation or "老师" in occupation) and role not in ("colleague",):
        questions.append(f"{{name}} 教书的时候，学生怎么评价 ta？")
        questions.append(f"有没有 {{name}} 说过的话，让学生记了很久？")

    # 格式化（替换 {name}）
    formatted = [q.format(name=name) for q in questions]

    # 去重
    seen = set()
    result = []
    for q in formatted:
        if q not in seen:
            seen.add(q)
            result.append(q)

    return result


def generate_self_questions(
    name: str,
    birth_year: Optional[int] = None,
    session_mode: str = "full",
) -> dict:
    """
    生成本人访谈问题（生前建档模式）。
    session_mode:
      'full'  — 一次性完整版（所有5个模块）
      'short' — 分次版，每次一个模块，适合体力不好的老人
    返回 dict，key 为模块名，value 为该模块问题列表。
    """
    modules = {}
    for module_key, module_data in SELF_QUESTIONS.items():
        questions = list(module_data["questions"])  # 复制，避免污染原始数据

        # 年代相关追加
        if module_key == "journey" and birth_year:
            era_key = get_era_key(birth_year)
            if era_key:
                questions.extend(SELF_ERA_QUESTIONS.get(era_key, []))

        modules[module_key] = {
            "label": module_data["label"],
            "intro": module_data["intro"],
            "questions": questions,
        }

    return modules


def format_self_guide(name: str, modules: dict, session_mode: str = "full") -> str:
    """格式化本人访谈指南为 Markdown。"""
    lines = [
        f"# {name} 的生前访谈问题",
        "",
        "> 这套问题是直接问 **ta 本人** 的，用于生前建档。",
        "> 由 ta 亲口讲述，是质量最高的档案材料。",
        "",
    ]

    if session_mode == "short":
        lines += [
            "**分次进行模式**：每次只聊一个模块，不用一次讲完。",
            "建议顺序：从哪里来 → 走过了什么 → 在乎什么 → 关于家人 → 留下什么",
            "",
        ]
    else:
        total = sum(len(m["questions"]) for m in modules.values())
        lines += [
            f"共 {total} 个问题，分 {len(modules)} 个模块。",
            "不必按顺序问，跟着对话自然展开。",
            "",
        ]

    lines += ["---", ""]

    for i, (module_key, module_data) in enumerate(modules.items(), 1):
        lines.append(f"## 模块 {i}：{module_data['label']}")
        lines.append(f"*{module_data['intro']}*")
        lines.append("")
        for j, q in enumerate(module_data["questions"], 1):
            lines.append(f"{j}. {q}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 访谈建议",
        "",
        "- **用 ta 自己的话**：逐字记录，不替 ta 总结或润色",
        "- **允许跑题**：跑题往往是最有价值的部分，跟着走",
        "- **不催促**：有时候 ta 需要想一想才能说出来",
        "- **分多次进行**：几十年的人生不适合一次谈透",
        "- **让家人也在场**：ta 可能会说出从未对你们说过的话",
        "",
        "## 记录建议",
        "",
        "- 录音（征得同意），事后整理为文字",
        "- 记录时注明：**[本人口述，{date}]**",
        "- 如果 ta 对某个话题沉默或不愿讲，记录这个观察本身，不要追问",
        "",
        "*访谈完成后，将整理好的文字上传到纪念档案中。*",
        "*本人口述的内容与家人口述严格区分标注，是最珍贵的一手材料。*",
    ]

    return "\n".join(lines)


def format_guide(name: str, role: str, questions: list[str]) -> str:
    """格式化家人访谈指南为 Markdown。"""
    role_labels = {
        "spouse": "配偶",
        "child": "子女",
        "grandchild": "孙辈",
        "sibling": "兄弟姐妹",
        "friend": "朋友",
        "colleague": "同事/学生",
    }
    role_label = role_labels.get(role, role)

    lines = [
        f"# 关于 {name} 的访谈问题（{role_label}版）",
        "",
        "以下问题仅供参考，不必按顺序提问。",
        "重要的是让对方自由叙述，这里的问题只是引子。",
        "",
        "---",
        "",
    ]

    # 按类型分段（简单起见，分为前5个通用+后面角色特定）
    universal_count = len(UNIVERSAL_QUESTIONS)
    universal_qs = questions[:universal_count]
    role_qs = questions[universal_count:]

    if universal_qs:
        lines.append("## 通用问题（任何角色都可以问）")
        lines.append("")
        for i, q in enumerate(universal_qs, 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    if role_qs:
        lines.append(f"## {role_label}专属问题")
        lines.append("")
        for i, q in enumerate(role_qs, len(universal_qs) + 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 访谈建议",
        "",
        "- 不要急着记笔记，先让对方把故事讲完",
        "- 遇到有故事性的回答，多问「然后呢？」「那时候你们怎么想的？」",
        "- 允许对方沉默，很多重要的事需要想一想才能说出来",
        "- 如果对方情绪波动，不要急着跳到下一个问题",
        "",
        "*访谈完成后，可以将录音或笔记上传到纪念档案中。*",
    ]

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="家人访谈问题生成器")
    parser.add_argument("--meta", help="meta.json 路径（自动读取基本信息）")
    parser.add_argument("--name", help="逝者称呼")
    parser.add_argument("--birth", type=int, help="出生年份")
    parser.add_argument("--death", type=int, help="离世年份")
    parser.add_argument("--occupation", help="职业")
    all_roles = list(ROLE_QUESTIONS.keys()) + ["self"]
    parser.add_argument("--role", choices=all_roles,
                        help="访谈对象角色（self = 本人访谈，用于生前建档）")
    parser.add_argument("--sessions", choices=["full", "short"], default="full",
                        help="本人访谈的分次模式：full=一次完成，short=每次一个模块（默认full）")
    parser.add_argument("--all-roles", action="store_true",
                        help="生成所有家人角色的问题（不含self）")
    parser.add_argument("--output", help="输出文件路径")
    args = parser.parse_args()

    # 从 meta.json 读取基本信息
    name = args.name
    birth_year = args.birth
    occupation = args.occupation

    if args.meta:
        if not os.path.exists(args.meta):
            print(f"[错误] 找不到 meta.json：{args.meta}")
            return
        with open(args.meta, encoding="utf-8") as f:
            meta = json.load(f)
        name = name or meta.get("name", "")
        profile = meta.get("profile", {})
        birth_year = birth_year or profile.get("birth_year")
        occupation = occupation or profile.get("occupation")

    if not name:
        print("[错误] 需要提供 --name 或 --meta 参数")
        return

    # 本人访谈模式（生前建档）
    if args.role == "self":
        modules = generate_self_questions(name, birth_year, args.sessions)
        full_output = format_self_guide(name, modules, args.sessions)
    else:
        roles = list(ROLE_QUESTIONS.keys()) if args.all_roles else [args.role or "child"]
        all_reports = []
        for role in roles:
            questions = generate_questions(name, role, birth_year, occupation)
            report = format_guide(name, role, questions)
            all_reports.append(report)
        full_output = "\n\n---\n\n".join(all_reports)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"[输出] 访谈问题已保存到 {args.output}")
    else:
        print(full_output)


if __name__ == "__main__":
    main()
