#!/usr/bin/env python3
"""
L2 Distill Script - 从 short-term memory 自动提炼 L2 事件
遍历最近 N 个 short-term 摘要，用规则判断是否需要提炼到 L2，
如果满足条件则调用 memory.py event 记录。
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

MEMORY_DIR = Path(__file__).parent.parent / "memory"
SHORT_TERM_DIR = MEMORY_DIR / "short-term"
EVENTS_DIR = MEMORY_DIR / "user" / "events"

# L2 提炼关键词（满足任一即提炼）
DISTILL_KEYWORDS = [
    "新发现", "新洞察", "重要信息",
    "重要决策", "关键选择", "架构变更", "架构",
    "踩坑", "教训", "错误", "bug",
    "偏好变化", "技术突破", "大模型",
    "Hook", "bootstrap", "记忆系统",
    "提炼", "修复", "升级", "重大",
    "TypeScript", "文档更新", "文档升级",
    "session", "conversations", "记忆加载",
    "飞书", "Bot", "插件", "多账号",
    "复盘", "晚间复盘", "日总结",
]


def get_recent_short_terms(hours=12):
    """获取最近N小时的 short-term 摘要"""
    if not SHORT_TERM_DIR.exists():
        return []
    
    cutoff = datetime.now() - timedelta(hours=hours)
    files = []
    
    for f in SHORT_TERM_DIR.glob("*.md"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime > cutoff:
            files.append((mtime, f))
    
    files.sort(key=lambda x: x[0], reverse=True)
    return [f for _, f in files]


def has_substantive_dialogue(content: str) -> bool:
    """检查是否有实质对话内容"""
    # 有"参与者"或多个"话题"段落说明有实质对话
    dialogue_markers = content.count("参与者") + content.count("话题")
    return dialogue_markers >= 2 or ("参与者" in content and "关键结论" in content)


def extract_dialogue_content(content: str) -> str:
    """提取对话的核心内容"""
    lines = content.split("\n")
    result = []
    capture = False
    
    for line in lines:
        if "实质性对话摘要" in line:
            capture = True
            continue
        elif capture and line.startswith("## "):
            break
        elif capture:
            stripped = line.strip()
            if not stripped:
                continue
            clean = stripped.strip("* ").strip()
            if clean:
                result.append(clean)
    
    return "\n".join(result[:20])


def should_distill(file_path: Path, content: str) -> tuple[bool, str]:
    """
    判断内容是否值得提炼到 L2
    """
    # 如果没有实质对话，直接跳过
    if not has_substantive_dialogue(content):
        return False, ""
    
    # 检查关键词匹配
    matched = []
    for kw in DISTILL_KEYWORDS:
        if kw in content:
            matched.append(kw)
    
    if matched:
        reason = f"匹配关键词: {', '.join(matched)}"
        return True, reason
    
    # 检查是否有明确的结论性内容
    if "关键结论" in content or "重要结论" in content:
        if len(content) > 800:
            return True, "有实质对话 + 关键结论"
    
    return False, ""


def event_exists_today(topic_hint: str = "") -> bool:
    """检查今天是否已有相关主题的事件"""
    if not EVENTS_DIR.exists():
        return False
    
    today = datetime.now().strftime("%Y-%m-%d")
    for f in EVENTS_DIR.glob(f"{today}*.md"):
        if not topic_hint:
            return True
        if topic_hint.lower() in f.read_text(encoding="utf-8").lower():
            return True
    return False


def record_event(title: str, description: str) -> bool:
    """调用 memory.py event 记录事件"""
    cmd = [
        sys.executable,
        str(MEMORY_DIR / "memory.py"),
        "event",
        title,
        description
    ]
    
    env = dict(os.environ)
    env["MEMORY_DIR"] = str(MEMORY_DIR)
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(MEMORY_DIR.parent),
        env=env
    )
    
    if result.returncode == 0:
        print(f"  ✅ 已记录: {title}")
        return True
    else:
        print(f"  ❌ 失败: {result.stderr[:200]}")
        return False


def distill_one(file_path: Path) -> bool:
    """处理单个 short-term 文件"""
    content = file_path.read_text(encoding="utf-8")
    
    should, reason = should_distill(file_path, content)
    
    if not should:
        return False
    
    print(f"  ✅ 提炼条件: {reason}")
    
    # 提取对话内容
    dialogue = extract_dialogue_content(content)
    
    # 生成事件标题
    today = datetime.now().strftime("%Y-%m-%d")
    topic = "重要对话"
    
    for kw in DISTILL_KEYWORDS:
        if kw in content and len(kw) > 2:
            topic = kw
            break
    
    title = f"{today}-{topic}"
    
    # 防止重复
    if event_exists_today(topic):
        print(f"  ⏭️  今天已有同类事件，跳过")
        return False
    
    # 构造描述
    description = f"""来源: {file_path.name}

{dialogue}

提炼原因: {reason}
"""
    
    return record_event(title, description)


def main():
    print("=" * 50)
    print(f"🧠 L2 Distill 检查 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    recent_files = get_recent_short_terms(hours=12)
    
    if not recent_files:
        print("\n📭 最近12小时无 short-term 摘要")
        return
    
    print(f"\n📋 检查 {len(recent_files)} 个 recent short-term 文件...")
    
    distilled_count = 0
    for f in recent_files:
        print(f"\n处理: {f.name}")
        result = distill_one(f)
        if result:
            distilled_count += 1
    
    print(f"\n{'='*50}")
    if distilled_count > 0:
        print(f"✅ L2 提炼完成: 新增 {distilled_count} 个事件")
    else:
        print(f"⏭️  无需提炼（最近对话无 L2 价值内容）")


if __name__ == "__main__":
    main()
