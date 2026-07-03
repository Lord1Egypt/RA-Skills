#!/usr/bin/env python3
"""huo15-token-optimizer clean — 安全清理工作区冗余文件"""
import os, json, sys, shutil, re
from datetime import datetime

WORKSPACE_BASE = os.path.expanduser("~/.openclaw")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_backup_dir():
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.expanduser(os.path.join(config["safety"]["backup_dir"], today))

def backup_file(path, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)
    fname = os.path.basename(path)
    ws = os.path.basename(os.path.dirname(path))
    dest = os.path.join(backup_dir, f"{ws}_{fname}")
    shutil.copy2(path, dest)
    return dest

def truncate_dreams(path, keep_entries):
    with open(path) as f:
        content = f.read()
    
    diary_match = re.search(r'(<!-- openclaw:dreaming:diary:start -->)(.*?)(<!-- openclaw:dreaming:diary:end -->)', content, re.DOTALL)
    deep_match = re.search(r'(## Deep Sleep.*)', content, re.DOTALL)
    
    if not diary_match:
        return None, None
    
    header = content[:diary_match.start(1)]
    start_tag = diary_match.group(1)
    diary_body = diary_match.group(2)
    end_tag = diary_match.group(3)
    
    entries = re.split(r'\n\*[A-Z]', diary_body)
    if len(entries) <= keep_entries + 1:
        return None, None
    
    kept = entries[0]
    for entry in entries[-keep_entries:]:
        kept += '\n*' + entry[1:] if entry.startswith(' ') else '\n*' + entry
    
    new_content = header + start_tag + kept.strip() + '\n\n' + end_tag
    if deep_match:
        new_content += '\n\n' + deep_match.group(1)
    
    return new_content, len(entries) - keep_entries - 1

def get_main_agents():
    """Get the slim AGENTS.md from main workspace"""
    path = os.path.join(WORKSPACE_BASE, "workspace", "AGENTS.md")
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return None

def clean(args):
    config = load_config()
    dry_run = "--dry-run" in args or "--force" not in args
    force = "--force" in args
    restore_date = None
    
    for i, a in enumerate(args):
        if a == "--restore" and i + 1 < len(args):
            restore_date = args[i + 1]
    
    if restore_date:
        restore(restore_date)
        return
    
    backup_dir = get_backup_dir()
    total_saved = 0
    actions = []
    
    # Determine workspaces to clean
    if "--all" in args:
        workspaces = [d for d in os.listdir(WORKSPACE_BASE) if d.startswith("workspace") and os.path.isdir(os.path.join(WORKSPACE_BASE, d))]
    else:
        # Specific workspace
        for a in args:
            if a.startswith("--workspace"):
                workspaces = [a.split("=")[1] if "=" in a else args[args.index(a)+1]]
                break
        else:
            workspaces = [d for d in os.listdir(WORKSPACE_BASE) if d.startswith("workspace") and os.path.isdir(os.path.join(WORKSPACE_BASE, d))]
    
    for ws in workspaces:
        ws_path = os.path.join(WORKSPACE_BASE, ws)
        ws_name = ws.replace("workspace-", "").replace("workspace.", "")
        
        # DREAMS truncation
        dreams_path = os.path.join(ws_path, "DREAMS.md")
        if os.path.exists(dreams_path):
            new_content, removed = truncate_dreams(dreams_path, config["thresholds"]["dreams_keep_entries"])
            if new_content and removed:
                before = os.path.getsize(dreams_path)
                action = {
                    "workspace": ws_name,
                    "file": "DREAMS.md",
                    "action": f"truncate {removed} entries → keep {config['thresholds']['dreams_keep_entries']}",
                    "before": before,
                    "after": len(new_content.encode('utf-8')),
                    "saved": before - len(new_content.encode('utf-8'))
                }
                actions.append(action)
                total_saved += action["saved"]
                
                if not dry_run and force:
                    backup_file(dreams_path, backup_dir)
                    with open(dreams_path, 'w') as f:
                        f.write(new_content)
        
        # AGENTS.md slim (only for old verbose format, not custom)
        agents_path = os.path.join(ws_path, "AGENTS.md")
        if os.path.exists(agents_path) and os.path.getsize(agents_path) > config["thresholds"]["agents_max_kb"] * 1024:
            with open(agents_path) as f:
                content = f.read()
            # Only auto-replace if it matches the old verbose pattern
            is_old_format = bool(re.search(r'AGENTS\.md\s*[-–]\s*全局规则', content))
            if is_old_format and config["safety"]["auto_replace_agents"]:
                slim = get_main_agents()
                if slim:
                    backup_file(agents_path, backup_dir)
                    if not dry_run and force:
                        with open(agents_path, 'w') as f:
                            f.write(slim)
                    action = {
                        "workspace": ws_name,
                        "file": "AGENTS.md",
                        "action": "replace with slim version",
                        "before": os.path.getsize(agents_path),
                        "after": len(slim.encode('utf-8')),
                        "saved": os.path.getsize(agents_path) - len(slim.encode('utf-8'))
                    }
                    actions.append(action)
                    total_saved += action["saved"]
            else:
                actions.append({
                    "workspace": ws_name,
                    "file": "AGENTS.md",
                    "action": "SKIPPED (custom format, needs manual review)",
                    "size": os.path.getsize(agents_path)
                })
    
    if dry_run:
        print(f"[DRY RUN] 预览 {len(actions)} 项变更，预计节省 {total_saved:,} bytes (~{int(total_saved*0.3):,} tokens)")
    else:
        print(f"[EXECUTED] {len(actions)} 项清理完成，节省 {total_saved:,} bytes (~{int(total_saved*0.3):,} tokens)")
        print(f"备份目录: {backup_dir}")
    
    for a in actions:
        print(f"  {a['workspace']}/{a['file']}: {a.get('action', '')}")
        if 'saved' in a:
            print(f"    {a['before']}B → {a['after']}B (saved {a['saved']}B)")

def restore(date_str):
    config = load_config()
    backup_dir = os.path.expanduser(os.path.join(config["safety"]["backup_dir"], date_str))
    if not os.path.exists(backup_dir):
        print(f"备份不存在: {backup_dir}")
        sys.exit(1)
    
    count = 0
    for f in os.listdir(backup_dir):
        # Parse ws_filename format
        parts = f.split("_", 1)
        if len(parts) != 2:
            continue
        ws_name, fname = parts
        
        # Find the actual workspace path
        for d in os.listdir(WORKSPACE_BASE):
            if d.endswith(ws_name) and os.path.isdir(os.path.join(WORKSPACE_BASE, d)):
                dest = os.path.join(WORKSPACE_BASE, d, fname)
                src = os.path.join(backup_dir, f)
                shutil.copy2(src, dest)
                print(f"恢复: {d}/{fname}")
                count += 1
                break
    
    print(f"已恢复 {count} 个文件")

if __name__ == "__main__":
    clean(sys.argv[1:])
