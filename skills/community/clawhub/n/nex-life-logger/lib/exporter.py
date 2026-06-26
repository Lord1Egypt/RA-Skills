"""
Nex Life Logger - Data Exporter
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import csv
import json
import sqlite3
import datetime as dt
import logging
from pathlib import Path
from config import DB_PATH

log = logging.getLogger("life-logger.exporter")


def _timestamp_suffix():
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def export_json(output_path):
    """Export everything to a single JSON file."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.row_factory = sqlite3.Row
    data = {
        "export_date": dt.datetime.now().isoformat(),
        "format_version": "1.0",
    }
    rows = conn.execute(
        "SELECT id, timestamp, source, kind, title, url, extra, created_at FROM activities ORDER BY timestamp"
    ).fetchall()
    data["activities"] = [dict(r) for r in rows]
    rows = conn.execute(
        "SELECT id, period, start_date, end_date, content, created_at FROM summaries ORDER BY start_date"
    ).fetchall()
    data["summaries"] = [dict(r) for r in rows]
    rows = conn.execute(
        "SELECT id, keyword, category, frequency, source_date, created_at FROM keywords ORDER BY source_date"
    ).fetchall()
    data["keywords"] = [dict(r) for r in rows]
    try:
        rows = conn.execute(
            "SELECT video_id, title, transcript, created_at FROM transcripts ORDER BY created_at"
        ).fetchall()
        data["transcripts"] = [dict(r) for r in rows]
    except Exception:
        data["transcripts"] = []
    conn.close()
    out = Path(output_path)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return out


def export_csv(output_path):
    """Export activities to CSV."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, timestamp, source, kind, title, url, extra, created_at FROM activities ORDER BY timestamp"
    ).fetchall()
    conn.close()
    out = Path(output_path)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "timestamp", "source", "kind", "title", "url", "extra", "created_at"])
        for r in rows:
            writer.writerow([r["id"], r["timestamp"], r["source"], r["kind"],
                             r["title"], r["url"], r["extra"], r["created_at"]])
    return out


def export_html(output_path):
    """Export a styled HTML report."""
    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.row_factory = sqlite3.Row
    summaries = conn.execute(
        "SELECT period, start_date, end_date, content FROM summaries ORDER BY period, start_date DESC"
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0]
    by_kind = conn.execute(
        "SELECT kind, COUNT(*) as cnt FROM activities GROUP BY kind ORDER BY cnt DESC"
    ).fetchall()
    date_range = conn.execute(
        "SELECT MIN(DATE(timestamp)), MAX(DATE(timestamp)) FROM activities"
    ).fetchone()
    conn.close()

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html><head><meta charset='utf-8'>")
    html.append("<title>Nex Life Logger Report</title>")
    html.append("<style>body{font-family:system-ui,sans-serif;max-width:800px;margin:40px auto;padding:0 20px;")
    html.append("background:#0e0e12;color:#e0e0e0;}h1{color:#00f0ff;}h2{color:#ff00ff;border-bottom:1px solid #333;")
    html.append("padding-bottom:8px;}h3{color:#00ff88;}.summary{background:#1a1a24;padding:16px;border-radius:8px;")
    html.append("margin:12px 0;border-left:3px solid #00f0ff;}.stat{display:inline-block;background:#1a1a24;")
    html.append("padding:8px 16px;border-radius:6px;margin:4px;}.footer{text-align:center;margin-top:40px;")
    html.append("color:#666;font-size:0.85em;}</style></head><body>")
    html.append("<h1>Nex Life Logger Report</h1>")
    html.append("<p>Generated: %s</p>" % dt.datetime.now().strftime("%A, %B %d, %Y at %H:%M"))
    html.append("<h2>Statistics</h2>")
    html.append("<p>Total activities: <strong>%s</strong></p>" % "{:,}".format(total))
    if date_range[0]:
        html.append("<p>Date range: %s to %s</p>" % (date_range[0], date_range[1]))
    html.append("<p>By type: ")
    for r in by_kind:
        html.append("<span class='stat'>%s: %s</span> " % (r["kind"], "{:,}".format(r["cnt"])))
    html.append("</p>")
    html.append("<h2>Summaries</h2>")
    for period in ["yearly", "monthly", "weekly", "daily"]:
        period_sums = [s for s in summaries if s["period"] == period]
        if not period_sums:
            continue
        html.append("<h3>%s (%d)</h3>" % (period.capitalize(), len(period_sums)))
        for s in period_sums[:10]:
            html.append("<div class='summary'><strong>%s to %s</strong>" % (s["start_date"], s["end_date"]))
            for para in s["content"].split("\n"):
                if para.strip():
                    html.append("<p>%s</p>" % para)
            html.append("</div>")
    html.append("<div class='footer'>Nex Life Logger by Nex AI | nex-ai.be</div>")
    html.append("</body></html>")

    out = Path(output_path)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    return out
