#!/usr/bin/env python3
"""
结构化记忆管理系统
参考 Claude Code 的 memdir 系统设计

用法:
  python3 memory_manager.py scan          # 扫描所有记忆文件
  python3 memory_manager.py read <name>   # 读取特定记忆
  python3 memory_manager.py write <type> <name> <content>  # 写入记忆
  python3 memory_manager.py relevant <query>  # relevance-based 检索
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

MEMORY_ROOT = Path.home() / ".openclaw" / "bw-openclaw-boost" / "memory"
MEMORY_TYPES = ["user", "feedback", "project", "reference", "log"]


def get_mtime(path: Path) -> datetime:
    """获取文件修改时间"""
    return datetime.fromtimestamp(path.stat().st_mtime)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """解析 YAML frontmatter"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2)
        fm = {}
        for line in fm_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                fm[key.strip()] = val.strip()
        return fm, body
    return {}, content


def scan_memory_files() -> list[dict]:
    """扫描所有记忆文件，返回 manifest"""
    results = []
    
    for root, dirs, files in os.walk(MEMORY_ROOT):
        # 跳过 .git 和临时目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for f in files:
            if not f.endswith('.md'):
                continue
            if f == 'MEMORY.md':
                continue
                
            path = Path(root) / f
            try:
                content = path.read_text(encoding='utf-8')
                fm, body = parse_frontmatter(content)
                
                # 提取前30行作为描述（如果没有 frontmatter description）
                desc = fm.get('description', '')
                if not desc:
                    first_lines = '\n'.join(body.split('\n')[:3])
                    desc = first_lines[:100] + '...' if len(first_lines) > 100 else first_lines
                
                results.append({
                    'name': fm.get('name', f.replace('.md', '')),
                    'description': desc,
                    'type': fm.get('type', 'unknown'),
                    'mtime': fm.get('mtime', get_mtime(path).isoformat()),
                    'path': str(path.relative_to(MEMORY_ROOT)),
                    'file_mtime': get_mtime(path).isoformat(),
                })
            except Exception as e:
                print(f"Error reading {path}: {e}", file=sys.stderr)
    
    # 按 mtime 排序（最新的在前）
    results.sort(key=lambda x: x.get('mtime', ''), reverse=True)
    return results


def format_manifest(memories: list[dict]) -> str:
    """格式化 manifest 用于 relevance selection"""
    lines = []
    for m in memories:
        age = get_memory_age(m.get('mtime', ''))
        type_tag = f"[{m.get('type', 'unknown')}]"
        lines.append(f"- {type_tag} {m['name']} ({age}): {m['description'][:80]}")
    return '\n'.join(lines)


def get_memory_age(mtime_str: str) -> str:
    """获取记忆的新鲜度"""
    if not mtime_str:
        return 'unknown'
    try:
        mtime = datetime.fromisoformat(mtime_str.replace('Z', '+00:00'))
        now = datetime.now()
        delta = now - mtime
        
        if delta.days == 0:
            return 'today'
        elif delta.days == 1:
            return 'yesterday'
        elif delta.days < 7:
            return f'{delta.days} days ago'
        else:
            return f'{delta.days} days ago'
    except:
        return 'unknown'


def get_freshness_warning(mtime_str: str) -> str:
    """获取新鲜度警告（超过1天的记忆）"""
    if not mtime_str:
        return ''
    try:
        mtime = datetime.fromisoformat(mtime_str.replace('Z', '+00:00'))
        now = datetime.now()
        delta = now - mtime
        
        if delta.days > 1:
            return f"[WARNING: 此记忆为 {delta.days} 天前的旧信息，可能已过时]"
        return ''
    except:
        return ''


def read_memory(name: str) -> Optional[dict]:
    """根据名称查找记忆"""
    memories = scan_memory_files()
    for m in memories:
        if name.lower() in m['name'].lower() or name.lower() in str(m['path']).lower():
            path = MEMORY_ROOT / m['path']
            content = path.read_text(encoding='utf-8')
            fm, body = parse_frontmatter(content)
            warning = get_freshness_warning(fm.get('mtime'))
            return {
                **m,
                'frontmatter': fm,
                'body': body,
                'warning': warning,
                'full_content': content,
            }
    return None


def write_memory(mtype: str, name: str, body: str, description: str = '') -> Path:
    """写入新记忆"""
    if mtype not in MEMORY_TYPES:
        raise ValueError(f"type 必须是: {MEMORY_TYPES}")
    
    # 确定目录
    if mtype == 'log':
        today = datetime.now().strftime('%Y/%m')
        dir_path = MEMORY_ROOT / 'logs' / today
    else:
        dir_path = MEMORY_ROOT / mtype
    
    dir_path.mkdir(parents=True, exist_ok=True)
    
    # 文件名
    safe_name = re.sub(r'[^\w\-]', '_', name)[:50]
    file_path = dir_path / f"{safe_name}.md"
    
    # 如果已存在，追加
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
    if file_path.exists():
        content = file_path.read_text(encoding='utf-8')
        content += f"\n\n---\n\n## 更新 {timestamp}\n\n{body}"
    else:
        content = f"""---
name: {name}
description: {description or name}
type: {mtype}
mtime: {timestamp}
---

{body}
"""
    
    file_path.write_text(content, encoding='utf-8')
    return file_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'scan':
        memories = scan_memory_files()
        print(f"找到 {len(memories)} 个记忆文件:\n")
        print(format_manifest(memories))
        
    elif cmd == 'read' and len(sys.argv) >= 3:
        name = sys.argv[2]
        result = read_memory(name)
        if result:
            print(f"# {result['name']}\n")
            if result['warning']:
                print(f"{result['warning']}\n")
            print(result['body'])
        else:
            print(f"未找到: {name}", file=sys.stderr)
            sys.exit(1)
    
    elif cmd == 'write' and len(sys.argv) >= 5:
        mtype, name, body = sys.argv[2], sys.argv[3], ' '.join(sys.argv[4:])
        path = write_memory(mtype, name, body)
        print(f"已写入: {path}")
    
    elif cmd == 'relevant' and len(sys.argv) >= 3:
        query = ' '.join(sys.argv[2:])
        memories = scan_memory_files()
        manifest = format_manifest(memories)
        print(f"查询: {query}\n")
        print("可用记忆 (可复制到上下文):\n")
        print(manifest)
    
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
