#!/usr/bin/env python3
"""
Narodmon daily summary — generates a chart of sensor readings for the last 24h.
Sends the chart as a photo to Telegram via Bot API.

Dependencies: matplotlib
Configuration: reads from a JSON config file (path via --config or default narodmon_config.json)
"""
import json
import hashlib
import urllib.request
import urllib.error
import sys
import os
import argparse
from datetime import datetime, timezone, timedelta

def load_config(path):
    """Load configuration from JSON file."""
    with open(path) as f:
        return json.load(f)

def parse_args():
    p = argparse.ArgumentParser(description="Narodmon daily sensor summary")
    p.add_argument("--config", default="narodmon_config.json", help="Path to config JSON")
    return p.parse_args()

# ─── API Functions ───

def api_request(api_url, api_key, uuid_val, lang, cmd, extra_params=None):
    """Send POST request to narodmon API."""
    payload = {"cmd": cmd, "uuid": uuid_val, "lang": lang}
    if extra_params:
        payload.update(extra_params)

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "User-Agent": "HermesNarodmon",
            "Narodmon-Api-Key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"API error {e.code}: {body}", file=sys.stderr)
        return json.loads(body) if body.strip() else {}
    except Exception as e:
        print(f"Request error: {e}", file=sys.stderr)
        return {"error": str(e)}


def authorize(cfg):
    """Authenticate user (once per 24h max)."""
    password_md5 = hashlib.md5(cfg["password"].encode()).hexdigest()
    auth_hash = hashlib.md5((cfg["uuid"] + password_md5).encode()).hexdigest()
    result = api_request(cfg["api_url"], cfg["api_key"], cfg["uuid"], cfg["lang"],
                         "userLogon", {"login": cfg["login"], "hash": auth_hash})
    if "error" in result:
        print(f"Auth failed: {result}", file=sys.stderr)
        return False
    print(f"Authorized: uid={result.get('uid')}, login={result.get('login')}", file=sys.stderr)
    return True


def get_history(cfg, sensor_ids, period="day", offset=0):
    result = api_request(cfg["api_url"], cfg["api_key"], cfg["uuid"], cfg["lang"],
                         "sensorsHistory", {"sensors": sensor_ids, "period": period, "offset": offset})
    if "error" in result:
        print(f"History error: {result}", file=sys.stderr)
        return None
    return result


def get_current_values(cfg, sensor_ids):
    result = api_request(cfg["api_url"], cfg["api_key"], cfg["uuid"], cfg["lang"],
                         "sensorsValues", {"sensors": sensor_ids, "trends": 1})
    if "error" in result:
        print(f"Values error: {result}", file=sys.stderr)
        return None
    return result


# ─── Chart Generation ───

