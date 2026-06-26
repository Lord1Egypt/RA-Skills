#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# -*- coding: utf-8 -*-

import re
from datetime import datetime
from pathlib import Path

from schemas import EcgListItem, ReportDetail

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_ROOT / "templates"


class TemplateRenderer:
    def __init__(self):
        self.report_list_tpl = (TEMPLATE_DIR / "report_list_view.md").read_text(encoding="utf-8")
        self.report_detail_tpl = (TEMPLATE_DIR / "report_view.md").read_text(encoding="utf-8")

    @staticmethod
    def _fmt_ts(ts_millis: int) -> str:
        if not ts_millis:
            return "--"
        dt = datetime.fromtimestamp(ts_millis / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _status_icon(status: int) -> str:
        return {
            0: "正常",
            1: "偏大",
            2: "偏小",
            3: "异常",
        }.get(status, "未知")

    @staticmethod
    def _clean_text(value) -> str:
        if value is None:
            return ""
        text = str(value).strip()
        text = text.replace("`", "").replace("\r\n", "\n").replace("\r", "\n")
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _clean_url(value) -> str:
        text = TemplateRenderer._clean_text(value)
        if not text:
            return "--"
        return text

    @staticmethod
    def _to_display(value, fallback="--") -> str:
        text = TemplateRenderer._clean_text(value)
        return text if text else fallback

    @staticmethod
    def _escape_table_cell(value: str) -> str:
        text = str(value)
        return text.replace("|", "\\|")

    @staticmethod
    def _to_int(value, default=0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _find_indicator(normal_list: list[dict], name: str) -> dict:
        for item in normal_list:
            if item.get("name") == name:
                return item
        return {}

    @staticmethod
    def _resolve(context: dict, key: str):
        key = key.strip()
        current = context
        for part in key.split("."):
            part = part.strip()
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = getattr(current, part, None)
            if current is None:
                return ""
        return current

    def _render_text(self, template: str, context: dict) -> str:
        loop_pattern = re.compile(r"{%\s*for\s+(\w+)\s+in\s+([a-zA-Z0-9_\.]+)\s*%}(.*?){%\s*endfor\s*%}", re.S)
        if_pattern = re.compile(r"{%\s*if\s+([a-zA-Z0-9_\.]+)\s*%}(.*?){%\s*endif\s*%}", re.S)
        var_pattern = re.compile(r"{{\s*([^}]+)\s*}}")

        def render_loops(text: str) -> str:
            while True:
                try:
                    m = loop_pattern.search(text)
                    if not m:
                        return text
                    var_name, list_name, block = m.group(1), m.group(2), m.group(3)
                    items = self._resolve(context, list_name)
                    rendered = ""
                    if isinstance(items, list):
                        parts = []
                        for item in items:
                            sub_ctx = dict(context)
                            sub_ctx[var_name] = item
                            rendered_part = self._render_text(block, sub_ctx).strip()
                            if rendered_part:
                                parts.append(rendered_part)
                        rendered = "\n".join(parts)
                    text = text[:m.start()] + rendered + text[m.end():]
                except (TypeError, ValueError, KeyError):
                    return text

        def render_ifs(text: str) -> str:
            while True:
                try:
                    m = if_pattern.search(text)
                    if not m:
                        return text
                    cond_key, block = m.group(1), m.group(2)
                    cond_value = self._resolve(context, cond_key)
                    replacement = self._render_text(block, context) if cond_value else ""
                    text = text[:m.start()] + replacement + text[m.end():]
                except (TypeError, ValueError, KeyError):
                    return text

        text = render_loops(template)
        text = render_ifs(text)
        text = var_pattern.sub(lambda m: str(self._resolve(context, m.group(1))), text)
        return text

    def render_report_list(self, datas: list[EcgListItem]) -> str:
        items = []
        for i, item in enumerate(datas, 1):
            result = item.ecgResult or "--"
            # 简单判断是否正常，添加图标
            icon = "🟢" if "正常" in result or "窦性" in result else "🟠"
            if result == "--":
                icon = "⚪"

            items.append(
                {
                    "index": i,
                    "takeTime": self._fmt_ts(item.takeTime),
                    "result": self._escape_table_cell(result),
                    "result_icon": icon,
                    "report_no": self._escape_table_cell(item.reportNo or "--"),
                }
            )
        if not items:
            return "当前未查询到可查看的报告。请稍后重试，或先确认在心脏+ App 已生成检测报告。"
        context = {"count": len(items), "list": items}
        return self._render_text(self.report_list_tpl, context).strip()

    def render_report_detail(self, detail: ReportDetail) -> str:
        normal_list = []
        for item in detail.normalList:
            state_val = self._to_int(item.state, 0)
            status_icon = self._status_icon(state_val)
            normal_list.append(
                {
                    "name": self._escape_table_cell(self._to_display(item.name)),
                    "value": self._escape_table_cell(self._to_display(item.ecg)),
                    "range": self._escape_table_cell(self._to_display(item.range)),
                    "status_icon": status_icon,
                    "explain": self._escape_table_cell(self._to_display(item.explain)),
                }
            )

        hrv_value = self._to_int(detail.hrv_value, 0)
        hdrisk_value = self._to_int(detail.hdrisk_value, 0)
        mental_value = self._to_int(detail.mental_value, 0)
        fatigue_value = self._to_int(detail.fatigue_value, 0)

        # 指标范围获取 (默认值)
        hr_cfg = {"min": 60, "max": 100}
        hrv_cfg = {"min": 102, "max": 180}
        hdrisk_cfg = {"min": 0, "max": 30}
        mental_cfg = {"min": 0, "max": 50}
        fatigue_cfg = {"min": 0, "max": 50}
        
        # 尝试从 ConfigManager 获取配置 (如果已实现)
        try:
            from config_manager import ConfigManager
            indicators = ConfigManager().get("indicators", {})
            if indicators:
                hr_cfg = indicators.get("heart_rate", hr_cfg)
                hrv_cfg = indicators.get("hrv", hrv_cfg)
                hdrisk_cfg = indicators.get("hdrisk", hdrisk_cfg)
                mental_cfg = indicators.get("mental", mental_cfg)
                fatigue_cfg = indicators.get("fatigue", fatigue_cfg)
        except ImportError:
            pass

        # 辅助函数：根据范围生成状态图标
        def get_range_icon(val, min_v, max_v):
            if val < min_v: return "📉"
            if val > max_v: return "📈"
            return "✅"

        context = {
            "title": self._to_display(detail.title),
            "ecg_result": self._to_display(detail.ecgResult),
            "abnor_analysis": self._to_display(detail.abnorAnalysis),
            "result_tz": self._to_display(detail.ecgResultTz),
            "avg_hr": self._to_display(detail.avg),
            "min_hr": self._to_display(detail.min),
            "max_hr": self._to_display(detail.max),
            "hr_status_icon": get_range_icon(self._to_int(detail.avg), hr_cfg["min"], hr_cfg["max"]),
            
            "hrv_value": hrv_value,
            "hrv_range": f"{hrv_cfg['min']}-{hrv_cfg['max']}",
            "hrv_status_icon": get_range_icon(hrv_value, hrv_cfg["min"], hrv_cfg["max"]),
            
            "hdrisk_value": hdrisk_value,
            "hdrisk_range": f"{hdrisk_cfg['min']}-{hdrisk_cfg['max']}",
            "hdrisk_status_icon": get_range_icon(hdrisk_value, hdrisk_cfg["min"], hdrisk_cfg["max"]),
            
            "mental_value": mental_value,
            "mental_range": f"{mental_cfg['min']}-{mental_cfg['max']}",
            "mental_status_icon": get_range_icon(mental_value, mental_cfg["min"], mental_cfg["max"]),
            "mental": self._to_display(detail.mentalPressure),
            
            "fatigue_value": fatigue_value,
            "fatigue_range": f"{fatigue_cfg['min']}-{fatigue_cfg['max']}",
            "fatigue_status_icon": get_range_icon(fatigue_value, fatigue_cfg["min"], fatigue_cfg["max"]),
            "fatigue": self._to_display(detail.fatigue),

            "normal_rate": self._to_int(detail.normalRate, 0),
            "slow_rate": self._to_int(getattr(detail, "slowRate", 0), 0),
            "fast_rate": max(0, 100 - self._to_int(detail.normalRate, 0) - self._to_int(getattr(detail, "slowRate", 0), 0)),
            
            "normalList": normal_list,
            "suggestion": self._to_display(detail.suggestion, ""),
            "health_care_advice": self._to_display(detail.healthCareAdvice, ""),
            "report_pdf_url": self._clean_url(detail.reportPdf),
        }
        return self._render_text(self.report_detail_tpl, context).strip()
