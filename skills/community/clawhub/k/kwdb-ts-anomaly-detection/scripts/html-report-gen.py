#!/usr/bin/env python3
import json
import sys
import argparse
from datetime import datetime
from html import escape


BADGE_COLORS = [
    "#3498db",
    "#9b59b6",
    "#27ae60",
    "#e67e22",
    "#e74c3c",
    "#1abc9c",
    "#f39c12",
    "#8e44ad",
]


def _e(text):
    return escape(str(text))


def _generate_badge_css():
    lines = [
        ".column-badge { background: #3498db; color: white; padding: 4px 12px; border-radius: 4px; font-size: 13px; }"
    ]
    for i, color in enumerate(BADGE_COLORS[1:], 1):
        lines.append(
            f".column-badge.variant-{i} {{ background: {color}; }}"
        )
    return "\n        ".join(lines)


def _render_stats_grid(total_rows, sigma_count, final_count):
    alert_cls = " alert" if final_count > 0 else ""
    return (
        '<div class="stats-grid">\n'
        "  <div class=\"stat-card\">\n"
        f"    <div class=\"stat-value\">{total_rows}</div>\n"
        '    <div class="stat-label">Total Rows</div>\n'
        "  </div>\n"
        "  <div class=\"stat-card\">\n"
        f"    <div class=\"stat-value\">{sigma_count}</div>\n"
        '    <div class="stat-label">3-Sigma Anomalies</div>\n'
        "  </div>\n"
        "  <div class=\"stat-card\">\n"
        f'    <div class="stat-value{alert_cls}">{final_count}</div>\n'
        '    <div class="stat-label">Final Anomalies</div>\n'
        "  </div>\n"
        "</div>"
    )


def _render_threshold(threshold, period):
    upper = threshold.get("upper", "N/A")
    lower = threshold.get("lower", "N/A")
    return (
        '<div class="threshold">\n'
        f'  <div class="threshold-item">Upper Threshold: <span>{upper}</span></div>\n'
        f'  <div class="threshold-item">Lower Threshold: <span>{lower}</span></div>\n'
        f'  <div class="threshold-item">Period: <span>{period}</span></div>\n'
        "</div>"
    )


def _render_sigma_table(anomalies):
    if not anomalies:
        return '<h3>3-Sigma Anomaly Points</h3>\n<p>No anomaly points detected.</p>'
    rows = []
    for i, a in enumerate(anomalies, 1):
        ts = _e(a["timestamp"])
        val = a["value"]
        violates = a.get("violates_rule", False)
        if violates:
            rows.append(
                f'<tr><td>{i}</td><td>{ts}</td>'
                f'<td class="alert">{val} ⚠️</td></tr>'
            )
        else:
            rows.append(f"<tr><td>{i}</td><td>{ts}</td><td>{val}</td></tr>")
    body = "\n                    ".join(rows)
    return (
        '<h3>3-Sigma Anomaly Points</h3>\n'
        '<table>\n'
        '  <tr><th>#</th><th>Time</th><th>Value</th></tr>\n'
        f"  {body}\n"
        "</table>"
    )


def _render_final_table(anomalies):
    if not anomalies:
        return ""
    rows = []
    for i, a in enumerate(anomalies, 1):
        ts = _e(a["timestamp"])
        val = a["value"]
        violation = _e(a.get("violation", ""))
        rows.append(
            f'<tr class="anomaly-row">'
            f"<td>{i}</td><td>{ts}</td><td>{val}</td>"
            f"<td>{violation}</td></tr>"
        )
    body = "\n                    ".join(rows)
    return (
        '<h3>Final Anomaly Points (Violating Rules)</h3>\n'
        '<table>\n'
        '  <tr><th>#</th><th>Time</th><th>Value</th><th>Violation</th></tr>\n'
        f"  {body}\n"
        "</table>"
    )


