#!/usr/bin/env python3
"""
OpenClaw Sync Bridge Skill v2.0
一键同步 OpenClaw 配置，智能检测，安全备份

用法:
  python sync_bridge.py setup   # 交互式配置向导（推荐）
  python sync_bridge.py push    # 上传本地 → 云端
  python sync_bridge.py pull    # 下载云端 → 本地
  python sync_bridge.py diff    # 对比差异
  python sync_bridge.py status  # 查看状态
  python sync_bridge.py backup  # 手动备份
"""

import os
import sys
import json
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from difflib import unified_diff

# ============ 配置 ============
CONFIG_FILE = "sync_config.json"
BACKUP_DIR = ".sync-bridge-backup"
DEFAULT_SYNC_FILES = ["SOUL.md", "AGENTS.md", "USER.md", "skills/", "IDENTITY.md", "TOOLS.md"]
IGNORE_PATTERNS = ["config.json", ".env", "*.token", "*.key", "sync_config.json", ".sync-bridge-backup"]

# 常见工作目录路径（按优先级排序）
WORKSPACE_CANDIDATES = [
    # 环境变量优先
    "$OPENCLAW_WORKSPACE",
    "$OPENCLAW_STATE_DIR/workspace",
    # Mac/Linux 默认
    "~/.openclaw/workspace",
    "~/.config/openclaw/workspace",
    "~/.local/share/openclaw/workspace",
    # Windows 默认
    "~/.qclaw/workspace",
    "~/.claw/workspace",
    "~/OpenClaw/workspace",
    # 当前目录及上级
    "./.openclaw/workspace",
    "./workspace",
    "../.openclaw/workspace",
]

# ============ 工具函数 ============
def log(msg, level="info"):
    """彩色日志"""
    ts = datetime.now().strftime("%H:%M:%S")
    icons = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️", "question": "❓"}
    colors = {
        "success": "\033[92m", "error": "\033[91m", 
        "warning": "\033[93m", "info": "\033[94m", "reset": "\033[0m"
    }
    icon = icons.get(level, "ℹ️")
    color = colors.get(level, "")
    reset = colors["reset"]
    print(f"{color}[{ts}] {icon} {msg}{reset}")

def find_workspace():
    """自动寻找工作目录"""
    log("正在寻找 OpenClaw 工作目录...", "info")
    
    found_paths = []
    for candidate in WORKSPACE_CANDIDATES:
        path = Path(os.path.expandvars(candidate)).expanduser().resolve()
        if path.exists():
            # 检查是否有 SOUL.md 或 AGENTS.md 作为确认
            has_soul = (path / "SOUL.md").exists()
            has_agents = (path / "AGENTS.md").exists()
            has_identity = (path / "IDENTITY.md").exists()
            
            if has_soul or has_agents or has_identity:
                found_paths.append({
                    "path": str(path),
                    "has_soul": has_soul,
                    "has_agents": has_agents,
                    "has_identity": has_identity,
                    "score": sum([has_soul, has_agents, has_identity])
                })
    
    if not found_paths:
        log("未自动找到工作目录", "warning")
        return input("请输入 OpenClaw 工作目录路径: ").strip()
    
    # 按匹配度排序
    found_paths.sort(key=lambda x: x["score"], reverse=True)
    
    if len(found_paths) == 1:
        path = found_paths[0]["path"]
        log(f"找到工作目录: {path}", "success")
        return path
    
    # 多个候选，让用户选择
    print("\n找到多个可能的工作目录:")
    for i, p in enumerate(found_paths, 1):
        indicators = []
        if p["has_soul"]: indicators.append("SOUL.md")
        if p["has_agents"]: indicators.append("AGENTS.md")
        if p["has_identity"]: indicators.append("IDENTITY.md")
        print(f"  {i}. {p['path']} ({', '.join(indicators)})")
    
    choice = input(f"\n请选择 [1-{len(found_paths)}] 或输入其他路径: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(found_paths):
        return found_paths[int(choice) - 1]["path"]
    return choice

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(cfg):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def should_ignore(filepath):
    """检查是否忽略"""
    name = os.path.basename(filepath)
    for p in IGNORE_PATTERNS:
        if p.startswith("*") and name.endswith(p[1:]): return True
        if name == p: return True
    return False

def collect_files(workspace, sync_list):
    """收集文件"""
    files = {}
    ws = Path(workspace)
    for item in sync_list:
        target = ws / item
        if not target.exists():
            continue
        if target.is_file() and not should_ignore(target):
            files[item] = target.read_text(encoding='utf-8')
        elif target.is_dir():
            for fp in target.rglob("*"):
                if fp.is_file() and not should_ignore(fp):
                    rel = str(fp.relative_to(ws)).replace(os.sep, "__")
                    try:
                        files[rel] = fp.read_text(encoding='utf-8')
                    except:
                        pass
    return files

def write_files(workspace, files_content):
    """写入文件"""
    ws = Path(workspace)
    written = []
    for gist_name, content in files_content.items():
        if any(p.replace("*", "") in gist_name for p in IGNORE_PATTERNS):
            continue
        local = ws / gist_name.replace("__", os.sep)
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(content, encoding='utf-8')
        written.append(str(local.relative_to(ws)))
    return written

def create_backup(workspace):
    """创建备份"""
    ws = Path(workspace)
    backup_path = ws / BACKUP_DIR / datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # 备份关键文件
    for item in ["SOUL.md", "AGENTS.md", "USER.md", "IDENTITY.md", "TOOLS.md", "skills"]:
        src = ws / item
        if src.exists():
            dst = backup_path / item
            if src.is_file():
                shutil.copy2(src, dst)
            elif src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))
    
    return str(backup_path)

