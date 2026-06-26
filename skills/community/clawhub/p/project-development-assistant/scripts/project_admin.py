#!/usr/bin/env python3
"""
项目管理员工具 - 统一状态管理 + 打通 briefing <-> state

用法:
    python project_admin.py -a init-state -p <项目路径> -n <项目名>    # 为已有项目初始化状态
    python project_admin.py -a sync -p <项目路径>                       # 将 briefing -> state 同步
    python project_admin.py -a new-briefing -p <项目路径>              # 从 state 生成简报
    python project_admin.py -a purge-test                             # 清理测试项目简报
    python project_admin.py -a stats                                  # 全局统计
"""

import os, sys, json, glob, re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
BRIEFINGS_DIR = os.path.join(SKILL_DIR, "briefings")
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")

def get_state_file(project_path):
    return os.path.join(project_path, ".project_state.json")

def get_briefing_file(project_name):
    os.makedirs(BRIEFINGS_DIR, exist_ok=True)
    safe = re.sub(r'[^\w\u4e00-\u9fff-]', '_', project_name)
    safe = re.sub(r'_+', '_', safe).strip('_')
    return os.path.join(BRIEFINGS_DIR, f"{safe}.json")

def get_logs_dir(project_path):
    return os.path.join(project_path, "logs")

def get_latest_log(project_path):
    logs_dir = get_logs_dir(project_path)
    if not os.path.exists(logs_dir):
        return None, []
    pattern = os.path.join(logs_dir, "devlog_*.md")
    files = glob.glob(pattern)
    if not files:
        return None, []
    latest = max(files, key=os.path.getmtime)
    with open(latest, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    entries = []
    for line in lines[4:]:
        line = line.strip()
        if not line or line == '---':
            continue
        m = re.match(r'## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] (.+)', line)
        if m:
            entries.append({"ts": m.group(1), "cat": m.group(2), "msg": m.group(3),
                            "dt": datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S')})
    return latest, entries[-20:]

DEFAULT_STATE = {
    "project": "",
    "status": "待开始",
    "current_task": "",
    "last_updated": "",
    "summary": "",
    "open_issues": [],
    "next_steps": [],
    "milestones": [],
}

def read_state(project_path):
    sf = get_state_file(project_path)
    if os.path.exists(sf):
        with open(sf, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    return None

def write_state(project_path, state):
    sf = get_state_file(project_path)
    os.makedirs(os.path.dirname(sf), exist_ok=True)
    state['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(sf, 'w', encoding='utf-8-sig') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return sf

def scan_projects():
    projects = []
    for base in [WORKSPACE, 'C:', 'D:']:
        if not os.path.exists(base):
            continue
        for item in os.listdir(base):
            item_path = os.path.join(base, item)
            if not os.path.isdir(item_path):
                continue
            if item in ['skills', 'memory', 'briefings', 'tools', 'logs', 'node_modules']:
                continue
            logs_dir = os.path.join(item_path, "logs")
            if os.path.exists(logs_dir):
                projects.append({"name": item, "path": item_path})
    seen = set()
    unique = []
    for p in projects:
        if p['path'] not in seen:
            seen.add(p['path'])
            unique.append(p)
    return unique

def briefing_to_state(briefing):
    state = DEFAULT_STATE.copy()
    state['project'] = briefing.get('project_name', '')
    status_map = {'pending': '待开始', 'in_progress': '进行中', 'completed': '已完成', 'blocked': '已阻塞'}
    state['status'] = status_map.get(briefing.get('status', 'pending'), '进行中')
    state['current_task'] = briefing.get('current_task', '')
    state['open_issues'] = briefing.get('open_issues', [])
    state['last_updated'] = briefing.get('last_update', '')
    return state

def state_to_briefing(state, project_path, project_name):
    status_map = {'待开始': 'pending', '进行中': 'in_progress', '已完成': 'completed', '已阻塞': 'blocked'}
    _, entries = get_latest_log(project_path)
    return {
        "project_name": project_name,
        "project_path": project_path,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status_map.get(state.get('status', '进行中'), 'in_progress'),
        "current_task": state.get('current_task', ''),
        "last_update": state.get('last_updated', ''),
        "open_issues": state.get('open_issues', []),
        "is_interrupted": False,
        "interruption_msg": None,
        "needs_resume": False,
    }

def cmd_init_state(project_path, project_name):
    if os.path.exists(get_state_file(project_path)):
        print(f"[!] 状态文件已存在：{project_path}")
        return
    bf_file = get_briefing_file(project_name)
    if os.path.exists(bf_file):
        with open(bf_file, 'r', encoding='utf-8-sig') as f:
            briefing = json.load(f)
        state = briefing_to_state(briefing)
    else:
        _, entries = get_latest_log(project_path)
        state = DEFAULT_STATE.copy()
        state['project'] = project_name
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
        else:
            state['status'] = '待开始'
    sf = write_state(project_path, state)
    print(f"[OK] 状态文件已创建")

def cmd_sync(project_path):
    state = read_state(project_path)
    if not state:
        print(f"[!] 无状态文件，先运行 init-state")
        return
    project_name = state.get('project', os.path.basename(project_path))
    bf_file = get_briefing_file(project_name)
    if os.path.exists(bf_file):
        with open(bf_file, 'r', encoding='utf-8-sig') as f:
            briefing = json.load(f)
        bstate = briefing_to_state(briefing)
        state['status'] = bstate['status']
        state['current_task'] = bstate['current_task']
        state['open_issues'] = bstate['open_issues']
        state['last_updated'] = bstate['last_updated']
        write_state(project_path, state)
        print(f"[OK] 已同步")
    else:
        print(f"[!] 无简报文件")

def cmd_new_briefing(project_path):
    state = read_state(project_path)
    if not state:
        print(f"[!] 无状态文件，先运行 init-state")
        return
    project_name = state.get('project', os.path.basename(project_path))
    briefing = state_to_briefing(state, project_path, project_name)
    bf_file = get_briefing_file(project_name)
    with open(bf_file, 'w', encoding='utf-8-sig') as f:
        json.dump(briefing, f, ensure_ascii=False, indent=2)
    print(f"[OK] 简报已生成")

def cmd_purge_test():
    os.makedirs(BRIEFINGS_DIR, exist_ok=True)
    test_names = ['test_project', 'test_proj', 'temp_project']
    removed = []
    for f in glob.glob(os.path.join(BRIEFINGS_DIR, "*.json")):
        name = os.path.basename(f)[:-5]
        if any(t in name for t in test_names):
            os.remove(f)
            removed.append(name)
    print(f"[OK] 已清理 {len(removed)} 个测试简报")

def cmd_stats():
    projects = scan_projects()
    print(f"\n=== 项目统计 ({len(projects)} 个) ===\n")
    total_states = 0
    with_state = []
    without_state = []
    for proj in projects:
        if os.path.exists(get_state_file(proj['path'])):
            total_states += 1
            with_state.append(proj['name'])
        else:
            without_state.append(proj['name'])
    print(f"  有状态文件：{len(with_state)} ({', '.join(with_state) or '无'})")
    print(f"  无状态文件：{len(without_state)} ({', '.join(without_state) or '无'})")
    # Clean old briefings
    now = datetime.now()
    removed = 0
    for f in glob.glob(os.path.join(BRIEFINGS_DIR, "*.json")):
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(f))
            if (now - mtime).days > 3:
                os.remove(f)
                removed += 1
        except:
            pass
    if removed:
        print(f"  清理过期简报：{removed} 个")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='项目管理员')
    parser.add_argument('--action', '-a', choices=['init-state', 'sync', 'new-briefing', 'purge-test', 'stats'], default='stats')
    parser.add_argument('--path', '-p', help='项目路径')
    parser.add_argument('--name', '-n', help='项目名称')
    args = parser.parse_args()
    if args.action == 'stats':
        cmd_stats()
    elif args.action == 'init-state':
        if not args.path:
            print("[X] 需要 --path"); sys.exit(1)
        cmd_init_state(args.path, args.name or os.path.basename(args.path))
    elif args.action == 'sync':
        if not args.path:
            print("[X] 需要 --path"); sys.exit(1)
        cmd_sync(args.path)
    elif args.action == 'new-briefing':
        if not args.path:
            print("[X] 需要 --path"); sys.exit(1)
        cmd_new_briefing(args.path)
    elif args.action == 'purge-test':
        cmd_purge_test()
