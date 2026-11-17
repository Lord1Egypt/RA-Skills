"""唯一通知管线（P0-3 / P0-7 / P0-8）。

收敛所有「组装消息 → 发送 → 重试 → 去重 → 记录状态」逻辑：
  - 通知器列表全部来自 config.yaml（增删渠道/收件人只改配置，零代码改动）
  - 消息经 stdin 或命令参数传入（可配置）
  - 退出码 0 且 stdout 含 success_marker 才算成功（可配置判定）
  - 默认超时 >=90s（本地 CLI 发送器冷启动可能 >40s，过短会误判失败）
  - 带重试与退避；失败不静默丢弃（由调用方决定保留 pending 重试）
  - 内容 hash 去重（记录最近已发送内容指纹，相同则跳过）
"""

import hashlib
import json
import os
import subprocess
import time

from . import paths, atomic, log


def _as_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def load_notifiers(cfg):
    """返回启用的通知器列表。"""
    out = []
    for n in cfg.get("notifiers", []) or []:
        if not isinstance(n, dict):
            continue
        if n.get("enabled", True):
            out.append(n)
    return out


def build_argv(notifier, message, extra_args):
    """把 notifier 配置组装成 argv 列表（相对路径解析到技能根目录）。

    若目标文件存在但不可执行，则用 `sh` 兜底运行（兼容未加执行位/从 git 拉取的情况）。
    """
    cmd = notifier.get("command", "")
    resolved = paths.resolve(cmd) if cmd else None
    argv = []
    if resolved is not None and resolved.exists():
        if os.access(resolved, os.X_OK):
            argv = [str(resolved)]
        else:
            argv = ["sh", str(resolved)]
    elif cmd:
        argv = [cmd]
    for a in (notifier.get("args", []) or []):
        argv.append(str(a).replace("{message}", message))
    argv.extend([str(x) for x in (extra_args or [])])
    return argv


def run_notifier(notifier, message, extra_args, cfg, dry_run=False):
    """执行单个通知器。返回 (success, stdout, stderr)。"""
    if dry_run:
        return True, "[dry-run] 未实际发送", ""

    argv = build_argv(notifier, message, extra_args)
    if not argv:
        return False, "", "notifier 缺少 command"

    use_stdin = bool(notifier.get("stdin", True))
    env = os.environ.copy()
    env["SKILL_ROOT"] = str(paths.ROOT)
    for k, v in (notifier.get("env", {}) or {}).items():
        env[str(k)] = str(v)

    timeout = _as_int(
        notifier.get("timeout_seconds"),
        _as_int(cfg.get("notification", {}).get("default_timeout_seconds"), 90),
    )
    success_marker = notifier.get("success_marker", "") or ""

    try:
        proc = subprocess.run(
            argv,
            input=message if use_stdin else None,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
            cwd=str(paths.ROOT),
        )
        ok = proc.returncode == 0
        if ok and success_marker:
            ok = success_marker in (proc.stdout or "")
        return ok, (proc.stdout or ""), (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return False, "", "超时({}s)".format(timeout)
    except Exception as e:  # noqa: BLE001
        return False, "", str(e)


def send_with_retry(notifier, message, extra_args, cfg, dry_run=False):
    """带重试与指数退避地发送。返回 (success, stdout, stderr, attempts)。"""
    retry = _as_int(
        notifier.get("retry_count"),
        _as_int(cfg.get("notification", {}).get("default_retry_count"), 0),
    )
    backoff = _as_int(cfg.get("notification", {}).get("retry_backoff_seconds"), 10)
    last = ("", "")
    for attempt in range(retry + 1):
        ok, out, err = run_notifier(notifier, message, extra_args, cfg, dry_run)
        if ok:
            return True, out, err, attempt + 1
        last = (out, err)
        if attempt < retry:
            time.sleep(backoff * (attempt + 1))
    return False, last[0], last[1], retry + 1


def dispatch(cfg, message, dry_run=False):
    """向所有启用的通知器发送消息。返回 (results, any_ok)。

    results: {notifier_name: bool}。any_ok：是否至少一个通知器送达（P0-7）。
    """
    notifiers = load_notifiers(cfg)
    results = {}
    for n in notifiers:
        name = n.get("name") or n.get("command") or "unnamed"
        ok, out, err, attempts = send_with_retry(n, message, [], cfg, dry_run)
        results[name] = ok
        log.get_logger().info(
            "notify name=%s ok=%s attempts=%d %s",
            name, ok, attempts, (err or "").strip()[:200],
        )
    any_ok = any(results.values()) if results else False
    return results, any_ok


def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _state_file():
    return paths.resolve("cache") / "notification_state.json"


def _load_state():
    f = _state_file()
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {"fingerprints": []}


def _save_state(state):
    atomic.atomic_write_json(_state_file(), state)


def is_duplicate(cfg, text):
    """内容指纹去重：相同内容已发送过则返回 True（P0-8）。"""
    limit = _as_int(cfg.get("notification", {}).get("dedup_max_fingerprints"), 0)
    if limit <= 0:
        return False
    state = _load_state()
    return fingerprint(text) in state.get("fingerprints", [])


def record_fingerprint(cfg, text):
    limit = _as_int(cfg.get("notification", {}).get("dedup_max_fingerprints"), 100)
    if limit <= 0:
        return
    state = _load_state()
    fps = state.get("fingerprints", [])
    fp = fingerprint(text)
    if fp not in fps:
        fps.append(fp)
    if len(fps) > limit:
        fps = fps[-limit:]
    state["fingerprints"] = fps
    _save_state(state)
