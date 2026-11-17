#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hidden-camera-scanner · wifi_survey.py
Wi-Fi 环境勘察（反偷拍排查的「前置第一步」）：枚举周边可见的无线接入点（AP），
列出数量、SSID、BSSID、信号强度、信道、加密方式，并标出你当前连接的网络，
识别隐藏 SSID / 开放网络 / 同名多 BSSID（疑似仿冒同名 AP）等异常。

为什么先做这步：
  - 先看清「周围有几张网、你连的是哪张」，再决定阶段①扫哪段局域网；
  - 酒店/民宿常见「客户端隔离」，会直接让局域网扫描失效——此时本步能提示你换思路（转人工排查）；
  - 隐藏 SSID、无加密网络、与官方同名却多 MAC 的 AP，都可能是可疑信号，值得先记录。

合规定位：仅做被动的 AP 枚举（列出你本就在物理范围内能收到的无线信号），
不连接、不破解、不向任何 AP 发包；只勘察你本人所在/已连接的环境。

实现与依赖：
  - 全部依赖系统自带命令行，零第三方依赖：
    macOS   : airport（Apple80211 私有框架，无需 sudo 即可扫描）
    Windows : netsh wlan
    Linux   : nmcli（NetworkManager）或 iw
    Termux  : termux-wifi-scaninfo（需授予 Wi-Fi 权限）
  - 跨平台通用，Python >= 3.8。

用法：
  python3 wifi_survey.py [--out survey.json]
