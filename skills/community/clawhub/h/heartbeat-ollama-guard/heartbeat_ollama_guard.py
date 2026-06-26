#!/usr/bin/env python3
# heartbeat-ollama-guard v1.0.0
"""
heartbeat-ollama-guard — 将 OpenClaw 心跳切换为本地 Ollama 模型，并部署守卫防止配置被静默修改。

用法：
  python3 heartbeat_ollama_guard.py --setup            # 完整安装向导
  python3 heartbeat_ollama_guard.py --status           # 查看当前状态
  python3 heartbeat_ollama_guard.py --check            # 单次守卫检查
  python3 heartbeat_ollama_guard.py --uninstall        # 卸载守卫
  python3 heartbeat_ollama_guard.py --model <id>       # 指定模型（配合 --setup）
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── constants ──────────────────────────────────────────────────────────────────

SKILL_VERSION   = "1.0.0"
GUARD_VERSION   = "1.0.0"
DEFAULT_MODEL   = "qwen3.5:4b-q4_K_M"

LIB_DIR         = Path.home() / ".openclaw" / "workspace" / ".lib"
GUARD_SCRIPT    = LIB_DIR / "heartbeat-guard.py"
GUARD_CONF      = LIB_DIR / "heartbeat-guard.conf.json"
GUARD_BACKUP_DIR= LIB_DIR / ".hog_backups"

LAUNCHAGENT_LABEL  = "com.openclaw.heartbeat-guard"
LAUNCHAGENT_PLIST  = Path.home() / "Library" / "LaunchAgents" / f"{LAUNCHAGENT_LABEL}.plist"
SYSTEMD_SERVICE    = Path.home() / ".config" / "systemd" / "user" / "openclaw-heartbeat-guard.service"

OPENCLAW_PROVIDER_KEY = "local"

# ── embedded guard daemon code ─────────────────────────────────────────────────

GUARD_DAEMON_CODE = '''#!/usr/bin/env python3
# heartbeat-guard v{version}
"""
heartbeat-guard.py — 心跳配置守卫
监控 openclaw.json 中 heartbeat.model 的值，发现未授权修改立即回滚并发出系统通知。

授权修改流程：
  1. 先更新 heartbeat-guard.conf.json 的 expected 值（视为签字授权）
  2. 再修改对应 openclaw.json
  守卫会自动识别已授权的变更（conf 与 json 一致 → 放行）

用法：
  python3 heartbeat-guard.py          # 守护进程模式（LaunchAgent 调用）
  python3 heartbeat-guard.py --check  # 单次检查（不循环）
