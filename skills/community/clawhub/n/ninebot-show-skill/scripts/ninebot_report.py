#!/usr/bin/env python3
"""Ninebot Show Skill v3.2.1.

Read-only vehicle/report helper for local AI agents.
- Ninebot data comes from the locally authenticated ``ninecli`` CLI.
- Ninebot account password is never read from this skill's config.
- AMap reverse geocoding is optional and uses AMAP_WEB_KEY from the environment.
- No messaging platform CLI is invoked; the host agent decides how to deliver the returned text.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from runtime_config import config_path, env_value
from typing import Any, Optional
from urllib.parse import quote

import requests

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python 3.8 fallback
    ZoneInfo = None  # type: ignore


VERSION = "3.2.1"
DEFAULT_CONFIG = config_path()
WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
PRIVACY_MODES = {"off", "district", "exact", "coordinates"}

WEATHER_CN = {
    "Clear": "晴", "Sunny": "晴", "Partly cloudy": "多云", "Partly Cloudy": "多云",
    "Cloudy": "阴", "Overcast": "阴", "Mist": "雾", "Fog": "雾",
    "Patchy rain nearby": "局部阵雨", "Light rain": "小雨", "Moderate rain": "中雨",
    "Heavy rain": "大雨", "Light drizzle": "毛毛雨", "Thundery outbreaks": "雷阵雨",
    "Light rain shower": "小阵雨", "Moderate or heavy rain shower": "大阵雨",
    "Patchy light rain": "细雨", "Patchy light rain in area with thunder": "局地雷雨",
    "Light snow": "小雪", "Moderate snow": "中雪", "Heavy snow": "大雪",
}
WEATHER_ORDER = [
    "晴", "多云", "阴", "雾", "局部阵雨", "毛毛雨", "细雨", "小雨", "小阵雨",
    "中雨", "大阵雨", "大雨", "雷阵雨", "局地雷雨", "小雪", "中雪", "大雪",
]


class ConfigError(RuntimeError):
    pass


@dataclass
class CliResult:
    data: Any = None
    error: str = ""
    returncode: int = 0


class Context:
    def __init__(self, cfg: dict[str, Any], debug: bool = False) -> None:
        self.cfg = cfg
        self.debug = debug
        self.warnings: list[str] = []
        self.errors: list[str] = []
        self.ninecli_prefix = find_ninecli_prefix()
        self.ninecli_config_dir = expand_optional_path(
            os.environ.get("NINEBOT_CONFIG_DIR") or cfg.get("ninecli_config_dir")
        )

    def warn(self, message: str) -> None:
        if message not in self.warnings:
            self.warnings.append(message)
        if self.debug:
            print(f"[warning] {message}", file=sys.stderr)

    def error(self, message: str) -> None:
        if message not in self.errors:
            self.errors.append(message)
        print(f"[error] {message}", file=sys.stderr)


def expand_optional_path(value: Any) -> Optional[str]:
    if value is None or str(value).strip() == "":
        return None
    return os.path.expandvars(os.path.expanduser(str(value)))


def resolve_config_path(cli_value: Optional[str]) -> Path:
    raw = cli_value or os.environ.get("NINEBOT_SHOW_CONFIG") or os.environ.get("NINEBOT_REPORT_CONFIG")
    if raw:
        return Path(os.path.expandvars(os.path.expanduser(raw)))
    return DEFAULT_CONFIG


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(
            f"配置文件不存在: {path}。先运行 skills/ninebot-show-skill/scripts/setup.sh 创建模板。"
        )
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"配置文件不是有效 JSON: {path}: {exc}") from exc
    if not isinstance(cfg, dict):
        raise ConfigError("配置根节点必须是 JSON 对象")

    ninebot = cfg.get("ninebot")
    if not isinstance(ninebot, dict):
        raise ConfigError("缺少 ninebot 配置对象")
    sn = str(ninebot.get("sn", "")).strip()
    if not sn or "请填写" in sn or sn.upper().startswith("REPLACE_WITH"):
        raise ConfigError("未配置 ninebot.sn；请把 ninecli vehicles --json 中的 wnumber 填入配置")

    privacy = str(cfg.get("privacy_mode", "district")).lower().strip()
    if privacy not in PRIVACY_MODES:
        raise ConfigError(f"privacy_mode 必须是 {sorted(PRIVACY_MODES)} 之一")
    cfg["privacy_mode"] = privacy
    return cfg


def get_tz(name: str):
    if ZoneInfo is not None:
        try:
            return ZoneInfo(name)
        except Exception:
            pass
    return timezone(timedelta(hours=8))


def find_ninecli_prefix() -> list[str]:
    override = os.environ.get("NINECLI_BIN", "").strip()
    if override:
        candidate = Path(os.path.expanduser(override))
        try:
            candidate = candidate.resolve(strict=True)
        except OSError:
            return []
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return [str(candidate)]
        return []

    sibling = Path(sys.executable).resolve().parent / "ninecli"
    if sibling.is_file() and os.access(sibling, os.X_OK):
        return [str(sibling)]

    exe = shutil.which("ninecli")
    if exe:
        return [exe]

    try:
        if importlib.util.find_spec("ninecli") is not None:
            return [sys.executable, "-m", "ninecli"]
    except Exception:
        pass

    local = Path.home() / ".local" / "bin" / "ninecli"
    if local.is_file() and os.access(local, os.X_OK):
        return [str(local)]
    return []


def run_process(args: list[str], timeout: int = 35) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def ninecli_call(ctx: Context, args: list[str], *, parse_json: bool = True, retries: int = 2) -> CliResult:
    if not ctx.ninecli_prefix:
        return CliResult(error="未找到 ninecli；请先运行 setup.sh", returncode=127)
    if not args or args[0] not in {"status", "battery", "travel", "whoami", "vehicles"}:
        return CliResult(error="拒绝非只读 ninecli 子命令", returncode=126)

    command = list(ctx.ninecli_prefix)
    if ctx.ninecli_config_dir:
        command += ["--config", ctx.ninecli_config_dir]
    command += args

    last_error = ""
    last_code = 1
    for attempt in range(retries):
        try:
            proc = run_process(command)
            last_code = proc.returncode
        except subprocess.TimeoutExpired:
            last_error = "ninecli 调用超时"
        except OSError as exc:
            last_error = f"无法启动 ninecli: {exc}"
        else:
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()
            if proc.returncode == 0:
                if not parse_json:
                    return CliResult(data=stdout, returncode=0)
                if not stdout:
                    last_error = "ninecli 返回空输出"
                else:
                    try:
                        return CliResult(data=json.loads(stdout), returncode=0)
                    except json.JSONDecodeError as exc:
                        last_error = f"ninecli 返回了非 JSON 数据: {exc}"
            else:
                last_error = stderr or stdout or f"ninecli 退出码 {proc.returncode}"
        if attempt + 1 < retries:
            time.sleep(1.0)

    return CliResult(error=sanitize_cli_error(last_error), returncode=last_code)


def sanitize_cli_error(message: str) -> str:
    """Keep diagnostics useful without echoing possible secrets."""
    text = (message or "未知错误").strip()
    lowered = text.lower()
    if any(token in lowered for token in ("unauthorized", "token", "login", "auth", "expired", "401")):
        return "ninecli 登录可能已失效，请在本机重新执行 ninecli login"
    return text[:500]


def unwrap_dict(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    nested = value.get("data")
    if isinstance(nested, dict):
        return nested
    return value


def coerce_float(value: Any) -> Optional[float]:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def coerce_int(value: Any) -> Optional[int]:
    number = coerce_float(value)
    return int(number) if number is not None else None


def first_value(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def normalize_status(payload: Any) -> dict[str, Any]:
    data = unwrap_dict(payload)
    loc = data.get("loc") if isinstance(data.get("loc"), dict) else {}
    return {
        "battery_percent": coerce_float(first_value(data, "dump_energy", "battery", "battery_percent")),
        "charging": coerce_int(first_value(data, "charging", "charge_status")),
        "estimated_range_km": coerce_float(first_value(data, "estimate_mileage", "estimated_mileage")),
        "precise_range_km": coerce_float(first_value(data, "precise_estimate_mileage", "precise_mileage")),
        "barrel_lock": coerce_int(first_value(data, "barrel_lock_status", "handlebar_lock")),
        "seat_lock": coerce_int(first_value(loc, "lock", "seat_lock")),
        "smart_service_expired": coerce_int(first_value(data, "is_smart_service_expired")),
        "lat": coerce_float(first_value(loc, "lat", "latitude") or first_value(data, "lat", "latitude")),
        "lon": coerce_float(first_value(loc, "lon", "lng", "longitude") or first_value(data, "lon", "lng", "longitude")),
        "raw_available": bool(data),
    }


def normalize_vehicle_meta(payload: Any, sn: str) -> dict[str, Any]:
    """Return non-secret vehicle metadata needed by the report.

    Do not expose VIN, BLE secrets, owner identifiers, or raw vehicle records.
    """
    candidates: list[dict[str, Any]] = []
    if isinstance(payload, list):
        candidates = [x for x in payload if isinstance(x, dict)]
    elif isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            candidates = [x for x in data if isinstance(x, dict)]
        else:
            candidates = [payload]

    target = None
    for item in candidates:
        item_sn = str(first_value(item, "wnumber", "sn") or "").strip()
        if item_sn == sn:
            target = item
            break
    if target is None:
        return {}

    return {
        "smart_service_surplus_days": coerce_int(first_value(target, "smart_service_surplus_days")),
    }


def normalize_battery(payload: Any) -> dict[str, Any]:
    data = unwrap_dict(payload)
    main = data.get("battery_main") if isinstance(data.get("battery_main"), dict) else {}
    battery_list = data.get("battery_list") if isinstance(data.get("battery_list"), list) else []
    first = battery_list[0] if battery_list and isinstance(battery_list[0], dict) else {}
    return {
        "present": bool(data),
        "percent": coerce_float(first_value(main, "electricity", "percent") or first_value(data, "electricity")),
        "voltage_v": coerce_float(first_value(first, "bms_volt", "voltage") or first_value(data, "bms_voltage")),
        "temperature_c": coerce_float(first_value(first, "bat_temp", "temperature") or first_value(data, "batt_temp")),
        "cycles": coerce_int(first_value(first, "bms_cycle", "cycles") or first_value(data, "bms_cycles")),
        "score": coerce_float(first_value(first, "score") or first_value(data, "bms_score")),
    }


def normalize_travel(payload: Any, now: datetime) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
    data = unwrap_dict(payload)
    detail = data.get("detail") if isinstance(data.get("detail"), list) else []
    today_value: Any = None
    index = now.day - 1
    if 0 <= index < len(detail):
        item = detail[index]
        if isinstance(item, dict):
            today_value = first_value(item, "mileages", "mileage", "distance")
        else:
            today_value = item

    rides = data.get("list") if isinstance(data.get("list"), list) else []
    ride_dicts = [r for r in rides if isinstance(r, dict)]
    ride_dicts.sort(key=lambda r: coerce_int(first_value(r, "start_time", "startTime")) or 0, reverse=True)
    last = normalize_ride(ride_dicts[0]) if ride_dicts else None

    travel = {
        "today_km": coerce_float(today_value) or 0.0,
        "month_km": coerce_float(first_value(data, "total_mileages", "total_mileage", "total_distance")) or 0.0,
        "times": coerce_int(first_value(data, "times", "count")) or 0,
        "duration_s": coerce_int(first_value(data, "duration", "total_duration")) or 0,
    }
    return travel, last


def normalize_ride(data: dict[str, Any]) -> dict[str, Any]:
    distance = coerce_float(first_value(data, "mileages", "mileage", "distance")) or 0.0
    duration = coerce_int(first_value(data, "duration", "duration_s")) or 0
    total_wh = coerce_float(first_value(data, "ec", "energy", "energy_wh"))
    used_percent = coerce_float(first_value(data, "used_electricity", "used_battery"))
    max_speed = coerce_float(first_value(data, "speed", "max_speed"))
    average_speed = distance / (duration / 3600) if duration > 0 else 0.0
    average_wh_km = total_wh / distance if total_wh is not None and distance > 0 else None
    return {
        "distance_km": distance,
        "duration_s": duration,
        "avg_speed_kmh": round(average_speed, 1),
        "max_speed_kmh": max_speed,
        "used_battery_percent": used_percent,
        "energy_wh": total_wh,
        "avg_wh_km": round(average_wh_km, 1) if average_wh_km is not None else None,
        "start_time": coerce_int(first_value(data, "start_time", "startTime")),
        "end_time": coerce_int(first_value(data, "end_time", "endTime")),
    }


def wgs84_to_gcj02(lat: float, lon: float) -> tuple[float, float]:
    """原始 GPS(WGS-84) -> GCJ-02（高德/腾讯坐标系）。

    九号接口上报的 ``loc.lat/lon`` 按原始 GPS 处理，直接当高德坐标使用可能产生
    数百米级偏移。九号地图页会调用高德
    ``v3/assistant/coordinate/convert?coordsys=gps`` 做这一步；这里内置等价算法，
    避免为一次逆地理额外发一次请求。
    """
    a = 6378245.0
    ee = 0.00669342162296594323

    def _tlat(x: float, y: float) -> float:
        r = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        r += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        r += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return r

    def _tlon(x: float, y: float) -> float:
        r = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        r += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        r += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return r

    dlat = _tlat(lon - 105.0, lat - 35.0)
    dlon = _tlon(lon - 105.0, lat - 35.0)
    rad = lat / 180.0 * math.pi
    m = math.sin(rad)
    m = 1 - ee * m * m
    sm = math.sqrt(m)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (m * sm) * math.pi)
    dlon = (dlon * 180.0) / (a / sm * math.cos(rad) * math.pi)
    return lat + dlat, lon + dlon


def _amap_key() -> str:
    """Read the optional AMap key without depending on any specific Agent home."""
    return env_value(("AMAP_WEBSERVICE_KEY", "AMAP_WEB_KEY"))


def reverse_geocode(lat: float, lon: float, mode: str, ctx: Context) -> str:
    if mode == "off":
        return "已隐藏"
    if mode == "coordinates":
        return f"{lat:.4f},{lon:.4f}"

    key = _amap_key()
    if not key:
        ctx.warn("未设置 AMAP_WEBSERVICE_KEY（或 AMAP_WEB_KEY），无法把 GPS 转为中文地址")
        return "已获取坐标（未配置地址解析）"

    # 设备坐标是 WGS-84，高德要 GCJ-02；不转换会偏 ~560 m。
    glat, glon = wgs84_to_gcj02(lat, lon)
    if mode == "district":
        glat, glon = round(glat, 2), round(glon, 2)

    try:
        resp = requests.get(
            "https://restapi.amap.com/v3/geocode/regeo",
            params={"location": f"{glon:.6f},{glat:.6f}", "key": key, "output": "JSON", "radius": 500},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "1":
            ctx.warn(f"高德逆地理编码失败: {data.get('info') or '未知错误'}")
            return "位置解析失败"
        regeocode = data.get("regeocode") if isinstance(data.get("regeocode"), dict) else {}
        if mode == "exact":
            return str(regeocode.get("formatted_address") or "位置解析失败")
        component = regeocode.get("addressComponent") if isinstance(regeocode.get("addressComponent"), dict) else {}
        province = stringify_component(component.get("province"))
        city = stringify_component(component.get("city"))
        district = stringify_component(component.get("district"))
        parts: list[str] = []
        for part in (province, city, district):
            if part and part not in parts:
                parts.append(part)
        return "".join(parts) or "位置解析失败"
    except Exception as exc:
        ctx.warn(f"高德逆地理编码请求失败: {type(exc).__name__}")
        return "位置解析失败"


def stringify_component(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "".join(str(x) for x in value if x)
    return ""


def parse_weather_day(day_data: dict[str, Any]) -> dict[str, Any]:
    hourly = day_data.get("hourly") if isinstance(day_data.get("hourly"), list) else []
    temps = [coerce_int(h.get("tempC")) for h in hourly if isinstance(h, dict)]
    temps = [x for x in temps if x is not None]
    hums = [coerce_int(h.get("humidity")) for h in hourly if isinstance(h, dict)]
    hums = [x for x in hums if x is not None]
    winds = [coerce_int(h.get("windspeedKmph")) for h in hourly if isinstance(h, dict)]
    winds = [x for x in winds if x is not None]
    uv_values = [coerce_float(h.get("uvIndex")) for h in hourly if isinstance(h, dict)]
    uv_values = [x for x in uv_values if x is not None]

    descriptions: list[str] = []
    for h in hourly:
        if not isinstance(h, dict):
            continue
        raw_time = coerce_int(h.get("time")) or 0
        hour = raw_time // 100
        if not 6 <= hour <= 18:
            continue
        desc_list = h.get("weatherDesc") if isinstance(h.get("weatherDesc"), list) else []
        if desc_list and isinstance(desc_list[0], dict):
            raw = str(desc_list[0].get("value", "")).strip()
            cn = WEATHER_CN.get(raw, raw)
            if cn and cn not in descriptions:
                descriptions.append(cn)
    descriptions.sort(key=lambda x: WEATHER_ORDER.index(x) if x in WEATHER_ORDER else 999)
    description = descriptions[0] if len(descriptions) == 1 else "转".join(descriptions[:3])

    astronomy = day_data.get("astronomy") if isinstance(day_data.get("astronomy"), list) else []
    astro = astronomy[0] if astronomy and isinstance(astronomy[0], dict) else {}
    return {
        "date": str(day_data.get("date", "")),
        "description": description or "未知",
        "temp_min_c": min(temps) if temps else None,
        "temp_max_c": max(temps) if temps else None,
        "humidity_min": min(hums) if hums else None,
        "humidity_max": max(hums) if hums else None,
        "wind_min_kmh": min(winds) if winds else None,
        "wind_max_kmh": max(winds) if winds else None,
        "uv": max(uv_values) if uv_values else None,
        "sunrise": astro.get("sunrise"),
        "sunset": astro.get("sunset"),
    }


def get_weather(location: str, now: datetime, ctx: Context) -> list[dict[str, Any]]:
    if not location or "请填写" in location:
        ctx.warn("未配置天气城市，跳过天气查询")
        return []
    try:
        url = f"https://wttr.in/{quote(location)}"
        resp = requests.get(url, params={"format": "j1"}, timeout=15, headers={"User-Agent": "ninebot-show-skill/3.2.1"})
        resp.raise_for_status()
        payload = resp.json()
        days = payload.get("weather") if isinstance(payload.get("weather"), list) else []
        targets = {now.strftime("%Y-%m-%d"), (now + timedelta(days=1)).strftime("%Y-%m-%d")}
        return [parse_weather_day(day) for day in days if isinstance(day, dict) and str(day.get("date")) in targets]
    except Exception as exc:
        ctx.warn(f"天气查询失败: {type(exc).__name__}")
        return []


def format_num(value: Optional[float], digits: int = 1) -> str:
    if value is None:
        return "未获取"
    rounded = round(value, digits)
    if digits == 0:
        return str(int(rounded))
    text = f"{rounded:.{digits}f}"
    return text.rstrip("0").rstrip(".")


def format_duration(seconds: int) -> str:
    seconds = max(0, int(seconds))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}小时{minutes}分钟{secs}秒"
    return f"{minutes}分{secs}秒"


def format_ts(timestamp: Optional[int], tz) -> Optional[str]:
    if not timestamp:
        return None
    # Accept seconds and millisecond epoch values.
    if timestamp > 10_000_000_000:
        timestamp = timestamp // 1000
    try:
        return datetime.fromtimestamp(timestamp, tz).strftime("%m/%d %H:%M")
    except (OSError, OverflowError, ValueError):
        return None


def uv_level(value: Optional[float]) -> str:
    if value is None:
        return "未知"
    if value <= 2:
        return "低"
    if value <= 5:
        return "中等"
    if value <= 7:
        return "高"
    if value <= 10:
        return "很高"
    return "极高"


def build_report(result: dict[str, Any], now: datetime, full_range: float, vehicle_name: str) -> str:
    vehicle = result["vehicle"]
    travel = result["travel"]
    last_ride = result.get("last_ride")
    weather = result.get("weather") or []

    lines = [
        "🛵 **九号电动车·车辆报告**",
        f"📅 {now.year}年{now.month}月{now.day}日 {WEEKDAYS[now.weekday()]}",
        "",
        f"🛣️ 今日里程: {format_num(travel.get('today_km'))} km",
        f"📅 本月骑行: {travel.get('times', 0)} 次 | 总里程 {format_num(travel.get('month_km'))} km | 总时长 {format_duration(travel.get('duration_s', 0))}",
        "",
        "──────────",
        "",
    ]

    if vehicle.get("available"):
        battery_percent = vehicle.get("battery_percent")
        charging = vehicle.get("charging")
        lines.append(f"🔋 电量: {format_num(battery_percent)}%")
        if charging is None:
            lines.append("🔌 充电: 未获取")
        else:
            lines.append(f"🔌 充电: {'是 ✅' if charging == 1 else '否 ❌'}")
        lines.append(
            f"📏 续航: 预估 {format_num(vehicle.get('estimated_range_km'))} km / "
            f"精确 {format_num(vehicle.get('precise_range_km'))} km"
        )
        if battery_percent is not None:
            theory = max(0.0, full_range * float(battery_percent) / 100.0)
            lines.append(f"📊 满电理论续航: {format_num(full_range)} km × {format_num(battery_percent)}% = {format_num(theory)} km")

        barrel = vehicle.get("barrel_lock")
        seat = vehicle.get("seat_lock")
        barrel_text = "未获取" if barrel is None else ("✅" if barrel == 1 else "❌")
        seat_text = "未获取" if seat is None else ("✅" if seat == 1 else "❌")
        lines.append(f"🔒 车锁: 龙头锁{barrel_text} / 座桶锁{seat_text}")

        battery_detail = vehicle.get("battery_detail") or {}
        if battery_detail.get("present"):
            parts = []
            if battery_detail.get("percent") is not None:
                parts.append(f"{format_num(battery_detail['percent'])}%")
            if battery_detail.get("voltage_v") is not None:
                parts.append(f"{format_num(battery_detail['voltage_v'])}V")
            if battery_detail.get("temperature_c") is not None:
                parts.append(f"{format_num(battery_detail['temperature_c'])}°C")
            lines.append(f"🔋 主电池: {' / '.join(parts) if parts else '已检测到，详情未获取'}")
        else:
            lines.append("🔋 主电池详情: 未获取")

        expired = vehicle.get("smart_service_expired")
        surplus_days = vehicle.get("smart_service_surplus_days")
        if surplus_days is not None:
            if surplus_days > 0:
                lines.append(f"🛡️ 智能服务: ✅ 有效（剩余 {surplus_days} 天）")
            elif expired == 1:
                lines.append("🛡️ 智能服务: ⚠️ 已过期（剩余 0 天）")
            else:
                lines.append("🛡️ 智能服务: 剩余 0 天")
        elif expired is not None:
            lines.append("🛡️ 智能服务: ⚠️ 已过期" if expired else "🛡️ 智能服务: ✅ 有效")
        lines.append(f"📍 位置: {vehicle.get('location_text') or '未获取'}")
        model = str(result.get("vehicle_model") or "").strip()
        lines.append(f"📶 车辆: {vehicle_name}" + (f"（{model}）" if model else ""))

        if battery_percent is not None:
            b = int(battery_percent)
            if charging == 1:
                lines.append(f"✅ 正在充电中，当前电量 {b}%")
            elif b <= 30:
                lines.append(f"⚠️ 建议充电: 当前电量 {b}%")
            elif b <= 50:
                lines.append(f"💡 当前电量 {b}%，可按明日行程决定是否充电")
            else:
                lines.append(f"✅ 当前电量 {b}%")
    else:
        lines.append("❌ 车辆状态未获取")

    lines += ["", "──────────", ""]

    if last_ride:
        start = last_ride.get("start_local") or "?"
        end = last_ride.get("end_local")
        end_part = end.split(" ", 1)[-1] if isinstance(end, str) and " " in end else (end or "?")
        lines.append(f"🏍️ 最近骑行 ({start}~{end_part})")
        lines.append(
            f"  里程: {format_num(last_ride.get('distance_km'), 2)} km | "
            f"耗时: {format_duration(last_ride.get('duration_s', 0))}"
        )
        lines.append(
            f"  均速: {format_num(last_ride.get('avg_speed_kmh'))} km/h | "
            f"极速: {format_num(last_ride.get('max_speed_kmh'))} km/h"
        )
        energy_parts = []
        if last_ride.get("used_battery_percent") is not None:
            energy_parts.append(f"耗电 {format_num(last_ride['used_battery_percent'])}%")
        if last_ride.get("energy_wh") is not None:
            energy_parts.append(f"总能耗 {format_num(last_ride['energy_wh'], 0)} Wh")
        if last_ride.get("avg_wh_km") is not None:
            energy_parts.append(f"平均能耗 {format_num(last_ride['avg_wh_km'])} Wh/km")
        if energy_parts:
            lines.append("  " + " | ".join(energy_parts))
    else:
        lines.append("🏍️ 最近骑行: 未获取")

    if weather:
        lines += ["", "──────────", ""]
        for idx, day in enumerate(weather):
            try:
                dt = datetime.strptime(day.get("date", ""), "%Y-%m-%d")
                date_cn = f"{dt.month}月{dt.day}日"
            except ValueError:
                date_cn = str(day.get("date") or "")
            label = "今天" if day.get("date") == now.strftime("%Y-%m-%d") else "明天"
            lines.append(f"🌤 {label}（{date_cn}）天气预报")
            tmin = day.get("temp_min_c")
            tmax = day.get("temp_max_c")
            temp = "未获取" if tmin is None or tmax is None else f"{tmin}~{tmax}°C"
            hmin, hmax = day.get("humidity_min"), day.get("humidity_max")
            humidity = "未获取" if hmin is None or hmax is None else f"{hmin}~{hmax}%"
            wmin, wmax = day.get("wind_min_kmh"), day.get("wind_max_kmh")
            wind = "未获取" if wmin is None or wmax is None else f"{wmin}~{wmax}km/h"
            lines.append(f"  天气: {day.get('description', '未知')} | {temp}")
            lines.append(f"  湿度: {humidity} | 风力: {wind}")
            uv = day.get("uv")
            lines.append(
                f"  ☀️ 紫外线: {format_num(uv)}（{uv_level(uv)}） | "
                f"日出{day.get('sunrise') or '?'} 🌇 日落{day.get('sunset') or '?'}"
            )
            if idx + 1 < len(weather):
                lines.append("")

    if result.get("warnings"):
        lines += ["", "──────────", "", "⚠️ 部分数据未获取："]
        lines.extend(f"  - {warning}" for warning in result["warnings"])

    return "\n".join(lines)


def collect_report(cfg: dict[str, Any], args: argparse.Namespace, ctx: Context) -> tuple[dict[str, Any], int]:
    tz_name = str(cfg.get("timezone") or "Asia/Shanghai")
    tz = get_tz(tz_name)
    now = datetime.now(tz)
    ninebot = cfg["ninebot"]
    sn = str(ninebot["sn"]).strip()
    privacy_mode = args.privacy or cfg.get("privacy_mode", "district")

    vehicles_res = ninecli_call(ctx, ["vehicles", "--json"])
    if vehicles_res.error:
        ctx.warn(f"车辆列表查询失败: {vehicles_res.error}")
    vehicle_meta = normalize_vehicle_meta(vehicles_res.data, sn)

    status_res = ninecli_call(ctx, ["status", sn, "--json"])
    if status_res.error:
        ctx.warn(f"车辆状态查询失败: {status_res.error}")
    status = normalize_status(status_res.data)

    battery_res = ninecli_call(ctx, ["battery", sn, "--json"])
    if battery_res.error:
        ctx.warn(f"电池详情查询失败: {battery_res.error}")
    battery = normalize_battery(battery_res.data)

    month = now.strftime("%Y%m")
    travel_res = ninecli_call(ctx, ["travel", sn, "--month", month, "--json"])
    if travel_res.error:
        ctx.warn(f"骑行统计查询失败: {travel_res.error}")
    travel, last_ride = normalize_travel(travel_res.data, now)

    location_text = "未获取"
    if privacy_mode == "off":
        location_text = "已隐藏"
    elif status.get("lat") is not None and status.get("lon") is not None:
        location_text = reverse_geocode(float(status["lat"]), float(status["lon"]), privacy_mode, ctx)

    vehicle = {
        "available": status.get("raw_available", False),
        "battery_percent": status.get("battery_percent"),
        "charging": status.get("charging"),
        "estimated_range_km": status.get("estimated_range_km"),
        "precise_range_km": status.get("precise_range_km"),
        "barrel_lock": status.get("barrel_lock"),
        "seat_lock": status.get("seat_lock"),
        "smart_service_expired": status.get("smart_service_expired"),
        "smart_service_surplus_days": vehicle_meta.get("smart_service_surplus_days"),
        "location_text": location_text,
        "privacy_mode": privacy_mode,
        "battery_detail": battery,
    }
    if privacy_mode == "coordinates" and status.get("lat") is not None and status.get("lon") is not None:
        vehicle["coordinates"] = {"lat": round(float(status["lat"]), 4), "lon": round(float(status["lon"]), 4)}

    if last_ride:
        last_ride["start_local"] = format_ts(last_ride.get("start_time"), tz)
        last_ride["end_local"] = format_ts(last_ride.get("end_time"), tz)

    weather_enabled = bool(cfg.get("weather_enabled", True)) and not args.no_weather
    weather = get_weather(str(cfg.get("location", "")), now, ctx) if weather_enabled else []

    result: dict[str, Any] = {
        "version": VERSION,
        "generated_at": now.isoformat(),
        "timezone": tz_name,
        "vehicle_name": str(ninebot.get("vehicle_name") or "九号电动车"),
        "vehicle_model": str(ninebot.get("vehicle_model") or "").strip(),
        "vehicle": vehicle,
        "travel": travel,
        "last_ride": last_ride,
        "weather": weather,
        "warnings": list(ctx.warnings),
    }
    full_range = coerce_float(ninebot.get("full_range")) or 80.0
    result["report"] = build_report(result, now, full_range, result["vehicle_name"])
    return result, 0 if status.get("raw_available") else 3


def check_environment(cfg_path: Path, debug: bool = False) -> int:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("Python", sys.version_info >= (3, 8), sys.version.split()[0]))

    prefix = find_ninecli_prefix()
    checks.append(("ninecli", bool(prefix), " ".join(prefix) if prefix else "未找到"))
    checks.append(("配置文件", cfg_path.exists(), str(cfg_path)))

    cfg: Optional[dict[str, Any]] = None
    if cfg_path.exists():
        try:
            cfg = load_config(cfg_path)
            checks.append(("ninebot.sn", True, "已配置"))
        except ConfigError as exc:
            checks.append(("ninebot.sn", False, str(exc)))

    if prefix:
        dummy_cfg = cfg or {"ninebot": {"sn": "dummy"}}
        ctx = Context(dummy_cfg, debug=debug)
        whoami = ninecli_call(ctx, ["whoami", "--json"], parse_json=True, retries=1)
        checks.append(("ninecli 登录", whoami.returncode == 0 and not whoami.error, whoami.error or "有效"))

    amap = bool((os.environ.get("AMAP_WEBSERVICE_KEY") or os.environ.get("AMAP_WEB_KEY") or "").strip())
    checks.append(("AMAP_WEBSERVICE_KEY", True, "已配置" if amap else "未配置（可选）"))

    for name, ok, detail in checks:
        print(f"{'✅' if ok else '❌'} {name}: {detail}")
    required = [item for item in checks if item[0] in {"Python", "ninecli", "配置文件", "ninebot.sn", "ninecli 登录"}]
    return 0 if required and all(ok for _, ok, _ in required) else 2


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ninebot read-only vehicle report")
    parser.add_argument("--version", action="version", version=f"ninebot-show-skill {VERSION}")
    parser.add_argument("--config", help=f"配置文件路径，默认 {DEFAULT_CONFIG}")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON（包含 report 字段）")
    parser.add_argument("--check", action="store_true", help="只检查环境、配置和 ninecli 登录")
    parser.add_argument("--no-weather", action="store_true", help="跳过天气查询")
    parser.add_argument("--privacy", choices=sorted(PRIVACY_MODES), help="临时覆盖位置隐私模式")
    parser.add_argument("--debug", action="store_true", help="把警告同时输出到 stderr")
    return parser


def main() -> int:
    args = make_parser().parse_args()
    cfg_path = resolve_config_path(args.config)

    if args.check:
        return check_environment(cfg_path, debug=args.debug)

    try:
        cfg = load_config(cfg_path)
    except ConfigError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2

    ctx = Context(cfg, debug=args.debug)
    result, code = collect_report(cfg, args, ctx)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["report"])
    return code


if __name__ == "__main__":
    raise SystemExit(main())
