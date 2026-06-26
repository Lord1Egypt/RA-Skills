#!/usr/bin/env python3
"""Generate a Weather Strip SVG widget from Open-Meteo data.

Usage: weather_strip.py [--lat LAT] [--lon LON] [--days DAYS] [--units fahrenheit|celsius]
                        [--schedule JSON] [--output FILE]
"""

import argparse
import json
import math
import urllib.request
from datetime import datetime


def moon_phase_fraction(dt):
    """Return moon phase as 0-1 (0=new, 0.5=full, 1=new again). Conway's approximation."""
    y = dt.year
    m = dt.month
    d = dt.day
    if m <= 2:
        y -= 1
        m += 12
    a = int(y / 100)
    b = int(a / 4)
    c = 2 - a + b
    e = int(365.25 * (y + 4716))
    f = int(30.6001 * (m + 1))
    jd = c + d + e + f - 1524.5
    days_since_new = (jd - 2451549.5) % 29.53059
    return days_since_new / 29.53059


def moon_phase_svg(fraction, cx, cy, r=8):
    """Generate an SVG moon phase circle. fraction: 0=new, 0.5=full."""
    # Map to illumination
    if fraction <= 0.5:
        illum = fraction * 2  # 0→1 (waxing)
        right_lit = True
    else:
        illum = (1 - fraction) * 2  # 1→0 (waning)
        right_lit = False
    
    # Draw the lit/dark parts
    # Full circle as dark background
    svg = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#2a2a3a" stroke="#555" stroke-width="0.5"/>'
    
    if illum < 0.01:
        # New moon — all dark
        return svg
    if illum > 0.99:
        # Full moon — all bright
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e8e4d4" stroke="#aaa" stroke-width="0.5"/>'
    
    # Partial illumination using an ellipse-based crescent
    # The lit part is a half-circle + elliptical curve
    kx = r * (1 - 2 * illum)  # control x for the inner edge
    
    if right_lit:
        # Right side lit: arc from top to bottom on right, inner curve back
        svg += (
            f'<path d="M{cx},{cy - r} '
            f'A{r},{r} 0 0 1 {cx},{cy + r} '
            f'A{abs(kx)},{r} 0 0 {"1" if illum > 0.5 else "0"} {cx},{cy - r}" '
            f'fill="#e8e4d4"/>'
        )
    else:
        # Left side lit
        svg += (
            f'<path d="M{cx},{cy - r} '
            f'A{r},{r} 0 0 0 {cx},{cy + r} '
            f'A{abs(kx)},{r} 0 0 {"0" if illum > 0.5 else "1"} {cx},{cy - r}" '
            f'fill="#e8e4d4"/>'
        )
    return svg

WMO_CODES = {
    0: ("☀️", "Clear"), 1: ("🌤️", "Mostly Clear"), 2: ("⛅", "Partly Cloudy"), 3: ("☁️", "Overcast"),
    45: ("🌫️", "Fog"), 48: ("🌫️", "Rime Fog"),
    51: ("🌦️", "Light Drizzle"), 53: ("🌦️", "Drizzle"), 55: ("🌧️", "Heavy Drizzle"),
    61: ("🌧️", "Light Rain"), 63: ("🌧️", "Rain"), 65: ("🌧️", "Heavy Rain"),
    71: ("🌨️", "Light Snow"), 73: ("🌨️", "Snow"), 75: ("❄️", "Heavy Snow"),
    80: ("🌦️", "Light Showers"), 81: ("🌧️", "Showers"), 82: ("⛈️", "Heavy Showers"),
    95: ("⛈️", "Thunderstorm"), 96: ("⛈️", "T-storm + Hail"), 99: ("⛈️", "T-storm + Heavy Hail"),
}

def wmo(code):
    return WMO_CODES.get(code, ("❓", "Unknown"))

def fetch_weather(lat, lon, days, units):
    temp_params = "&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch" if units == "fahrenheit" else ""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,"
        f"weather_code,cloud_cover,wind_speed_10m,uv_index,is_day,relative_humidity_2m,dew_point_2m"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,"
        f"apparent_temperature_min,precipitation_sum,precipitation_probability_max,"
        f"sunrise,sunset,uv_index_max,wind_speed_10m_max"
        f"&forecast_days={days}&timezone=auto{temp_params}"
    )
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())