"""

import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

CONF_FILE = Path(__file__).parent / "heartbeat-guard.conf.json"
LOG_FILE  = Path(__file__).parent / "heartbeat-guard.log"
CHECK_INTERVAL = 60  # 秒

_running = True


def _signal_handler(sig, frame):
    global _running
    _running = False


signal.signal(signal.SIGTERM, _signal_handler)
signal.signal(signal.SIGINT,  _signal_handler)


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"{{ts}} {{msg}}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\\n")
    except OSError:
        pass


def notify(title: str, body: str):
    """macOS 系统通知（不依赖第三方库）"""
    script = (
        f\'display notification "{{body}}" with title "{{title}}" \'
        f\'sound name "Basso"\'
    )
    try:
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, timeout=5
        )
    except Exception:
        pass


def get_nested(obj: dict, dotted_path: str):
    parts = dotted_path.split(".")
    cur = obj
    for p in parts:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def set_nested(obj: dict, dotted_path: str, value):
    parts = dotted_path.split(".")
    cur = obj
    for p in parts[:-1]:
        cur = cur.setdefault(p, {{}})
    cur[parts[-1]] = value


def load_json(path: Path) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"[ERROR] 读取 {{path}} 失败: {{e}}")
        return None


def save_json(path: Path, data: dict) -> bool:
    try:
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\\n"
        path.write_text(text, encoding="utf-8")
        return True
    except Exception as e:
        log(f"[ERROR] 写入 {{path}} 失败: {{e}}")
        return False


def check_once() -> bool:
    conf = load_json(CONF_FILE)
    if conf is None:
        log("[WARN] conf 文件不可读，跳过本次检查")
        return True

    protected = conf.get("protected", {{}})
    all_ok = True

    for cfg_path_str, rule in protected.items():
        cfg_path  = Path(cfg_path_str)
        dot_path  = rule.get("path", "")
        expected  = rule.get("expected")

        if not cfg_path.exists():
            log(f"[WARN] 目标文件不存在，跳过: {{cfg_path_str}}")
            continue

        cfg_data = load_json(cfg_path)
        if cfg_data is None:
            continue

        actual = get_nested(cfg_data, dot_path)

        if actual == expected:
            continue

        all_ok = False
        log(
            f"[ALERT] 未授权修改！文件={{cfg_path.name}} "
            f"路径={{dot_path}} "
            f"期望={{expected!r}} 实际={{actual!r}}"
        )

        set_nested(cfg_data, dot_path, expected)
        if save_json(cfg_path, cfg_data):
            log(f"[REVERT] 已回滚 {{cfg_path.name}} {{dot_path}} → {{expected!r}}")
            notify(
                "🛡️ OpenClaw 心跳守卫",
                f"检测到未授权修改并已回滚\\n"
                f"文件: {{cfg_path.name}}\\n"
                f"改回: {{expected}}"
            )
        else:
            log(f"[ERROR] 回滚失败！需手动检查 {{cfg_path_str}}")
            notify(
                "🚨 OpenClaw 心跳守卫（回滚失败）",
                f"未授权修改且回滚失败，请立即检查:\\n{{cfg_path_str}}"
            )

    return all_ok


def main():
    single_check = "--check" in sys.argv

    log("[START] heartbeat-guard 启动")
    log(f"[INFO]  conf={{CONF_FILE}}")
    log(f"[INFO]  interval={{CHECK_INTERVAL}}s  mode={{\'single\' if single_check else \'daemon\'}}")

    if single_check:
        ok = check_once()
        sys.exit(0 if ok else 1)

    while _running:
        try:
            check_once()
        except Exception as e:
            log(f"[ERROR] 检查异常: {{e}}")
        for _ in range(CHECK_INTERVAL):
            if not _running:
                break
            time.sleep(1)

    log("[STOP] heartbeat-guard 退出")


if __name__ == "__main__":
    main()
'''.format(version=GUARD_VERSION)

# ── helpers ────────────────────────────────────────────────────────────────────

def _ok(msg):  print(f"  ✅ {msg}")
def _warn(msg): print(f"  ⚠️  {msg}")
def _err(msg):  print(f"  ❌ {msg}")
def _info(msg): print(f"     {msg}")
def _step(n, title): print(f"\nStep {n}: {title}")
def _hr(): print("=" * 52)


def run(cmd, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, **kw)


def get_nested(obj: dict, dotted_path: str):
    parts = dotted_path.split(".")
    cur = obj
    for p in parts:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def set_nested(obj: dict, dotted_path: str, value):
    parts = dotted_path.split(".")
    cur = obj
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value


def load_json(path: Path) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  [ERROR] 读取 {path} 失败: {e}")
        return None


def save_json(path: Path, data: dict) -> bool:
    try:
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        path.write_text(text, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  [ERROR] 写入 {path} 失败: {e}")
        return False


def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_linux() -> bool:
    return platform.system() == "Linux"


# ── ollama detection ───────────────────────────────────────────────────────────

def find_ollama() -> Optional[str]:
    """Return path to ollama binary, or None."""
    p = shutil.which("ollama")
    if p:
        return p
    # common extra paths
    for extra in ["/usr/local/bin/ollama", "/opt/homebrew/bin/ollama"]:
        if Path(extra).exists():
            return extra
    return None


def get_ollama_version(ollama_bin: str) -> str:
    try:
        r = run([ollama_bin, "--version"], capture_output=True, text=True, timeout=5)
        return r.stdout.strip() or r.stderr.strip()
    except Exception:
        return "unknown"


def model_is_pulled(ollama_bin: str, model_id: str) -> bool:
    try:
        r = run([ollama_bin, "list"], capture_output=True, text=True, timeout=10)
        # model_id like "qwen3.5:4b-q4_K_M"
        base = model_id.split(":")[0]
        tag  = model_id.split(":")[1] if ":" in model_id else ""
        for line in r.stdout.splitlines():
            if base in line and (not tag or tag.lower() in line.lower()):
                return True
        return False
    except Exception:
        return False


def pull_model(ollama_bin: str, model_id: str) -> bool:
    print(f"     正在拉取模型 {model_id}（可能需要几分钟）...")
    try:
        r = run([ollama_bin, "pull", model_id])
        return r.returncode == 0
    except Exception as e:
        print(f"  [ERROR] pull 失败: {e}")
        return False


# ── openclaw.json discovery ────────────────────────────────────────────────────

def discover_instances() -> list[Path]:
    instances = []
    primary = Path.home() / ".openclaw" / "openclaw.json"
    if primary.exists():
        instances.append(primary)
    # glob for .openclaw-* siblings
    home = Path.home()
    for d in sorted(home.glob(".openclaw-*")):
        if d.is_dir():
            cand = d / "openclaw.json"
            if cand.exists():
                instances.append(cand)
    return instances


# ── openclaw.json patching ─────────────────────────────────────────────────────

HEARTBEAT_PATH = "agents.defaults.heartbeat.model"


def patch_openclaw_json(cfg_path: Path, model_id: str) -> bool:
    """
    写入 agents.defaults.heartbeat.model = "local/<model_id>"
    若 models.providers.local 不存在则创建 Ollama provider 配置。
    返回 True 表示实际写入（False 表示已是目标值，跳过）。
    """
    data = load_json(cfg_path)
    if data is None:
        return False

    target_value = f"{OPENCLAW_PROVIDER_KEY}/{model_id}"
    current = get_nested(data, HEARTBEAT_PATH)

    if current == target_value:
        return False  # 已是目标值，幂等跳过

    # backup
    GUARD_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = GUARD_BACKUP_DIR / f"{cfg_path.parent.name}_openclaw_{ts}.json"
    shutil.copy2(cfg_path, backup)

    set_nested(data, HEARTBEAT_PATH, target_value)

    # ensure models.providers.local exists
    providers = get_nested(data, "models.providers") or {}
    if not isinstance(providers, dict):
        providers = {}
    if OPENCLAW_PROVIDER_KEY not in providers:
        local_provider = {
            "name": "Ollama (Local)",
            "type": "ollama",
            "baseUrl": "http://localhost:11434",
            "models": [model_id]
        }
        set_nested(data, f"models.providers.{OPENCLAW_PROVIDER_KEY}", local_provider)

    return save_json(cfg_path, data)


# ── guard conf.json ────────────────────────────────────────────────────────────

def load_conf() -> dict:
    if GUARD_CONF.exists():
        d = load_json(GUARD_CONF)
        return d if d else {}
    return {}


def save_conf(conf: dict) -> bool:
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    return save_json(GUARD_CONF, conf)


def update_conf(instances: list[Path], model_id: str) -> bool:
    conf = load_conf()
    if "_comment" not in conf:
        conf["_comment"] = (
            "授权修改 heartbeat.model 的流程：先更新本文件的 expected 值（视为签字授权），"
            "再修改对应 openclaw.json。守卫会自动识别已授权的变更。"
        )
    protected = conf.setdefault("protected", {})
    target_value = f"{OPENCLAW_PROVIDER_KEY}/{model_id}"
    for p in instances:
        protected[str(p)] = {
            "path": HEARTBEAT_PATH,
            "expected": target_value
        }
    return save_conf(conf)


# ── guard daemon script ────────────────────────────────────────────────────────

def get_guard_version() -> Optional[str]:
    """Read version from first line comment of existing guard script."""
    if not GUARD_SCRIPT.exists():
        return None
    try:
        with open(GUARD_SCRIPT, "r") as f:
            first = f.readline()
        m = re.search(r"heartbeat-guard v(\S+)", first)
        return m.group(1) if m else None
    except Exception:
        return None


def write_guard_script() -> bool:
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    try:
        GUARD_SCRIPT.write_text(GUARD_DAEMON_CODE, encoding="utf-8")
        GUARD_SCRIPT.chmod(0o755)
        return True
    except Exception as e:
        print(f"  [ERROR] 写入守卫脚本失败: {e}")
        return False


# ── launchagent / systemd ──────────────────────────────────────────────────────

PLIST_CONTENT = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>{guard_script}</string>
  </array>

  <key>KeepAlive</key>
  <true/>

  <key>RunAtLoad</key>
  <true/>

  <key>StandardOutPath</key>
  <string>{lib_dir}/heartbeat-guard-stdout.log</string>

  <key>StandardErrorPath</key>
  <string>{lib_dir}/heartbeat-guard-stderr.log</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
  </dict>
</dict>
</plist>
"""

