#!/usr/bin/env python3
"""
hidden-camera-scanner · bt_scan.py
蓝牙低能耗（BLE）扫描：发现附近疑似追踪器（AirTag / Find My、Samsung SmartTag、
Tile、Google FMDN、Chipolo 等），并结合地址轮换分析可疑信号（反偷拍排查阶段②）。

合规定位：仅被动监听广播，不连接、不配对、不写入任何设备，目的是发现针对用户
的非法追踪。识别结果是启发式的，不等于法律结论。

依赖：pip install bleak
权限：macOS 需给运行 Python 的终端授予蓝牙权限
      （系统设置 → 隐私与安全性 → 蓝牙）。
平台：Windows 10 16299+（WinRT 后端）、macOS 10.15+（CoreBluetooth）、
      Linux（BlueZ ≥ 5.43）原生支持；Android 仅限打包成 App 的 Python
      （p4a/Chaquopy），Termux 不可用（脚本会检测并明确报错）。

用法：
  python3 bt_scan.py [--rounds 5] [--listen 30] [--interval 120] [--out result.json]
    默认：5 轮 × 30s，轮间 120s（呼应「10 分钟内每隔 2 分钟监听 30 秒」）
    快速模式：--rounds 1 --listen 30
  python3 bt_scan.py --help

输出：JSON（stdout，--out 时同时写文件）；人类可读摘要（stderr）。

签名来源（公开资料，已核实）：
  - Apple AirTag 逆向：adamcatley.com/AirTag（0x004C + payload type 0x12）
  - AirTag 检测项目：Itheras/AirFlag、nitekry/airtag-recon
  - VIGIL 论文 (KaraZajac)：Tile 服务 0xFEED/0xFEEC/0xFE84、SmartTag 0xFD5A、
    Google FMDN 0xFEAA frame 0x40/0x41、DULT 0xFCB2
  - Network Survey 文档：厂商 ID Apple 0x004C、Samsung 0x0075、Tile 0x02E5、Google 0x00E0
"""

import argparse
import asyncio
import json
import os
import sys
import time

# Termux/普通 Linux 手机环境没有可用的 BLE 后端（bleak 的 Android 后端
# 是给 python-for-android / Chaquopy 打包的 App 用的），提前给出明确指引。
if "TERMUX_VERSION" in os.environ:
    print("⚠️ Termux 环境无法运行 BLE 扫描：bleak 的 Android 后端仅支持打包成 App 的"
          " Python（python-for-android / Chaquopy），Termux Python 没有 Java 桥。", file=sys.stderr)
    print("   替代方案：① 用 AirGuard / 系统自带的「未知追踪器警报」；"
          "② 把本脚本放到 Mac 上跑（本技能阶段②）。", file=sys.stderr)
    sys.exit(3)

try:
    from bleak import BleakScanner
except ImportError:
    print("缺少依赖 bleak：", file=sys.stderr)
    if sys.platform == "win32":
        print("  pip install bleak（需 Windows 10 16299+，WinRT 后端）", file=sys.stderr)
    elif sys.platform == "darwin":
        print("  pip install bleak", file=sys.stderr)
        print("  首次运行需在 系统设置 → 隐私与安全性 → 蓝牙 中给终端授权", file=sys.stderr)
    else:
        print("  pip install bleak（Linux 需 BlueZ >= 5.43）", file=sys.stderr)
    print("  若平台为 Termux/iOS：BLE 扫描不可用，请用 AirGuard / 系统未知追踪器警报替代"
          "（详见技能 references/platforms.md）", file=sys.stderr)
    sys.exit(2)


def uuid16(n: int) -> str:
    return f"0000{n:04x}-0000-1000-8000-00805f9b34fb"


APPLE_CIC = 0x004C
TILE_CIC = 0x02E5
CHIPOTO_CIC = 0x0133

SVC_SMARTTAG = uuid16(0xFD5A)   # Samsung SmartTag 服务
SVC_TILE = {uuid16(0xFEED), uuid16(0xFEEC), uuid16(0xFE84)}
SVC_GOOGLE_FMDN = uuid16(0xFEAA)  # Eddystone / Google Find My Device
SVC_DULT = uuid16(0xFCB2)

KNOWN_CIC_NAME = {
    0x004C: "Apple",
    0x0075: "Samsung",
    0x02E5: "Tile",
    0x00E0: "Google",
    0x0133: "Chipolo",
}

devices = {}          # addr -> record
sig_addresses = {}    # correlation_key -> set(addr)


def classify(adv) -> list:
    """基于已核实的广播签名判定追踪器类型。"""
    tags = []
    md = adv.manufacturer_data or {}
    sd = adv.service_data or {}
    name = (adv.local_name or "").lower()

    # Apple Find My / AirTag：必须 payload 首字节为 0x12（未注册态 0x07）。
    # 仅 0x004C 不足以判定——iPhone/Mac 的 Handoff 等也用 0x004C。
    if APPLE_CIC in md:
        payload = md[APPLE_CIC]
        if payload and payload[0] in (0x12, 0x07):
            tags.append("apple-findmy")

    if SVC_SMARTTAG in sd:
        tags.append("samsung-smarttag")
    if any(s in sd for s in SVC_TILE):
        tags.append("tile")
    if TILE_CIC in md:
        tags.append("tile")
    if SVC_GOOGLE_FMDN in sd:
        data = sd[SVC_GOOGLE_FMDN]
        if data and data[0] in (0x40, 0x41):
            tags.append("google-fmdn")
    if SVC_DULT in sd:
        tags.append("dult")
    if CHIPOTO_CIC in md:
        tags.append("chipolo")

    # 名称兜底
    if "tile" in name:
        tags.append("tile")
    if "smarttag" in name:
        tags.append("samsung-smarttag")

    return sorted(set(tags))