def fetch_multi_location(schedule, days, units):
    all_data = {}
    for loc in schedule:
        data = fetch_weather(loc["lat"], loc["lon"], days, units)
        all_data[loc["name"]] = data

    ranges = []
    for loc in schedule:
        if "ranges" in loc:
            for r in loc["ranges"]:
                ranges.append((datetime.fromisoformat(r[0]), datetime.fromisoformat(r[1]), loc["name"]))
        elif "dates" in loc:
            for d in loc["dates"]:
                dt = datetime.fromisoformat(d)
                ranges.append((dt.replace(hour=0, minute=0), dt.replace(hour=23, minute=59), loc["name"]))
    ranges.sort(key=lambda x: x[0])

    def city_for_time(t_str):
        t = datetime.fromisoformat(t_str)
        for start, end, name in ranges:
            if start <= t <= end:
                return name
        return None

    def primary_city_for_date(date_str):
        d = datetime.fromisoformat(date_str)
        city_hours = {}
        for h in range(24):
            t = d.replace(hour=h)
            for start, end, name in ranges:
                if start <= t <= end:
                    city_hours[name] = city_hours.get(name, 0) + 1
                    break
        if not city_hours:
            return None
        return max(city_hours, key=city_hours.get)

    base_city = schedule[0]["name"]
    base = all_data[base_city]
    hourly_keys = [k for k in base["hourly"].keys() if k != "time"]
    filtered_hourly = {"time": []}
    for k in hourly_keys:
        filtered_hourly[k] = []
    filtered_hourly_cities = []

    for i, t in enumerate(base["hourly"]["time"]):
        city = city_for_time(t)
        if city is None:
            continue
        filtered_hourly["time"].append(t)
        filtered_hourly_cities.append(city)
        src = all_data[city]
        try:
            src_idx = src["hourly"]["time"].index(t)
        except (ValueError, IndexError):
            for k in hourly_keys:
                filtered_hourly[k].append(base["hourly"][k][i])
            continue
        for k in hourly_keys:
            filtered_hourly[k].append(src["hourly"][k][src_idx])

    daily_keys = [k for k in base["daily"].keys() if k != "time"]
    merged_daily = {"time": list(base["daily"]["time"])}
    for k in daily_keys:
        merged_daily[k] = list(base["daily"][k])
    daily_cities = []

    for i, d in enumerate(base["daily"]["time"]):
        city = primary_city_for_date(d)
        daily_cities.append(city or base_city)
        if city and city != base_city:
            src = all_data[city]
            try:
                src_idx = src["daily"]["time"].index(d)
            except (ValueError, IndexError):
                continue
            for k in daily_keys:
                merged_daily[k][i] = src["daily"][k][src_idx]

    return {
        "hourly": filtered_hourly,
        "hourly_units": base.get("hourly_units", {}),
        "daily": merged_daily,
        "daily_units": base.get("daily_units", {}),
        "_hourly_cities": filtered_hourly_cities,
        "_daily_cities": daily_cities,
    }


def smooth_path(points, tension=0.3):
    if len(points) < 2:
        return ""
    if len(points) == 2:
        return f"M{points[0][0]:.1f},{points[0][1]:.1f}L{points[1][0]:.1f},{points[1][1]:.1f}"
    path = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    for i in range(1, len(points)):
        p0 = points[max(0, i - 2)]
        p1 = points[i - 1]
        p2 = points[i]
        p3 = points[min(len(points) - 1, i + 1)]
        cp1x = p1[0] + (p2[0] - p0[0]) * tension
        cp1y = p1[1] + (p2[1] - p0[1]) * tension
        cp2x = p2[0] - (p3[0] - p1[0]) * tension
        cp2y = p2[1] - (p3[1] - p1[1]) * tension
        path += f" C{cp1x:.1f},{cp1y:.1f} {cp2x:.1f},{cp2y:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return path


def smooth_area_path(points_top, y_bottom):
    if len(points_top) < 2:
        return ""
    line = smooth_path(points_top)
    last = points_top[-1]
    first = points_top[0]
    line += f" L{last[0]:.1f},{y_bottom:.1f} L{first[0]:.1f},{y_bottom:.1f} Z"
    return line


