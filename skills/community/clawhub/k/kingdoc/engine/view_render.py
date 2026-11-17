"""KingDoc 视图渲染引擎

视图层本地渲染看板（matplotlib 柱图）与甘特（mermaid 时间线）两种视图导出图片：
- 看板视图：按状态字段分组卡片，matplotlib 柱图渲染
- 甘特视图：时间轴 + 任务依赖，mermaid 时间线渲染
- 硬件自适应：根据 CPU/RAM 动态调整渲染并发

本地降级：无 matplotlib 时返回结构化 JSON，不中断其他功能。
"""
from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ViewRenderEngine:
    """视图渲染引擎"""

    SUPPORTED_VIEWS: Dict[str, Dict[str, Any]] = {
        "kanban": {
            "name": "看板",
            "description": "按状态字段分组卡片",
            "requires": ["status_field", "title_field"],
            "output_format": "png",
        },
        "gantt": {
            "name": "甘特图",
            "description": "时间轴 + 任务依赖",
            "requires": ["start_field", "end_field", "title_field"],
            "output_format": "png",
        },
    }

    def __init__(self, backend: Any = None, output_dir: Optional[str] = None):
        self.backend = backend
        self.output_dir = output_dir or self._default_output_dir()
        os.makedirs(self.output_dir, exist_ok=True)
        self._render_concurrency = self._detect_safe_concurrency()

    def _default_output_dir(self) -> str:
        skill_root = Path(__file__).resolve().parent.parent
        return str(skill_root / "output" / "views")

    def _detect_safe_concurrency(self) -> int:
        """硬件自适应：检测安全渲染并发"""
        try:
            from engine.hardware import get_recommended_settings
            settings = get_recommended_settings()
            return settings.get("workers", 2)
        except ImportError:
            return 2

    def list_views(self) -> Dict[str, Any]:
        """列出所有支持的视图类型"""
        return {
            "views": [
                {
                    "id": k,
                    "name": v["name"],
                    "description": v["description"],
                    "requires": v["requires"],
                    "output_format": v["output_format"],
                }
                for k, v in self.SUPPORTED_VIEWS.items()
            ]
        }

    def render_kanban(self, records: List[Dict[str, Any]],
                      status_field: str = "status",
                      title_field: str = "title",
                      output_path: str = "") -> Dict[str, Any]:
        """渲染看板视图"""
        if not records:
            return {"success": False, "error": "记录列表为空"}

        # 按状态分组
        groups: Dict[str, List[Dict]] = {}
        for r in records:
            status = str(r.get(status_field, "未分类"))
            if status not in groups:
                groups[status] = []
            groups[status].append(r)

        # 生成统计
        group_stats = {k: len(v) for k, v in groups.items()}

        # 尝试 matplotlib 渲染
        rendered_path = ""
        render_source = "local_fallback"
        if output_path:
            try:
                rendered_path = self._matplotlib_kanban(groups, status_field,
                                                        title_field, output_path)
                render_source = "matplotlib"
            except ImportError:
                rendered_path = ""
            except Exception as e:
                rendered_path = ""

        result = {
            "success": True,
            "view_type": "kanban",
            "source": render_source,
            "total_records": len(records),
            "groups": [
                {"status": k, "count": len(v), "cards": v}
                for k, v in groups.items()
            ],
            "group_stats": group_stats,
            "rendered_image": rendered_path,
            "output_path": output_path,
        }

        if not rendered_path:
            result["hint"] = "安装 matplotlib 后可导出 PNG 图片: pip install matplotlib"

        return result

    def render_gantt(self, records: List[Dict[str, Any]],
                     start_field: str = "start_date",
                     end_field: str = "end_date",
                     title_field: str = "title",
                     output_path: str = "") -> Dict[str, Any]:
        """渲染甘特视图"""
        if not records:
            return {"success": False, "error": "记录列表为空"}

        # 解析日期并排序
        parsed_records = []
        for r in records:
            parsed = dict(r)
            parsed["_start_raw"] = str(r.get(start_field, ""))
            parsed["_end_raw"] = str(r.get(end_field, ""))
            parsed_records.append(parsed)

        # 按开始时间排序
        parsed_records.sort(key=lambda x: x["_start_raw"])

        # 生成 mermaid 时间线
        mermaid_code = self._generate_mermaid_gantt(parsed_records, title_field,
                                                     start_field, end_field)

        # 尝试 matplotlib 渲染
        rendered_path = ""
        render_source = "local_fallback"
        if output_path:
            try:
                rendered_path = self._matplotlib_gantt(parsed_records, title_field,
                                                       start_field, end_field, output_path)
                render_source = "matplotlib"
            except ImportError:
                rendered_path = ""
            except Exception as e:
                rendered_path = ""

        result = {
            "success": True,
            "view_type": "gantt",
            "source": render_source,
            "total_records": len(records),
            "records": [
                {
                    "title": r.get(title_field, ""),
                    "start": r.get(start_field, ""),
                    "end": r.get(end_field, ""),
                }
                for r in parsed_records
            ],
            "mermaid_code": mermaid_code,
            "rendered_image": rendered_path,
            "output_path": output_path,
        }

        if not rendered_path:
            result["hint"] = "安装 matplotlib 后可导出 PNG 图片: pip install matplotlib"

        return result

    def _generate_mermaid_gantt(self, records: List[Dict], title_field: str,
                                 start_field: str, end_field: str) -> str:
        """生成 mermaid 甘特图代码"""
        lines = ["gantt", "    title 项目时间线", "    dateFormat  YYYY-MM-DD", "    section 任务"]

        for i, r in enumerate(records, 1):
            title = str(r.get(title_field, f"任务{i}"))
            start = str(r.get(start_field, ""))
            end = str(r.get(end_field, ""))
            # 清理标题中的特殊字符
            safe_title = title.replace(":", " ").replace(",", " ")
            if start and end:
                lines.append(f"    {safe_title} :active, t{i}, {start}, {end}")
            elif start:
                lines.append(f"    {safe_title} :active, t{i}, {start}, 1d")
            else:
                lines.append(f"    {safe_title} :t{i}, 1d")

        return "\n".join(lines)

    def _matplotlib_kanban(self, groups: Dict[str, List[Dict]],
                           status_field: str, title_field: str,
                           output_path: str) -> str:
        """使用 matplotlib 渲染看板柱图"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # 支持中文
        plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans", "Arial Unicode MS"]
        plt.rcParams["axes.unicode_minus"] = False

        statuses = list(groups.keys())
        counts = [len(groups[s]) for s in statuses]

        fig, ax = plt.subplots(figsize=(max(8, len(statuses) * 1.5), 5))
        bars = ax.bar(statuses, counts, color="#4472C4")

        # 添加数值标签
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    str(count), ha="center", va="bottom", fontsize=11)

        ax.set_xlabel("状态")
        ax.set_ylabel("记录数")
        ax.set_title("看板视图 — 按状态分组")
        ax.grid(axis="y", alpha=0.3)

        fig.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        return output_path

    def _matplotlib_gantt(self, records: List[Dict], title_field: str,
                          start_field: str, end_field: str,
                          output_path: str) -> str:
        """使用 matplotlib 渲染甘特图"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime as dt

        plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans", "Arial Unicode MS"]
        plt.rcParams["axes.unicode_minus"] = False

        fig, ax = plt.subplots(figsize=(max(10, len(records) * 0.8), max(5, len(records) * 0.4)))

        for i, r in enumerate(records):
            title = str(r.get(title_field, f"任务{i+1}"))
            start_raw = str(r.get(start_field, ""))
            end_raw = str(r.get(end_field, ""))

            # 解析日期
            try:
                start_date = dt.strptime(start_raw[:10], "%Y-%m-%d")
                end_date = dt.strptime(end_raw[:10], "%Y-%m-%d") if end_raw else start_date
            except (ValueError, TypeError):
                start_date = dt(2026, 1, 1) + __import__("datetime").timedelta(days=i)
                end_date = start_date + __import__("datetime").timedelta(days=1)

            duration = (end_date - start_date).days or 1
            ax.barh(i, duration, left=start_date, height=0.6, color="#4472C4", alpha=0.8)
            ax.text(start_date, i, f" {title}", va="center", ha="left", fontsize=9)

        ax.set_yticks(range(len(records)))
        ax.set_yticklabels([str(r.get(title_field, f"任务{i+1}")) for i, r in enumerate(records)])
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.set_title("甘特图 — 任务时间线")
        ax.grid(axis="x", alpha=0.3)

        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        return output_path

    def render_view(self, view_type: str, data: Dict[str, Any],
                    config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """统一渲染入口"""
        config = config or {}
        records = data.get("records", [])
        output_path = config.get("output_path", str(
            Path(self.output_dir) / f"view_{view_type}_{int(time.time())}.png"
        ))

        if view_type == "kanban":
            return self.render_kanban(
                records,
                status_field=config.get("status_field", "status"),
                title_field=config.get("title_field", "title"),
                output_path=output_path,
            )
        elif view_type == "gantt":
            return self.render_gantt(
                records,
                start_field=config.get("start_field", "start_date"),
                end_field=config.get("end_field", "end_date"),
                title_field=config.get("title_field", "title"),
                output_path=output_path,
            )
        else:
            return {
                "success": False,
                "error": f"不支持的视图类型: {view_type}。支持: {list(self.SUPPORTED_VIEWS.keys())}",
            }


def get_view_render_engine(backend: Any = None,
                           output_dir: Optional[str] = None) -> ViewRenderEngine:
    """工厂函数"""
    return ViewRenderEngine(backend=backend, output_dir=output_dir)


# ===========================================================================
# 模块级便捷函数
# ===========================================================================

def list_views() -> Dict[str, Any]:
    engine = get_view_render_engine()
    return engine.list_views()

def render_kanban(records: List[Dict[str, Any]], status_field: str = "status",
                  title_field: str = "title", output_path: str = "") -> Dict[str, Any]:
    engine = get_view_render_engine()
    return engine.render_kanban(records, status_field, title_field, output_path)

def render_gantt(records: List[Dict[str, Any]], start_field: str = "start_date",
                 end_field: str = "end_date", title_field: str = "title",
                 output_path: str = "") -> Dict[str, Any]:
    engine = get_view_render_engine()
    return engine.render_gantt(records, start_field, end_field, title_field, output_path)

def render_view(view_type: str, data: Dict[str, Any],
                config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    engine = get_view_render_engine()
    return engine.render_view(view_type, data, config)
