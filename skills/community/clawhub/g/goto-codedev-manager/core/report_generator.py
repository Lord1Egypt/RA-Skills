"""用 Jinja2 模板生成中文开发同步报告（沿用 goto-cloudserver-manager 写法）。"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

REPORTS_DIR = Path(__file__).parent.parent / "reports"


class ReportGenerator:
    def __init__(self, reports_dir: Path = REPORTS_DIR) -> None:
        self._env = Environment(
            loader=FileSystemLoader(str(reports_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._env.globals["now"] = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._env.globals["today"] = lambda: datetime.now().strftime("%Y-%m-%d")

    def generate(self, report_type: str, **context: Any) -> str:
        template_name = f"{report_type}.md.j2"
        try:
            template = self._env.get_template(template_name)
        except Exception:
            return self._fallback_report(report_type, context)
        return template.render(**context)

    @staticmethod
    def _fallback_report(report_type: str, context: dict) -> str:
        ws = context.get("workspace")
        ws_name = getattr(ws, "name", "未知工作区") if ws else "未知工作区"
        return (
            f"# {report_type} 报告\n\n"
            f"- 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- 工作区：{ws_name}\n\n"
            f"报告内容：\n```\n{context}\n```\n"
        )
