#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量级主机入侵检测与日志分析系统（Mini-HIDS）
版本：v1.5
功能：实时监控系统日志，检测暴力破解和 Webshell，自动封禁恶意 IP
定位：后台守护进程，负责 7x24 小时底层监控与自动防御
"""

import os
import re
import threading
import time
from collections import deque

from hids_common import (
    FirewallManager,
    delete_blacklist_entry,
    execute_ban,
    execute_unban,
    extract_client_ip,
    init_db,
    list_blacklist_rows,
    load_config,
    purge_expired_blacklist_entries,
    scan_web_roots,
    validate_ip,
)


CONFIG = load_config()
FIREWALL = FirewallManager(CONFIG.get("FIREWALL_BACKEND"))

WEB_ATTACK_PATTERNS = [
    r"' OR\s+",
    r"UNION\s+SELECT",
    r"<script>",
    r"javascript:",
    r"\.\./",
]
COMPILED_WEB_ATTACK_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in WEB_ATTACK_PATTERNS]

SSH_FAILURE_PATTERN = re.compile(r"Failed password for .* from (\S+)")

state_lock = threading.RLock()
ban_times = {}
blacklist = set()
ip_failures = {}
file_modification_times = {}


def log_alert(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    alert_message = f"[{timestamp}] {message}\n"
    print(alert_message, end="")

    with open(CONFIG["ALERT_LOG"], "a", encoding="utf-8") as alert_file:
        alert_file.write(alert_message)


def is_trusted_ip(ip):
    return ip in CONFIG["TRUSTED_IPS"]


def setup_environment():
    init_db(CONFIG["BLACKLIST_DB"])
    os.makedirs(os.path.dirname(CONFIG["ALERT_LOG"]) or ".", exist_ok=True)
    os.makedirs("logs", mode=0o755, exist_ok=True)
    load_runtime_state()


def load_runtime_state():
    current_time = int(time.time())
    active_bans = {}
    active_blacklist = set()
    expired_ips = []

    for ip, ban_time, _reason in list_blacklist_rows(CONFIG["BLACKLIST_DB"]):
        if ban_time > current_time:
            active_bans[ip] = ban_time
            active_blacklist.add(ip)
        else:
            expired_ips.append(ip)

    for ip in expired_ips:
        delete_blacklist_entry(CONFIG["BLACKLIST_DB"], ip)

    with state_lock:
        ban_times.clear()
        ban_times.update(active_bans)
        blacklist.clear()
        blacklist.update(active_blacklist)

    log_alert(f"[状态加载] 从数据库加载了 {len(active_bans)} 个未过期的封禁")
    if expired_ips:
        log_alert(f"[状态清理] 清理了 {len(expired_ips)} 条过期封禁记录")


def ban_ip(ip, reason):
    if is_trusted_ip(ip) or not validate_ip(ip):
        return False

    with state_lock:
        if ip in blacklist:
            return False

    try:
        expiry_time = execute_ban(ip, reason, CONFIG["BAN_TIME"], FIREWALL, CONFIG["BLACKLIST_DB"])
    except Exception as exc:
        log_alert(f"[错误] 执行封禁失败 {ip}: {exc}")
        return False

    with state_lock:
        blacklist.add(ip)
        ban_times[ip] = expiry_time
        ip_failures.pop(ip, None)

    log_alert(f"[封禁] IP {ip} 因 {reason} 被封禁")
    return True


def unban_ip(ip, reason="封禁到期自动解封"):
    if not validate_ip(ip):
        return False

    with state_lock:
        was_banned = ip in blacklist or ip in ban_times

    if not was_banned:
        delete_blacklist_entry(CONFIG["BLACKLIST_DB"], ip)
        return False

    try:
        execute_unban(ip, FIREWALL, CONFIG["BLACKLIST_DB"])
    except Exception as exc:
        log_alert(f"[错误] 执行解封失败 {ip}: {exc}")
        return False

    with state_lock:
        blacklist.discard(ip)
        ban_times.pop(ip, None)

    log_alert(f"[解封] IP {ip} 已解封，原因: {reason}")
    return True


def check_ban_expiry():
    current_time = int(time.time())
    with state_lock:
        expired_ips = [ip for ip, expiry in ban_times.items() if current_time >= expiry]

    for ip in expired_ips:
        unban_ip(ip)


def tail_log_file(log_path):
    while True:
        try:
            stat_info = os.stat(log_path)
            inode = stat_info.st_ino
            offset = stat_info.st_size

            with open(log_path, "r", encoding="utf-8", errors="ignore") as log_file:
                log_file.seek(offset)

                while True:
                    try:
                        new_stat = os.stat(log_path)
                    except FileNotFoundError:
                        log_alert(f"[日志轮转] {log_path} 暂时不可见，等待重新打开")
                        break

                    if new_stat.st_ino != inode or new_stat.st_size < log_file.tell():
                        log_alert(f"[日志轮转] {log_path} 发生轮转，重新打开")
                        break

                    line = log_file.readline()
                    if not line:
                        time.sleep(0.2)
                        continue

                    process_log_line(line, log_path)
        except FileNotFoundError:
            log_alert(f"[警告] 日志文件 {log_path} 不存在，5 秒后重试")
            time.sleep(5)
        except Exception as exc:
            log_alert(f"[错误] 监控日志文件 {log_path} 时出错: {exc}")
            time.sleep(5)


def process_log_line(line, log_path):
    if "auth.log" in log_path or "secure" in log_path:
        detect_ssh_brute_force(line)
    elif "access.log" in log_path:
        detect_web_attack(line)


def _register_failure(ip):
    current_time = time.time()
    with state_lock:
        if ip in blacklist:
            return False

        failures = ip_failures.setdefault(ip, deque())
        failures.append(current_time)

        while failures and current_time - failures[0] > CONFIG["WINDOW_SECONDS"]:
            failures.popleft()

        while len(failures) > CONFIG["MAX_FAILURES"]:
            failures.popleft()

        return len(failures) >= CONFIG["MAX_FAILURES"]


def detect_ssh_brute_force(line):
    match = SSH_FAILURE_PATTERN.search(line)
    if not match:
        return

    ip = match.group(1)
    if is_trusted_ip(ip) or not validate_ip(ip):
        return

    if _register_failure(ip):
        log_alert(f"[SSH暴力破解] 检测到来自 {ip} 的登录失败，已达到阈值")
        ban_ip(ip, "SSH暴力破解")


def detect_web_attack(line):
    for pattern in COMPILED_WEB_ATTACK_PATTERNS:
        if not pattern.search(line):
            continue

        ip = extract_client_ip(line)
        if not ip:
            return

        if is_trusted_ip(ip) or not validate_ip(ip):
            return

        if _register_failure(ip):
            log_alert(f"[Web攻击] 检测到来自 {ip} 的可能攻击: {pattern.pattern}，已达到阈值")
            ban_ip(ip, "Web攻击")
        return


def scan_webshell():
    scan_start_time = time.time()
    scan_result = scan_web_roots(CONFIG["WEB_ROOT"], file_modification_times)
    for suspicious_file in scan_result["suspicious_files"]:
        log_alert(f"[Webshell] 检测到可疑文件: {suspicious_file['file']}")

    scan_duration = time.time() - scan_start_time
    log_alert(
        "[Webshell扫描] 完成扫描，共扫描 {} 个文件，其中 {} 个为新增或修改文件，耗时 {:.2f} 秒".format(
            scan_result["scanned_files"], scan_result["modified_files"], scan_duration
        )
    )


def create_pid_file():
    os.makedirs(os.path.dirname(CONFIG["PID_FILE"]) or ".", exist_ok=True)

    while True:
        try:
            pid_fd = os.open(CONFIG["PID_FILE"], os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                with open(CONFIG["PID_FILE"], "r", encoding="utf-8") as pid_file:
                    pid = int(pid_file.read().strip())
                os.kill(pid, 0)
                print("Mini-HIDS 已经在运行中")
                return False
            except Exception:
                try:
                    os.remove(CONFIG["PID_FILE"])
                except FileNotFoundError:
                    pass

    with os.fdopen(pid_fd, "w", encoding="utf-8") as pid_file:
        pid_file.write(str(os.getpid()))
    return True


def main():
    if os.name != "posix":
        print("Mini-HIDS 仅支持 Linux 系统")
        return

    if not create_pid_file():
        return

    try:
        setup_environment()
        purge_expired_blacklist_entries(CONFIG["BLACKLIST_DB"])

        for _log_type, paths in CONFIG["LOG_PATHS"].items():
            for path in paths:
                if os.path.exists(path):
                    thread = threading.Thread(target=tail_log_file, args=(path,), daemon=True)
                    thread.start()
                    log_alert(f"[监控启动] 开始监控 {path}")

        log_alert(f"[防火墙] 当前后端: {FIREWALL.backend or '未检测到'}")
        scan_webshell()
        next_webshell_scan = time.time() + CONFIG["WEBSHELL_SCAN_INTERVAL"]

        while True:
            check_ban_expiry()
            now = time.time()
            if now >= next_webshell_scan:
                scan_webshell()
                next_webshell_scan = now + CONFIG["WEBSHELL_SCAN_INTERVAL"]
            time.sleep(max(1, int(CONFIG["CHECK_INTERVAL"])))

    except KeyboardInterrupt:
        log_alert("[停止] Mini-HIDS 已停止")
    finally:
        if os.path.exists(CONFIG["PID_FILE"]):
            os.remove(CONFIG["PID_FILE"])


if __name__ == "__main__":
    main()
