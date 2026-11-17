#!/usr/bin/env python3
"""输出简洁的九号车辆今日状态卡片。"""
from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

from runtime_config import config_path, ninecli_argv

SKILL_DIR = Path(__file__).resolve().parents[1]
RUN = SKILL_DIR / "scripts" / "run.sh"
LOCATE = SKILL_DIR / "scripts" / "locate.py"
PYTHON = SKILL_DIR / ".venv" / "bin" / "python"
CFG = config_path()


def load_cfg() -> dict:
    return json.loads(CFG.read_text(encoding="utf-8"))


def duration_text(sec) -> str:
    sec = int(sec or 0)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    parts = []
    if h:
        parts.append(f"{h}小时")
    if m:
        parts.append(f"{m}分钟")
    if s or not parts:
        parts.append(f"{s}秒")
    return "".join(parts)


def run_json(cmd: list[str], timeout: int = 180) -> dict:
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if out.returncode != 0:
        raise SystemExit(out.stderr.strip() or out.stdout.strip() or "命令执行失败")
    return json.loads(out.stdout)


def main() -> None:
    cfg = load_cfg()
    nb = cfg.get("ninebot") or {}
    sn = str(nb.get("sn") or "").strip()
    if not sn or sn.upper().startswith("REPLACE_WITH"):
        raise SystemExit("ninebot.sn 未配置")
    full_range = float(nb.get("full_range") or 80)

    rep = run_json([str(RUN), "--json"])
    status = run_json(ninecli_argv(SKILL_DIR, "status", sn, "--json"), timeout=60)
    py = str(PYTHON if PYTHON.exists() else Path(sys.executable))
    privacy = str(cfg.get("privacy_mode") or "district")
    loc = run_json([py, str(LOCATE), "--privacy", privacy, "--json"], timeout=120)

    v = rep.get("vehicle") or {}
    t = rep.get("travel") or {}
    lr = rep.get("last_ride") or {}
    now = datetime.datetime.now()
    wk = "一二三四五六日"[now.weekday()]

    online = "🟢 在线" if status.get("pwr") == 1 else "⚫ 离线/休眠"
    lock_b = "已锁" if v.get("barrel_lock") else "未锁"
    lock_s = "已锁" if v.get("seat_lock") else "未锁"
    pct = v.get("battery_percent")
    bat = v.get("battery_detail") or {}
    days = v.get("smart_service_surplus_days")
    expired = v.get("smart_service_expired")
    if days is not None:
        smart = f"有效（剩余 {days} 天）" if days > 0 else ("已过期" if expired == 1 else "剩余 0 天")
    elif expired is not None:
        smart = "已过期" if expired else "有效"
    else:
        smart = "未获取"

    name = rep.get("vehicle_name") or "九号电动车"
    model = rep.get("vehicle_model") or ""
    title_name = f"{name} · {model}" if model else name

    lines = [
        f"🛵 {title_name}·今日报告",
        f"📅 {now.year}年{now.month}月{now.day}日 星期{wk}",
        "",
        f"🛣️ 今日里程: {t.get('today_km', 0)} km",
        f"📅 本月骑行: {t.get('times', 0)} 次 · 总里程 {t.get('month_km', 0)} km · 总时长 {duration_text(t.get('duration_s'))}",
        "",
        "──────────",
        "",
        f"车辆状态: {online}",
        f"📍 位置: {loc.get('location') or '未获取'}",
        f"🔒 车锁: 龙头锁{lock_b} / 座桶锁{lock_s}",
        f"🛡️ 智能服务: {smart}",
        f"🔌 充电: {'充电中' if v.get('charging') == 1 else '未充电'}",
        f"📏 续航: 预估 {v.get('estimated_range_km')} km / 精确 {v.get('precise_range_km')} km",
    ]
    if pct is not None:
        lines.append(f"📊 满电理论续航: {full_range:g}km × {float(pct):g}% = {full_range * float(pct) / 100:g}km")
    lines.append("🔋 电池:")
    lines.append(f"   主电池剩余电量: {float(pct):g}%" if pct is not None else "   主电池剩余电量: 未获取")
    if bat.get("voltage_v") is not None:
        lines.append(f"   主电池电压: {bat['voltage_v']}V")
    if bat.get("temperature_c") is not None:
        lines.append(f"   主电池温度: {bat['temperature_c']}°C")

    if lr:
        lines += ["", "──────────", "", "🏍️ 最近骑行"]
        lines.append(f"   {lr.get('start_local') or '?'} → {lr.get('end_local') or '?'}")
        lines.append(f"   里程: {float(lr.get('distance_km') or 0):.2f} km | 耗时: {duration_text(lr.get('duration_s'))}")
        lines.append(f"   均速: {lr.get('avg_speed_kmh')} km/h | 极速: {lr.get('max_speed_kmh')} km/h")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
