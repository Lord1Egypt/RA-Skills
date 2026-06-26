#!/usr/bin/env python3
"""
Memory Tree 🌳 v2.0 — 简化的记忆管理

核心功能：
1. weekly - 周报生成（本周新记、本周遗忘、永久记忆清单）
2. search - 语义搜索（关键词模式，无外部依赖）
3. mark - 永久标记（📌）

v2.0 变更：
- 删除：decay 命令、枯叶/土壤概念、ollama embedding
- 新增：周报内容重构、推送渠道自动检测
"""

import json
import os
import hashlib
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ==================== 路径配置 ====================
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_MD = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"
DATA_DIR = WORKSPACE / "memory-tree" / "data"
CONFIDENCE_DB = DATA_DIR / "confidence.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
WEEKLY_REPORTS_DIR = MEMORY_DIR / "weekly-reports"

# ==================== 数据工具 ====================

def load_json(path, default=None):
    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default or {}
    return default or {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def text_hash(text):
    return hashlib.md5(text.strip().encode()).hexdigest()[:12]


def estimate_tokens(text):
    """粗略估算 token 数（字符/4）"""
    return len(text) // 4


def fmt_tokens(num):
    """格式化 token 数量"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.0f}K"
    else:
        return str(num)


def fmt_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f}KB"
    else:
        return f"{size_bytes/1024/1024:.1f}MB"


# ==================== Memory 解析 ====================

def parse_memory_blocks(content):
    """解析 MEMORY.md 中的知识块"""
    blocks = []
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    for section in sections:
        section = section.strip()
        if not section:
            continue
        title_match = re.match(r'^##\s+(.+)', section)
        title = title_match.group(1).strip() if title_match else "无标题"
        
        # 检测永久标记
        is_permanent = "📌" in title or "[P0]" in title
        
        # 检测优先级
        priority = "P2"
        if "[P0]" in title or "📌" in title:
            priority = "P0"
        elif "[P1]" in title:
            priority = "P1"
        
        lines = section.split('\n')
        body = '\n'.join(lines[1:]).strip()
        
        blocks.append({
            "title": title,
            "body": body,
            "priority": priority,
            "is_permanent": is_permanent,
            "hash": text_hash(title + body),
            "full_text": title + "\n" + body
        })
    return blocks


def get_permanent_memories():
    """提取 MEMORY.md 中的永久记忆"""
    if not MEMORY_MD.exists():
        return []
    
    content = MEMORY_MD.read_text(encoding='utf-8')
    blocks = parse_memory_blocks(content)
    
    permanent = []
    for block in blocks:
        if block["is_permanent"] or block["priority"] == "P0":
            # 提取摘要（第一行或前100字符）
            lines = block["body"].split('\n')
            summary = ""
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    summary = line[:100]
                    break
            if not summary:
                summary = block["title"][:100]
            
            permanent.append({
                "title": block["title"].replace("📌", "").replace("[P0]", "").strip(),
                "summary": summary,
                "priority": block["priority"]
            })
    
    return permanent


# ==================== 周报生成 (v2.0 核心功能) ====================

def scan_weekly_new_memories():
    """扫描本周新增的 memory 文件"""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())  # 本周一
    week_end = week_start + timedelta(days=6)  # 本周日
    
    new_memories = []
    
    for f in MEMORY_DIR.glob("*.md"):
        if f.name == "README.md":
            continue
        
        # 检查文件修改时间
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if week_start <= mtime <= week_end + timedelta(days=1):
            try:
                content = f.read_text(encoding='utf-8')
                # 提取标题和摘要
                lines = content.split('\n')
                title = ""
                summary = ""
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('# ') and not title:
                        title = line[2:].strip()
                    elif line and not line.startswith('#') and not summary:
                        summary = line[:80]
                
                if not title:
                    title = f.stem
                
                # 检测是否永久记忆
                is_permanent = "📌" in content or "[P0]" in content or "记住这个" in content
                
                new_memories.append({
                    "title": title,
                    "summary": summary,
                    "file": f.name,
                    "date": mtime.strftime('%Y-%m-%d'),
                    "is_permanent": is_permanent
                })
            except Exception:
                pass
    
    # 按日期排序
    new_memories.sort(key=lambda x: x["date"], reverse=True)
    return new_memories


def detect_forgotten_memories():
    """检测本周遗忘的内容（对比 MEMORY.md 和历史记录）"""
    forgotten = []
    
    # 读取当前 MEMORY.md
    if not MEMORY_MD.exists():
        return forgotten
    
    current_content = MEMORY_MD.read_text(encoding='utf-8')
    current_blocks = parse_memory_blocks(current_content)
    current_titles = {b["title"] for b in current_blocks}
    
    # 检查 archive 目录
    archive_dir = MEMORY_DIR / "archive"
    if archive_dir.exists():
        for f in archive_dir.glob("MEMORY-*.md"):
            try:
                content = f.read_text(encoding='utf-8')
                blocks = parse_memory_blocks(content)
                for block in blocks:
                    if block["title"] not in current_titles:
                        # 提取摘要
                        lines = block["body"].split('\n')
                        summary = ""
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                summary = line[:60]
                                break
                        
                        forgotten.append({
                            "title": block["title"],
                            "summary": summary,
                            "reason": "被新内容替代或归档"
                        })
            except Exception:
                pass
    
    return forgotten[:10]  # 最多显示10条


def detect_enabled_channels():
    """从 openclaw.json 检测已启用的推送渠道"""
    config = load_json(OPENCLAW_CONFIG)
    channels = config.get('channels', {})
    
    enabled = []
    for name, cfg in channels.items():
        if cfg.get('enabled', False):
            enabled.append({
                'name': name,
                'config': cfg,
            })
    
    return enabled


def get_feishu_chat_id(config):
    """从飞书配置获取默认 chatId"""
    group_allow = config.get('groupAllowFrom', [])
    if group_allow:
        return group_allow[0]
    return None


def cmd_weekly():
    """生成周报"""
    print(f"🌳 记忆树 — 周报生成 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    
    # 确保输出目录存在
    WEEKLY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 计算周数
    today = datetime.now()
    week_number = today.isocalendar()[1]
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    report_date = today.strftime('%Y-%m-%d')
    report_file = WEEKLY_REPORTS_DIR / f"memory-tree-{report_date}-W{week_number}.md"
    
    # 收集数据
    print("📊 收集记忆数据...")
    
    # 1. 本周新记
    new_memories = scan_weekly_new_memories()
    permanent_new = [m for m in new_memories if m["is_permanent"]]
    normal_new = [m for m in new_memories if not m["is_permanent"]]
    
    # 2. 本周遗忘
    forgotten = detect_forgotten_memories()
    
    # 3. 永久记忆清单
    permanent_memories = get_permanent_memories()
    
    # 4. MEMORY.md 统计
    memory_size = MEMORY_MD.stat().st_size if MEMORY_MD.exists() else 0
    memory_tokens = estimate_tokens(MEMORY_MD.read_text(encoding='utf-8')) if MEMORY_MD.exists() else 0
    
    # 生成报告
    report_lines = [
        f"# 🌳 记忆树周报 | {today.year}-W{week_number}",
        f"",
        f"> 生成时间：{report_date} {today.strftime('%H:%M')}",
        f"> 统计周期：{week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}",
        f"",
        f"---",
        f"",
    ]
    
    # 本周新记
    report_lines.append("## 📝 本周新记")
    report_lines.append("")
    
    if permanent_new:
        report_lines.append("📌 **永久记忆**：")
        report_lines.append("")
        for m in permanent_new[:10]:
            report_lines.append(f"  • {m['title']} ({m['date']})")
            if m['summary']:
                report_lines.append(f"    _{m['summary']}_")
        report_lines.append("")
    
    if normal_new:
        report_lines.append("🍃 **普通记忆**：")
        report_lines.append("")
        for m in normal_new[:15]:
            report_lines.append(f"  • {m['title']} ({m['date']})")
        report_lines.append("")
    
    if not new_memories:
        report_lines.append("_本周无新增记忆_")
        report_lines.append("")
    
    # 本周遗忘
    report_lines.append("## 🗑️ 本周遗忘")
    report_lines.append("")
    
    if forgotten:
        for f in forgotten:
            report_lines.append(f"  • {f['title']}")
            report_lines.append(f"    _{f['reason']}_")
        report_lines.append("")
    else:
        report_lines.append("_本周无遗忘内容_")
        report_lines.append("")
    
    # 永久记忆清单
    report_lines.append("## 📌 永久记忆清单")
    report_lines.append("")
    
    if permanent_memories:
        for i, p in enumerate(permanent_memories, 1):
            report_lines.append(f"  {i}. {p['title']}")
            if p['summary']:
                report_lines.append(f"     _{p['summary'][:60]}_")
        report_lines.append("")
    else:
        report_lines.append("_暂无永久记忆_")
        report_lines.append("")
    
    # 记忆健康
    report_lines.append("## 💡 记忆健康")
    report_lines.append("")
    report_lines.append(f"| 指标 | 数值 |")
    report_lines.append(f"|------|------|")
    report_lines.append(f"| MEMORY.md 大小 | {fmt_size(memory_size)} (~{fmt_tokens(memory_tokens)} tokens) |")
    report_lines.append(f"| 永久记忆 | {len(permanent_memories)} 条 |")
    report_lines.append(f"| 本周新增 | {len(new_memories)} 条 |")
    report_lines.append(f"| 本周遗忘 | {len(forgotten)} 条 |")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append(f"*由记忆树自动生成*")
    
    report_content = "\n".join(report_lines)
    
    # 写入本地文件
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 周报已保存: {report_file}\n")
    
    # 检测推送渠道
    channels = detect_enabled_channels()
    
    if channels:
        print(f"📡 检测到已启用渠道: {', '.join(c['name'] for c in channels)}")
        
        for ch in channels:
            if ch['name'] == 'feishu':
                chat_id = get_feishu_chat_id(ch['config'])
                if chat_id:
                    print(f"\n📱 飞书推送配置:")
                    print(f"   chat_id: {chat_id}")
                    print(f"\n💡 推送命令:")
                    print(f"   message send --target {chat_id} --file {report_file}")
    else:
        print("📭 未检测到已启用的外部推送渠道")
        print("   周报已保存到本地")
    
    # 输出到终端
    print(f"\n{'='*60}")
    print(report_content)
    
    return report_file


# ==================== 搜索功能（关键词模式）====================

def keyword_similarity(query, text):
    """关键词相似度计算"""
    import string
    
    # 中文按字切分 + 英文按词切分
    query_words = set()
    for char in query:
        if '\u4e00' <= char <= '\u9fff':
            query_words.add(char)
    
    for word in re.findall(r'[a-zA-Z]{2,}', query.lower()):
        query_words.add(word)
    
    text_words = set()
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            text_words.add(char)
    
    for word in re.findall(r'[a-zA-Z]{2,}', text.lower()):
        text_words.add(word)
    
    if not query_words or not text_words:
        return 0
    
    common = query_words & text_words
    return len(common) / len(query_words)


def cmd_search(query):
    """关键词搜索"""
    if not MEMORY_MD.exists():
        print("❌ MEMORY.md 不存在")
        return
    
    content = MEMORY_MD.read_text(encoding='utf-8')
    blocks = parse_memory_blocks(content)
    
    results = []
    for block in blocks:
        sim = keyword_similarity(query, block["full_text"])
        if sim > 0.1:
            results.append({
                "similarity": round(sim, 2),
                "title": block["title"],
                "body": block["body"][:200],
                "is_permanent": block["is_permanent"],
                "priority": block["priority"]
            })
    
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    if not results:
        print("🔍 未找到相关记忆")
        return
    
    print(f"🔍 找到 {len(results)} 条相关记忆:\n")
    for r in results[:10]:
        marker = "📌" if r["is_permanent"] else "  "
        print(f"  {marker} 相似:{r['similarity']:.0%} | {r['title']}")
        preview = r['body'][:100].replace('\n', ' ')
        if preview:
            print(f"     {preview}...")
        print()


# ==================== 永久标记 ====================

def cmd_mark(title_keyword):
    """标记为永久记忆"""
    if not MEMORY_MD.exists():
        print("❌ MEMORY.md 不存在")
        return
    
    content = MEMORY_MD.read_text(encoding='utf-8')
    blocks = parse_memory_blocks(content)
    
    # 查找匹配的知识块
    found = None
    for block in blocks:
        if title_keyword.lower() in block["title"].lower():
            found = block
            break
    
    if not found:
        print(f"❌ 未找到匹配的知识块: {title_keyword}")
        return
    
    if found["is_permanent"]:
        print(f"✅ 已经是永久记忆: {found['title']}")
        return
    
    # 在标题中添加 📌 标记
    old_title = found["title"]
    new_title = old_title + " 📌"
    
    # 替换内容
    new_content = content.replace(
        f"## {old_title}",
        f"## {new_title}"
    )
    
    if new_content != content:
        MEMORY_MD.write_text(new_content, encoding='utf-8')
        print(f"✅ 已标记为永久记忆: {new_title}")
        print(f"   该记忆永不衰减，永不参与清理")
    else:
        print(f"❌ 标记失败，请手动编辑 MEMORY.md")


# ==================== 可视化 ====================

def cmd_visualize():
    """显示 MEMORY.md 概览"""
    if not MEMORY_MD.exists():
        print("❌ MEMORY.md 不存在")
        return
    
    content = MEMORY_MD.read_text(encoding='utf-8')
    blocks = parse_memory_blocks(content)
    
    permanent = [b for b in blocks if b["is_permanent"]]
    normal = [b for b in blocks if not b["is_permanent"]]
    
    memory_size = MEMORY_MD.stat().st_size
    memory_tokens = estimate_tokens(content)
    
    print(f"🌳 记忆树概览 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    print(f"├── 📊 MEMORY.md: {fmt_size(memory_size)} (~{fmt_tokens(memory_tokens)} tokens)")
    print(f"├── 📌 永久记忆: {len(permanent)} 条")
    print(f"├── 🍃 普通记忆: {len(normal)} 条")
    print(f"└── 📝 总计: {len(blocks)} 条知识块\n")
    
    if permanent:
        print("📌 永久记忆清单:")
        for b in permanent[:10]:
            title = b["title"].replace("📌", "").replace("[P0]", "").strip()
            print(f"   • {title}")
        if len(permanent) > 10:
            print(f"   ... 还有 {len(permanent) - 10} 条")
        print()
    
    print("💡 使用 `search \"关键词\"` 搜索记忆")
    print("💡 使用 `mark \"标题关键词\"` 标记为永久记忆")


# ==================== CLI ====================

def main():
    if len(sys.argv) < 2:
        print("🌳 Memory Tree v2.0 — 简化的记忆管理")
        print()
        print("用法:")
        print("  weekly              生成周报（本周新记、遗忘、永久清单）")
        print("  search \"查询\"       搜索记忆")
        print("  mark \"标题关键词\"   标记为永久记忆")
        print("  visualize           查看记忆概览")
        print()
        print("v2.0 变更:")
        print("  - 删除 decay 命令（衰减无效）")
        print("  - 删除枯叶/土壤概念")
        print("  - 删除 ollama embedding（失败率高）")
        print("  - 新增周报内容重构")
        print("  - 新增推送渠道自动检测")
        return

    cmd = sys.argv[1]
    if cmd == "weekly":
        cmd_weekly()
    elif cmd == "search":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not query:
            print("❌ 请提供搜索内容")
            return
        cmd_search(query)
    elif cmd == "mark":
        if len(sys.argv) < 3:
            print("❌ 请提供标题关键词")
            return
        cmd_mark(sys.argv[2])
    elif cmd == "visualize":
        cmd_visualize()
    else:
        print(f"❌ 未知命令: {cmd}")
        print()
        print("可用命令: weekly, search, mark, visualize")


if __name__ == "__main__":
    main()