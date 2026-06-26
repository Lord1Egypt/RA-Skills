#!/usr/bin/env python3
"""
PansXNG Websearch - 自包含的本地元搜索引擎技能
自动检测、安装、启动 SearXNG，无需手动配置
"""
import sys
import json
import argparse
import subprocess
import os
import time

# ─── 配置 ───
SEARXNG_URL = "http://127.0.0.1:8888"
SEARXNG_DIR = os.path.expanduser("~/Downloads/searxng")
SEARXNG_LOG = "/tmp/searxng.log"
BREW = "/opt/homebrew/bin/brew"
PYTHON3_11 = "/opt/homebrew/bin/python3.11"


# ═══════════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════════

def _run(cmd, timeout=120, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)


def _popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw):
    return subprocess.Popen(cmd, stdout=stdout, stderr=stderr, **kw)


# ═══════════════════════════════════════════════════════════════
#  Homebrew 自动安装
# ═══════════════════════════════════════════════════════════════

def is_homebrew_available():
    return os.path.isfile(BREW)


def install_homebrew():
    """自动安装 Homebrew（若缺失）"""
    if is_homebrew_available():
        return True, "Homebrew 已在"
    print("📦 检测到 Homebrew 未安装，正在自动安装...", flush=True)
    try:
        r = _run(
            ['/bin/bash', '-c',
             'NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL '
             'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'],
            timeout=300
        )
        if r.returncode != 0:
            return False, ("Homebrew 安装失败，请手动运行：\n"
                           "  /bin/bash -c \"$(curl -fsSL "
                           "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        # 写入 PATH 到 shell rc
        shell_rc = os.path.expanduser("~/.zshrc")
        path_line = 'eval "$(/opt/homebrew/bin/brew shellenv)"'
        if not os.path.exists(shell_rc) or path_line not in open(shell_rc).read():
            with open(shell_rc, "a") as f:
                f.write("\n" + path_line + "\n")
        return True, "Homebrew 安装完成"
    except subprocess.TimeoutExpired:
        return False, "Homebrew 安装超时"
    except Exception as e:
        return False, f"Homebrew 安装异常: {e}"


# ═══════════════════════════════════════════════════════════════
#  Python 3.11 自动安装
# ═══════════════════════════════════════════════════════════════

def is_python311_available():
    return os.path.isfile(PYTHON3_11)


def install_python311():
    """自动安装 Python 3.11"""
    if is_python311_available():
        return True, "Python 3.11 已在"

    print("📦 安装 Python 3.11（通过 Homebrew）...", flush=True)
    ok, msg = install_homebrew()
    if not ok:
        return False, msg

    try:
        r = _run([BREW, "install", "python@3.11", "--quiet"], timeout=300)
        if r.returncode != 0:
            r2 = _run([BREW, "list", "python@3.11"])
            if r2.returncode != 0:
                return False, (f"Python 3.11 安装失败:\n{r.stderr}\n\n"
                               "可手动运行: brew install python@3.11")
        _run([PYTHON3_11, "-m", "pip", "--version"], timeout=10)
        return True, "Python 3.11 安装完成"
    except subprocess.TimeoutExpired:
        return False, "Python 3.11 安装超时"
    except Exception as e:
        return False, f"Python 3.11 安装异常: {e}"


# ═══════════════════════════════════════════════════════════════
#  Valkey 自动安装 + 启动
# ═══════════════════════════════════════════════════════════════

def _valkey_paths():
    """遍历查找 valkey-server / valkey-cli 路径"""
    names = ["valkey-server", "valkey-cli"]
    prefixes = [
        "/opt/homebrew/opt/valkey/bin",
        "/usr/local/opt/valkey/bin",
        "/opt/homebrew/bin",
        "/usr/local/bin",
    ]
    for prefix in prefixes:
        for name in names:
            p = os.path.join(prefix, name)
            if os.path.isfile(p):
                yield name.replace("valkey-", ""), p


def is_valkey_running():
    # 方法1：valkey-cli ping
    for _, cli in _valkey_paths():
        if "cli" not in cli:
            continue
        try:
            r = _run([cli, "ping"], timeout=3)
            if "PONG" in r.stdout:
                return True
        except Exception:
            pass
    # 方法2：进程检查
    try:
        r = _run(["pgrep", "-f", "valkey"], timeout=5)
        return r.returncode == 0
    except Exception:
        pass
    return False


def _start_valkey_daemon(server_bin):
    """启动 valkey-server 为守护进程（端口 56379）"""
    try:
        _popen([server_bin, "--port", "56379", "--save", "", "--daemonize", "yes"])
        for _ in range(12):
            time.sleep(0.5)
            if is_valkey_running():
                return True
    except Exception:
        pass
    return False


def start_valkey():
    """自动安装 + 启动 Valkey"""
    if is_valkey_running():
        return True

    print("📦 安装 Valkey（通过 Homebrew）...", flush=True)
    ok, msg = install_homebrew()
    if not ok:
        return False

    # 安装 valkey
    try:
        r = _run([BREW, "install", "valkey", "--quiet"], timeout=180)
        if r.returncode != 0:
            r2 = _run([BREW, "list", "valkey"])
            if r2.returncode != 0:
                print(f"⚠️ Valkey 安装失败: {r.stderr[:200]}", file=sys.stderr)
                return False
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        pass

    # 启动
    for _, server_bin in _valkey_paths():
        if "server" in server_bin:
            return _start_valkey_daemon(server_bin)

    # 完全找不到
    return False


# ═══════════════════════════════════════════════════════════════
#  SearXNG 生命周期管理
# ═══════════════════════════════════════════════════════════════

def is_searxng_running():
    try:
        r = _run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                  "--max-time", "3", f"{SEARXNG_URL}/"], timeout=5)
        return r.stdout.strip().startswith("2")
    except Exception:
        return False


