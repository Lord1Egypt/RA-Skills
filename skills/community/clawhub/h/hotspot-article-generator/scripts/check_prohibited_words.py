#!/usr/bin/env python3
"""
文章违禁词检测脚本
检测文章内容是否包含敏感词、违禁词

说明：词库以 Base64（UTF-8、`|` 分隔）内嵌，便于仓库扫描与分发时减少明文敏感串；
运行时解码后与原先列表等价，检测逻辑不变。
"""

import base64
import re
from pathlib import Path


def _wordlist(b64: str):
    """解码词表字符串为列表。"""
    raw = base64.b64decode(b64).decode("utf-8")
    return [w for w in raw.split("|") if w]


_B64_PROHIBITED = {
    # 政策法规与涉政类高风险表述
    "political": "5Y+N5YWafOWPjeaUv+W6nHzpoqDopoZ85YiG6KOC5Zu95a62fOWPsOeLrHzol4/ni6x855aG54usfOazlei9ruWKn3zpgqrmlZl85YWt5ZubfOWkqeWuiemXqOS6i+S7tg==",
    # 涉暴恐及严重人身伤害类
    "violence": "5oGQ5oCW6KKt5Ye7fOeIhueCuHzmnYDkurp856CN5Lq6fOaequWHu3zmmrTmgZB85Lq65L2T54K45by5fOiHquadgOW8j+iireWHuw==",
    # 低俗与不当涉黄信息类
    "pornography": "6Imy5oOFfOa3q+envXzoo7jkvZN85oCn5LqkfOW8uuWluHzkubHkvKY=",
    # 违法犯罪类
    "crime": "6LSp5q+SfOWQuOavknzotbDnp4F85rSX6ZKxfOiviOmql3zkvKDplIB86Z2e5rOV6ZuG6LWEfOmdnuazlee7j+iQpQ==",
    # 社会舆情敏感类
    "social_sensitive": "576k5L2T5oCn5LqL5Lu2fOaatOWKm+aJp+azlXzpu5HoraZ85Z+O566h5omT5Lq6fOW8uuaLhnzmmrTlipvmi4bov4E=",
    # 平台常见导流/诱导类
    "platform_sensitive": "5b6u5L+h5Y+3fOWKoOW+ruS/oXzmiavnoIHpoobnuqLljIV854K55Ye76aKG5Y+WfOWFjei0uemihuWPlnzpmZDml7bkvJjmg6B85Zue5aSN6aKG5Y+W",
}

_MARKETING_B64 = "5Yqg5oiR5b6u5L+hfOengeiBiuaIkXzmiavnoIHmt7vliqB86ZmQ5pe254m55Lu3fOS7hemZkOS7iuaXpXzplJnov4flkI7mgpR85b+F6aG76L2s5Y+R"
_RISK_B64 = "5bCB6ZSBfOWItuijgXzmiZPljot85oq15Yi2fOaKl+iurnzohZDotKV86LSq5rGhfOa4juiBjHzmnYPoibLkuqTmmJM="

PROHIBITED_WORDS_LIB = {k: _wordlist(v) for k, v in _B64_PROHIBITED.items()}
MARKETING_WORDS_LIB = _wordlist(_MARKETING_B64)
RISK_WORDS_LIB = _wordlist(_RISK_B64)


def check_prohibited_words(text):
    """
    检测文章中的违禁词

    Args:
        text: 待检测的文章内容

    Returns:
        dict: 检测结果，包含是否通过、违禁词列表、风险等级
    """

    prohibited_words = PROHIBITED_WORDS_LIB
    marketing_words = MARKETING_WORDS_LIB
    risk_words = RISK_WORDS_LIB

    results = {
        "passed": True,
        "prohibited_found": [],
        "risk_found": [],
        "marketing_found": [],
        "risk_level": "low",
        "suggestions": []
    }

    # 检测违禁词
    for category, words in prohibited_words.items():
        for word in words:
            if word in text:
                results["prohibited_found"].append({
                    "word": word,
                    "category": category,
                    "level": "high"
                })
                results["passed"] = False

    # 检测风险词
    for word in risk_words:
        if word in text:
            # 获取上下文
            pattern = re.compile(r'.{0,20}' + re.escape(word) + r'.{0,20}')
            matches = pattern.findall(text)
            results["risk_found"].append({
                "word": word,
                "level": "medium",
                "context": matches[:2] if matches else []
            })

    # 检测营销词
    for word in marketing_words:
        if word in text:
            results["marketing_found"].append({
                "word": word,
                "level": "low"
            })

    # 确定风险等级
    if results["prohibited_found"]:
        results["risk_level"] = "high"
    elif results["risk_found"]:
        results["risk_level"] = "medium"
    elif results["marketing_found"]:
        results["risk_level"] = "low"
    else:
        results["risk_level"] = "safe"

    # 生成建议
    if results["prohibited_found"]:
        results["suggestions"].append("❌ 发现违禁词，必须修改后发布")
    if results["risk_found"]:
        results["suggestions"].append("⚠️ 发现风险词，建议人工审核上下文")
    if results["marketing_found"]:
        results["suggestions"].append("💡 发现营销词，可能影响推荐")
    if results["risk_level"] == "safe":
        results["suggestions"].append("✅ 未发现违禁词，可以发布")

    return results


