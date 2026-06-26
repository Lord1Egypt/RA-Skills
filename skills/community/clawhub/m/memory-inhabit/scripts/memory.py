#!/usr/bin/env python3
"""
Memory-Inhabit Memory — 对话历史与记忆管理

用法：
  python3 memory.py save <persona> <message>      保存一条对话记录
  python3 memory.py save-batch <persona> <file>    从文件批量保存对话
  python3 memory.py search <persona> <query>       搜索相关记忆
  python3 memory.py today <persona>                查看今天的对话历史
  python3 memory.py consolidate <persona>          从历史提炼长期记忆
  python3 memory.py context <persona> [query]      获取注入 prompt 的记忆上下文
"""

import json
import re
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

PERSONAS_DIR = Path(__file__).parent.parent / "personas"
EXTERNAL_PERSONAS_DIR = Path.home() / ".openclaw" / "personas"


def sanitize_path_name(name):
    """防止路径遍历，只允许安全字符"""
    if not name:
        return "unknown"
    # 先按 / 分割，移除 .. 和空段，再拼回（避免 .. 逃过检测）
    parts = name.replace("\\", "/").split("/")
    safe_parts = [p for p in parts if p and p != ".."]
    safe = "/".join(safe_parts)
    # 再限制字符集（禁止 / 出现）
    safe = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9 _\-]", "", safe)
    return safe[:50].strip() if safe else "unknown"


def resolve_persona_dir(persona_name):
    """从两个可能的位置中找到人格包目录"""
    local = PERSONAS_DIR / persona_name
    external = EXTERNAL_PERSONAS_DIR / persona_name
    if local.exists():
        return local
    if external.exists():
        return external
    return local  # 返回 local，触发"不存在"报错


def get_persona_dirs(persona_name):
    """获取 persona 的记忆目录路径"""
    base = resolve_persona_dir(persona_name) / "memories"
    return {
        "base": base,
        "history": base / "history",
        "memory_md": base / "MEMORY.md",
        "raw": base / "raw_memories.json",
    }


def ensure_dirs(persona_name):
    """确保记忆目录存在"""
    dirs = get_persona_dirs(persona_name)
    dirs["history"].mkdir(parents=True, exist_ok=True)
    return dirs


def save_message(persona_name, message, role="user"):
    """保存一条对话记录"""
    dirs = ensure_dirs(persona_name)
    today = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M")
    
    history_file = dirs["history"] / f"{today}.md"
    
    # 追加到当天的历史文件
    with open(history_file, "a", encoding="utf-8") as f:
        if history_file.stat().st_size == 0:
            f.write(f"# 对话记录 — {today}\n\n")
        
        role_label = "👤 用户" if role == "user" else "🧠 人格"
        f.write(f"**[{time_str}] {role_label}**\n{message}\n\n")
    
    print(f"✅ 已保存 [{time_str}] {role}: {message[:50]}...")