def is_searxng_installed():
    return os.path.isfile(os.path.join(SEARXNG_DIR, "searx", "webapp.py"))


def install_searxng():
    """一键安装 SearXNG（自动安装 Python 3.11）"""
    # 0. Python 3.11
    if not is_python311_available():
        ok, msg = install_python311()
        if not ok:
            return False, f"Python 3.11 不可用: {msg}"
        if not is_python311_available():
            return False, "Python 3.11 安装后仍不可用，请检查 Homebrew PATH"

    # 1. Clone
    if not is_searxng_installed():
        print(f"📦 克隆 SearXNG 到 {SEARXNG_DIR}...", flush=True)
        try:
            r = _run(
                ["git", "clone", "--depth", "1",
                 "https://github.com/searxng/searxng.git", SEARXNG_DIR],
                timeout=180
            )
            if r.returncode != 0:
                return False, f"克隆失败: {r.stderr}"
        except subprocess.TimeoutExpired:
            return False, "克隆超时（网络慢）"
        except Exception as e:
            return False, f"克隆异常: {e}"

        if not is_searxng_installed():
            return False, "克隆后找不到 searx/webapp.py"

    # 2. Python 依赖
    req_file = os.path.join(SEARXNG_DIR, "requirements.txt")
    if os.path.isfile(req_file):
        print("📦 安装 SearXNG Python 依赖...", flush=True)
        # 确保 pyyaml
        try:
            import yaml
        except ImportError:
            _run([PYTHON3_11, "-m", "pip", "install", "-q", "pyyaml"], timeout=30)
        try:
            _run(
                [PYTHON3_11, "-m", "pip", "install", "-q",
                 "-r", req_file, "--quiet", "--disable-pip-version-check"],
                timeout=180
            )
        except subprocess.TimeoutExpired:
            print("⚠️ 依赖安装超时，继续尝试...", flush=True)
        except Exception:
            pass

    # 3. 配置
    configure_searxng()
    return True, "SearXNG 已安装"


