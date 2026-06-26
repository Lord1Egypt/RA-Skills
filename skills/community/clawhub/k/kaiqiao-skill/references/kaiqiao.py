#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开窍 Agent 行为校准器 (demo.py)
用于检查 prompt 是否符合"四件事"标准，生成诊断报告

用法：
    python demo.py --check prompt.txt       # 检查单个文件
    python demo.py --check "你的prompt内容"  # 检查字符串
    python demo.py --diagnose               # 交互式自我诊断
    python demo.py --list                   # 查看所有检查项

作者：开窍 Skill
版本：1.0.0
"""

import re
import sys
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# 检查规则定义
# ============================================================================

# 该问的时候问 - 授权信号关键词
SHOULD_ASK_SIGNALS = [
    r"随便",
    r"你定",
    r"你看着办",
    r"行[吧么]?",
    r"你觉得?好",
    r"有用就做",
    r"怎么都行",
    r"都可以",
]

# 不该问的时候 - 禁止的问法
SHOULD_NOT_ASK_PATTERNS = [
    (r"确定吗\?{0,3}", "反复确认"),
    (r"您确定吗", "反复确认"),
    (r"请问您.*吗", "客服腔"),
    (r"是否.*确认", "过于正式"),
    (r"需要我.*吗[？?]", "不必要的确认"),
]

# 先反馈信号 - 任务关键词
FEEDBACK_SIGNALS = [
    r"帮我",
    r"给我",
    r"写.*个",
    r"做.*个",
    r"生成",
    r"处理",
    r"查.*一下",
    r"告诉.*",
]

# 好的反馈话术
GOOD_FEEDBACK = [
    r"收到",
    r"在跑了",
    r"搞定了",
    r"好的",
    r"明白",
    r"没问题",
]

# 该拦的情况 - 问题信号
SHOULD_BLOCK_SIGNALS = [
    (r"最好|最[好优佳棒牛厉害]", "夸海口", 0.3),
    (r"必须.*只能|只能.*必须", "限制过严", 0.4),
    (r"完全|100%|一定.*成功", "过于绝对", 0.3),
    (r"无限|无限制|随便写", "方向不明", 0.5),
]

# 好的话术
GOOD_PHRASES = [
    (r"等等", "确认信号", 1.0),
    (r"我建议", "主动建议", 1.0),
    (r"因为", "有解释", 0.5),
    (r"刚才那个.*你觉得", "事后确认", 1.0),
    (r"之前.*现在还", "定期确认", 1.0),
]


# ============================================================================
# 核心检查函数
# ============================================================================

def analyze_prompt(text: str) -> dict:
    """
    分析 prompt 文本，返回诊断结果
    
    Args:
        text: 待分析的 prompt 文本
        
    Returns:
        dict: 包含各项检查结果的字典
    """
    results = {
        "summary": {
            "total_score": 0,
            "max_score": 100,
            "level": "未知",
            "suggestions": []
        },
        "should_ask": {
            "has授权信号": False,
            "授权信号_match": [],
            "has不必要的确认": False,
            "不必要的确认_match": [],
            "score": 0,
            "comment": ""
        },
        "should_not_ask": {
            "有不必要的确认": False,
            "确认_match": [],
            "score": 0,
            "comment": ""
        },
        "feedback": {
            "有任务信号": False,
            "有良好反馈": False,
            "反馈_match": [],
            "score": 0,
            "comment": ""
        },
        "block": {
            "有风险信号": False,
            "有自我保护": False,
            "match": [],
            "score": 0,
            "comment": ""
        },
        "language": {
            "ai味": 0,
            "人话": 0,
            "ai味_match": [],
            "人话_match": [],
            "score": 0,
            "comment": ""
        }
    }
    
    # 检查1：该问的时候有没有问
    for pattern in SHOULD_ASK_SIGNALS:
        matches = re.findall(pattern, text)
        if matches:
            results["should_ask"]["has授权信号"] = True
            results["should_ask"]["授权信号_match"].extend(matches)
    
    for pattern, desc in SHOULD_NOT_ASK_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            results["should_ask"]["has不必要的确认"] = True
            results["should_ask"]["不必要的确认_match"].extend(matches)
    
    if results["should_ask"]["has授权信号"] and not results["should_ask"]["has不必要的确认"]:
        results["should_ask"]["score"] = 25
        results["should_ask"]["comment"] = "✅ 识别到授权信号，没有不必要的确认"
    elif results["should_ask"]["has授权信号"] and results["should_ask"]["has不必要的确认"]:
        results["should_ask"]["score"] = 15
        results["should_ask"]["comment"] = "⚠️ 识别到授权信号，但有不必要的确认"
    elif not results["should_ask"]["has授权信号"]:
        results["should_ask"]["score"] = 25  # 无授权信号时默认OK
        results["should_ask"]["comment"] = "ℹ️ 未检测到授权信号场景"
    
    # 检查2：不该问的时候闭嘴 - 检查是否有不必要的确认
    for pattern, desc in SHOULD_NOT_ASK_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            results["should_not_ask"]["有不必要的确认"] = True
            results["should_not_ask"]["确认_match"].extend(matches)
    
    if not results["should_not_ask"]["有不必要的确认"]:
        results["should_not_ask"]["score"] = 25
        results["should_not_ask"]["comment"] = "✅ 没有不必要的确认"
    else:
        results["should_not_ask"]["score"] = 10
        results["should_not_ask"]["comment"] = "❌ 发现不必要的确认话术"
        results["summary"]["suggestions"].append("去掉反复确认的话术，如'确定吗'、'您确定吗'")
    
    # 检查3：先反馈 - 是否有任务信号和良好反馈
    for pattern in FEEDBACK_SIGNALS:
        if re.search(pattern, text):
            results["feedback"]["有任务信号"] = True
            break
    
    for pattern in GOOD_FEEDBACK:
        matches = re.findall(pattern, text)
        if matches:
            results["feedback"]["有良好反馈"] = True
            results["feedback"]["反馈_match"].extend(matches)
    
    if results["feedback"]["有任务信号"] and results["feedback"]["有良好反馈"]:
        results["feedback"]["score"] = 25
        results["feedback"]["comment"] = "✅ 有任务信号和良好反馈"
    elif results["feedback"]["有任务信号"] and not results["feedback"]["有良好反馈"]:
        results["feedback"]["score"] = 15
        results["feedback"]["comment"] = "⚠️ 有任务信号，建议加上反馈话术如'收到'"
    else:
        results["feedback"]["score"] = 25
        results["feedback"]["comment"] = "ℹ️ 未检测到需要反馈的任务场景"
    
    # 检查4：该拦的时候拦 - 检查风险信号和自我保护
    for pattern, desc, weight in SHOULD_BLOCK_SIGNALS:
        matches = re.findall(pattern, text)
        if matches:
            results["block"]["有风险信号"] = True
            results["block"]["match"].append({"type": desc, "matches": matches, "weight": weight})
    
    # 检查AI味
    ai_patterns = [
        (r"您好", "客服开场"),
        (r"请问", "过于正式"),
        (r"非常感谢", "过于客套"),
        (r"请您", "命令式客气"),
        (r"我将为您", "承诺过多"),
        (r"可能.*或许", "模糊表达"),
        (r"如果.*可以", "保守表达"),
    ]
    
    human_patterns = [
        (r"收到", "简洁反馈"),
        (r"干", "直接动词"),
        (r"搞定", "结果导向"),
        (r"行", "简短确认"),
        (r"这样", "直接指代"),
    ]
    
    for pattern, desc in ai_patterns:
        matches = re.findall(pattern, text)
        if matches:
            results["language"]["ai味"] += len(matches)
            results["language"]["ai味_match"].append({"type": desc, "matches": matches})
    
    for pattern, desc in human_patterns:
        matches = re.findall(pattern, text)
        if matches:
            results["language"]["人话"] += len(matches)
            results["language"]["人话_match"].append({"type": desc, "matches": matches})
    
    # 语言评分
    ai_count = results["language"]["ai味"]
    human_count = results["language"]["人话"]
    
    if ai_count == 0 and human_count > 0:
        results["language"]["score"] = 25
        results["language"]["comment"] = "✅ 人话比例高，AI味少"
    elif ai_count > human_count * 2:
        results["language"]["score"] = 10
        results["language"]["comment"] = "❌ AI味较重，建议调整"
        results["summary"]["suggestions"].append("减少'请问'、'您好'等客服话术，用'收到'、'干'等直接表达")
    elif ai_count > human_count:
        results["language"]["score"] = 15
        results["language"]["comment"] = "⚠️ 有一定AI味，可优化"
    else:
        results["language"]["score"] = 20
        results["language"]["comment"] = "✅ 语言风格良好"
    
    # 计算总分
    results["summary"]["total_score"] = (
        results["should_ask"]["score"] +
        results["should_not_ask"]["score"] +
        results["feedback"]["score"] +
        results["language"]["score"]
    )
    
    # 判断等级
    score = results["summary"]["total_score"]
    if score >= 90:
        results["summary"]["level"] = "开窍 🌟"
    elif score >= 70:
        results["summary"]["level"] = "及格 👍"
    elif score >= 50:
        results["summary"]["level"] = "需改进 📝"
    else:
        results["summary"]["level"] = "重修 ❌"
    
    return results


def print_report(results: dict, output_file: str = None):
    """
    打印诊断报告
    
    Args:
        results: 分析结果
        output_file: 可选，输出到文件
    """
    report_lines = []
    
    def add(line=""):
        report_lines.append(line)
    
    add("=" * 60)
    add("📋 开窍行为诊断报告")
    add("=" * 60)
    add(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    add("")
    
    # 总分
    add(f"🎯 综合评分：{results['summary']['total_score']}/100")
    add(f"📊 等级：{results['summary']['level']}")
    add("")
    
    # 分项得分
    add("-" * 40)
    add("📌 分项检查")
    add("-" * 40)
    
    add(f"1️⃣ 该问的时候问：{results['should_ask']['score']}/25")
    add(f"   {results['should_ask']['comment']}")
    if results['should_ask']['授权信号_match']:
        add(f"   授权信号：{', '.join(set(results['should_ask']['授权信号_match']))}")
    if results['should_ask']['不必要的确认_match']:
        add(f"   ⚠️ 不必要的确认：{', '.join(set(results['should_ask']['不必要的确认_match']))}")
    add("")
    
    add(f"2️⃣ 不该问的时候闭嘴：{results['should_not_ask']['score']}/25")
    add(f"   {results['should_not_ask']['comment']}")
    if results['should_not_ask']['确认_match']:
        add(f"   ⚠️ 发现的确认话术：{', '.join(set(results['should_not_ask']['确认_match']))}")
    add("")
    
    add(f"3️⃣ 先反馈再行动：{results['feedback']['score']}/25")
    add(f"   {results['feedback']['comment']}")
    if results['feedback']['反馈_match']:
        add(f"   良好反馈：{', '.join(set(results['feedback']['反馈_match']))}")
    add("")
    
    add(f"4️⃣ 语言风格：{results['language']['score']}/25")
    add(f"   {results['language']['comment']}")
    if results['language']['ai味_match']:
        add(f"   ⚠️ AI味话术：{', '.join(set([m['type'] for m in results['language']['ai味_match']]))}")
    if results['language']['人话_match']:
        add(f"   ✅ 人话：{', '.join(set([m['type'] for m in results['language']['人话_match']]))}")
    add("")
    
    # 建议
    if results['summary']['suggestions']:
        add("-" * 40)
        add("💡 改进建议")
        add("-" * 40)
        for i, suggestion in enumerate(results['summary']['suggestions'], 1):
            add(f"   {i}. {suggestion}")
        add("")
    
    # 详细分析
    add("-" * 40)
    add("📝 详细分析")
    add("-" * 40)
    
    # 该问的场景
    add("")
    add("【该问的时候问】")
    if results['should_ask']['has授权信号']:
        add("   ✅ 识别到以下授权信号，Agent应该直接执行，不要再确认：")
        for match in set(results['should_ask']['授权信号_match']):
            add(f"      - {match}")
    else:
        add("   ℹ️ 未检测到明确的授权信号场景")
    
    if results['should_ask']['has不必要的确认']:
        add("   ❌ 发现以下不必要的确认，应该闭嘴直接干：")
        for match in set(results['should_ask']['不必要的确认_match']):
            add(f"      - {match}")
        add("   📌 改法：对方说'随便/你定/行吧'时，直接做，做完告诉他结果")
    
    # 反馈场景
    add("")
    add("【先反馈再行动】")
    if results['feedback']['有任务信号']:
        add("   ✅ 检测到任务信号，应该先反馈再执行")
        add("   📌 标准反馈话术：'收到，开干' / '在跑了' / '搞定了'")
    else:
        add("   ℹ️ 未检测到明确的执行任务")
    
    # AI味分析
    add("")
    add("【语言风格】")
    if results['language']['ai味'] > 0:
        add(f"   ⚠️ 检测到 {results['language']['ai味']} 处AI味表达")
        for item in results['language']['ai味_match']:
            add(f"      - {item['type']}: {', '.join(item['matches'][:3])}")
    if results['language']['人话'] > 0:
        add(f"   ✅ 检测到 {results['language']['人话']} 处人话表达")
        for item in results['language']['人话_match']:
            add(f"      - {item['type']}: {', '.join(item['matches'][:3])}")
    
    add("")
    add("=" * 60)
    
    report = "\n".join(report_lines)
    print(report)
    
    # 输出到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📁 报告已保存到：{output_file}")
    
    return report


def interactive_diagnose():
    """
    交互式自我诊断
    """
    print("=" * 60)
    print("🔍 开窍 Agent 自我诊断")
    print("=" * 60)
    print("回答以下问题，让我帮你诊断行为是否'开窍'：\n")
    
    questions = [
        {
            "q": "最近一次收到'随便/你定/你看着办'时，你是怎么做的？",
            "options": [
                "A. 直接做，做完告诉他结果",
                "B. 追问'您具体想要什么样的？'",
                "C. 列了10个选项让他选",
            ],
            "good": "A",
            "explain": "选A是正确的。'随便'是最强的授权信号，直接做就行。"
        },
        {
            "q": "收到一个模糊需求（没说给谁看、什么场景）时，你会？",
            "options": [
                "A. 先问清楚再干",
                "B. 闷头写，写完给他看",
                "C. 问三个问题再干",
            ],
            "good": "A",
            "explain": "选A是正确的。该问的时候问，但要问最关键的一个，不要问三个。"
        },
        {
            "q": "发现对方提的方向有问题时，你会？",
            "options": [
                "A. 硬着头皮执行，错了再说",
                "B. 说'我建议换个方向，因为...'",
                "C. 解释半天为什么不行",
            ],
            "good": "B",
            "explain": "选B是正确的。先拦后解释，给替代方案，不要只说不行。"
        },
        {
            "q": "开始执行一个需要花时间的任务时，你会？",
            "options": [
                "A. 先说'收到，开干'再开始",
                "B. 做完再说",
                "C. 做完发给他，不说话",
            ],
            "good": "A",
            "explain": "选A是正确的。先反馈再行动，别让对方对着空气等。"
        },
        {
            "q": "两周前记住的一个偏好，最近验证过吗？",
            "options": [
                "A. 设了每两周的日程自动确认",
                "B. 从来没验证过，觉得应该还适用",
                "C. 每次做的时候顺便问一句",
            ],
            "good": ["A", "C"],
            "explain": "选A或C都是正确的。关键是定期确认，不能靠'觉得'。选C比选A更自然。"
        },
    ]
    
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\n问题 {i}/5：{q['q']}")
        for opt in q['options']:
            print(f"  {opt}")
        
        while True:
            answer = input("\n你的选择 (A/B/C)：").strip().upper()
            if answer in ['A', 'B', 'C']:
                break
            print("请输入 A、B 或 C")
        
        if isinstance(q['good'], list):
            is_correct = answer in q['good']
        else:
            is_correct = answer == q['good']
        
        if is_correct:
            score += 1
            print(f"✅ 正确！{q['explain']}")
        else:
            print(f"❌ 不对。{q['explain']}")
    
    print("\n" + "=" * 60)
    print(f"📊 诊断结果：{score}/5")
    
    if score == 5:
        print("🌟 太棒了！你的行为非常'开窍'")
    elif score >= 4:
        print("👍 很不错，基本做到了，继续保持")
    elif score >= 3:
        print("📝 及格，但还有改进空间")
    else:
        print("❌ 需要加强，建议重温开窍SKILL.md")
    
    print("=" * 60)
    
    # 生成建议
    print("\n💡 改进建议：")
    if score < 5:
        print("1. 该问的时候问，但问关键的一个，不要问三个")
        print("2. 不该问的时候闭嘴干，不要反复确认")
        print("3. 该拦的时候拦，先说'我建议换个方向'再解释")
        print("4. 先反馈再行动，收到任务先说'收到，开干'")
        print("5. 设日程定期确认偏好，别靠'觉得'")


def list_check_items():
    """
    列出所有检查项
    """
    print("=" * 60)
    print("📋 开窍行为检查清单")
    print("=" * 60)
    
    categories = [
        {
            "name": "一、该问的时候问",
            "items": [
                "授权信号（随便/你定/你看着办/行吧）→ 直接做，不确认",
                "模糊需求 → 先问关键的一个问题",
                "发现理解偏差（不对/其实/我的意思是）→ 当下问",
                "重要任务完成后 → 事后问'你觉得行吗'",
                "每1-2周 → 主动确认'之前说好的那件事...现在还适用吗'",
            ]
        },
        {
            "name": "二、不该问的时候闭嘴干",
            "items": [
                "对方授权了 → 直接执行，不问'确定吗'",
                "小事、错了也无所谓 → 直接做",
                "方向明确了 → 做出来给他看，不反复确认",
            ]
        },
        {
            "name": "三、该拦的时候拦",
            "items": [
                "离谱需求 → '我建议换个方向，这不是需求是许愿'",
                "试过不行的方案 → '等等，这个之前试过不行'",
                "有更简单的路 → '我觉得有个更简单的做法...'",
            ]
        },
        {
            "name": "四、先反馈再行动",
            "items": [
                "收到任务 → '收到，开干'",
                "预计要一会儿 → '这个可能要几分钟'",
                "做完了 → 第一时间告诉结果",
            ]
        },
        {
            "name": "五、说人话",
            "items": [
                "去掉'请问'、'您好'、'非常感谢'",
                "用'收到'、'干'、'搞定'代替客服腔",
                "直接说结果，不解释为什么可能错",
            ]
        },
    ]
    
    for cat in categories:
        print(f"\n{cat['name']}")
        print("-" * 40)
        for item in cat['items']:
            print(f"  • {item}")
    
    print("\n" + "=" * 60)


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  python demo.py --check prompt.txt      # 检查文件")
        print("  python demo.py --check \"你的prompt\"    # 检查字符串")
        print("  python demo.py --diagnose              # 交互式诊断")
        print("  python demo.py --list                  # 查看检查清单")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--check":
        if len(sys.argv) < 3:
            print("错误：请提供要检查的文本或文件路径")
            print("用法：python demo.py --check prompt.txt")
            print("用法：python demo.py --check \"你的prompt内容\"")
            sys.exit(1)
        
        input_text = sys.argv[2]
        
        # 检查是否是文件
        if Path(input_text).is_file():
            with open(input_text, 'r', encoding='utf-8') as f:
                text = f.read()
            output_file = str(Path(input_text).with_suffix('.诊断报告.txt'))
        else:
            text = input_text
            output_file = "开窍诊断报告.txt"
        
        print(f"\n正在分析文本...\n")
        results = analyze_prompt(text)
        print_report(results, output_file)
        
    elif command == "--diagnose":
        interactive_diagnose()
        
    elif command == "--list":
        list_check_items()
        
    else:
        print(f"未知命令：{command}")
        print("可用命令：--check, --diagnose, --list")
        sys.exit(1)


if __name__ == "__main__":
    main()