def save_batch(persona_name, transcript_file):
    """从 JSON 文件批量保存对话"""
    with open(transcript_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
    
    for msg in messages:
        content = msg.get("content", "")
        role = msg.get("role", "user")
        if content:
            save_message(persona_name, content, role)
    
    print(f"✅ 批量保存 {len(messages)} 条对话")


def search_memories(persona_name, query, top_k=5):
    """关键词搜索 persona 的记忆"""
    dirs = get_persona_dirs(persona_name)
    results = []
    
    query_lower = query.lower()
    query_terms = set(query_lower.split())
    
    # 1. 搜索 raw_memories.json
    if dirs["raw"].exists():
        with open(dirs["raw"], "r", encoding="utf-8") as f:
            raw_memories = json.load(f)
        
        for mem in raw_memories:
            content = mem.get("content", "").lower()
            # 简单的关键词匹配评分
            score = sum(1 for term in query_terms if term in content)
            if score > 0:
                results.append({
                    "source": "raw_memories",
                    "score": score,
                    "content": mem.get("content", ""),
                    "category": mem.get("category", ""),
                })
    
    # 2. 搜索 MEMORY.md
    if dirs["memory_md"].exists():
        with open(dirs["memory_md"], "r", encoding="utf-8") as f:
            memory_content = f.read()
        
        # 按段落分割搜索
        paragraphs = memory_content.split("\n\n")
        for para in paragraphs:
            para_lower = para.lower()
            score = sum(1 for term in query_terms if term in para_lower)
            if score > 0 and para.strip():
                results.append({
                    "source": "MEMORY.md",
                    "score": score,
                    "content": para.strip(),
                })
    
    # 3. 搜索最近 7 天的历史
    for days_ago in range(7):
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        history_file = dirs["history"] / f"{date}.md"
        
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                history = f.read()
            
            # 按消息块分割
            blocks = history.split("**[")
            for block in blocks:
                block_lower = block.lower()
                score = sum(1 for term in query_terms if term in block_lower)
                if score > 0 and len(block.strip()) > 10:
                    # 提取内容（去掉时间戳）
                    lines = block.strip().split("\n")
                    content = "\n".join(lines[1:]).strip() if len(lines) > 1 else block.strip()
                    if content:
                        results.append({
                            "source": f"history/{date}",
                            "score": score,
                            "content": content[:200],
                        })
    
    # 按分数排序，去重
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # 去重（相似内容只保留最高分的）
    seen = set()
    unique_results = []
    for r in results:
        key = r["content"][:50]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    return unique_results[:top_k]


def get_today_history(persona_name):
    """获取今天的对话历史"""
    dirs = get_persona_dirs(persona_name)
    today = datetime.now().strftime("%Y-%m-%d")
    history_file = dirs["history"] / f"{today}.md"
    
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            return f.read()
    return None


def get_recent_history(persona_name, days=3):
    """获取最近 N 天的对话摘要"""
    dirs = get_persona_dirs(persona_name)
    all_history = []
    
    for days_ago in range(days):
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        history_file = dirs["history"] / f"{date}.md"
        
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                all_history.append(f"## {date}\n{content}")
    
    return "\n\n---\n\n".join(all_history) if all_history else None


def consolidate(persona_name):
    """从对话历史提炼长期记忆写入 MEMORY.md"""
    dirs = ensure_dirs(persona_name)
    
    # 获取最近 7 天的历史
    recent = get_recent_history(persona_name, days=7)
    if not recent:
        print("ℹ️ 无对话历史可提炼")
        return
    
    # 读取现有 MEMORY.md
    existing_memory = ""
    if dirs["memory_md"].exists():
        with open(dirs["memory_md"], "r", encoding="utf-8") as f:
            existing_memory = f.read()
    
    # 输出提炼建议（实际提炼由 agent 完成）
    print("📝 提炼建议：")
    print(f"   历史范围：最近 7 天")
    print(f"   现有长期记忆：{len(existing_memory)} 字")
    print(f"   待提炼历史：{len(recent)} 字")
    print()
    print("请将以下内容交给 agent 提炼后写入 MEMORY.md：")
    print("=" * 50)
    print(recent[:2000])
    if len(recent) > 2000:
        print(f"... (共 {len(recent)} 字，仅显示前 2000)")
    print("=" * 50)
    
    return recent


def get_context(persona_name, query=None, top_k=5):
    """获取用于注入 prompt 的记忆上下文"""
    dirs = get_persona_dirs(persona_name)
    context_parts = []
    
    # 1. 始终注入长期记忆（MEMORY.md）
    if dirs["memory_md"].exists():
        with open(dirs["memory_md"], "r", encoding="utf-8") as f:
            memory = f.read().strip()
        if memory:
            context_parts.append(f"## 长期记忆\n{memory[:1000]}")
    
    # 2. 如果有 query，搜索相关记忆
    if query:
        results = search_memories(persona_name, query, top_k=top_k)
        if results:
            mem_lines = []
            for r in results:
                source_tag = f"[{r['source']}]"
                cat_tag = f" ({r['category']})" if r.get('category') else ""
                mem_lines.append(f"- {source_tag}{cat_tag} {r['content'][:150]}")
            context_parts.append(f"## 相关记忆\n" + "\n".join(mem_lines))
    
    # 3. 注入最近 1-2 天的对话摘要
    recent = get_recent_history(persona_name, days=2)
    if recent:
        # 只取最后几条
        lines = recent.strip().split("\n")
        recent_summary = "\n".join(lines[-10:]) if len(lines) > 10 else recent
        context_parts.append(f"## 最近对话\n{recent_summary[:500]}")
    
    return "\n\n".join(context_parts) if context_parts else None


def main():
    if len(sys.argv) < 2:
        print("Memory-Inhabit Memory — 对话历史与记忆管理")
        print()
        print("用法：")
        print("  python3 memory.py save <persona> <message> [role]   保存对话")
        print("  python3 memory.py save-batch <persona> <file>       批量保存")
        print("  python3 memory.py search <persona> <query>          搜索记忆")
        print("  python3 memory.py today <persona>                   今日历史")
        print("  python3 memory.py recent <persona> [days]           最近历史")
        print("  python3 memory.py consolidate <persona>             提炼长期记忆")
        print("  python3 memory.py context <persona> [query]         获取 prompt 上下文")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "save":
        if len(sys.argv) < 4:
            print("用法: python3 memory.py save <persona> <message> [role]")
            sys.exit(1)
        role = sys.argv[4] if len(sys.argv) > 4 else "user"
        save_message(sanitize_path_name(sys.argv[2]), sys.argv[3], role)
    
    elif cmd == "save-batch":
        if len(sys.argv) < 4:
            print("用法: python3 memory.py save-batch <persona> <file>")
            sys.exit(1)
        save_batch(sanitize_path_name(sys.argv[2]), sys.argv[3])
    
    elif cmd == "search":
        if len(sys.argv) < 4:
            print("用法: python3 memory.py search <persona> <query>")
            sys.exit(1)
        results = search_memories(sanitize_path_name(sys.argv[2]), sys.argv[3])
        if results:
            print(f"🔍 找到 {len(results)} 条相关记忆：\n")
            for i, r in enumerate(results, 1):
                print(f"  {i}. [{r['source']}] (score:{r['score']})")
                print(f"     {r['content'][:100]}")
                print()
        else:
            print("🔍 未找到相关记忆")
    
    elif cmd == "today":
        if len(sys.argv) < 3:
            print("用法: python3 memory.py today <persona>")
            sys.exit(1)
        history = get_today_history(sanitize_path_name(sys.argv[2]))
        if history:
            print(history)
        else:
            print("ℹ️ 今天暂无对话记录")
    
    elif cmd == "recent":
        if len(sys.argv) < 3:
            print("用法: python3 memory.py recent <persona> [days]")
            sys.exit(1)
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        history = get_recent_history(sanitize_path_name(sys.argv[2]), days)
        if history:
            print(history)
        else:
            print(f"ℹ️ 最近 {days} 天无对话记录")
    
    elif cmd == "consolidate":
        if len(sys.argv) < 3:
            print("用法: python3 memory.py consolidate <persona>")
            sys.exit(1)
        consolidate(sanitize_path_name(sys.argv[2]))
    
    elif cmd == "context":
        if len(sys.argv) < 3:
            print("用法: python3 memory.py context <persona> [query]")
            sys.exit(1)
        query = sys.argv[3] if len(sys.argv) > 3 else None
        ctx = get_context(sanitize_path_name(sys.argv[2]), query)
        if ctx:
            print(ctx)
        else:
            print("ℹ️ 无可用记忆上下文")
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