def configure_searxng():
    """配置 SearXNG：启用 JSON API + 国内引擎"""
    settings_path = os.path.join(SEARXNG_DIR, "searx", "settings.yml")
    if not os.path.isfile(settings_path):
        return False
    try:
        import yaml
    except ImportError:
        try:
            _run([PYTHON3_11, "-m", "pip", "install", "-q", "pyyaml"], timeout=30)
            import yaml
        except Exception:
            _run(["sed", "-i", "", "s/ultrasecretkey/pans-searxng-2024/",
                 settings_path], timeout=5)
            return True
    try:
        with open(settings_path, "r") as f:
            data = yaml.safe_load(f)
        data.setdefault("server", {})["secret_key"] = "pans-searxng-2024"
        data.setdefault("search", {})["formats"] = ["html", "json", "csv", "rss"]
        # 启用国内引擎
        enabled = ["baidu", "sogou", "360search", "bing", "duckduckgo", "google"]
        for engine in data.get("engines", []):
            name = engine.get("name", "").lower()
            eng = engine.get("engine", "").lower()
            for target in enabled:
                if target in name or target in eng:
                    if engine.get("disabled", False):
                        engine["disabled"] = False
        with open(settings_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        return True
    except Exception:
        return False


def start_searxng():
    """启动 SearXNG（含全部依赖自动安装）"""
    if is_searxng_running():
        return True, "SearXNG 已在运行"

    if not is_searxng_installed():
        ok, msg = install_searxng()
        if not ok:
            return False, f"安装失败: {msg}"

    if not start_valkey():
        print("⚠️ Valkey 未启动，限流功能不可用（不影响基本搜索）", file=sys.stderr)

    configure_searxng()

    try:
        log_f = open(SEARXNG_LOG, "a")
        _popen(
            [PYTHON3_11, "-m", "searx.webapp",
             "--host", "127.0.0.1", "--port", "8888"],
            cwd=SEARXNG_DIR, stdout=log_f, stderr=subprocess.STDOUT
        )
        print("🚀 启动 SearXNG 中（首次约需 10-15 秒）...", flush=True)
        for i in range(20):
            time.sleep(1)
            if is_searxng_running():
                return True, "SearXNG 启动成功"
        return False, "启动超时（20s），日志: " + SEARXNG_LOG
    except Exception as e:
        return False, f"启动异常: {e}"


def stop_searxng():
    _run(["pkill", "-f", "searx.webapp"])
    return True, "SearXNG 已停止"


# ═══════════════════════════════════════════════════════════════
#  搜索功能
# ═══════════════════════════════════════════════════════════════

def search(query, lang="zh-CN", engines=None, categories=None):
    """调用 SearXNG JSON API"""
    if not is_searxng_running():
        ok, msg = start_searxng()
        if not ok:
            return {"error": f"SearXNG 不可用: {msg}", "fallback": True}

    params = [("q", query), ("format", "json"), ("lang", lang)]
    if engines:
        params.append(("engines", engines))
    if categories:
        params.append(("categories", categories))

    cmd = ["curl", "-s", "--max-time", "30", f"{SEARXNG_URL}/search"]
    for k, v in params:
        cmd += ["--data-urlencode", f"{k}={v}"]

    try:
        result = _run(cmd, timeout=35)
        if result.returncode != 0:
            return {"error": f"请求失败: {result.stderr}", "fallback": True}
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raw = result.stdout[:500] if result.stdout else ""
        return {"error": "JSON 解析失败", "raw": raw, "fallback": True}
    except subprocess.TimeoutExpired:
        return {"error": "搜索超时 (30s)", "fallback": True}
    except Exception as e:
        return {"error": str(e), "fallback": True}


def format_results(data, count=10):
    if "error" in data:
        fb = "（已回退到内置搜索）" if data.get("fallback") else ""
        return f"❌ 搜索错误{fb}: {data['error']}"

    results = data.get("results", [])
    query = data.get("query", "")
    total = data.get("number_of_results", 0)

    if not results:
        unresp = data.get("unresponsive_engines", [])
        if unresp:
            names = ", ".join([str(e[0]) for e in unresp[:5]])
            return (f"⚠️「{query}」无结果\n"
                    f"💡 未响应引擎: {names}\n"
                    f"   建议用 -e baidu 指定国内引擎")
        return f"⚠️「{query}」无结果"

    lines = [f"🔍「{query}」约 {total} 个结果：\n"]
    for i, r in enumerate(results[:count], 1):
        title = r.get("title", "").strip()
        url = r.get("url", "").strip()
        content = r.get("content", "").strip()[:200]
        engine = r.get("engine", "")
        lines.append(f"  {i}. {title}")
        lines.append(f"     🔗 {url}")
        if content:
            lines.append(f"     {content}")
        if engine:
            lines.append(f"     📌 {engine}")
        lines.append("")

    unresp = data.get("unresponsive_engines", [])
    if unresp:
        names = ", ".join([str(e[0]) for e in unresp[:3]])
        lines.append(f"  ⚠️ 部分引擎超时: {names}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  状态报告
# ═══════════════════════════════════════════════════════════════

def status():
    brew_ok = is_homebrew_available()
    py_ok = is_python311_available()
    v_ok = is_valkey_running()
    sx_ok = is_searxng_running()
    sx_inst = is_searxng_installed()

    lines = ["📋 PansXNG 完整状态："]
    lines.append(f"  Homebrew:    {'✅' if brew_ok else '❌ → 首次搜索时自动安装'}")
    lines.append(f"  Python 3.11: {'✅' if py_ok else '❌ → 首次搜索时自动安装'}")
    lines.append(f"  Valkey:      {'✅' if v_ok else '❌ → 首次搜索时自动安装'}")
    lines.append(f"  SearXNG 安装: {'✅' if sx_inst else '❌ → 首次搜索时自动安装'}")
    lines.append(f"  SearXNG 运行: {'✅' if sx_ok else '❌'}")
    lines.append(f"\n  SearXNG 地址: {SEARXNG_URL}")
    if sx_inst:
        lines.append(f"  安装目录: {SEARXNG_DIR}")
    lines.append(f"  日志: {SEARXNG_LOG}")

    if not (brew_ok and py_ok and v_ok and sx_inst):
        lines.append("\n  💡 首次搜索时所有依赖将自动安装完成")
    elif not sx_ok:
        lines.append("\n  💡 搜索时将自动启动 SearXNG")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="PansXNG - 自包含元搜索引擎（自动安装一切依赖）")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("--lang", "-l", default="zh-CN")
    parser.add_argument("--count", "-n", type=int, default=10)
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--engines", "-e", default=None)
    parser.add_argument("--categories", "-c", default=None)
    parser.add_argument("--status", "-s", action="store_true")
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--stop", action="store_true")
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    if args.status:
        print(status()); return
    if args.install:
        ok, msg = install_searxng(); print(f"{'✅' if ok else '❌'} {msg}"); return
    if args.start:
        ok, msg = start_searxng(); print(f"{'✅' if ok else '❌'} {msg}"); return
    if args.stop:
        ok, msg = stop_searxng(); print(f"{'✅' if ok else '❌'} {msg}"); return
    if not args.query:
        parser.print_help(); return

    data = search(args.query, lang=args.lang,
                  engines=args.engines, categories=args.categories)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_results(data, args.count))


if __name__ == "__main__":
    main()