SYSTEMD_CONTENT = """\
[Unit]
Description=OpenClaw Heartbeat Guard
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {guard_script}
Restart=always
RestartSec=10
StandardOutput=append:{lib_dir}/heartbeat-guard-stdout.log
StandardError=append:{lib_dir}/heartbeat-guard-stderr.log

[Install]
WantedBy=default.target
"""


def deploy_launchagent() -> bool:
    LAUNCHAGENT_PLIST.parent.mkdir(parents=True, exist_ok=True)
    content = PLIST_CONTENT.format(
        label=LAUNCHAGENT_LABEL,
        guard_script=GUARD_SCRIPT,
        lib_dir=LIB_DIR,
    )
    try:
        LAUNCHAGENT_PLIST.write_text(content)
    except Exception as e:
        print(f"  [ERROR] 写 plist 失败: {e}")
        return False

    # unload if already loaded (ignore errors)
    run(["launchctl", "unload", str(LAUNCHAGENT_PLIST)], capture_output=True)
    r = run(["launchctl", "load", str(LAUNCHAGENT_PLIST)], capture_output=True)
    return r.returncode == 0


def deploy_systemd() -> bool:
    SYSTEMD_SERVICE.parent.mkdir(parents=True, exist_ok=True)
    content = SYSTEMD_CONTENT.format(
        guard_script=GUARD_SCRIPT,
        lib_dir=LIB_DIR,
    )
    try:
        SYSTEMD_SERVICE.write_text(content)
    except Exception as e:
        print(f"  [ERROR] 写 systemd service 失败: {e}")
        return False

    run(["systemctl", "--user", "daemon-reload"], capture_output=True)
    run(["systemctl", "--user", "enable", "openclaw-heartbeat-guard"], capture_output=True)
    r = run(["systemctl", "--user", "start", "openclaw-heartbeat-guard"], capture_output=True)
    return r.returncode == 0


