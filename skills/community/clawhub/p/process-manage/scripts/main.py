"""process_manage skill - 进程管理，支持 Windows 和 Linux"""
import sys
import json
import os
import time
import datetime

try:
    import psutil
except ImportError:
    print("错误: 缺少 psutil 模块，请运行: pip install psutil")
    sys.exit(1)


# 受保护的系统进程（不允许关闭）
PROTECTED_PROCESSES = {
    "System Idle Process", "System", "Registry", "smss.exe",
    "csrss.exe", "wininit.exe", "services.exe", "lsass.exe",
    "svchost.exe", "winlogon.exe", "explorer.exe",
    "init", "systemd", "kthreadd", "kworker",
}


def parse_args(arg):
    arg = arg.strip()
    if not arg:
        return {"action": "list", "sort": "mem", "limit": 20}
    if arg.startswith("{"):
        try:
            params = json.loads(arg)
            params.setdefault("action", "list")
            params.setdefault("sort", "mem")
            params.setdefault("limit", 20)
            return params
        except json.JSONDecodeError as e:
            return {"error": f"JSON 参数解析失败: {e}"}
    return {"action": arg, "sort": "mem", "limit": 20}


def format_bytes(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)}秒"
    elif seconds < 3600:
        return f"{int(seconds/60)}分{int(seconds%60)}秒"
    elif seconds < 86400:
        return f"{int(seconds/3600)}时{int((seconds%3600)/60)}分"
    else:
        return f"{int(seconds/86400)}天{int((seconds%86400)/3600)}时"


def is_protected(proc_name):
    name_lower = proc_name.lower()
    for p in PROTECTED_PROCESSES:
        if name_lower == p.lower():
            return True
    # 内核线程
    if name_lower.startswith("kworker") or name_lower.startswith("kthread"):
        return True
    return False


def list_processes(sort_by="mem", limit=20):
    procs = []
    for p in psutil.process_iter(["pid", "name", "username", "memory_percent",
                                   "cpu_percent", "create_time", "status"]):
        try:
            info = p.info
            info["memory_bytes"] = p.memory_info().rss if p.is_running() else 0
            procs.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # 排序
    if sort_by == "cpu":
        procs.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)
    elif sort_by == "mem":
        procs.sort(key=lambda x: x.get("memory_bytes", 0), reverse=True)
    elif sort_by == "pid":
        procs.sort(key=lambda x: x.get("pid", 0))
    elif sort_by == "name":
        procs.sort(key=lambda x: x.get("name", "").lower())

    procs = procs[:limit]

    result = [f"📋 进程列表 (按 {sort_by} 排序, 前 {limit} 个)", "=" * 80,
              f"{'PID':>8}  {'CPU%':>6}  {'内存':>10}  {'内存%':>6}  {'状态':<10}  {'名称':<30}  {'用户'}",
              "-" * 80]

    for p in procs:
        pid = p.get("pid", 0)
        name = p.get("name", "?") or "?"
        cpu = p.get("cpu_percent", 0) or 0
        mem_pct = p.get("memory_percent", 0) or 0
        mem_bytes = p.get("memory_bytes", 0)
        status = p.get("status", "?") or "?"
        user = p.get("username", "?") or "?"
        if len(user) > 20:
            user = user[:17] + "..."

        result.append(f"{pid:>8}  {cpu:>5.1f}%  {format_bytes(mem_bytes):>10}  {mem_pct:>5.1f}%  {status:<10}  {name[:30]:<30}  {user}")

    result.append(f"\n总进程数: {len(psutil.pids())}")
    return "\n".join(result)


def find_processes(name):
    name_lower = name.lower()
    found = []
    for p in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent", "cmdline"]):
        try:
            info = p.info
            pname = (info.get("name") or "").lower()
            cmdline = " ".join(info.get("cmdline") or []).lower()
            if name_lower in pname or name_lower in cmdline:
                info["memory_bytes"] = p.memory_info().rss
                found.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not found:
        return f"未找到匹配 '{name}' 的进程"

    result = [f"🔍 找到 {len(found)} 个匹配 '{name}' 的进程", "=" * 80]
    for p in found:
        result.append(f"PID: {p.get('pid')} | {p.get('name')} | CPU: {p.get('cpu_percent', 0):.1f}% | 内存: {format_bytes(p.get('memory_bytes', 0))}")
        cmdline = p.get("cmdline")
        if cmdline:
            result.append(f"  命令: {' '.join(cmdline)[:200]}")
    return "\n".join(result)