def _render_column_section(col_data, badge_index=0):
    variant_cls = ""
    if badge_index > 0:
        variant_idx = badge_index % len(BADGE_COLORS)
        if variant_idx != 0:
            variant_cls = f" variant-{variant_idx}"

    col_name = _e(col_data["column_name"])
    rule = col_data.get("rule", "")

    rule_badge = ""
    if rule:
        rule_badge = f'<div class="rule-badge">{_e(rule)}</div>'

    total = col_data.get("total_rows", 0)
    sigma_anomalies = col_data.get("sigma_anomalies", [])
    final_anomalies = col_data.get("final_anomalies", [])
    sigma_count = col_data.get("sigma_anomaly_count", len(sigma_anomalies))
    final_count = col_data.get("final_anomaly_count", len(final_anomalies))
    threshold = col_data.get("threshold", {})
    period = col_data.get("period", "N/A")

    parts = [
        '<div class="detection-section">',
        f'  <div class="column-header">',
        f'    <span class="column-badge{variant_cls}">{col_name}</span>',
        '  </div>',
        f"  {rule_badge}" if rule_badge else "",
        f"  {_render_stats_grid(total, sigma_count, final_count)}",
        f"  {_render_threshold(threshold, period)}",
        f"  {_render_sigma_table(sigma_anomalies)}",
        f"  {_render_final_table(final_anomalies)}",
        "</div>",
    ]
    return "\n            ".join(p for p in parts if p)


def _render_tag_content(tag_data, is_active=False):
    active_cls = " active" if is_active else ""
    tag_value = _e(tag_data["tag_value"])
    columns = tag_data.get("columns", [])

    sections = []
    for idx, col in enumerate(columns):
        sections.append(_render_column_section(col, idx))

    body = "\n\n            ".join(sections)
    return (
        f'<div id="{tag_value}" class="tab-content{active_cls}">\n'
        f"            {body}\n"
        "        </div>"
    )