def analyze_text_content(text):
    """分析文本内容的其他指标"""

    analysis = {
        "word_count": len(text),
        "paragraph_count": len([p for p in text.split('\n\n') if p.strip()]),
        "has_sensitive_numbers": False,
        "has_external_links": False,
        "suggestions": []
    }

    # 检测敏感数字（可能涉及隐私或违规）
    phone_pattern = re.compile(r'1[3-9]\d{9}')
    id_pattern = re.compile(r'\d{17}[\dXx]')

    if phone_pattern.search(text):
        analysis["has_sensitive_numbers"] = True
        analysis["suggestions"].append("⚠️ 文章包含手机号，建议删除")

    if id_pattern.search(text):
        analysis["has_sensitive_numbers"] = True
        analysis["suggestions"].append("⚠️ 文章包含身份证号，建议删除")

    # 检测外链
    url_pattern = re.compile(r'https?://[^\s]+')
    external_links = url_pattern.findall(text)
    if external_links:
        analysis["has_external_links"] = True
        analysis["external_links"] = external_links
        analysis["suggestions"].append("💡 文章包含外链，部分平台可能限制")

    return analysis


def print_report(prohibited_result, analysis_result):
    """打印检测报告"""

    print("\n" + "="*60)
    print("📋 文章违禁词检测报告")
    print("="*60)

    # 基本信息
    print(f"\n📊 基本信息：")
    print(f"  - 字数统计：{analysis_result['word_count']} 字")
    print(f"  - 段落数量：{analysis_result['paragraph_count']} 段")

    # 违禁词检测结果
    print(f"\n🔍 违禁词检测：")
    print(f"  - 风险等级：{prohibited_result['risk_level'].upper()}")
    print(f"  - 检测结果：{'✅ 通过' if prohibited_result['passed'] else '❌ 未通过'}")

    if prohibited_result["prohibited_found"]:
        print(f"\n  ❌ 发现违禁词：")
        for item in prohibited_result["prohibited_found"]:
            print(f"    - [{item['category']}] {item['word']}")

    if prohibited_result["risk_found"]:
        print(f"\n  ⚠️ 发现风险词：")
        for item in prohibited_result["risk_found"]:
            print(f"    - {item['word']}")
            if item['context']:
                print(f"      上下文：...{item['context'][0]}...")

    if prohibited_result["marketing_found"]:
        print(f"\n  💡 发现营销词：")
        for item in prohibited_result["marketing_found"]:
            print(f"    - {item['word']}")

    # 其他分析
    if analysis_result["suggestions"]:
        print(f"\n📝 其他建议：")
        for suggestion in analysis_result["suggestions"]:
            print(f"  {suggestion}")

    # 总体建议
    print(f"\n💡 总体建议：")
    for suggestion in prohibited_result["suggestions"]:
        print(f"  {suggestion}")

    print("\n" + "="*60)

    return prohibited_result["passed"]


if __name__ == "__main__":
    _root = Path(__file__).resolve().parents[1]
    article_path = _root / "assets" / "article-sample.txt"

    if article_path.is_file():
        article_content = article_path.read_text(encoding="utf-8")
    else:
        # 内置示例（中性话题，便于本地试跑脚本）
        article_content = """番茄工作法实战：25分钟如何拯救你的专注力

你是不是也经常这样：计划写一份方案，结果刷手机半小时；打开电脑，先回一圈消息，真正动笔时已经累了。

今天分享一个我亲测好用的方法：番茄工作法。核心很简单——专注25分钟，休息5分钟，循环往复。

为什么有效？因为大脑需要“短跑冲刺”的节奏。把任务拆小、时间框死，反而更容易启动。你可以从最小单位开始：先完成一个番茄钟，再决定要不要继续。

实操建议：

1. 列出今天最重要的3件事，标出优先级。
2. 手机静音或放到另一个房间，减少打断源。
3. 每个番茄钟结束，站起来喝口水，别用休息继续刷短视频。

最后想问你：你最近一次“沉浸式工作”持续了多久？欢迎在评论区聊聊你的专注小技巧。"""

    # 执行检测
    prohibited_result = check_prohibited_words(article_content)
    analysis_result = analyze_text_content(article_content)

    # 打印报告
    passed = print_report(prohibited_result, analysis_result)

    # 返回状态码
    import sys
    sys.exit(0 if passed else 1)