输出：JSON 到 stdout；--out 时同时写文件；人类可读摘要到 stderr。
"""

import argparse
import json
import re
import subprocess
import sys
import platform

IS_MACOS = platform.system() == "Darwin"
IS_WIN = platform.system() == "Windows"

e = sys.stderr


def log(msg):
    print(msg, file=e)


# ---------- 各平台采集 ----------

def _run(cmd, timeout=20):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception as ex:
        log(f"  （执行失败 {cmd[0] if cmd else '?'}：{ex}）")
        return ""


def survey_macos():
    airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    # 注意：macOS Sequoia 起 `airport -s` 带接口名（如 en0）会返回空，且非提权下不返回 BSSID；
    # 用无参数 `airport -s` 才能正常枚举 SSID/RSSI/信道/加密。
    raw = _run([airport, "-s"], timeout=25)
    if not raw.strip():
        return [], "airport", ""
    aps = []
    # 以 HT 列（恒为单个 Y/N）为锚点从右往左定位，避免 SSID 内含数字（如 "HP-Print-08-... 4640 series"）被误判为 RSSI。
    # 列序：SSID [BSSID] RSSI CHANNEL HT CC SECURITY；macOS Sequoia 起非提权不返回 BSSID 列。
    mac_pat = re.compile(r"^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$")
    for line in raw.splitlines():
        tk = line.split()
        # 找 HT 锚点（精确为 Y 或 N 的 token）
        ht_idx = None
        for i, t in enumerate(tk):
            if t in ("Y", "N"):
                ht_idx = i
                break
        if ht_idx is None or ht_idx < 2:
            continue
        rssi_tk = tk[ht_idx - 2]          # RSSI（有符号整数）
        chan_tk = tk[ht_idx - 1]          # CHANNEL（可能为 "6,-1"）
        bssid = ""
        ssid_tk = tk[:ht_idx - 2]
        if ht_idx >= 3 and mac_pat.match(tk[ht_idx - 3]):
            bssid = tk[ht_idx - 3].lower()
            ssid_tk = tk[:ht_idx - 3]
        ssid = " ".join(ssid_tk).strip()
        if not re.match(r"^-?\d+$", rssi_tk):
            continue
        sec = " ".join(tk[ht_idx + 2:]) if len(tk) > ht_idx + 2 else ""
        aps.append({
            "ssid": ssid or "<隐藏>",
            "hidden": (ssid == ""),
            "bssid": bssid,
            "rssi": int(rssi_tk),
            "channel": int(chan_tk.split(",")[0]) if chan_tk.split(",")[0].isdigit() else None,
            "security": sec.strip() or "未知",
        })
    # 当前连接
    info = _run([airport, "-I", "en0"], timeout=10) or _run([airport, "-I"], timeout=10)
    conn = _parse_macos_connected(info)
    return aps, "airport", conn


def _parse_macos_connected(info):
    ssid_m = re.search(r"^\s*SSID:\s*(.+?)\s*$", info, re.M)
    bssid_m = re.search(r"^\s*BSSID:\s*([0-9a-fA-F:]+)", info, re.M)
    if ssid_m and ssid_m.group(1).strip():
        return {"ssid": ssid_m.group(1).strip(), "bssid": (bssid_m.group(1).lower() if bssid_m else "")}
    return ""


def survey_windows():
    raw = _run(["netsh", "wlan", "show", "networks", "mode=bssid"], timeout=25)
    aps = []
    cur = {}
    ssid = None
    bssid = None
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("SSID") and ":" in s and "BSSID" not in s:
            # 新 SSID 块
            ssid = s.split(":", 1)[1].strip() or "<隐藏>"
            bssid = None
            cur = {"ssid": ssid, "hidden": (ssid == "<隐藏>"), "bssid": "",
                   "rssi": None, "channel": None, "security": ""}
            aps.append(cur)
        elif s.startswith("BSSID") and ":" in s:
            bssid = s.split(":", 1)[1].strip().replace("-", ":").lower()
            if cur:
                cur["bssid"] = bssid
        elif s.startswith("Signal") and ":" in s and cur:
            pct = re.search(r"(\d+)", s.split(":", 1)[1])
            if pct:
                cur["rssi"] = round(int(pct.group(1)) / 2 - 100)  # 百分比→估算 RSSI
        elif s.startswith("Channel") and ":" in s and cur:
            c = re.search(r"(\d+)", s.split(":", 1)[1])
            if c:
                cur["channel"] = int(c.group(1))
        elif s.startswith("Authentication") and ":" in s and cur:
            cur["security"] = s.split(":", 1)[1].strip()
    conn = _parse_windows_connected(_run(["netsh", "wlan", "show", "interfaces"], timeout=15))
    return aps, "netsh", conn


def _parse_windows_connected(info):
    ssid_m = re.search(r"^\s*SSID\s*:\s*(.+?)\s*$", info, re.M)
    bssid_m = re.search(r"^\s*BSSID\s*:\s*([0-9a-fA-F-:]+)", info, re.M)
    if ssid_m and ssid_m.group(1).strip():
        return {"ssid": ssid_m.group(1).strip(),
                "bssid": (bssid_m.group(1).replace("-", ":").lower() if bssid_m else "")}
    return ""


def survey_linux():
    # 优先 nmcli（NetworkManager）
    raw = _run(["nmcli", "-t", "-f", "IN-USE,SSID,BSSID,SIGNAL,CHAN,SECURITY", "dev", "wifi", "list"], timeout=25)
    aps = []
    if raw.strip():
        for line in raw.splitlines():
            f = line.split(":")
            if len(f) < 6:
                continue
            in_use, ssid, bssid, sig, chan, sec = f[0], f[1], f[2], f[3], f[4], f[5]
            aps.append({
                "ssid": ssid or "<隐藏>",
                "hidden": (ssid == ""),
                "bssid": bssid.lower(),
                "rssi": round(int(sig) / 2 - 100) if sig.isdigit() else None,
                "channel": int(chan) if chan.isdigit() else None,
                "security": sec or "未知",
            })
        return aps, "nmcli", _linux_connected()
    # 回退 iw（需接口名）
    iface = _run(["iw", "dev"], timeout=10).split()[1] if "Interface" in _run(["iw", "dev"], timeout=10) else ""
    if iface:
        raw = _run(["iw", iface, "scan"], timeout=25)
        # iw 输出解析较繁，仅做基础提取（BSSID / SSID / signal / primary channel）
        aps = []
        cur = None
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("BSS"):
                if cur:
                    aps.append(cur)
                cur = {"ssid": "<隐藏>", "hidden": True, "bssid": line.split()[1].lower(),
                       "rssi": None, "channel": None, "security": "未知"}
            elif line.startswith("SSID:") and cur is not None:
                cur["ssid"] = line.split(":", 1)[1].strip() or "<隐藏>"
                cur["hidden"] = (cur["ssid"] == "<隐藏>")
            elif line.startswith("signal:") and cur is not None:
                m = re.search(r"(-?\d+)", line)
                if m:
                    cur["rssi"] = int(m.group(1))
            elif line.startswith("primary channel:") and cur is not None:
                cur["channel"] = int(line.split(":")[1].strip())
        if cur:
            aps.append(cur)
        return aps, "iw", _linux_connected()
    return [], "none", ""


def _linux_connected():
    info = _run(["nmcli", "-t", "-f", "GENERAL.CONNECTION,DEVICE", "dev", "show", "wlan0"], timeout=10)
    # 简化：从 iw dev link 取已连 SSID/BSSID
    link = _run(["iw", "dev", "wlan0", "link"], timeout=10) if info == "" else ""
    ssid_m = re.search(r"SSID:\s*(.+)", link)
    bssid_m = re.search(r"BSSID:\s*([0-9a-fA-F:]+)", link)
    if ssid_m:
        return {"ssid": ssid_m.group(1).strip(),
                "bssid": (bssid_m.group(1).lower() if bssid_m else "")}
    return ""


def survey_termux():
    raw = _run(["termux-wifi-scaninfo"], timeout=20)
    aps = []
    if not raw.strip():
        return aps, "termux", ""
    try:
        data = json.loads(raw)
        for ap in data:
            ssid = ap.get("ssid") or ""
            aps.append({
                "ssid": ssid or "<隐藏>",
                "hidden": (ssid == ""),
                "bssid": (ap.get("bssid") or "").lower(),
                "rssi": ap.get("rssi", None),
                "channel": ap.get("channel", None),
                "security": ",".join(ap.get("capabilities", []) or []) or "未知",
            })
    except Exception as ex:
        log(f"  （termux-wifi-scaninfo 解析失败：{ex}）")
    return aps, "termux", ""


# ---------- 异常分析 ----------

def analyze(aps, conn):
    flags = []
    warnings = []
    hidden = [a for a in aps if a["hidden"]]
    open_aps = [a for a in aps if _is_open(a["security"])]
    if hidden:
        flags.append(f"隐藏 SSID：{len(hidden)} 个（不广播名称，可能是刻意规避，也可能是普通设备）")
    if open_aps:
        flags.append(f"开放网络（无加密）：{len(open_aps)} 个（任何人都可接入，酒店/民宿里出现需留意）")
    # 同名多 BSSID（疑似仿冒 / 或正常 Mesh、中继）——需要 BSSID 才有意义
    have_bssid = any(a["bssid"] for a in aps)
    if have_bssid:
        by_ssid = {}
        for a in aps:
            if a["hidden"] or not a["ssid"] or not a["bssid"]:
                continue
            by_ssid.setdefault(a["ssid"].lower(), []).append(a["bssid"])
        dup = {s: bs for s, bs in by_ssid.items() if len(set(bs)) >= 2}
        for s, bs in dup.items():
            flags.append(f"同名 SSID「{s}」出现 {len(set(bs))} 个 BSSID（可能是 Mesh/中继，也可能是仿冒同名 AP，需人工确认）")
    else:
        warnings.append("本机在非提权模式下未返回 AP 的 BSSID（如 macOS Sequoia），"
                        "无法做「同名多 MAC」仿冒比对；SSID/信号/信道/加密 勘察不受影响。")
    if not conn:
        warnings.append("未能确定当前连接网络（可能未连 Wi-Fi，或命令无权限）。")
    elif conn.get("ssid") and conn.get("bssid"):
        if not any(a["bssid"] == conn.get("bssid", "").lower() for a in aps if a["bssid"]):
            warnings.append(f"当前连接「{conn['ssid']}」的 BSSID 未出现在周边 AP 列表（已连 5G/不同频段或权限不足）")
    return flags, warnings


def _is_open(sec):
    s = (sec or "").upper()
    if "NONE" in s or "OPEN" in s:
        return True
    if "WPA" in s or "WEP" in s or "WPS" in s:
        return False
    return False  # 未知按非开放处理，避免误报


# ---------- 主流程 ----------

def main():
    ap = argparse.ArgumentParser(description="Wi-Fi 环境勘察（反偷拍前置步骤，免依赖）")
    ap.add_argument("--out", default="", help="JSON 结果同时写入此文件")
    args = ap.parse_args()

    log("▶ Wi-Fi 环境勘察：枚举周边无线接入点（被动，不连接、不破解）...")
    if IS_MACOS:
        aps, tool, conn = survey_macos()
    elif IS_WIN:
        aps, tool, conn = survey_windows()
    elif "TERMUX_VERSION" in __import__("os").environ:
        aps, tool, conn = survey_termux()
    else:
        aps, tool, conn = survey_linux()

    # 标注当前连接：优先用 BSSID 精确匹配；BSSID 缺失（如 macOS 非提权）时回退用 SSID 标记
    conn_bssid = (conn or {}).get("bssid", "").lower()
    conn_ssid = (conn or {}).get("ssid", "")
    for a in aps:
        if conn_bssid and a["bssid"] and a["bssid"] == conn_bssid:
            a["connected"] = True
        elif conn_bssid == "" and conn_ssid and a["ssid"] == conn_ssid:
            a["connected"] = True
        else:
            a["connected"] = False

    flags, warnings = analyze(aps, conn)

    result = {
        "scan_type": "wifi_survey",
        "tool": tool,
        "ap_count": len(aps),
        "hidden_count": sum(1 for a in aps if a["hidden"]),
        "open_count": sum(1 for a in aps if _is_open(a["security"])),
        "connected_ssid": (conn or {}).get("ssid", ""),
        "connected_bssid": conn_bssid,
        "aps": sorted(aps, key=lambda x: (x["rssi"] is None, -(x["rssi"] or -999))),
        "flags": flags,
        "warnings": warnings,
    }
    out = json.dumps(result, ensure_ascii=False, indent=2)
    print(out)
    if args.out:
        with open(args.out, "w") as f:
            f.write(out)
        log(f"▶ JSON 已写入: {args.out}")

    # 人类可读摘要
    log("\n=== Wi-Fi 环境勘察摘要 ===")
    log(f"工具: {tool} | 周边 AP: {len(aps)} 个 | 隐藏: {result['hidden_count']} | 开放: {result['open_count']}")
    if conn and conn.get("ssid"):
        log(f"当前连接: {conn['ssid']}  BSSID {conn_bssid or '?'}（接下来扫这张网的局域网）")
    else:
        log("当前连接: 未确定（请确认已连上要排查的 Wi-Fi）")
    if flags:
        for fl in flags:
            log(f"  ⚠️ {fl}")
    if warnings:
        for w in warnings:
            log(f"  ⓘ {w}")
    if not flags and not warnings:
        log("未发现明显异常信号；继续阶段①局域网扫描即可。")


if __name__ == "__main__":
    main()