def generate_chart(cfg, history_data, current_data):
    """Generate PNG chart of sensor readings for the last 24h."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime as dt

    sensors = cfg["sensors"]
    utc_offset = cfg.get("utc_offset", 3)
    output_path = cfg.get("output_path", "/tmp/narodmon_daily.png")

    sensors_info = {}
    series = {}
    for s in history_data.get("sensors", []):
        sid = s["id"]
        sensors_info[sid] = {
            "name": s.get("name", f"S{sid}"),
            "type": s.get("type", 255),
            "unit": s.get("unit", ""),
        }
        points = [(p["time"], p["value"]) for p in history_data.get("data", []) if p["id"] == sid]
        if points:
            series[sid] = points

    current = {}
    if current_data:
        for s in current_data.get("sensors", []):
            current[s["id"]] = {"value": s["value"], "trend": s.get("trend", 0), "time": s.get("time", 0)}

    tz = timezone(timedelta(hours=utc_offset))
    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    ax2 = ax1.twinx()

    all_temp_vals = []
    for s in sensors:
        if not s.get("secondary") and s["id"] in series:
            all_temp_vals.extend([v for _, v in series[s["id"]]])
    if all_temp_vals:
        ax1.set_ylim(min(all_temp_vals) - 2.5, max(all_temp_vals) + 2.5)
    ax1.margins(x=0.03)

    temp_max_points = []
    for idx, sensor in enumerate(sensors):
        sid = sensor["id"]
        if sid not in series:
            continue
        points = series[sid]
        times = [dt.fromtimestamp(t, tz=tz) for t, _ in points]
        values = [v for _, v in points]
        label = sensor["label"]
        color = sensor["color"]

        if sensor.get("secondary"):
            ax2.plot(times, values, color=color, linewidth=1.8, label=label, alpha=0.8)
            ax2.set_ylabel("Давление (mmHg)", color="#9C27B0", fontsize=11)
            ax2.tick_params(axis="y", labelcolor="#9C27B0")
            ax2.set_ylim(min(values) - 2, max(values) + 2)
        else:
            ax1.plot(times, values, color=color, linewidth=1.8, label=label, alpha=0.85)

            mn_val, mx_val = min(values), max(values)
            mn_idx, mx_idx = values.index(mn_val), values.index(mx_val)
            mn_time, mx_time = times[mn_idx], times[mx_idx]

            ax1.plot(mn_time, mn_val, "v", color=color, markersize=6, zorder=5)
            ax1.plot(mx_time, mx_val, "^", color=color, markersize=6, zorder=5)
            temp_max_points.append((mx_time, mx_val, idx, mn_val, mn_time))

            ax1.annotate(f"min {mn_val:.1f}°", xy=(mn_time, mn_val),
                         xytext=(0, -14), textcoords="offset points",
                         fontsize=8, color=color, fontweight="bold", ha="center", va="top",
                         arrowprops=dict(color=color, arrowstyle="-", lw=0.8))

    # Collision avoidance for max labels
    temp_max_points.sort(key=lambda x: x[0])
    x_offsets = {}
    for i, (mx_time, mx_val, idx, _, _) in enumerate(temp_max_points):
        x_off = 0
        if i > 0:
            prev_time = temp_max_points[i - 1][0]
            if (mx_time - prev_time).total_seconds() < 7200 and abs(mx_val - temp_max_points[i - 1][1]) < 3:
                x_off = 28
        if i < len(temp_max_points) - 1 and x_off == 0:
            next_time = temp_max_points[i + 1][0]
            if (next_time - mx_time).total_seconds() < 7200 and abs(mx_val - temp_max_points[i + 1][1]) < 3:
                x_off = -28
        x_offsets[idx] = x_off

    for mx_time, mx_val, idx, _, _ in temp_max_points:
        color = sensors[idx]["color"]
        ax1.annotate(f"max {mx_val:.1f}°", xy=(mx_time, mx_val),
                     xytext=(x_offsets.get(idx, 0), 14), textcoords="offset points",
                     fontsize=8, color=color, fontweight="bold", ha="center", va="bottom",
                     arrowprops=dict(color=color, arrowstyle="-", lw=0.8))

    today = dt.now(tz=tz).strftime("%d.%m.%Y")
    ax1.set_title(f"Показания датчиков за {today}", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Время", fontsize=10)
    ax1.set_ylabel("Температура (°C)", fontsize=11, color="#333")
    ax1.grid(True, alpha=0.25, linestyle="--")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=tz))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    fig.autofmt_xdate(rotation=35)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", framealpha=0.9, fontsize=10, ncol=2)

    summary_lines = []
    for sensor in sensors:
        sid = sensor["id"]
        info = sensors_info.get(sid, {})
        name = sensor["label"]
        unit = info.get("unit", "")
        if sid in series:
            vals = [v for _, v in series[sid]]
            mn, mx = min(vals), max(vals)
            cur = current.get(sid, {}).get("value", vals[-1])
            trend = current.get(sid, {}).get("trend", 0)
            arrow = "↑" if trend > 0.5 else ("↓" if trend < -0.5 else "→")
            summary_lines.append(f"{name}: {cur:.1f}{unit} {arrow}  (min {mn:.1f}, max {mx:.1f})")
        else:
            summary_lines.append(f"{name}: нет данных")

    fig.text(0.5, 0.01, "  •  ".join(summary_lines), ha="center", fontsize=9, color="#555", style="italic")
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(output_path, dpi=150, facecolor="white", bbox_inches="tight")
    plt.close()
    print(f"Chart saved: {output_path}", file=sys.stderr)
    return output_path


# ─── Telegram Delivery ───

def send_telegram_photo(cfg, photo_path, caption):
    """Send photo to Telegram via Bot API."""
    tg = cfg.get("telegram", {})
    token = tg.get("token", "")
    chat_id = tg.get("chat_id", "")
    if not token or not chat_id:
        print("Telegram credentials not in config", file=sys.stderr)
        return False

    import mimetypes
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    with open(photo_path, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(photo_path)
    mime = mimetypes.guess_type(photo_path)[0] or "image/png"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f"{chat_id}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="caption"\r\n\r\n'
        f"{caption}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="{filename}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("ok"):
                print(f"Telegram: photo sent (message_id={result['result']['message_id']})", file=sys.stderr)
                return True
            print(f"Telegram error: {result}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Telegram send error: {e}", file=sys.stderr)
        return False


# ─── Main ───

def main():
    args = parse_args()
    cfg = load_config(args.config)

    if not authorize(cfg):
        print("Auth failed")
        sys.exit(1)

    sensor_ids = [s["id"] for s in cfg["sensors"]]
    history = get_history(cfg, sensor_ids, period="day", offset=0)
    if not history or "sensors" not in history:
        print("Failed to get sensor history")
        sys.exit(1)

    current = get_current_values(cfg, sensor_ids)
    chart_path = generate_chart(cfg, history, current)

    tz = timezone(timedelta(hours=cfg.get("utc_offset", 3)))
    today = datetime.now(tz=tz).strftime("%d.%m.%Y")
    send_telegram_photo(cfg, chart_path, f"Sensor readings for {today}")
    print(chart_path)


if __name__ == "__main__":
    main()