# ============ GitHub API ============
class GistAPI:
    def __init__(self, token, gist_id=None):
        self.token = token
        self.gist_id = gist_id
    
    def _request(self, method, url, data=None):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "OpenClaw-Sync-Bridge"
        }
        req = urllib.request.Request(url, data=data.encode('utf-8') if data else None, 
                                     headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise Exception("Token 无效或已过期，请重新申请")
            raise Exception(f"API 错误: {e.read().decode('utf-8')}")
    
    def verify_token(self):
        """验证 Token"""
        req = urllib.request.Request(
            "https://api.github.com/user",
            headers={"Authorization": f"token {self.token}", "User-Agent": "OpenClaw-Sync-Bridge"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    
    def create_gist(self):
        """创建 Gist"""
        data = json.dumps({
            "description": "OpenClaw Sync Bridge",
            "public": False,
            "files": {"sync-manifest.json": {"content": json.dumps({"created_at": datetime.now().isoformat()}, indent=2)}}
        })
        result = self._request("POST", "https://api.github.com/gists", data)
        self.gist_id = result["id"]
        return self.gist_id
    
    def get_gist(self):
        return self._request("GET", f"https://api.github.com/gists/{self.gist_id}")
    
    def update_gist(self, files):
        data = json.dumps({"files": {k: {"content": v} for k, v in files.items()}})
        return self._request("PATCH", f"https://api.github.com/gists/{self.gist_id}", data)

# ============ 差异对比 ============
def compute_diff(local_files, remote_files):
    """计算文件差异"""
    diff_result = {
        "added": [],      # 本地有，云端没有
        "modified": [],   # 两边都有，内容不同
        "deleted": [],    # 云端有，本地没有
        "same": []        # 内容相同
    }
    
    all_files = set(local_files.keys()) | set(remote_files.keys())
    
    for f in all_files:
        local_content = local_files.get(f, "")
        remote_content = remote_files.get(f, "")
        
        if f not in local_files:
            diff_result["deleted"].append(f)
        elif f not in remote_files:
            diff_result["added"].append(f)
        elif local_content != remote_content:
            diff_result["modified"].append(f)
        else:
            diff_result["same"].append(f)
    
    return diff_result

def show_diff_preview(local_files, remote_files, filename, max_lines=20):
    """显示差异预览"""
    local_content = local_files.get(filename, "").splitlines()
    remote_content = remote_files.get(filename, "").splitlines()
    
    diff = list(unified_diff(remote_content, local_content, 
                             fromfile=f"cloud/{filename}", tofile=f"local/{filename}", lineterm=""))
    
    if len(diff) > max_lines:
        diff = diff[:max_lines] + ["... (更多差异省略)"]
    
    print("\n" + "="*60)
    print(f"差异预览: {filename}")
    print("="*60)
    for line in diff:
        if line.startswith('+'):
            print(f"\033[92m{line}\033[0m")  # 绿色（本地新增）
        elif line.startswith('-'):
            print(f"\033[91m{line}\033[0m")  # 红色（云端删除）
        elif line.startswith('@@'):
            print(f"\033[94m{line}\033[0m")  # 蓝色（位置信息）
        else:
            print(line)
    print("="*60)

# ============ 命令 ============
def cmd_setup():
    """交互式配置向导"""
    print("\n" + "="*60)
    print("🔄 OpenClaw Sync Bridge 配置向导")
    print("="*60 + "\n")
    
    cfg = load_config()
    
    # 1. 工作目录
    if cfg.get("workspace"):
        log(f"当前工作目录: {cfg['workspace']}")
        change = input("是否更改工作目录? [y/N]: ").strip().lower()
        if change == 'y':
            workspace = find_workspace()
        else:
            workspace = cfg["workspace"]
    else:
        workspace = find_workspace()
    
    # 2. GitHub Token
    if cfg.get("token"):
        log("已配置 GitHub Token")
        change = input("是否更换 Token? [y/N]: ").strip().lower()
        if change == 'y':
            token = input("请输入新的 GitHub Token: ").strip()
        else:
            token = cfg["token"]
    else:
        print("\n📋 请访问 https://github.com/settings/tokens 申请 Token")
        print("   勾选 'gist' 权限即可\n")
        token = input("请输入 GitHub Token: ").strip()
    
    if not token:
        log("Token 不能为空", "error")
        return
    
    # 验证 Token
    log("验证 Token...", "info")
    try:
        api = GistAPI(token)
        user = api.verify_token()
        log(f"验证成功！用户: @{user.get('login')}", "success")
    except Exception as e:
        log(f"验证失败: {e}", "error")
        return
    
    # 3. Gist ID
    gist_id = cfg.get("gist_id", "")
    if gist_id:
        log(f"已有 Gist ID: {gist_id}")
        print("\n1. 使用现有 Gist")
        print("2. 创建新的 Gist")
        choice = input("请选择 [1/2]: ").strip()
        if choice == "2":
            gist_id = ""
    
    if not gist_id:
        log("创建新的 Gist...", "info")
        try:
            gist_id = api.create_gist()
            log(f"创建成功: {gist_id}", "success")
        except Exception as e:
            log(f"创建失败: {e}", "error")
            return
    
    # 4. 保存配置
    cfg = {
        "token": token,
        "gist_id": gist_id,
        "workspace": workspace,
        "sync_files": cfg.get("sync_files", DEFAULT_SYNC_FILES)
    }
    save_config(cfg)
    
    log("配置已保存！", "success")
    
    # 5. 首次同步方向选择
    print("\n" + "="*60)
    print("🎯 首次同步设置")
    print("="*60)
    
    local_files = collect_files(workspace, cfg["sync_files"])
    try:
        remote_data = api.get_gist()
        remote_files = {k: v["content"] for k, v in remote_data["files"].items() if k != "sync-manifest.json"}
    except:
        remote_files = {}
    
    print(f"\n本地文件: {len(local_files)} 个")
    print(f"云端文件: {len(remote_files)} 个")
    
    if not local_files and not remote_files:
        log("本地和云端都没有文件，请先创建一些配置", "warning")
    elif not local_files:
        print("\n📥 云端有文件，本地为空")
        if input("是否下载到本地? [Y/n]: ").strip().lower() != 'n':
            cmd_pull(skip_confirm=True)
    elif not remote_files:
        print("\n📤 本地有文件，云端为空")
        if input("是否上传到云端? [Y/n]: ").strip().lower() != 'n':
            cmd_push(skip_confirm=True)
    else:
        # 两边都有，显示对比
        print("\n1. 📤 上传本地 → 云端（覆盖云端）")
        print("2. 📥 下载云端 → 本地（覆盖本地）")
        print("3. ⚖️  对比差异")
        print("4. ⏭️  稍后决定")
        
        choice = input("\n请选择 [1/2/3/4]: ").strip()
        if choice == "1":
            cmd_push(skip_confirm=True)
        elif choice == "2":
            cmd_pull(skip_confirm=True)
        elif choice == "3":
            cmd_diff()
            # 对比后再选择
            print("\n" + "="*60)
            print("🔄 同步方向选择")
            print("="*60)
            print("1. 📤 上传本地 → 云端")
            print("2. 📥 下载云端 → 本地")
            choice2 = input("请选择 [1/2] 或按 Enter 取消: ").strip()
            if choice2 == "1":
                cmd_push(skip_confirm=True)
            elif choice2 == "2":
                cmd_pull(skip_confirm=True)

def cmd_push(skip_confirm=False):
    """上传"""
    cfg = load_config()
    if not cfg.get("token") or not cfg.get("gist_id"):
        log("未配置，请先运行: python sync_bridge.py setup", "error")
        return
    
    # Token 检测
    try:
        api = GistAPI(cfg["token"], cfg["gist_id"])
        api.verify_token()
    except Exception as e:
        log(f"Token 检测失败: {e}", "error")
        return
    
    workspace = cfg["workspace"]
    local_files = collect_files(workspace, cfg["sync_files"])
    
    if not local_files:
        log("没有文件需要上传", "warning")
        return
    
    # 获取云端文件用于预览
    try:
        remote_data = api.get_gist()
        remote_files = {k: v["content"] for k, v in remote_data["files"].items() if k != "sync-manifest.json"}
        diff = compute_diff(local_files, remote_files)
    except:
        diff = {"added": list(local_files.keys()), "modified": [], "deleted": [], "same": []}
    
    # 同步预览
    print("\n" + "="*60)
    print("📋 同步预览（本地 → 云端）")
    print("="*60)
    print(f"工作目录: {workspace}")
    print(f"\n本次将上传 {len(local_files)} 个文件:")
    
    if diff["added"]:
        print(f"  🆕 新增: {len(diff['added'])} 个")
        for f in diff["added"][:5]:
            print(f"     + {f}")
        if len(diff["added"]) > 5:
            print(f"     ... 还有 {len(diff['added']) - 5} 个")
    
    if diff["modified"]:
        print(f"  📝 修改: {len(diff['modified'])} 个")
        for f in diff["modified"][:5]:
            print(f"     ~ {f}")
        if len(diff["modified"]) > 5:
            print(f"     ... 还有 {len(diff['modified']) - 5} 个")
    
    if diff["deleted"]:
        print(f"  🗑️  删除（云端）: {len(diff['deleted'])} 个")
    
    print("="*60)
    
    if not skip_confirm:
        confirm = input("\n确认上传? 云端文件将被覆盖 [y/N/查看差异diff]: ").strip().lower()
        if confirm == "diff":
            for f in diff["modified"][:3]:
                show_diff_preview(local_files, remote_files, f)
            confirm = input("\n确认上传? [y/N]: ").strip().lower()
        if confirm != 'y':
            log("已取消", "info")
            return
    
    # 自动备份（上传前备份云端）
    if remote_files:
        backup_path = create_backup(workspace)
        log(f"已备份现有文件到: {backup_path}", "info")
    
    # 执行上传
    files = local_files.copy()
    files["sync-manifest.json"] = json.dumps({
        "last_push": datetime.now().isoformat(),
        "count": len(local_files),
        "device": os.uname().nodename if hasattr(os, 'uname') else "unknown"
    }, indent=2)
    
    try:
        api.update_gist(files)
        log(f"上传成功！共 {len(local_files)} 个文件", "success")
    except Exception as e:
        log(f"上传失败: {e}", "error")

def cmd_pull(skip_confirm=False):
    """下载"""
    cfg = load_config()
    if not cfg.get("token") or not cfg.get("gist_id"):
        log("未配置，请先运行: python sync_bridge.py setup", "error")
        return
    
    # Token 检测
    try:
        api = GistAPI(cfg["token"], cfg["gist_id"])
        api.verify_token()
    except Exception as e:
        log(f"Token 检测失败: {e}", "error")
        return
    
    workspace = cfg["workspace"]
    local_files = collect_files(workspace, cfg["sync_files"])
    
    # 获取云端文件
    try:
        remote_data = api.get_gist()
        remote_files = {k: v["content"] for k, v in remote_data["files"].items() if k != "sync-manifest.json"}
    except Exception as e:
        log(f"获取云端文件失败: {e}", "error")
        return
    
    if not remote_files:
        log("云端没有文件", "warning")
        return
    
    # 计算差异
    diff = compute_diff(local_files, remote_files)
    
    # 同步预览
    print("\n" + "="*60)
    print("📋 同步预览（云端 → 本地）")
    print("="*60)
    print(f"工作目录: {workspace}")
    print(f"\n本次将下载 {len(remote_files)} 个文件:")
    
    if diff["deleted"]:  # 从云端看是删除，从本地看是新增
        print(f"  🆕 新增: {len(diff['deleted'])} 个")
        for f in diff["deleted"][:5]:
            print(f"     + {f}")
    
    if diff["modified"]:
        print(f"  📝 覆盖: {len(diff['modified'])} 个")
        for f in diff["modified"][:5]:
            print(f"     ~ {f}")
    
    if diff["added"]:  # 本地有但云端没有
        print(f"  ⚠️  本地独有（保留）: {len(diff['added'])} 个")
    
    print("="*60)
    
    if not skip_confirm:
        confirm = input("\n确认下载? 本地文件将被覆盖 [y/N/查看差异diff]: ").strip().lower()
        if confirm == "diff":
            for f in diff["modified"][:3]:
                show_diff_preview(local_files, remote_files, f)
            confirm = input("\n确认下载? [y/N]: ").strip().lower()
        if confirm != 'y':
            log("已取消", "info")
            return
    
    # 自动备份
    if local_files:
        backup_path = create_backup(workspace)
        log(f"已备份现有文件到: {backup_path}", "info")
    
    # 执行下载
    try:
        count = write_files(workspace, remote_files)
        log(f"下载成功！写入 {count} 个文件", "success")
    except Exception as e:
        log(f"下载失败: {e}", "error")

def cmd_diff():
    """对比差异"""
    cfg = load_config()
    if not cfg.get("token") or not cfg.get("gist_id"):
        log("未配置", "error")
        return
    
    workspace = cfg["workspace"]
    local_files = collect_files(workspace, cfg["sync_files"])
    
    try:
        api = GistAPI(cfg["token"], cfg["gist_id"])
        remote_data = api.get_gist()
        remote_files = {k: v["content"] for k, v in remote_data["files"].items() if k != "sync-manifest.json"}
    except Exception as e:
        log(f"获取云端文件失败: {e}", "error")
        return
    
    diff = compute_diff(local_files, remote_files)
    
    print("\n" + "="*60)
    print("⚖️  文件差异对比")
    print("="*60)
    print(f"工作目录: {workspace}")
    print(f"\n📊 统计:")
    print(f"  🆕 本地新增: {len(diff['added'])} 个（云端没有）")
    print(f"  📝 内容不同: {len(diff['modified'])} 个")
    print(f"  🗑️  云端独有: {len(diff['deleted'])} 个（本地没有）")
    print(f"  ✅ 完全相同: {len(diff['same'])} 个")
    
    if diff["modified"]:
        print(f"\n📝 内容不同的文件:")
        for i, f in enumerate(diff["modified"], 1):
            print(f"  {i}. {f}")
        
        view = input("\n查看具体差异? [文件编号/all/跳过]: ").strip().lower()
        if view == "all":
            for f in diff["modified"]:
                show_diff_preview(local_files, remote_files, f)
        elif view.isdigit():
            idx = int(view) - 1
            if 0 <= idx < len(diff["modified"]):
                show_diff_preview(local_files, remote_files, diff["modified"][idx])

def cmd_backup():
    """手动备份"""
    cfg = load_config()
    workspace = cfg.get("workspace", ".")
    
    backup_path = create_backup(workspace)
    log(f"备份完成: {backup_path}", "success")
    
    # 清理旧备份（保留最近 10 个）
    backup_root = Path(workspace) / BACKUP_DIR
    if backup_root.exists():
        backups = sorted(backup_root.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        for old in backups[10:]:
            shutil.rmtree(old)
            log(f"清理旧备份: {old.name}", "info")

def cmd_status():
    """状态"""
    cfg = load_config()
    print("\n" + "="*60)
    print("📊 Sync Bridge 状态")
    print("="*60 + "\n")
    
    print(f"工作目录: {cfg.get('workspace', '未设置')}")
    print(f"Gist ID: {cfg.get('gist_id', '未设置')}")
    print(f"同步列表: {', '.join(cfg.get('sync_files', DEFAULT_SYNC_FILES))}")
    
    if cfg.get("token") and cfg.get("gist_id"):
        try:
            api = GistAPI(cfg["token"], cfg["gist_id"])
            api.verify_token()
            print("\n✅ Token 有效")
            
            data = api.get_gist()
            print(f"Gist 文件数: {len(data.get('files', {}))}")
            print(f"最后更新: {data.get('updated_at')}")
            
            if "sync-manifest.json" in data["files"]:
                manifest = json.loads(data["files"]["sync-manifest.json"]["content"])
                print(f"上次上传: {manifest.get('last_push', '未知')}")
                print(f"上传设备: {manifest.get('device', '未知')}")
        except Exception as e:
            log(f"连接失败: {e}", "error")
    
    # 本地文件统计
    if cfg.get("workspace"):
        local_files = collect_files(cfg["workspace"], cfg.get("sync_files", DEFAULT_SYNC_FILES))
        print(f"\n本地文件数: {len(local_files)}")
    
    # 备份目录
    backup_root = Path(cfg.get("workspace", ".")) / BACKUP_DIR
    if backup_root.exists():
        backups = list(backup_root.iterdir())
        print(f"备份历史: {len(backups)} 个")

# ============ 入口 ============
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    if cmd == "setup": cmd_setup()
    elif cmd == "push": cmd_push()
    elif cmd == "pull": cmd_pull()
    elif cmd == "diff": cmd_diff()
    elif cmd == "status": cmd_status()
    elif cmd == "backup": cmd_backup()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
