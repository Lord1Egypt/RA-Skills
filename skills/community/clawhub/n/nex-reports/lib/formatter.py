"""
Nex Reports - Output Formatting
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import json
from typing import Any, Dict, List

from .config import REPORT_FOOTER


def format_report_telegram(title: str, module_results: List[Dict[str, Any]]) -> str:
    """
    Format report for Telegram with emojis for status.
    Compact format suitable for mobile viewing.
    """
    emoji_status = {
        "ok": "✓",
        "warning": "⚠",
        "error": "✗",
    }

    lines = [f"📋 {title}"]
    lines.append("")

    for module in module_results:
        status_emoji = emoji_status.get(module.get("status", "ok"), "?")
        title_text = module.get("title", "Module")
        content = module.get("content", "")

        lines.append(f"{status_emoji} {title_text}")
        if content:
            lines.append(f"  {content}")

        items = module.get("items", [])
        if items:
            for item in items[:3]:  # Limit to 3 items per module for Telegram
                lines.append(f"  • {item}")

        lines.append("")

    lines.append(REPORT_FOOTER)

    return "\n".join(lines)


def format_report_markdown(title: str, module_results: List[Dict[str, Any]]) -> str:
    """
    Format report as markdown.
    Full format suitable for email or documents.
    """
    status_emoji = {
        "ok": "✓",
        "warning": "⚠",
        "error": "✗",
    }

    lines = [f"# {title}"]
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")

    for module in module_results:
        status = module.get("status", "ok")
        status_symbol = status_emoji.get(status, "?")
        module_title = module.get("title", "Module")
        content = module.get("content", "")

        lines.append(f"## {status_symbol} {module_title}")
        lines.append("")

        if content:
            lines.append(f"> {content}")
            lines.append("")

        items = module.get("items", [])
        if items:
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

    lines.append("---")
    lines.append(f"_{REPORT_FOOTER}_")

    return "\n".join(lines)


def format_report_html(title: str, module_results: List[Dict[str, Any]]) -> str:
    """
    Format report as simple HTML.
    """
    from datetime import datetime

    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "<title>Nex Reports</title>",
        "<style>",
        "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }",
        "h1 { color: #333; border-bottom: 2px solid #007AFF; padding-bottom: 10px; }",
        ".meta { color: #666; font-size: 12px; margin-bottom: 20px; }",
        ".module { background: white; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }",
        ".module h2 { margin: 0 0 10px 0; font-size: 18px; }",
        ".status-ok { color: #34C759; }",
        ".status-warning { color: #FF9500; }",
        ".status-error { color: #FF3B30; }",
        ".content { color: #555; margin: 10px 0; }",
        ".items { list-style: none; padding: 10px 0; margin: 10px 0; }",
        ".items li { padding: 5px 0; color: #666; }",
        ".footer { text-align: center; color: #999; font-size: 12px; margin-top: 40px; border-top: 1px solid #e0e0e0; padding-top: 20px; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>{title}</h1>",
        f"<p class='meta'>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
    ]

    status_class = {
        "ok": "status-ok",
        "warning": "status-warning",
        "error": "status-error",
    }

    for module in module_results:
        status = module.get("status", "ok")
        module_title = module.get("title", "Module")
        content = module.get("content", "")
        status_cls = status_class.get(status, "status-ok")

        html_lines.append(f"<div class='module'>")
        html_lines.append(f"<h2 class='{status_cls}'>{module_title}</h2>")

        if content:
            html_lines.append(f"<p class='content'>{content}</p>")

        items = module.get("items", [])
        if items:
            html_lines.append("<ul class='items'>")
            for item in items:
                html_lines.append(f"<li>{item}</li>")
            html_lines.append("</ul>")

        html_lines.append("</div>")

    html_lines.append(f"<p class='footer'>{REPORT_FOOTER}</p>")
    html_lines.append("</body>")
    html_lines.append("</html>")

    return "\n".join(html_lines)


def format_report_json(title: str, module_results: List[Dict[str, Any]]) -> str:
    """
    Format report as JSON.
    """
    from datetime import datetime

    report_data = {
        "title": title,
        "generated_at": datetime.now().isoformat(),
        "modules": module_results,
        "footer": REPORT_FOOTER,
    }

    return json.dumps(report_data, indent=2)


def format_report(title: str, results: List[Dict[str, Any]], format_type: str) -> str:
    """
    Dispatcher for format functions.
    format_type: "telegram", "markdown", "html", "json"
    """
    format_map = {
        "telegram": format_report_telegram,
        "markdown": format_report_markdown,
        "html": format_report_html,
        "json": format_report_json,
    }

    formatter = format_map.get(format_type.lower(), format_report_markdown)
    return formatter(title, results)


# Import datetime for HTML formatter
from datetime import datetime
