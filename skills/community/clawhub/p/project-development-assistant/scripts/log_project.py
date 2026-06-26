#!/usr/bin/env python3
"""
项目日志工具 - 跨平台 Python 版本

设计原则：静默写入文件，聊天只回简洁摘要，避免刷屏。

用法:
    python log_project.py -a init -p <项目路径> -n <项目名称>     # 初始化
    python log_project.py -a log -p <项目路径> -m <消息> -c INFO   # 记录（静默）
    python log_project.py -a log -p <项目路径> -m <消息> -c INFO --show  # 记录+显示摘要
    python log_project.py -a read -p <项目路径>                    # 读日志（简洁）
    python log_project.py -a progress -p <项目路径>                # 进度摘要（简洁）
    python log_project.py -a structure -p <项目路径>              # 项目结构
    python log_project.py -a list -p <项目路径>                    # 日志列表
    python log_project.py -a state -p <项目路径>                    # 读取状态文件
    python log_project.py -a state -p <项目路径> -s 进行中 -t "开发某功能"  # 更新状态
"""

import os
import sys
import re
import argparse
import json
from datetime import datetime
import glob

# ─────────────────────────────────────────────
# 路径工具
# ─────────────────────────────────────────────

def get_log_file(project_path, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    log_dir = os.path.join(project_path, 'logs')
    return os.path.join(log_dir, f'devlog_{date}.md'), log_dir

def get_index_file(log_dir):
    return os.path.join(log_dir, 'index.md')

def get_state_file(project_path):
    return os.path.join(project_path, '.project_state.json')

def get_progress_file(project_path):
    candidates = [
        os.path.join(project_path, 'PROJECT_INFO.md'),
        os.path.join(project_path, 'project_info.md'),
        os.path.join(project_path, 'README.md'),
    ]
    for f in candidates:
        if os.path.exists(f):
            return f
    return None

# ─────────────────────────────────────────────
# 状态文件读写（结构化状态，避免读散乱日志）
# ─────────────────────────────────────────────

DEFAULT_STATE = {
    "project": "",
    "status": "待开始",   # 待开始 / 进行中 / 已完成 / 已阻塞
    "current_task": "",
    "last_updated": "",
    "summary": "",        # 一句话当前状态描述
    "open_issues": [],    # 未解决的问题列表
    "next_steps": [],     # 下一步计划
    "milestones": []      # 已完成里程碑
}

def read_state(project_path):
    state_file = get_state_file(project_path)
    if os.path.exists(state_file):
        with open(state_file, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    return None

def write_state(project_path, state):
    state_file = get_state_file(project_path)
    state['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def init_state(project_path, project_name):
    state = DEFAULT_STATE.copy()
    state['project'] = project_name
    state['status'] = '待开始'
    state['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_state(project_path, state)
    return state

# ─────────────────────────────────────────────
# 日志操作
# ─────────────────────────────────────────────

def init_log(project_path):
    log_file, log_dir = get_log_file(project_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.exists(log_file):
        return log_file
    header = f"""# Development Log
Project: {project_path}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

"""
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(header)
    return log_file

def write_log(project_path, message, category="INFO", show=False):
    """写入日志条目。默认静默，只写文件。show=True时才输出。"""
    log_file, log_dir = get_log_file(project_path)
    if not os.path.exists(log_file):
        init_log(project_path)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"## [{timestamp}] [{category}] {message}\n"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(entry)

    # 更新索引（始终静默）
    index_file = get_index_file(log_dir)
    index_entry = f"| {timestamp} | {category} | {message} |\n"
    if not os.path.exists(index_file):
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("| Time | Category | Content |\n|------|----------|--------|\n")
    with open(index_file, 'a', encoding='utf-8') as f:
        f.write(index_entry)

    if show:
        emoji = {"INFO":"[i]","ERROR":"[X]","FIXED":"[#]","PROGRESS":"[>]","WARNING":"[!]","SUCCESS":"[OK]"}.get(category,"[-]")
        print(f"{emoji} [{category}] {message}")

def read_log(project_path, date=None, lines=30):
    """读取日志，默认只显示最近 N 行，避免刷屏"""
    log_file, _ = get_log_file(project_path, date)
    if not os.path.exists(log_file):
        print("[?] 暂无日志")
        return
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')
    # 去掉前4行 header（#标题 + Project + Created + ---）
    body = content[4:] if len(content) > 4 else content
    # 去掉开头的空行和 --- 分隔符
    while body and (not body[0].strip() or body[0].strip() == '---'):
        body.pop(0)
    # 只显示最后 lines 条
    tail = body[-lines:] if len(body) > lines else body
    for line in tail:
        print(line)

def read_latest_log(project_path, lines=20):
    """读取最新日志，只显示最近 lines 行"""
    log_dir = os.path.join(project_path, 'logs')
    if not os.path.exists(log_dir):
        print("[?] 暂无日志")
        return
    pattern = os.path.join(log_dir, 'devlog_*.md')
    files = glob.glob(pattern)
    if not files:
        print("[?] 暂无日志")
        return
    latest = max(files, key=os.path.getmtime)
    with open(latest, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')
    # 去掉前4行 header
    body = content[4:] if len(content) > 4 else content
    while body and (not body[0].strip() or body[0].strip() == '---'):
        body.pop(0)
    tail = body[-lines:] if len(body) > lines else body
    print(f"[=] {os.path.basename(latest)}")
    for line in tail:
        print(line)

def show_progress(project_path):
    """显示项目进度摘要：状态文件 + 最近日志"""
    state = read_state(project_path)
    if state:
        status_icon = {"待开始":"[?]","进行中":"[>]","已完成":"[OK]","已阻塞":"[X]"}.get(state['status'],"[-]")
        print(f"[=] {state['project']} | {status_icon} {state['status']}")
        if state['current_task']:
            print(f"   当前：{state['current_task']}")
        if state['open_issues']:
            print(f"   问题：{', '.join(state['open_issues'])}")
        if state['next_steps']:
            print(f"   下步：{' | '.join(state['next_steps'][:2])}")
    else:
        print("[=] 暂无状态文件")

    latest = get_latest_log(project_path)
    if latest:
        with open(latest, 'r', encoding='utf-8') as f:
            content = f.read().strip().split('\n')
        body = content[4:] if len(content) > 4 else content
        while body and (not body[0].strip() or body[0].strip() == '---'):
            body.pop(0)
        tail = body[-8:] if len(body) > 8 else body
        if tail:
            print("\n[*] 最近记录：")
            for line in tail:
                print(f"   {line}")

def show_structure(project_path, max_depth=2):
    """显示项目结构，限制深度避免过长输出"""
    print(f"[>] {project_path}")
    for root, dirs, files in os.walk(project_path):
        level = root.replace(project_path, '').count(os.sep)
        if level >= max_depth:
            dirs.clear()
            continue
        indent = '  ' * level
        folder_name = os.path.basename(root)
        if folder_name.startswith('.') or folder_name in ['node_modules', '__pycache__', 'venv', '.git']:
            dirs.clear()
            continue
        print(f"{indent}[D] {folder_name}/")
        sub_indent = '  ' * (level + 1)
        for file in files[:10]:  # 每个目录最多显示10个文件
            if not file.startswith('.'):
                print(f"{sub_indent}[F] {file}")
        if len(files) > 10:
            print(f"{sub_indent}   ... 还有 {len(files)-10} 个文件")

def list_logs(project_path):
    """列出所有日志文件"""
    log_dir = os.path.join(project_path, 'logs')
    if not os.path.exists(log_dir):
        print("[?] 暂无日志")
        return
    pattern = os.path.join(log_dir, 'devlog_*.md')
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    if not files:
        print("[?] 暂无日志")
        return
    print(f"[=] 共 {len(files)} 个日志文件：")
    for f in files[:10]:
        mtime = datetime.fromtimestamp(os.path.getmtime(f))
        print(f"   {os.path.basename(f)} ({mtime.strftime('%Y-%m-%d')})")
    if len(files) > 10:
        print(f"   ... 还有 {len(files)-10} 个")

def create_project_structure(project_path, project_name):
    """创建标准项目结构"""
    folders = ['logs', 'sessions', 'configs', 'firmware', 'docs', 'hardware', 'references', 'tools']
    for folder in folders:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)

    info_file = os.path.join(project_path, 'PROJECT_INFO.md')
    if not os.path.exists(info_file):
        info_content = f"""# {project_name}

## 项目信息
- 项目名称：{project_name}
- 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 项目路径：{project_path}

## 项目概述
<!-- 简要描述项目 -->

## 技术栈
<!-- 列出主要技术、框架、芯片等 -->

## 开发进度
- [ ] 待开始
- [ ] 进行中
- [ ] 已完成

## 当前问题
<!-- 记录待解决的问题 -->

## 下一步计划
1.

## 版本历史
| 日期 | 版本 | 变化 |
|------|------|------|
| | | |
"""
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(info_content)

    init_log(project_path)
    init_state(project_path, project_name)

def get_latest_log(project_path):
    log_dir = os.path.join(project_path, 'logs')
    if not os.path.exists(log_dir):
        return None
    pattern = os.path.join(log_dir, 'devlog_*.md')
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='项目日志工具（防刷屏设计）')
    parser.add_argument('--action', '-a',
                        choices=['init', 'log', 'read', 'progress', 'structure', 'list', 'new', 'state'],
                        default='log',
                        help='动作')
    parser.add_argument('--path', '-p', required=True, help='项目路径')
    parser.add_argument('--msg', '-m', help='日志内容')
    parser.add_argument('--cat', '-c',
                        choices=['INFO', 'ERROR', 'FIXED', 'PROGRESS', 'STANDARD', 'WARNING', 'SUCCESS'],
                        default='INFO', help='日志类别')
    parser.add_argument('--name', '-n', help='项目名称（新建时）')
    parser.add_argument('--date', '-d', help='日期（读取时，YYYY-MM-DD）')
    parser.add_argument('--show', action='store_true', help='写入日志后显示摘要（默认静默）')
    parser.add_argument('--status', '-s', help='项目状态（更新状态时）')
    parser.add_argument('--task', '-t', help='当前任务（更新状态时）')
    parser.add_argument('--summary', help='一句话状态描述（更新状态时）')
    parser.add_argument('--issue', '-i', action='append', help='添加问题（可多次）')
    parser.add_argument('--step', action='append', help='添加下一步（可多次）')

    args = parser.parse_args()

    if args.action not in ('new') and not os.path.exists(args.path):
        print(f"[X] 路径不存在：{args.path}")
        print("   提示：使用 new action 创建新项目")
        sys.exit(1)

    if args.action == 'init':
        init_log(args.path)
        print(f"[OK] 日志初始化完成")

    elif args.action == 'log':
        if not args.msg:
            print("[X] log action 需要 --msg")
            sys.exit(1)
        write_log(args.path, args.msg, args.cat, show=args.show)

    elif args.action == 'read':
        read_log(args.path, args.date)

    elif args.action == 'progress':
        show_progress(args.path)

    elif args.action == 'structure':
        show_structure(args.path)

    elif args.action == 'list':
        list_logs(args.path)

    elif args.action == 'new':
        if not args.name:
            print("[X] new action 需要 --name")
            sys.exit(1)
        if os.path.exists(args.path):
            response = input(f"[!] 项目已存在：{args.path}，继续初始化？（y/n）:")
            if response.lower() != 'y':
                sys.exit(0)
        else:
            os.makedirs(args.path)
        create_project_structure(args.path, args.name)
        print(f"[OK] 项目已创建：{args.name}")
        print(f"   路径：{args.path}")

    elif args.action == 'state':
        # 读取或自动创建状态
        state = read_state(args.path)
        if not state:
            # 自动从日志推断创建
            state = DEFAULT_STATE.copy()
            state['project'] = os.path.basename(args.path)
            state['status'] = '待开始'
            latest = get_latest_log(args.path)
            if latest:
                with open(latest, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                entries = []
                for line in lines[4:]:
                    line = line.strip()
                    if not line or line == '---': continue
                    m = re.match(r'## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] (.+)', line)
                    if m:
                        entries.append({"ts": m.group(1), "cat": m.group(2), "msg": m.group(3)})
                if entries:
                    last = entries[-1]
                    state['last_updated'] = last['ts']
                    if last['cat'] == 'SUCCESS':
                        state['status'] = '已完成'
                    elif last['cat'] in ('ERROR', 'WARNING'):
                        state['status'] = '已阻塞'
                        state['open_issues'] = [last['msg'][:80]]
                    else:
                        state['status'] = '进行中'
                        state['current_task'] = last['msg']
            print(f"[i] 自动创建状态文件（项目从未初始化）")

        if args.status or args.task or args.summary or args.issue or args.step:
            # 更新状态
            if args.status:
                state['status'] = args.status
            if args.task:
                state['current_task'] = args.task
            if args.summary:
                state['summary'] = args.summary
            if args.issue:
                state['open_issues'].extend(args.issue)
            if args.step:
                state['next_steps'] = args.step
            write_state(args.path, state)
            status_icon = {"待开始":"[?]","进行中":"[>]","已完成":"[OK]","已阻塞":"[!]"}.get(state['status'],"[-]")
            print(f"[OK] 状态已更新：{status_icon} {state['status']}")
            if state['current_task']:
                print(f"   当前：{state['current_task']}")
        else:
            # 读取状态
            status_icon = {"待开始":"[?]","进行中":"[>]","已完成":"[OK]","已阻塞":"[!]"}.get(state['status'],"[-]")
            print(f"[=] {state['project']} | {status_icon} {state['status']}")
            if state['current_task']:
                print(f"   当前：{state['current_task']}")
            if state['summary']:
                print(f"   状态：{state['summary']}")
            if state['open_issues']:
                print(f"   问题：{', '.join(state['open_issues'])}")
            if state['next_steps']:
                print(f"   下步：{' | '.join(state['next_steps'][:3])}")

if __name__ == '__main__':
    main()