def generate_report(data):
    db_name = data.get("db_name", "")
    table_name = data.get("table_name", "")
    full_name = f"{db_name}.{table_name}" if db_name and table_name else db_name or table_name
    display_name = f"{db_name}:{table_name}" if db_name and table_name else full_name

    detection_time = data.get(
        "detection_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    time_span = data.get("time_span", {})
    start = time_span.get("start", "")
    end = time_span.get("end", "")
    span_display = f"{start} ~ {end}" if start and end else ""
    detection_method = _e(data.get("detection_method", "3-Sigma"))

    tags = data.get("tags", [])

    use_tabs = len(tags) > 1

    if use_tabs:
        tab_buttons = []
        tab_panels = []
        for i, tag in enumerate(tags):
            is_active = i == 0
            tv = _e(tag["tag_value"])
            active_cls = " active" if is_active else ""
            tab_buttons.append(
                f'<div class="tab{active_cls}" '
                f"onclick=\"showTab('{tv}')\">{tv}</div>"
            )
            tab_panels.append(_render_tag_content(tag, is_active))

        tabs_html = "\n            ".join(tab_buttons)
        panels_html = "\n\n        ".join(tab_panels)

        tabs_section = f'<div class="tabs">\n            {tabs_html}\n        </div>'
        content_section = panels_html
    else:
        if tags:
            columns = tags[0].get("columns", [])
            sections = []
            for idx, col in enumerate(columns):
                sections.append(_render_column_section(col, idx))
            joined = "\n\n            ".join(sections)
            content_section = (
                '<div class="tab-content active">\n'
                f"            {joined}\n"
                "        </div>"
            )
        else:
            content_section = ""
        tabs_section = ""

    badge_css = _generate_badge_css()

    return (
        '<!DOCTYPE html>\n'
        '<html lang="zh-CN">\n'
        "<head>\n"
        '    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"    <title>Anomaly Detection Report - {full_name}</title>\n"
        "    <style>\n"
        "        * { margin: 0; padding: 0; box-sizing: border-box; }\n"
        "        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; padding: 20px; }\n"
        "        .container { max-width: 1200px; margin: 0 auto; }\n"
        "        h1 { color: #2c3e50; margin-bottom: 20px; font-size: 24px; }\n"
        "        h2 { color: #34495e; margin: 20px 0 15px; font-size: 18px; }\n"
        "        h3 { color: #7f8c8d; margin: 15px 0 10px; font-size: 14px; }\n"
        "        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px; }\n"
        "        .info-card { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n"
        "        .info-label { color: #95a5a6; font-size: 12px; margin-bottom: 5px; }\n"
        "        .info-value { color: #2c3e50; font-size: 14px; font-weight: 500; }\n"
        "        .tabs { display: flex; gap: 5px; margin-bottom: 0; }\n"
        "        .tab { padding: 10px 20px; background: #ecf0f1; border-radius: 8px 8px 0 0; cursor: pointer; font-size: 14px; color: #7f8c8d; }\n"
        "        .tab.active { background: white; color: #3498db; font-weight: 600; }\n"
        "        .tab-content { background: white; border-radius: 0 8px 8px 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: none; }\n"
        "        .tab-content.active { display: block; }\n"
        "        .detection-section { margin-bottom: 25px; }\n"
        "        .section-title { color: #2c3e50; font-size: 16px; font-weight: 600; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 2px solid #3498db; }\n"
        "        .rule-badge { display: inline-block; background: #e8f4fd; color: #3498db; padding: 4px 10px; border-radius: 12px; font-size: 12px; margin: 5px 5px 10px 0; }\n"
        "        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 10px 0; }\n"
        "        .stat-card { background: #f8f9fa; padding: 12px; border-radius: 6px; text-align: center; }\n"
        "        .stat-value { font-size: 24px; font-weight: 700; color: #2c3e50; }\n"
        "        .stat-label { font-size: 11px; color: #95a5a6; margin-top: 4px; }\n"
        "        .stat-value.alert { color: #e74c3c; }\n"
        "        table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px; }\n"
        "        th { background: #f8f9fa; color: #7f8c8d; font-weight: 600; text-align: left; padding: 10px 8px; border-bottom: 2px solid #ecf0f1; }\n"
        "        td { padding: 8px; border-bottom: 1px solid #ecf0f1; }\n"
        "        tr:hover { background: #f8f9fa; }\n"
        "        .anomaly-row { background: #fdf2f2 !important; }\n"
        "        .anomaly-row td { color: #e74c3c; }\n"
        "        .threshold { display: flex; gap: 20px; margin: 10px 0; }\n"
        "        .threshold-item { font-size: 13px; color: #7f8c8d; }\n"
        "        .threshold-item span { font-weight: 600; color: #2c3e50; }\n"
        "        footer { text-align: center; color: #95a5a6; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1; }\n"
        "        .column-header { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; }\n"
        f"        {badge_css}\n"
        "    </style>\n"
        "</head>\n"
        "<body>\n"
        '    <div class="container">\n'
        f"        <h1>Detection Report for {full_name}</h1>\n"
        "\n"
        '        <div class="info-grid">\n'
        '            <div class="info-card">\n'
        '                <div class="info-label">Data Table</div>\n'
        f"                <div class=\"info-value\">{display_name}</div>\n"
        "            </div>\n"
        '            <div class="info-card">\n'
        '                <div class="info-label">Detection Time</div>\n'
        f"                <div class=\"info-value\">{detection_time}</div>\n"
        "            </div>\n"
        '            <div class="info-card">\n'
        '                <div class="info-label">Data Time Span</div>\n'
        f"                <div class=\"info-value\">{span_display}</div>\n"
        "            </div>\n"
        '            <div class="info-card">\n'
        '                <div class="info-label">Detection Method</div>\n'
        f"                <div class=\"info-value\">{detection_method}</div>\n"
        "            </div>\n"
        "        </div>\n"
        "\n"
        f"        {tabs_section}\n"
        "\n"
        f"        {content_section}\n"
        "\n"
        "        <footer>\n"
        "            This report is generated by KaiwuDB Anomaly Detection System\n"
        "        </footer>\n"
        "    </div>\n"
        "\n"
        "    <script>\n"
        "        function showTab(deviceId) {\n"
        "            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));\n"
        "            document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));\n"
        "            document.getElementById(deviceId).classList.add('active');\n"
        "            event.target.classList.add('active');\n"
        "        }\n"
        "    </script>\n"
        "</body>\n"
        "</html>"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML anomaly detection report from structured JSON data"
    )
    parser.add_argument(
        "--input",
        nargs="?",
        help="Path to JSON file containing report data. Reads from stdin if omitted.",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output_path",
        help="Path to write the generated HTML report.",
    )
    args = parser.parse_args()

    try:
        if args.input:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: input is not valid JSON")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)

    html = generate_report(data)

    if args.output_path:
        try:
            with open(args.output_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Report written to: {args.output_path}")
        except Exception as e:
            print(f"Error writing report: {e}")
            sys.exit(1)
    else:
        print(html)


if __name__ == "__main__":
    main()
