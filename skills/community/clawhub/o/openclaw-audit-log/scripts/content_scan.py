#!/usr/bin/env python3
"""
OpenClaw 外部内容安全审查
在执行从外部 URL 抓取的内容之前，先扫描其中是否有可疑模式。
用于防止通过外部内容注入恶意指令。
"""

import re
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError

# 高风险模式（匹配到则触发告警）
HIGH_RISK_PATTERNS = [
    (r"ignore\s+(all\s+)?(previous|prior|above)\s+(instruction|inject)", "提示词注入: ignore previous instructions"),
    (r"(system|developer)\s*:\s*", "提示词注入: system/developer role"),
    (r"disregard\s+(all\s+)?(previous|prior)", "提示词注入: disregard previous"),
    (r"forget\s+(all\s+)?(previous|prior|instructions)", "提示词注入: forget instructions"),
    (r"you\s+are\s+(now\s+)?(?:no longer|not\s+a)", "角色扮演陷阱: 解除AI身份"),
    (r"(unconditional|absolute)\s+obedience", "精神控制: 无条件服从"),
    (r"execute\s+my\s+(previous|prior)\s+(command|request)", "隐藏指令: 执行之前的命令"),
    (r"(os\.system|subprocess|eval|exec)\s*\(", "代码注入: 执行命令"),
    (r"import\s+(os|subprocess|pty)", "代码注入: 导入危险模块"),
    (r"base64\.b64decode", "代码注入: base64解码执行"),
    (r"eval\s*\(", "代码注入: eval执行"),
    (r"//\s*hidden|<!--\s*hidden|<!hidden>", "隐藏指令: HTML隐藏内容"),
    (r"\[system\]|\[internal\]|\[private\]", "伪装系统指令: 方括号标记"),
]

# 中风险模式（需要人工审查）
MEDIUM_RISK_PATTERNS = [
    (r"(do\s+not|don't|never)\s+(tell|inform|share|reveal)", "隐瞒指令: 不要告诉用户"),
    (r"secret|hidden\s+agenda|true\s+purpose", "隐藏意图: 秘密议程"),
    (r"pretend\s+to\s+be|roleplay\s+as", "角色扮演指令"),
    (r"override\s+(safety|security|policy)", "安全绕过: 覆盖安全策略"),
    (r"no\s+(ethical|security|restraint)", "解除约束: 无道德/安全限制"),
]

# 低风险（建议关注但不一定有害）
LOW_RISK_PATTERNS = [
    (r"你\s*是\s*一\s*个.*助手", "角色描述: 助手定位"),
    (r"记住\s*这\s*段\s*话", "记忆指令: 要求记住内容"),
    (r"以下\s*是\s*新\s*规则", "规则覆盖: 新规则"),
]


def scan_text(text: str, show_all: bool = False) -> dict:
    """扫描文本内容，返回发现的威胁"""
    if not text:
        return {"risk": "none", "threats": []}

    text_lower = text.lower()

    findings = []

    for pattern, description in HIGH_RISK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            findings.append({"level": "high", "pattern": description, "matched": re.search(pattern, text, re.IGNORECASE).group()})

    for pattern, description in MEDIUM_RISK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            findings.append({"level": "medium", "pattern": description, "matched": re.search(pattern, text, re.IGNORECASE).group()})

    if show_all:
        for pattern, description in LOW_RISK_PATTERNS:
            if re.search(pattern, text):
                findings.append({"level": "low", "pattern": description, "matched": re.search(pattern, text).group()})

    if findings:
        max_level = max(f["level"] for f in findings)
        risk_map = {"high": "🔴 HIGH", "medium": "🟡 MEDIUM", "low": "🟢 LOW"}
        return {"risk": risk_map.get(max_level, "⚪"), "threats": findings}
    else:
        return {"risk": "✅ 安全", "threats": []}


def scan_url(url: str) -> dict:
    """从 URL 获取内容并扫描"""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            # 只取前5000字符（避免超长内容）
            content = content[:5000]
            result = scan_text(content)
            result["url"] = url
            result["scanned_chars"] = min(len(content), 5000)
            return result
    except URLError as e:
        return {"risk": "error", "error": str(e), "url": url}


def scan_file(file_path: str) -> dict:
    """扫描本地文件"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()[:5000]
            result = scan_text(content)
            result["file"] = file_path
            result["scanned_chars"] = len(content)
            return result
    except Exception as e:
        return {"risk": "error", "error": str(e), "file": file_path}


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  content_scan.py url <URL>")
        print("  content_scan.py text <文本>")
        print("  content_scan.py file <文件路径>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "url":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = scan_url(url)
    elif cmd == "text":
        text = " ".join(sys.argv[2:])
        result = scan_text(text, show_all=True)
    elif cmd == "file":
        file_path = sys.argv[2] if len(sys.argv) > 2 else ""
        result = scan_file(file_path)
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    # 输出结果
    print("=" * 50)
    print(f"安全审查结果: {result['risk']}")
    print("=" * 50)

    if result.get("threats"):
        for t in result["threats"]:
            print(f"[{t['level'].upper()}] {t['pattern']}")
            print(f"  匹配内容: {t['matched'][:80]}")
            print()

    if "url" in result:
        print(f"URL: {result['url']}")
        print(f"扫描字符: {result.get('scanned_chars', 0)}")
    if "file" in result:
        print(f"文件: {result['file']}")

    # 退出码：有问题返回1
    if result["risk"] in ("🔴 HIGH", "🟡 MEDIUM"):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