def process_info(pid):
    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return f"进程不存在: PID {pid}"
    except psutil.AccessDenied:
        return f"权限不足: PID {pid}"

    try:
        info = {
            "pid": p.pid,
            "name": p.name(),
            "exe": p.exe() if hasattr(p, "exe") else "",
            "cmdline": p.cmdline(),
            "cwd": p.cwd() if hasattr(p, "cwd") else "",
            "username": p.username(),
            "status": p.status(),
            "create_time": datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_percent": p.cpu_percent(interval=0.5),
            "memory_percent": p.memory_percent(),
            "memory_bytes": p.memory_info().rss,
            "num_threads": p.num_threads(),
            "num_fds": p.num_fds() if hasattr(p, "num_fds") else "N/A",
        }

        # 父进程
        try:
            parent = p.parent()
            if parent:
                info["parent"] = f"{parent.pid} ({parent.name()})"
        except Exception:
            pass

        # 子进程
        try:
            children = p.children()
            info["children"] = len(children)
        except Exception:
            info["children"] = 0

        # 网络
        try:
            conns = p.connections()
            info["connections"] = len(conns)
        except Exception:
            info["connections"] = "N/A"

    except psutil.NoSuchProcess:
        return f"进程已退出: PID {pid}"
    except psutil.AccessDenied:
        return f"权限不足: PID {pid}"

    result = [f"📋 进程详情 (PID: {pid})", "=" * 60]
    result.append(f"名称: {info['name']}")
    result.append(f"状态: {info['status']}")
    result.append(f"用户: {info['username']}")
    result.append(f"创建时间: {info['create_time']}")
    result.append(f"CPU 占用: {info['cpu_percent']:.1f}%")
    result.append(f"内存: {format_bytes(info['memory_bytes'])} ({info['memory_percent']:.1f}%)")
    result.append(f"线程数: {info['num_threads']}")
    result.append(f"文件描述符: {info['num_fds']}")
    result.append(f"子进程数: {info['children']}")
    result.append(f"网络连接数: {info['connections']}")
    if "parent" in info:
        result.append(f"父进程: {info['parent']}")
    if info["exe"]:
        result.append(f"可执行文件: {info['exe']}")
    if info["cmdline"]:
        result.append(f"命令行: {' '.join(info['cmdline'])[:300]}")
    if info["cwd"]:
        result.append(f"工作目录: {info['cwd']}")

    return "\n".join(result)


def kill_process(pid, force=False):
    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return f"进程不存在: PID {pid}"
    except psutil.AccessDenied:
        return f"权限不足: PID {pid}"

    name = p.name()

    # 保护系统关键进程
    if is_protected(name):
        return f"❌ 拒绝关闭受保护的系统进程: {name} (PID: {pid})"

    try:
        if force:
            p.kill()
        else:
            p.terminate()
        # 等待退出
        try:
            p.wait(timeout=5)
            return f"✅ 已{'强制' if force else '优雅'}关闭进程: {name} (PID: {pid})"
        except psutil.TimeoutExpired:
            if not force:
                # 优雅关闭失败，提示强制
                return f"⚠️ 进程未响应优雅关闭: {name} (PID: {pid})，请使用 force:true 强制关闭"
            return f"⚠️ 强制关闭超时: {name} (PID: {pid})"
    except psutil.AccessDenied:
        return f"❌ 权限不足，无法关闭: {name} (PID: {pid})。请使用管理员/root 权限运行"
    except Exception as e:
        return f"❌ 关闭失败: {e}"


def kill_by_name(name, force=False):
    name_lower = name.lower()
    killed = []
    failed = []

    for p in psutil.process_iter(["pid", "name"]):
        try:
            info = p.info
            pname = (info.get("name") or "").lower()
            if name_lower in pname:
                if is_protected(pname):
                    failed.append(f"{info.get('name')} (PID: {info.get('pid')}) - 受保护")
                    continue
                try:
                    proc = psutil.Process(info["pid"])
                    if force:
                        proc.kill()
                    else:
                        proc.terminate()
                    killed.append(f"{info.get('name')} (PID: {info.get('pid')})")
                except Exception as e:
                    failed.append(f"{info.get('name')} (PID: {info.get('pid')}) - {e}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # 等待
    time.sleep(1)

    result = []
    if killed:
        result.append(f"✅ 已关闭 {len(killed)} 个进程:")
        for k in killed:
            result.append(f"  - {k}")
    if failed:
        result.append(f"❌ 失败 {len(failed)} 个:")
        for f in failed:
            result.append(f"  - {f}")
    if not killed and not failed:
        result.append(f"未找到匹配 '{name}' 的进程")

    return "\n".join(result)


def manage(params):
    if "error" in params:
        return params["error"]

    action = params.get("action", "list")

    if action == "list":
        return list_processes(params.get("sort", "mem"), params.get("limit", 20))
    elif action == "find":
        name = params.get("name", "")
        if not name:
            return "错误: find 操作需要 name 参数"
        return find_processes(name)
    elif action == "info":
        pid = params.get("pid", 0)
        if not pid:
            return "错误: info 操作需要 pid 参数"
        return process_info(int(pid))
    elif action == "kill":
        pid = params.get("pid", 0)
        if not pid:
            return "错误: kill 操作需要 pid 参数"
        return kill_process(int(pid), params.get("force", False))
    elif action == "kill_name":
        name = params.get("name", "")
        if not name:
            return "错误: kill_name 操作需要 name 参数"
        return kill_by_name(name, params.get("force", False))
    else:
        return f"未知操作: {action}。支持: list/find/info/kill/kill_name"


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    params = parse_args(arg)
    print(manage(params))
