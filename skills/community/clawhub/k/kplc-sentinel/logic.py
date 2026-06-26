import calendar
import logging
import os
import re
import sqlite3
import tempfile
from datetime import datetime, timedelta
from urllib.parse import urlparse

from init_db import get_db

logger = logging.getLogger(__name__)

KPLC_SCHEDULE_URL = "https://www.kplc.co.ke/storage/01KPWN6FYWZ5Q9MKXJDHW7EG1A.pdf"
ALLOWED_HOSTS = ("www.kplc.co.ke", "kplc.co.ke")
MAX_READING = 100_000  # sanity cap for meter readings (units)
MIN_READING_INTERVAL_SEC = 60  # ignore duplicate readings within 1 minute


# ── helpers ──────────────────────────────────────────────────────────────

def _validate_url(url):
    """Only allow HTTPS URLs on the KPLC domain."""
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS


# ── purchases ────────────────────────────────────────────────────────────

def add_purchase(token, units, amount, raw_text):
    with get_db() as conn:
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO purchases (token, units, amount, raw_text) VALUES (?, ?, ?, ?)",
                (token, units, amount, raw_text),
            )
        except sqlite3.IntegrityError:
            return False  # duplicate token

        # Update balance: add purchased units to the latest reading
        c.execute("SELECT balance FROM readings ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        new_balance = (row[0] if row else 0) + units
        c.execute(
            "INSERT INTO readings (balance, notes) VALUES (?, ?)",
            (new_balance, f"Auto: purchased {units} units"),
        )
    return True


# ── readings ─────────────────────────────────────────────────────────────

def add_reading(balance, notes=None):
    """Add a meter reading with validation and duplicate protection."""
    if balance < 0 or balance > MAX_READING:
        raise ValueError(f"Reading must be between 0 and {MAX_READING}")

    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT balance, timestamp FROM readings ORDER BY id DESC LIMIT 1")
        last = c.fetchone()
        if last:
            elapsed = (datetime.now() - datetime.strptime(last[1], "%Y-%m-%d %H:%M:%S")).total_seconds()
            if elapsed < MIN_READING_INTERVAL_SEC and abs(last[0] - balance) < 0.01:
                return  # duplicate, skip silently
        c.execute("INSERT INTO readings (balance, notes) VALUES (?, ?)", (balance, notes))


# ── burn rate ────────────────────────────────────────────────────────────

def calculate_burn_rate():
    """Weighted average burn rate (units/hour) with exponential decay."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp, balance, notes FROM readings ORDER BY timestamp ASC")
        readings = c.fetchall()

    if len(readings) < 2:
        return None

    fmt = "%Y-%m-%d %H:%M:%S"
    rates = []
    for i in range(1, len(readings)):
        old_ts, old_bal, _ = readings[i - 1]
        new_ts, new_bal, new_notes = readings[i]

        # Skip auto-purchase readings — they aren't consumption data points
        if new_notes and new_notes.startswith("Auto:"):
            continue

        hours = (datetime.strptime(new_ts, fmt) - datetime.strptime(old_ts, fmt)).total_seconds() / 3600.0
        if hours <= 0:
            continue

        burned = old_bal - new_bal
        if burned <= 0:
            continue

        rates.append(burned / hours)

    if not rates:
        return None

    decay = 0.7
    total_w = 0.0
    weighted = 0.0
    for i, rate in enumerate(rates):
        w = decay ** (len(rates) - 1 - i)
        weighted += rate * w
        total_w += w
    return weighted / total_w


# ── appliance estimates ───────────────────────────────────────────────────

# Average consumption for common Kenyan household appliances
# (watts, typical_hours_per_day) — accounts for actual usage patterns
_APPLIANCE_WATTS_HOURS = {
    "fridge": (150, 24),        # runs continuously (compressor cycles)
    "refrigerator": (150, 24),
    "freezer": (200, 24),
    "tv": (100, 5),             # ~5 hours evening viewing
    "television": (100, 5),
    "iron": (1000, 0.15),       # ~10 min a few times a week → avg/day
    "pressing iron": (1000, 0.15),
    "heater": (3000, 0.08),     # ~5 min/day
    "water heater": (3000, 0.08),
    "geyser": (3000, 0.08),
    "boiler": (3000, 0.08),
    "shower": (3500, 0.08),     # instant shower, ~5 min
    "oven": (2000, 0.3),        # ~20 min/day
    "microwave": (1000, 0.1),   # ~6 min/day
    "washing machine": (500, 0.3),  # ~2 loads/week → avg/day
    "washer": (500, 0.3),
    "kettle": (1500, 0.08),     # ~5 min/day, 2-3 boils
    "electric kettle": (1500, 0.08),
    "fan": (60, 8),
    "ac": (1500, 6),
    "air conditioner": (1500, 6),
    "bulb": (10, 6),            # LED bulb
    "light": (10, 6),
    "lighting": (40, 6),        # ~4 bulbs
    "laptop": (60, 5),
    "computer": (200, 4),
    "pc": (200, 4),
    "router": (10, 24),
    "wifi": (10, 24),
    "phone charger": (10, 2),
    "charger": (10, 2),
}


def estimate_appliance_burn_rate():
    """Estimate units/hour from the user's appliance list when no readings exist."""
    appliances = get_profile("appliances")
    if not appliances:
        return None
    items = [a.strip().lower() for a in re.split(r'[,/]|\band\b', appliances) if a.strip()]
    total_kwh = 0.0
    for item in items:
        for name, (watts, hours) in _APPLIANCE_WATTS_HOURS.items():
            if name in item:
                total_kwh += (watts * hours) / 1000  # Wh → kWh per day
                break
    if total_kwh == 0:
        return None
    # Scale by occupants (more people = slightly more usage)
    occ = get_profile("occupants")
    if occ:
        try:
            n = max(1, int(occ))
            total_kwh *= min(1.0 + (n - 1) * 0.1, 2.0)  # +10% per extra person, cap 2x
        except ValueError:
            pass
    return total_kwh / 24  # convert kWh/day to kWh/hour (≈ units/hour)


# ── predictions ──────────────────────────────────────────────────────────

def predict_blackout():
    burn_rate = calculate_burn_rate() or estimate_appliance_burn_rate()
    if not burn_rate:
        return None
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT balance FROM readings ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
    if not row:
        return None
    return row[0] / burn_rate


def estimate_days(units):
    burn_rate = calculate_burn_rate() or estimate_appliance_burn_rate()
    if not burn_rate:
        return None
    return units / (burn_rate * 24)


# ── profile ──────────────────────────────────────────────────────────────

_INTERNAL_KEYS = {"onboarding_step", "menu_pending"}


def set_profile(key, value):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO profile (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?",
            (key, value, value),
        )


def get_profile(key):
    with get_db() as conn:
        row = conn.execute("SELECT value FROM profile WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def get_all_profile():
    with get_db() as conn:
        rows = conn.execute("SELECT key, value FROM profile").fetchall()
    return {k: v for k, v in rows if k not in _INTERNAL_KEYS}


def is_onboarded():
    return get_profile("occupants") is not None


def reset_profile():
    """Clear all profile data to allow re-onboarding."""
    with get_db() as conn:
        conn.execute("DELETE FROM profile")


# ── budget ───────────────────────────────────────────────────────────────

def set_budget(amount):
    set_profile("budget", str(amount))


def check_budget():
    budget_str = get_profile("budget")
    if not budget_str:
        return None
    budget = float(budget_str)
    now = datetime.now()
    start = f"{now.year}-{now.month:02d}-01 00:00:00"
    end = f"{now.year + (now.month // 12)}-{(now.month % 12) + 1:02d}-01 00:00:00"

    with get_db() as conn:
        spent = conn.execute(
            "SELECT COALESCE(SUM(amount),0) FROM purchases WHERE timestamp >= ? AND timestamp < ?",
            (start, end),
        ).fetchone()[0]

    pct = (spent / budget) * 100 if budget > 0 else 0
    if pct >= 100:
        return f"🚨 Umepita budget! KES {spent:,.0f}/{budget:,.0f} ({pct:.0f}%) this month."
    elif pct >= 80:
        return f"⚠️ Budget almost done — KES {spent:,.0f}/{budget:,.0f} ({pct:.0f}%) used this month."
    return f"💰 Budget: KES {spent:,.0f}/{budget:,.0f} ({pct:.0f}%) used this month."


def budget_data():
    budget_str = get_profile("budget")
    if not budget_str:
        return None
    budget = float(budget_str)
    now = datetime.now()
    start = f"{now.year}-{now.month:02d}-01 00:00:00"
    end = f"{now.year + (now.month // 12)}-{(now.month % 12) + 1:02d}-01 00:00:00"
    with get_db() as conn:
        spent = conn.execute(
            "SELECT COALESCE(SUM(amount),0) FROM purchases WHERE timestamp >= ? AND timestamp < ?",
            (start, end),
        ).fetchone()[0]
    pct = (spent / budget) * 100 if budget > 0 else 0
    return {"budget": budget, "spent": spent, "percent": round(pct, 0)}


# ── summaries ────────────────────────────────────────────────────────────

def monthly_summary(year=None, month=None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    start = f"{year}-{month:02d}-01 00:00:00"
    end = f"{year + (month // 12)}-{(month % 12) + 1:02d}-01 00:00:00"

    with get_db() as conn:
        units, spent, count = conn.execute(
            "SELECT COALESCE(SUM(units),0), COALESCE(SUM(amount),0), COUNT(*) "
            "FROM purchases WHERE timestamp >= ? AND timestamp < ?",
            (start, end),
        ).fetchone()

    return {
        "month": calendar.month_name[month], "year": year,
        "topups": count, "units": round(units, 1), "spent": spent,
        "avg_cost_per_unit": round(spent / units, 2) if units > 0 else None,
    }


def yearly_summary(year=None):
    year = year or datetime.now().year
    start = f"{year}-01-01 00:00:00"
    end = f"{year + 1}-01-01 00:00:00"

    with get_db() as conn:
        c = conn.cursor()
        total_units, total_spent, total_count = c.execute(
            "SELECT COALESCE(SUM(units),0), COALESCE(SUM(amount),0), COUNT(*) "
            "FROM purchases WHERE timestamp >= ? AND timestamp < ?",
            (start, end),
        ).fetchone()
        months = c.execute(
            "SELECT strftime('%m', timestamp) as m, SUM(units), SUM(amount), COUNT(*) "
            "FROM purchases WHERE timestamp >= ? AND timestamp < ? GROUP BY m ORDER BY m",
            (start, end),
        ).fetchall()

    return {
        "year": year, "topups": total_count,
        "units": round(total_units, 0), "spent": total_spent,
        "avg_cost_per_unit": round(total_spent / total_units, 2) if total_units > 0 else None,
        "months": [
            {"month": calendar.month_abbr[int(m)], "units": round(units, 0), "spent": spent, "topups": count}
            for m, units, spent, count in months
        ],
    }


def price_trend_data():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT strftime('%Y-%m', timestamp) as m, SUM(amount), SUM(units) "
            "FROM purchases WHERE units > 0 AND amount > 0 GROUP BY m ORDER BY m",
        ).fetchall()

    months = []
    prev_cpu = None
    for m, amount, units in rows:
        cpu = amount / units
        change_pct = round(((cpu - prev_cpu) / prev_cpu) * 100, 1) if prev_cpu else None
        months.append({"month": m, "cost_per_unit": round(cpu, 2), "change_pct": change_pct})
        prev_cpu = cpu

    overall_pct = None
    if len(rows) >= 2:
        first_cpu = rows[0][1] / rows[0][2]
        last_cpu = rows[-1][1] / rows[-1][2]
        overall_pct = round(((last_cpu - first_cpu) / first_cpu) * 100, 1)

    return {"months": months, "overall_change_pct": overall_pct}


def price_trend():
    """Formatted version for sentinel.py."""
    data = price_trend_data()
    if not data["months"]:
        return "Not enough purchase data to detect price trends yet."
    lines = ["💰 *KPLC Price Trend (cost per unit)*", ""]
    for m in data["months"]:
        indicator = ""
        if m["change_pct"] is not None:
            if abs(m["change_pct"]) < 1:
                indicator = " →"
            elif m["change_pct"] > 0:
                indicator = f" ↑ +{m['change_pct']}%"
            else:
                indicator = f" ↓ {m['change_pct']}%"
        lines.append(f"  {m['month']}: KES {m['cost_per_unit']:.2f}/unit{indicator}")
    if data["overall_change_pct"] is not None:
        lines.append("")
        o = data["overall_change_pct"]
        if abs(o) < 1:
            lines.append("Overall: prices stable")
        elif o > 0:
            lines.append(f"Overall: prices UP {o}% since {data['months'][0]['month']}")
        else:
            lines.append(f"Overall: prices DOWN {abs(o)}% since {data['months'][0]['month']}")
    return "\n".join(lines)


# ── outages ──────────────────────────────────────────────────────────────

def _fetch_outage_schedule():
    """Download and parse the KPLC Power Maintenance Notice PDF."""
    import urllib.request

    try:
        import pdfplumber
    except ImportError:
        logger.warning("pdfplumber not installed — cannot parse outage PDF")
        return []

    if not _validate_url(KPLC_SCHEDULE_URL):
        logger.error("Outage URL failed validation: %s", KPLC_SCHEDULE_URL)
        return []

    try:
        pdf_path = os.path.join(tempfile.gettempdir(), "kplc_schedule.pdf")

        # Cache: skip download if PDF is less than 1 hour old
        use_cache = False
        if os.path.exists(pdf_path):
            age = datetime.now().timestamp() - os.path.getmtime(pdf_path)
            use_cache = age < 3600

        if not use_cache:
            req = urllib.request.Request(KPLC_SCHEDULE_URL, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                with tempfile.NamedTemporaryFile(dir=tempfile.gettempdir(), suffix=".pdf", delete=False) as tmp:
                    tmp.write(resp.read())
                    tmp_path = tmp.name
            os.replace(tmp_path, pdf_path)
            os.chmod(pdf_path, 0o600)

        chunks = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                w = page.width
                for crop in [(0, 0, w / 2, page.height), (w / 2, 0, w, page.height)]:
                    chunks.append(page.crop(crop).extract_text() or "")

        full_text = "\n".join(chunks)
        pattern = r'AREA:\s*(.+?)\s*\n[Dd][Aa][Tt][Ee]:\s*(\w+ \d{2}\.\d{2}\.\d{4})\s*TIME:\s*(.+?)[\n\r]'
        raw = re.findall(pattern, full_text)

        results = []
        for area_raw, date_raw, time_raw in raw:
            area = area_raw.strip().title()
            area_clean = re.sub(r'^Part Of\s+', '', area)
            day_name, date_str = date_raw.split(" ", 1)
            parts = date_str.split(".")
            day = int(parts[0])
            month_num = int(parts[1])
            suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            date_fmt = f"{day_name} {day}{suffix} {calendar.month_name[month_num]}"
            time_clean = re.sub(r'(\d+)\.(\d+)', r'\1:\2', time_raw.strip())
            time_clean = time_clean.replace("A.M.", "AM").replace("P.M.", "PM").replace("A.M", "AM").replace("P.M", "PM")
            results.append({"area": area, "area_clean": area_clean, "date": date_fmt, "time": time_clean,
                            "iso_date": f"{parts[2]}-{parts[1]}-{parts[0]}"})
        return results
    except Exception:
        logger.exception("Failed to fetch/parse KPLC outage schedule")
        return []


def check_outages(area=None):
    area = area or get_profile("area")
    if not area:
        return {"area": None, "matches": [], "error": "no_area"}

    scheduled = _fetch_outage_schedule()
    if not scheduled:
        return {"area": area, "matches": [], "error": "fetch_failed"}

    area_lower = area.lower()
    area_words = [w for w in area_lower.split() if len(w) > 3]
    matches = [
        s for s in scheduled
        if area_lower in s["area_clean"].lower()
        or s["area_clean"].lower() in area_lower
        or any(w in s["area_clean"].lower() for w in area_words)
    ]

    return {"area": area, "matches": [{"date": m["date"], "time": m["time"], "iso_date": m["iso_date"]} for m in matches]}


# ── insights ─────────────────────────────────────────────────────────────

def comparison_insights_data():
    """Week-over-week and day-of-week usage patterns."""
    now = datetime.now()
    week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    two_weeks_ago = (now - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        c = conn.cursor()
        this_spent, this_units = c.execute(
            "SELECT COALESCE(SUM(amount),0), COALESCE(SUM(units),0) FROM purchases WHERE timestamp >= ?",
            (week_ago,),
        ).fetchone()
        last_spent, last_units = c.execute(
            "SELECT COALESCE(SUM(amount),0), COALESCE(SUM(units),0) FROM purchases WHERE timestamp >= ? AND timestamp < ?",
            (two_weeks_ago, week_ago),
        ).fetchone()
        readings = c.execute(
            "SELECT timestamp, balance, notes FROM readings ORDER BY timestamp ASC",
        ).fetchall()

    result = {
        "this_week": {"units": this_units, "spent": this_spent},
        "last_week": {"units": last_units, "spent": last_spent},
    }

    if last_units > 0 and this_units > 0:
        result["change_pct"] = round(((this_units - last_units) / last_units) * 100, 0)

    # Day-of-week patterns
    # NOTE: attributes all burned units to the end reading's day, which skews
    # if readings span multiple days.  Acceptable for frequent-reading users.
    fmt = "%Y-%m-%d %H:%M:%S"
    if len(readings) >= 7:
        day_usage = {}
        for i in range(1, len(readings)):
            _, _, notes = readings[i]
            if notes and notes.startswith("Auto:"):
                continue
            old_ts, old_bal, _ = readings[i - 1]
            new_ts, new_bal, _ = readings[i]
            burned = old_bal - new_bal
            if burned <= 0:
                continue
            dow = datetime.strptime(new_ts, fmt).weekday()
            day_usage.setdefault(dow, []).append(burned)

        if day_usage:
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            avgs = {d: sum(v) / len(v) for d, v in day_usage.items()}
            peak = max(avgs, key=avgs.get)
            low = min(avgs, key=avgs.get)
            result["heaviest_day"] = {"day": day_names[peak], "avg_units": round(avgs[peak], 1)}
            result["lightest_day"] = {"day": day_names[low], "avg_units": round(avgs[low], 1)}

    has_data = this_units > 0 or last_units > 0 or "heaviest_day" in result
    return result if has_data else None


def comparison_insights():
    """Formatted version for sentinel.py."""
    data = comparison_insights_data()
    if not data:
        return None
    lines = ["📈 *Usage Insights*", ""]
    if "change_pct" in data:
        d = data["change_pct"]
        if d > 5:
            lines.append(f"⬆️ You used {d:.0f}% more units this week than last week.")
        elif d < -5:
            lines.append(f"⬇️ You used {abs(d):.0f}% fewer units this week. Poa!")
        else:
            lines.append("↔️ Usage ni sawa sawa with last week.")
    elif data["this_week"]["units"] > 0:
        lines.append(f"This week: {data['this_week']['units']:.0f} units (KES {data['this_week']['spent']:,.0f}).")
    if "heaviest_day" in data:
        lines.append(f"📅 Heaviest day: {data['heaviest_day']['day']} ({data['heaviest_day']['avg_units']} units avg)")
        lines.append(f"📅 Lightest day: {data['lightest_day']['day']} ({data['lightest_day']['avg_units']} units avg)")
    return "\n".join(lines) if len(lines) > 2 else None