def corr_key(adv) -> str:
    """用于跨轮关联的稳定签名（与 MAC 无关）。"""
    parts = []
    md = adv.manufacturer_data or {}
    for cid in sorted(md):
        parts.append(f"m{cid:04x}:{bytes(md[cid]).hex()[:12]}")
    sd = adv.service_data or {}
    for u in sorted(sd):
        parts.append(f"s{u}:{bytes(sd[u]).hex()[:6]}")
    if adv.local_name:
        parts.append(f"n{adv.local_name}")
    return "|".join(parts)


def on_advert(device, adv):
    addr = device.address
    rssi = getattr(adv, "rssi", None)
    tags = classify(adv)
    key = corr_key(adv)

    rec = devices.setdefault(addr, {
        "address": addr,
        "name": adv.local_name or "",
        "company_ids": {},
        "service_uuids": [str(u) for u in (adv.service_uuids or [])],
        "service_data_keys": [str(u) for u in (adv.service_data or {})],
        "tags": set(),
        "rssi_min": rssi, "rssi_max": rssi, "detections": 0,
    })
    rec["detections"] += 1
    rec["tags"].update(tags)
    if adv.local_name and not rec["name"]:
        rec["name"] = adv.local_name
    for cid in (adv.manufacturer_data or {}):
        rec["company_ids"][f"0x{cid:04x}"] = KNOWN_CIC_NAME.get(cid, "unknown")
    if rssi is not None:
        rec["rssi_min"] = rssi if rec["rssi_min"] is None else min(rec["rssi_min"], rssi)
        rec["rssi_max"] = rssi if rec["rssi_max"] is None else max(rec["rssi_max"], rssi)
    if key:
        sig_addresses.setdefault(key, set()).add(addr)
        rec["corr_key"] = key


async def run_round(listen_s: int):
    scanner = BleakScanner(detection_callback=on_advert)
    await scanner.start()
    await asyncio.sleep(listen_s)
    await scanner.stop()


async def main_async(args):
    for r in range(1, args.rounds + 1):
        print(f"▶ 第 {r}/{args.rounds} 轮监听 {args.listen}s ...", file=sys.stderr)
        await run_round(args.listen)
        if r < args.rounds:
            print(f"  等待 {args.interval}s 后继续...", file=sys.stderr)
            await asyncio.sleep(args.interval)


def summarize():
    # 地址轮换：同一签名出现在多个地址
    rotating = {}
    for key, addrs in sig_addresses.items():
        if len(addrs) > 1:
            for a in addrs:
                rotating[a] = True
                if a in devices:
                    devices[a]["tags"].add("rotating-address")

    out = {
        "scan_type": "bluetooth",
        "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device_count": len(devices),
        "tracker_count": sum(1 for d in devices.values() if d["tags"] - {"rotating-address"}),
        "rotating_suspect_count": sum(1 for d in devices.values() if "rotating-address" in d["tags"]),
        "devices": [
            {
                "address": d["address"],
                "name": d["name"],
                "company_ids": d["company_ids"],
                "service_uuids": d["service_uuids"],
                "service_data_keys": d["service_data_keys"],
                "tags": sorted(d["tags"]),
                "rssi_min": d["rssi_min"],
                "rssi_max": d["rssi_max"],
                "detections": d["detections"],
            }
            for d in devices.values()
        ],
    }
    return out


def main():
    ap = argparse.ArgumentParser(description="BLE 追踪器扫描（反偷拍阶段②）")
    ap.add_argument("--rounds", type=int, default=5, help="扫描轮数（默认 5）")
    ap.add_argument("--listen", type=int, default=30, help="每轮监听秒数（默认 30）")
    ap.add_argument("--interval", type=int, default=120, help="轮间隔秒数（默认 120）")
    ap.add_argument("--out", type=str, default="", help="JSON 输出文件路径")
    args = ap.parse_args()

    print("▶ 仅被动监听 BLE 广播，不连接、不配对任何设备。", file=sys.stderr)
    if sys.platform == "darwin":
        print("  ⚠️ macOS 蓝牙权限：宿主 App（运行本脚本的终端 / WorkBuddy）需在"
              " 系统设置 → 隐私与安全性 → 蓝牙 中开启；", file=sys.stderr)
        print("     若进程无报错即被中止（退出码 134/SIGABRT），即为权限被拒——授权后重跑。", file=sys.stderr)
    asyncio.run(main_async(args))
    out = summarize()
    text = json.dumps(out, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print(f"▶ JSON 已写入: {args.out}", file=sys.stderr)

    e = sys.stderr
    print("\n=== 蓝牙扫描摘要 ===", file=e)
    print(f"发现设备 {out['device_count']} 台；命中追踪器签名 {out['tracker_count']} 台；"
          f"地址轮换可疑 {out['rotating_suspect_count']} 台", file=e)
    suspects = [d for d in out["devices"] if d["tags"]]
    if not suspects:
        print("未发现命中追踪器签名的设备（不代表安全：仅限蓝牙可发现范围）。", file=e)
    for d in suspects:
        print(f"  可疑 {d['address']}  名称[{d['name'] or '无'}]  "
              f"RSSI {d['rssi_min']}~{d['rssi_max']}dBm", file=e)
        for t in d["tags"]:
            print(f"    - {t}", file=e)
    print("提示：识别为启发式，需多轮扫描 + 人工确认；发现疑似追踪器请按报告建议处置。", file=e)


if __name__ == "__main__":
    main()