def generate_html(data, units="fahrenheit"):
    hourly = data["hourly"]
    daily = data["daily"]
    hourly_cities = data.get("_hourly_cities", [])
    daily_cities = data.get("_daily_cities", [])
    unit_sym = "°F" if units == "fahrenheit" else "°C"
    now = datetime.now()

    n = len(hourly["time"])
    if n == 0:
        return "<div>No weather data available</div>"

    # --- Dimensions (narrower: ~24px per hour = one day in ~576px phone width) ---
    cell_w = 14
    svg_w = n * cell_w

    # Vertical layout
    uv_bar_y = 0
    uv_bar_h = 6
    city_label_y = 20
    time_axis_y = 34
    chart_top = 48
    chart_bottom = 200
    rain_top = 210
    rain_bottom = 260
    sunrise_y = 275
    svg_h = 300

    # --- Data arrays ---
    temps = hourly["temperature_2m"]
    dews = hourly.get("dew_point_2m", [t - 10 for t in temps])
    clouds = hourly["cloud_cover"]
    rain_probs = hourly["precipitation_probability"]
    precips = hourly["precipitation"]
    uv_vals = hourly["uv_index"]
    is_days = hourly["is_day"]
    weather_codes = hourly["weather_code"]
    winds = hourly["wind_speed_10m"]
    humids = hourly["relative_humidity_2m"]
    feels = hourly["apparent_temperature"]

    # Fixed scale: 0-110°F (or -18 to 43°C)
    if units == "fahrenheit":
        temp_min = 0
        temp_max = 110
    else:
        temp_min = -18
        temp_max = 43
    temp_range = temp_max - temp_min

    def temp_y(t):
        return chart_bottom - ((t - temp_min) / temp_range) * (chart_bottom - chart_top)

    def rain_y(pct):
        return rain_bottom - (pct / 100) * (rain_bottom - rain_top)

    def x_at(i):
        return i * cell_w + cell_w / 2

    # --- Padding for scrubber scroll ---
    # pad_left = small (scrubber is at 40px, so graph data starts at x=40 in SVG)
    # pad_right = screen width so last hour can reach scrubber
    # Scrubber is fixed at 40px from left. When scroll=0, the SVG x=0 is at the left edge.
    # For the first data point (at pad_left in SVG) to appear under the scrubber at scroll=0,
    # pad_left should = 40 (scrubber pos). That's already correct.
    # For the LAST data point to reach the scrubber, we need:
    #   pad_right >= viewport_width - 40
    # Phone viewport is ~390px, so pad_right needs to be ~350px minimum.
    # But the REAL issue: when fully scrolled LEFT (scroll=0), 
    # the first hour is at SVG x=40, which IS at the scrubber.
    # When scrolled RIGHT to max, the last hour should be at the scrubber.
    # Max scroll = svg_total_width - viewport_width
    # Last hour SVG x = pad_left + (n-1)*cell_w
    # We need: last_hour_x - max_scroll = 40 (scrubber pos)
    # So: pad_right = viewport - 40... but we don't know viewport.
    # Solution: just make pad_right very large.
    pad_left = 40    # matches scrubber x position
    pad_right = 500  # viewport-width of padding so last hour reaches scrubber
    svg_w = n * cell_w + pad_left + pad_right

    def x_padded(i):
        return pad_left + i * cell_w + cell_w / 2

    # Override x_at to include padding
    x_at_orig = x_at
    x_at = x_padded

    elements = []

    # --- Build sunrise/sunset lookup per date ---
    sr_ss_map = {}
    for si, sd in enumerate(daily.get("time", [])):
        sr = daily.get("sunrise", [None])[si]
        ss = daily.get("sunset", [None])[si]
        sr_h = None
        ss_h = None
        if sr:
            sr_dt = datetime.fromisoformat(sr)
            sr_h = sr_dt.hour + sr_dt.minute / 60
        if ss:
            ss_dt = datetime.fromisoformat(ss)
            ss_h = ss_dt.hour + ss_dt.minute / 60
        sr_ss_map[sd] = (sr_h, ss_h)

    # --- Sky background: one smooth horizontal gradient ---
    # Build color stops across all hours
    def sky_color_at(i):
        """Return RGB tuple for sky at hour index i."""
        t = datetime.fromisoformat(hourly["time"][i])
        h = t.hour + 0.5
        date_str = hourly["time"][i].split("T")[0]
        sr_hour, ss_hour = sr_ss_map.get(date_str, (6.5, 18.5))
        sr_hour = sr_hour or 6.5
        ss_hour = ss_hour or 18.5

        # Midnight blue → sky blue, pure RGB interpolation (no green)
        night = (25, 35, 70)       # softer navy
        dawn = (55, 70, 120)      # intermediate: still blue-purple
        day = (95, 155, 215)
        dusk = (55, 60, 110)      # intermediate: dusky blue-purple

        # 3-hour transition windows (1.5hr each side of sunrise/sunset)
        if h <= sr_hour - 1.5:
            return night
        elif h <= sr_hour + 1.5:
            # 3hr sunrise transition: night → dawn → day
            t = (h - (sr_hour - 1.5)) / 3.0  # 0→1 over 3 hours
            t = t * t * (3 - 2 * t)  # smoothstep
            if t < 0.5:
                t2 = t * 2
                return tuple(int(night[j] + (dawn[j] - night[j]) * t2) for j in range(3))
            else:
                t2 = (t - 0.5) * 2
                return tuple(int(dawn[j] + (day[j] - dawn[j]) * t2) for j in range(3))
        elif h <= ss_hour - 1.5:
            return day
        elif h <= ss_hour + 1.5:
            # 3hr sunset transition: day → dusk → night
            t = (h - (ss_hour - 1.5)) / 3.0
            t = t * t * (3 - 2 * t)
            if t < 0.5:
                t2 = t * 2
                return tuple(int(day[j] + (dusk[j] - day[j]) * t2) for j in range(3))
            else:
                t2 = (t - 0.5) * 2
                return tuple(int(dusk[j] + (night[j] - dusk[j]) * t2) for j in range(3))
        else:
            return night

    # Build SVG with per-column rects colored by interpolated sky
    # Padding areas get night color
    night_color = "rgb(25,35,70)"
    elements.append(
        f'<rect x="0" y="0" width="{pad_left}" height="{svg_h}" fill="{night_color}" />'
    )
    elements.append(
        f'<rect x="{pad_left + n * cell_w}" y="0" width="{pad_right}" height="{svg_h}" fill="{night_color}" />'
    )
    # Render sky with sub-hour slices (4 per hour) for smooth gradients
    slices_per_hour = 4
    slice_w = cell_w / slices_per_hour
    for i in range(n):
        for s in range(slices_per_hour):
            # Interpolate between this hour and next hour
            frac = s / slices_per_hour
            r1, g1, b1 = sky_color_at(i)
            r2, g2, b2 = sky_color_at(min(i + 1, n - 1))
            r = int(r1 + (r2 - r1) * frac)
            g = int(g1 + (g2 - g1) * frac)
            b = int(b1 + (b2 - b1) * frac)
            x = pad_left + i * cell_w + s * slice_w
            elements.append(
                f'<rect x="{x:.1f}" y="0" width="{slice_w + 0.5:.1f}" height="{svg_h}" fill="rgb({r},{g},{b})" />'
            )

    # --- UV bar across top (only visible at moderate+ UV) ---
    for i in range(n):
        uv = uv_vals[i]
        x = pad_left + i * cell_w
        if uv <= 2:
            continue  # skip low UV — invisible
        elif uv <= 5:
            color = "rgba(240,210,60,0.5)"    # moderate - yellow
        elif uv <= 7:
            color = "rgba(240,150,30,0.7)"    # high - orange
        elif uv <= 10:
            color = "rgba(220,50,50,0.8)"     # very high - red
        else:
            color = "rgba(180,30,180,0.85)"   # extreme - purple
        elements.append(
            f'<rect x="{x}" y="{uv_bar_y}" width="{cell_w}" height="{uv_bar_h}" fill="{color}" />'
        )

    # --- Cloud cover area graph (line + semi-transparent fill, 0-100% scale) ---
    # 0% at chart_bottom, 100% at chart_top
    cloud_points = []
    for i in range(n):
        x = x_at(i)
        cy = chart_bottom - (clouds[i] / 100) * (chart_bottom - chart_top)
        cloud_points.append((x, cy))
    if cloud_points:
        cloud_area = smooth_area_path(cloud_points, chart_bottom)
        cloud_line = smooth_path(cloud_points)
        elements.append(f'<path d="{cloud_area}" fill="rgba(200,210,230,0.15)" />')
        elements.append(f'<path d="{cloud_line}" fill="none" stroke="rgba(200,210,230,0.35)" stroke-width="1" />')

    # --- Rain amount bar graph (opaque light blue, 0-2 in/hr scale) ---
    for i in range(n):
        amt = min(precips[i], 2.0)
        if amt > 0.001:
            bar_h = (amt / 2.0) * (rain_bottom - rain_top)
            x = pad_left + i * cell_w
            y = rain_bottom - bar_h
            elements.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{bar_h}" '
                f'fill="#7cb9e8" />'
            )
            if amt >= 0.05 and i % 3 == 0:
                elements.append(
                    f'<text x="{x_at(i)}" y="{y - 2}" text-anchor="middle" '
                    f'fill="#4a90d0" font-size="7" font-weight="600">{precips[i]:.2f}"</text>'
                )
    
    # --- Rain probability line (overlay on top of bars) ---
    rain_points = [(x_at(i), rain_y(rain_probs[i])) for i in range(n)]
    if rain_points:
        rain_line = smooth_path(rain_points)
        elements.append(f'<path d="{rain_line}" fill="none" stroke="rgba(40,80,160,0.7)" stroke-width="1.5" />')
        for i in range(n):
            if i % 8 == 0 and rain_probs[i] > 5:
                elements.append(
                    f'<text x="{x_at(i)}" y="{rain_y(rain_probs[i]) - 4}" text-anchor="middle" '
                    f'fill="#3868b0" font-size="9" font-weight="500">{rain_probs[i]}%</text>'
                )

    # --- Dew point line ---
    dew_points = [(x_at(i), temp_y(dews[i])) for i in range(n)]
    elements.append(
        f'<path d="{smooth_path(dew_points)}" fill="none" stroke="rgba(180,140,220,0.5)" '
        f'stroke-width="1.5" stroke-dasharray="4,3" />'
    )

    # --- Temperature line ---
    temp_points = [(x_at(i), temp_y(temps[i])) for i in range(n)]
    elements.append(
        f'<path d="{smooth_path(temp_points)}" fill="none" stroke="#e06090" stroke-width="2.5" />'
    )

    # --- Dots and labels ---
    for i in range(n):
        x = x_at(i)
        y = temp_y(temps[i])
        elements.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#e06090" />')
        if i % 4 == 0:
            elements.append(
                f'<text x="{x}" y="{y - 7}" text-anchor="middle" fill="#f0f0f0" '
                f'font-size="9" font-weight="600">{temps[i]:.0f}°</text>'
            )
    for i in range(n):
        if i % 6 == 3:
            x = x_at(i)
            y = temp_y(dews[i])
            elements.append(
                f'<text x="{x}" y="{y + 13}" text-anchor="middle" fill="rgba(180,140,220,0.7)" '
                f'font-size="8">{dews[i]:.0f}°</text>'
            )

    # --- Time axis ---
    for i in range(n):
        x = x_at(i)
        t = datetime.fromisoformat(hourly["time"][i])
        if t.hour == 0:
            label = t.strftime("%a")
            elements.append(
                f'<line x1="{pad_left + i * cell_w}" y1="{chart_top}" x2="{pad_left + i * cell_w}" y2="{rain_bottom}" '
                f'stroke="rgba(255,255,255,0.15)" stroke-width="1" />'
            )
            elements.append(
                f'<text x="{x}" y="{time_axis_y}" text-anchor="middle" fill="#fff" '
                f'font-size="11" font-weight="700">{label}</text>'
            )
        elif t.hour % 3 == 0:
            h = t.hour
            ampm = "a" if h < 12 else "p"
            h12 = h % 12 or 12
            elements.append(
                f'<text x="{x}" y="{time_axis_y}" text-anchor="middle" fill="#777" '
                f'font-size="9">{h12}{ampm}</text>'
            )

    # --- City labels ---
    if hourly_cities:
        for i in range(n):
            show = (i == 0) or (hourly_cities[i] != hourly_cities[i - 1])
            if show:
                if i > 0:
                    elements.append(
                        f'<line x1="{pad_left + i * cell_w}" y1="0" x2="{pad_left + i * cell_w}" y2="{svg_h}" '
                        f'stroke="#f0c040" stroke-width="1.5" stroke-dasharray="4,2" />'
                    )
                elements.append(
                    f'<text x="{pad_left + i * cell_w + 3}" y="{city_label_y}" fill="#f0c040" '
                    f'font-size="9" font-weight="700">{hourly_cities[i]}</text>'
                )

    # --- Sunrise/sunset markers ---
    for sr in daily.get("sunrise", []):
        if not sr: continue
        sr_dt = datetime.fromisoformat(sr)
        for i, t in enumerate(hourly["time"]):
            ht = datetime.fromisoformat(t)
            if ht.date() == sr_dt.date() and ht.hour == sr_dt.hour:
                elements.append(
                    f'<text x="{x_at(i)}" y="{sunrise_y}" text-anchor="middle" '
                    f'fill="#e8a040" font-size="9">🌅{sr_dt.strftime("%-I:%M")}</text>'
                )
                break
    for ss in daily.get("sunset", []):
        if not ss: continue
        ss_dt = datetime.fromisoformat(ss)
        for i, t in enumerate(hourly["time"]):
            ht = datetime.fromisoformat(t)
            if ht.date() == ss_dt.date() and ht.hour == ss_dt.hour:
                x = x_at(i)
                elements.append(
                    f'<text x="{x}" y="{sunrise_y}" text-anchor="middle" '
                    f'fill="#c06030" font-size="9">🌇{ss_dt.strftime("%-I:%M")}</text>'
                )
                # Moon phase at sunset
                phase = moon_phase_fraction(ss_dt)
                elements.append(moon_phase_svg(phase, x, sunrise_y + 14, r=7))
                break

    # --- "Now" marker ---
    now_idx = 0
    for i, t in enumerate(hourly["time"]):
        dt = datetime.fromisoformat(t)
        if dt.hour == now.hour and dt.day == now.day:
            now_idx = i
            x = x_at(i)
            elements.append(
                f'<line x1="{x}" y1="{chart_top}" x2="{x}" y2="{rain_bottom}" '
                f'stroke="#ff6040" stroke-width="1.5" opacity="0.8" />'
            )
            elements.append(
                f'<text x="{x}" y="{chart_top - 3}" text-anchor="middle" '
                f'fill="#ff6040" font-size="8" font-weight="700">NOW</text>'
            )
            break

    # --- Current conditions ---
    curr_temp = temps[now_idx]
    curr_feels = feels[now_idx]
    curr_wind = winds[now_idx]
    curr_humidity = humids[now_idx]
    curr_uv = uv_vals[now_idx]
    curr_code = weather_codes[now_idx]
    curr_cloud = clouds[now_idx]
    curr_dew = dews[now_idx]
    curr_rain = rain_probs[now_idx]
    curr_emoji, curr_desc = wmo(curr_code)
    wind_unit = "mph" if units == "fahrenheit" else "km/h"

    # --- JSON data for scrubber ---
    scrubber_data = []
    for i in range(n):
        t = datetime.fromisoformat(hourly["time"][i])
        scrubber_data.append({
            "time": t.strftime("%-I:%M %p"),
            "day": t.strftime("%a %-m/%-d"),
            "temp": f"{temps[i]:.0f}{unit_sym}",
            "feels": f"{feels[i]:.0f}°",
            "dew": f"{dews[i]:.0f}°",
            "cloud": f"{clouds[i]}%",
            "rain": f"{rain_probs[i]}%",
            "wind": f"{winds[i]:.0f} {wind_unit}",
            "uv": f"{uv_vals[i]:.0f}",
            "humidity": f"{humids[i]}%",
            "city": hourly_cities[i] if i < len(hourly_cities) else "",
        })

    # --- Daily strip ---
    n_days = len(daily["time"])
    day_cell_w = max(46, 340 // n_days)
    daily_w = n_days * day_cell_w
    daily_h = 100

    day_hi = daily["temperature_2m_max"]
    day_lo = daily["temperature_2m_min"]
    day_all = day_hi + day_lo
    day_tmin = min(day_all) - 2
    day_tmax = max(day_all) + 2
    day_trange = max(day_tmax - day_tmin, 10)

    def day_temp_y(t):
        return 80 - ((t - day_tmin) / day_trange) * 45

    hi_pts = [(i * day_cell_w + day_cell_w / 2, day_temp_y(day_hi[i])) for i in range(n_days)]
    lo_pts = [(i * day_cell_w + day_cell_w / 2, day_temp_y(day_lo[i])) for i in range(n_days)]

    dsvg = []
    # Band fill
    if len(hi_pts) >= 2:
        hi_path = smooth_path(hi_pts)
        lo_rev = smooth_path(list(reversed(lo_pts)))
        band = hi_path + " L" + lo_rev[1:] + " Z"
        dsvg.append(f'<path d="{band}" fill="rgba(224,96,144,0.1)" />')

    dsvg.append(f'<path d="{smooth_path(hi_pts)}" fill="none" stroke="#e06090" stroke-width="2" />')
    dsvg.append(f'<path d="{smooth_path(lo_pts)}" fill="none" stroke="rgba(180,140,220,0.5)" stroke-width="1.5" stroke-dasharray="4,3" />')

    for i in range(n_days):
        x = i * day_cell_w + day_cell_w / 2
        d = datetime.fromisoformat(daily["time"][i])
        emoji, _ = wmo(daily["weather_code"][i])
        precip_p = daily["precipitation_probability_max"][i]
        city = daily_cities[i] if i < len(daily_cities) else ""

        dsvg.append(f'<text x="{x}" y="14" text-anchor="middle" fill="#ccc" font-size="11" font-weight="600">{d.strftime("%a")}</text>')
        if city and (i == 0 or daily_cities[i] != daily_cities[i-1]):
            dsvg.append(f'<text x="{x}" y="25" text-anchor="middle" fill="#f0c040" font-size="8" font-weight="700">{city}</text>')

        hy = day_temp_y(day_hi[i])
        ly = day_temp_y(day_lo[i])
        dsvg.append(f'<circle cx="{x}" cy="{hy}" r="2.5" fill="#e06090" />')
        dsvg.append(f'<text x="{x}" y="{hy - 5}" text-anchor="middle" fill="#f0f0f0" font-size="10" font-weight="600">{day_hi[i]:.0f}°</text>')
        dsvg.append(f'<circle cx="{x}" cy="{ly}" r="2" fill="rgba(180,140,220,0.6)" />')
        dsvg.append(f'<text x="{x}" y="{ly + 13}" text-anchor="middle" fill="#999" font-size="9">{day_lo[i]:.0f}°</text>')
        if precip_p > 10:
            dsvg.append(f'<text x="{x}" y="{ly + 24}" text-anchor="middle" fill="#5b9bd5" font-size="8">💧{precip_p}%</text>')

    # --- Assemble ---
    # Unique ID for this widget instance
    wid = f"ws_{id(data) % 100000}"

    html = f'''<div class="weather-strip-widget" id="{wid}">
  <style>
    .weather-strip-widget {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro", "Segoe UI", system-ui, sans-serif;
      background: linear-gradient(160deg, hsl(225,30%,13%), hsl(235,25%,18%));
      border-radius: 16px;
      padding: 16px;
      color: #e0e0e0;
      margin-bottom: 24px;
      overflow: hidden;
      -webkit-user-select: none;
      user-select: none;
    }}
    .ws-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .ws-current-temp {{
      font-size: 46px;
      font-weight: 300;
      line-height: 1;
      color: #fff;
    }}
    .ws-current-desc {{
      font-size: 13px;
      color: #aaa;
      margin-top: 2px;
    }}
    .ws-badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 6px;
    }}
    .ws-badge {{
      padding: 2px 7px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 600;
      background: rgba(255,255,255,0.08);
    }}
    .ws-badge-rain {{ color: #5b9bd5; }}
    .ws-badge-uv {{ color: #6ecf6e; }}
    .ws-badge-wind {{ color: #e8a040; }}
    .ws-meta {{
      display: flex;
      gap: 14px;
    }}
    .ws-meta-item {{ text-align: center; }}
    .ws-meta-value {{ font-size: 15px; color: #ccc; font-weight: 500; }}
    .ws-meta-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #777; }}
    .ws-scroll {{
      position: relative;
      overflow-x: auto;
      margin: 0 -16px;
      padding: 0 16px;
      scrollbar-width: thin;
      scrollbar-color: #333 transparent;
      cursor: crosshair;
    }}
    .ws-scroll::-webkit-scrollbar {{ height: 3px; }}
    .ws-scroll::-webkit-scrollbar-thumb {{ background: #444; border-radius: 2px; }}
    .ws-scroll svg {{ display: block; }}
    .ws-divider {{
      height: 1px;
      background: rgba(255,255,255,0.06);
      margin: 12px 0;
    }}
    .ws-section-label {{
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #555;
      margin-bottom: 6px;
      font-weight: 600;
    }}
    /* Scrubber - fixed position */
    .ws-scroll-wrap {{
      position: relative;
    }}
    .ws-scrubber {{
      position: absolute;
      top: 0;
      left: 40px;
      width: 2px;
      height: 100%;
      background: rgba(255,255,255,0.6);
      pointer-events: none;
      z-index: 10;
    }}
    .ws-scrubber::before {{
      content: '';
      position: absolute;
      top: -2px;
      left: -3px;
      width: 8px;
      height: 8px;
      background: #fff;
      border-radius: 50%;
    }}
    .ws-scrubber::after {{
      content: '';
      position: absolute;
      bottom: -2px;
      left: -3px;
      width: 8px;
      height: 8px;
      background: #fff;
      border-radius: 50%;
    }}
    .ws-scrubber-tooltip {{
      position: absolute;
      top: 4px;
      left: 12px;
      background: rgba(15,17,30,0.92);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 10px;
      padding: 6px 9px;
      font-size: 11px;
      line-height: 1.5;
      color: #ddd;
      white-space: nowrap;
      pointer-events: none;
      z-index: 11;
    }}
    .ws-scrubber-tooltip .ws-tt-time {{
      font-weight: 700;
      color: #fff;
      font-size: 12px;
      margin-bottom: 2px;
    }}
    .ws-scrubber-tooltip .ws-tt-city {{
      color: #f0c040;
      font-weight: 600;
      font-size: 10px;
    }}
    .ws-scrubber-tooltip .ws-tt-row {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
    }}
    .ws-scrubber-tooltip .ws-tt-label {{ color: #888; }}
    .ws-scrubber-tooltip .ws-tt-val {{ font-weight: 600; }}
    .ws-tt-temp {{ color: #e06090; }}
    .ws-tt-dew {{ color: #b48cdc; }}
    .ws-tt-rain {{ color: #5b9bd5; }}
    .ws-tt-wind {{ color: #e8a040; }}
    .ws-tt-uv {{ color: #6ecf6e; }}
  </style>

  <div class="ws-header">
    <div>
      <div class="ws-current-temp">{curr_temp:.0f}{unit_sym}</div>
      <div class="ws-current-desc">{curr_emoji} {curr_desc}</div>
      <div class="ws-badges">
        <span class="ws-badge ws-badge-rain">🌧️ {curr_rain}% rain</span>
        <span class="ws-badge ws-badge-uv">☀️ UV {curr_uv:.0f}</span>
        <span class="ws-badge ws-badge-wind">💨 {curr_wind:.0f} {wind_unit}</span>
      </div>
    </div>
    <div class="ws-meta">
      <div class="ws-meta-item">
        <div class="ws-meta-value">{curr_feels:.0f}°</div>
        <div class="ws-meta-label">Feels Like</div>
      </div>
      <div class="ws-meta-item">
        <div class="ws-meta-value">{curr_humidity}%</div>
        <div class="ws-meta-label">Humidity</div>
      </div>
    </div>
  </div>

  <div class="ws-section-label">Hourly — scroll to scrub →</div>
  <div class="ws-scroll-wrap">
    <div class="ws-scrubber" id="{wid}_scrubber">
      <div class="ws-scrubber-tooltip" id="{wid}_tooltip"></div>
    </div>
    <div class="ws-scroll" id="{wid}_scroll">
      <svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg"
           style="font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
        {"".join(elements)}
      </svg>
    </div>
  </div>

  <div class="ws-divider"></div>
  <div class="ws-section-label">7-Day</div>
  <div class="ws-scroll">
    <svg width="{daily_w}" height="{daily_h}" viewBox="0 0 {daily_w} {daily_h}" xmlns="http://www.w3.org/2000/svg"
         style="font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
      {"".join(dsvg)}
    </svg>
  </div>

  <script>
  (function() {{
    const data = {json.dumps(scrubber_data)};
    const cellW = {cell_w};
    const scroll = document.getElementById("{wid}_scroll");
    const scrubber = document.getElementById("{wid}_scrubber");
    const tooltip = document.getElementById("{wid}_tooltip");
    const SCRUBBER_X = 40; // fixed position from left edge
    const PAD_LEFT = {pad_left};

    function update() {{
      const x = scroll.scrollLeft + SCRUBBER_X - PAD_LEFT;
      const idx = Math.max(0, Math.min(data.length - 1, Math.floor(x / cellW)));
      const d = data[idx];

      tooltip.innerHTML = `
        <div class="ws-tt-time">${{d.day}} ${{d.time}}</div>
        ${{d.city ? '<div class="ws-tt-city">' + d.city + '</div>' : ''}}
        <div class="ws-tt-row"><span class="ws-tt-label">Temp</span><span class="ws-tt-val ws-tt-temp">${{d.temp}}</span></div>
        <div class="ws-tt-row"><span class="ws-tt-label">Feels</span><span class="ws-tt-val">${{d.feels}}</span></div>
        <div class="ws-tt-row"><span class="ws-tt-label">Dew</span><span class="ws-tt-val ws-tt-dew">${{d.dew}}</span></div>
        <div class="ws-tt-row"><span class="ws-tt-label">Cloud</span><span class="ws-tt-val">${{d.cloud}}</span></div>
        <div class="ws-tt-row"><span class="ws-tt-label">Rain</span><span class="ws-tt-val ws-tt-rain">${{d.rain}}</span></div>
        <div class="ws-tt-row"><span class="ws-tt-label">Wind</span><span class="ws-tt-val ws-tt-wind">${{d.wind}}</span></div>
        <div class="ws-tt-row"><span class="ws-tt-label">UV</span><span class="ws-tt-val ws-tt-uv">${{d.uv}}</span></div>
        <div class="ws-tt-row"><span class="ws-tt-label">Humid</span><span class="ws-tt-val">${{d.humidity}}</span></div>
      `;
    }}

    // Resize right padding so entire graph can scroll under the scrubber
    const svg = scroll.querySelector("svg");
    function resizePad() {{
      const vw = scroll.clientWidth;
      const dataWidth = PAD_LEFT + data.length * cellW;
      const neededWidth = dataWidth + vw;
      svg.setAttribute("width", neededWidth);
      svg.setAttribute("viewBox", "0 0 " + neededWidth + " " + svg.getAttribute("viewBox").split(" ")[3]);
    }}
    resizePad();
    window.addEventListener("resize", resizePad);
    
    scroll.addEventListener("scroll", update, {{passive: true}});
    update(); // initial
  }})();
  </script>
</div>'''

    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, default=37.75)
    parser.add_argument("--lon", type=float, default=-122.43)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--units", default="fahrenheit", choices=["fahrenheit", "celsius"])
    parser.add_argument("--schedule", help="JSON location schedule")
    parser.add_argument("--output", help="Write standalone HTML file")
    args = parser.parse_args()

    if args.schedule:
        data = fetch_multi_location(json.loads(args.schedule), args.days, args.units)
    else:
        data = fetch_weather(args.lat, args.lon, args.days, args.units)

    html = generate_html(data, args.units)

    if args.output:
        page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weather Strip</title>
<style>body {{ background: #12142a; padding: 16px; margin: 0; }}</style>
</head>
<body>
{html}
</body>
</html>'''
        with open(args.output, "w") as f:
            f.write(page)
        print(f"Written to {args.output}")
    else:
        print(html)

if __name__ == "__main__":
    main()