def get_guard_pid() -> Optional[int]:
    """Find PID of running heartbeat-guard.py process."""
    try:
        r = run(["pgrep", "-f", "heartbeat-guard.py"], capture_output=True, text=True)
        if r.returncode == 0:
            pids = [int(x) for x in r.stdout.strip().splitlines() if x.strip()]
            return pids[0] if pids else None
    except Exception:
        pass
    return None


def is_launchagent_loaded() -> bool:
    try:
        r = run(["launchctl", "list", LAUNCHAGENT_LABEL], capture_output=True, text=True)
        return r.returncode == 0
    except Exception:
        return False


def unload_launchagent() -> bool:
    if not LAUNCHAGENT_PLIST.exists():
        return True
    r = run(["launchctl", "unload", str(LAUNCHAGENT_PLIST)], capture_output=True)
    return r.returncode == 0


def stop_systemd() -> bool:
    try:
        run(["systemctl", "--user", "stop", "openclaw-heartbeat-guard"], capture_output=True)
        run(["systemctl", "--user", "disable", "openclaw-heartbeat-guard"], capture_output=True)
        return True
    except Exception:
        return False


# ── commands ───────────────────────────────────────────────────────────────────

def cmd_setup(model_id: str):
    print()
    _hr()
    print(f"  heartbeat-ollama-guard v{SKILL_VERSION} — 安装向导")
    _hr()

    # Step 1: detect ollama
    _step(1, "检测 Ollama")
    ollama_bin = find_ollama()
    if not ollama_bin:
        _err("Ollama 未安装")
        print()
        print("  请先安装 Ollama：")
        print("    macOS:  brew install ollama")
        print("            或访问 https://ollama.com 下载")
        print("    Linux:  curl -fsSL https://ollama.com/install.sh | sh")
        print()
        print("  安装完成后，重新运行：")
        print("    python3 heartbeat_ollama_guard.py --setup")
        sys.exit(1)
    ver = get_ollama_version(ollama_bin)
    _ok(f"已安装 Ollama ({ver})")
    _info(f"路径: {ollama_bin}")

    # Step 2: check/pull model
    _step(2, f"检测目标模型 ({model_id})")
    if model_is_pulled(ollama_bin, model_id):
        _ok(f"{model_id} 已存在")
    else:
        _warn(f"{model_id} 尚未拉取，开始下载…")
        if pull_model(ollama_bin, model_id):
            _ok(f"{model_id} 拉取完成")
        else:
            _err(f"拉取失败，请手动执行: ollama pull {model_id}")
            _warn("继续安装守卫，但 heartbeat 在模型可用前可能出错")

    # Step 3: discover openclaw instances
    _step(3, "发现 OpenClaw 配置实例")
    instances = discover_instances()
    if not instances:
        _err("未找到任何 openclaw.json，请确认 OpenClaw 已安装")
        sys.exit(1)
    for p in instances:
        _info(f"{p}")
    print()
    answer = input("  以上实例全部配置？[Y/n] ").strip().lower()
    if answer in ("n", "no"):
        selected = []
        for p in instances:
            a = input(f"  配置 {p}？[Y/n] ").strip().lower()
            if a not in ("n", "no"):
                selected.append(p)
        instances = selected
    if not instances:
        print("  未选择任何实例，退出。")
        sys.exit(0)

    # Step 4: patch openclaw.json
    _step(4, "配置 openclaw.json")
    patched = []
    skipped = []
    for p in instances:
        did_write = patch_openclaw_json(p, model_id)
        if did_write:
            _ok(f"已写入 {p.parent.name}/openclaw.json")
            patched.append(p)
        else:
            current = get_nested(load_json(p) or {}, HEARTBEAT_PATH)
            if current == f"{OPENCLAW_PROVIDER_KEY}/{model_id}":
                _ok(f"已是目标值，跳过 {p.parent.name}/openclaw.json")
            else:
                _warn(f"写入失败或跳过 {p}")
            skipped.append(p)

    # Step 5: write guard files
    _step(5, "生成并部署守卫")
    existing_ver = get_guard_version()
    if existing_ver:
        if existing_ver == GUARD_VERSION:
            _ok(f"守卫脚本已是最新版 v{GUARD_VERSION}，跳过重写")
        else:
            _info(f"升级守卫脚本 v{existing_ver} → v{GUARD_VERSION}")
            write_guard_script() and _ok("守卫脚本已更新") or _err("守卫脚本写入失败")
    else:
        if write_guard_script():
            _ok("守卫脚本已写入")
        else:
            _err("守卫脚本写入失败")
            sys.exit(1)

    # update conf.json
    if update_conf(instances, model_id):
        _ok(f"守卫配置已更新 ({GUARD_CONF.name})")
    else:
        _err("守卫配置写入失败")

    # deploy daemon
    if is_macos():
        if deploy_launchagent():
            _ok(f"LaunchAgent 已加载 ({LAUNCHAGENT_LABEL})")
        else:
            _err("LaunchAgent 加载失败，请检查 plist 文件")
    elif is_linux():
        if deploy_systemd():
            _ok("systemd 服务已启动 (openclaw-heartbeat-guard)")
        else:
            _err("systemd 服务启动失败")
    else:
        _warn("不支持的平台，守卫守护进程未自动部署")
        _info(f"可手动运行: python3 {GUARD_SCRIPT}")

    # Step 6: verify
    _step(6, "验证")
    time.sleep(2)  # give daemon a moment to start
    pid = get_guard_pid()
    if pid:
        _ok(f"守卫进程运行中 (PID {pid})")
    else:
        _warn("守卫进程未检测到（可能需要几秒启动）")

    # run single check
    try:
        r = run(["python3", str(GUARD_SCRIPT), "--check"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            _ok("单次检查通过")
        else:
            _warn("单次检查返回非零，请查看日志")
    except Exception as e:
        _warn(f"单次检查执行异常: {e}")

    # Step 7: restart reminder
    _step(7, "提示重启 gateway")
    print()
    print("  ⚡ 请运行: openclaw gateway restart")
    print()

    # summary
    _hr()
    print("  安装完成！")
    print(f"  模型:   local/{model_id}")
    print(f"  守卫:   {GUARD_SCRIPT}")
    print(f"  配置:   {GUARD_CONF}")
    if is_macos():
        print(f"  Plist:  {LAUNCHAGENT_PLIST}")
    _hr()
    print()


def cmd_status(model_id: str):
    print()
    _hr()
    print(f"  heartbeat-ollama-guard 状态报告")
    _hr()

    # Ollama
    ollama_bin = find_ollama()
    if ollama_bin:
        ver = get_ollama_version(ollama_bin)
        _ok(f"Ollama 已安装 ({ver})")
    else:
        _err("Ollama 未安装")

    # model
    if ollama_bin:
        if model_is_pulled(ollama_bin, model_id):
            _ok(f"本地模型: {model_id} (已拉取)")
        else:
            _warn(f"本地模型: {model_id} (未拉取)")
    else:
        _warn(f"本地模型: {model_id} (无法检测，Ollama 未安装)")

    # guard process
    pid = get_guard_pid()
    if pid:
        _ok(f"守卫进程: 运行中 (PID {pid})")
    else:
        _err("守卫进程: 未运行")

    # launchagent / systemd
    if is_macos():
        if is_launchagent_loaded():
            _ok(f"LaunchAgent: 已加载 ({LAUNCHAGENT_LABEL})")
        else:
            _warn(f"LaunchAgent: 未加载")
    elif is_linux():
        try:
            r = run(["systemctl", "--user", "is-active", "openclaw-heartbeat-guard"],
                    capture_output=True, text=True)
            if r.stdout.strip() == "active":
                _ok("systemd 服务: 运行中")
            else:
                _warn(f"systemd 服务: {r.stdout.strip()}")
        except Exception:
            _warn("systemd 服务: 无法检测")

    # instances
    print()
    print("  配置实例:")
    conf = load_conf()
    protected = conf.get("protected", {})
    if not protected:
        _warn("conf.json 为空或不存在")
    else:
        for cfg_path_str, rule in protected.items():
            cfg_path = Path(cfg_path_str)
            expected = rule.get("expected")
            dot_path = rule.get("path", "")
            print(f"    {cfg_path}")
            if cfg_path.exists():
                data = load_json(cfg_path)
                actual = get_nested(data or {}, dot_path)
                if actual == expected:
                    print(f"      {dot_path}: {actual}  ✅ 符合授权")
                else:
                    print(f"      {dot_path}: {actual!r}  ❌ 期望 {expected!r}")
            else:
                print(f"      ⚠️  文件不存在")

    print()
    _hr()
    print()


def cmd_check():
    if not GUARD_SCRIPT.exists():
        print("守卫脚本不存在，请先运行 --setup")
        sys.exit(1)
    r = run(["python3", str(GUARD_SCRIPT), "--check"])
    sys.exit(r.returncode)


def cmd_uninstall():
    print()
    _hr()
    print("  heartbeat-ollama-guard — 卸载")
    _hr()

    answer = input("  确认卸载守卫？配置文件和 openclaw.json 不会被还原。[y/N] ").strip().lower()
    if answer not in ("y", "yes"):
        print("  已取消。")
        return

    if is_macos():
        if unload_launchagent():
            _ok("LaunchAgent 已卸载")
        LAUNCHAGENT_PLIST.unlink(missing_ok=True)
        _ok("plist 文件已删除")
    elif is_linux():
        stop_systemd()
        SYSTEMD_SERVICE.unlink(missing_ok=True)
        _ok("systemd service 已停止并删除")

    GUARD_SCRIPT.unlink(missing_ok=True)
    _ok("守卫脚本已删除")

    GUARD_CONF.unlink(missing_ok=True)
    _ok("守卫配置已删除")

    print()
    print("  卸载完成。备份文件保留于:")
    print(f"    {GUARD_BACKUP_DIR}")
    print()
    _hr()
    print()


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="heartbeat-ollama-guard: 将 OpenClaw 心跳切换为本地 Ollama 并部署守卫",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 heartbeat_ollama_guard.py --setup
  python3 heartbeat_ollama_guard.py --setup --model llama3:8b
  python3 heartbeat_ollama_guard.py --status
  python3 heartbeat_ollama_guard.py --check
  python3 heartbeat_ollama_guard.py --uninstall
"""
    )
    parser.add_argument("--setup",     action="store_true", help="完整安装向导")
    parser.add_argument("--status",    action="store_true", help="显示当前状态")
    parser.add_argument("--check",     action="store_true", help="单次守卫检查")
    parser.add_argument("--uninstall", action="store_true", help="卸载守卫")
    parser.add_argument("--model", default=DEFAULT_MODEL,   help=f"本地模型 ID（默认 {DEFAULT_MODEL}）")

    args = parser.parse_args()

    if args.setup:
        cmd_setup(args.model)
    elif args.status:
        cmd_status(args.model)
    elif args.check:
        cmd_check()
    elif args.uninstall:
        cmd_uninstall()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
