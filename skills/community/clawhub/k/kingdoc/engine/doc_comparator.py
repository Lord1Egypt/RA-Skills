"""KingDoc 文档对比模块

复用 conflict_resolver.py 的 difflib 引擎，提供面向用户的文档对比能力：
- 差异高亮（HTML/Markdown）
- 变更摘要（增删改统计）
- 导出对比报告

设计原则：
- 复用 difflib：不重新发明算法
- 硬件自适应：大文档分块对比
"""
from __future__ import annotations

import difflib
from pathlib import Path
from typing import Dict, List, Optional

from engine.hardware import get_recommended_settings


# ---------------------------------------------------------------------------
# 文档对比器
# ---------------------------------------------------------------------------

class DocComparator:
    """文档对比器"""

    def __init__(self):
        hw = get_recommended_settings()
        self.max_chunk_chars = hw["batch_chunk"] * 200

    def compare(self, text_a: str, text_b: str,
                label_a: str = "版本A", label_b: str = "版本B") -> Dict:
        """对比两版文档的差异。

        返回：
        {
          "identical": bool,
          "diff_lines": [{"type": "same/remove/add", "text": "...", "line_no": N}],
          "summary": {"added": N, "removed": N, "same": N, "total_changed": N},
          "similarity": float  # 0-1
        }
        """
        lines_a = text_a.splitlines()
        lines_b = text_b.splitlines()

        matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
        diff_lines = []
        summary = {"added": 0, "removed": 0, "same": 0, "total_changed": 0}
        line_no_a = 0
        line_no_b = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for i in range(i1, i2):
                    line_no_a += 1
                    line_no_b += 1
                    diff_lines.append({
                        "type": "same",
                        "text": lines_a[i],
                        "line_no_a": line_no_a,
                        "line_no_b": line_no_b,
                    })
                summary["same"] += (i2 - i1)
            elif tag == "delete":
                for i in range(i1, i2):
                    line_no_a += 1
                    diff_lines.append({
                        "type": "remove",
                        "text": lines_a[i],
                        "line_no_a": line_no_a,
                        "line_no_b": None,
                    })
                summary["removed"] += (i2 - i1)
                summary["total_changed"] += (i2 - i1)
            elif tag == "insert":
                for j in range(j1, j2):
                    line_no_b += 1
                    diff_lines.append({
                        "type": "add",
                        "text": lines_b[j],
                        "line_no_a": None,
                        "line_no_b": line_no_b,
                    })
                summary["added"] += (j2 - j1)
                summary["total_changed"] += (j2 - j1)
            elif tag == "replace":
                for i in range(i1, i2):
                    line_no_a += 1
                    diff_lines.append({
                        "type": "remove",
                        "text": lines_a[i],
                        "line_no_a": line_no_a,
                        "line_no_b": None,
                    })
                for j in range(j1, j2):
                    line_no_b += 1
                    diff_lines.append({
                        "type": "add",
                        "text": lines_b[j],
                        "line_no_a": None,
                        "line_no_b": line_no_b,
                    })
                summary["removed"] += (i2 - i1)
                summary["added"] += (j2 - j1)
                summary["total_changed"] += (i2 - i1) + (j2 - j1)

        similarity = matcher.ratio()

        return {
            "identical": text_a == text_b,
            "diff_lines": diff_lines,
            "summary": summary,
            "similarity": round(similarity, 4),
        }

    def compare_files(self, file_a: str, file_b: str,
                      label_a: str = "文件A", label_b: str = "文件B") -> Dict:
        """对比两个文件。"""
        path_a = Path(file_a)
        path_b = Path(file_b)

        if not path_a.exists() or not path_b.exists():
            return {"error": f"文件不存在: {file_a} 或 {file_b}"}

        text_a = path_a.read_text(encoding="utf-8")
        text_b = path_b.read_text(encoding="utf-8")

        result = self.compare(text_a, text_b, label_a, label_b)
        result["file_a"] = str(path_a)
        result["file_b"] = str(path_b)
        return result

    def diff_highlight(self, text_a: str, text_b: str,
                       format: str = "markdown") -> str:
        """生成差异高亮（HTML 或 Markdown）。

        format: "markdown" | "html"
        """
        comparison = self.compare(text_a, text_b)
        diff_lines = comparison["diff_lines"]

        if format == "html":
            rows = []
            for item in diff_lines:
                css_class = {"same": "diff-same", "remove": "diff-remove", "add": "diff-add"}[item["type"]]
                prefix = {"same": "  ", "remove": "- ", "add": "+ "}[item["type"]]
                rows.append(
                    f'<tr class="{css_class}">'
                    f"<td class='num'>{item.get('line_no_a') or ''}</td>"
                    f"<td class='num'>{item.get('line_no_b') or ''}</td>"
                    f"<td class='prefix'>{prefix}</td>"
                    f"<td class='content'>{item['text']}</td>"
                    f"</tr>"
                )
            return (
                "<html><head><style>"
                "body{font-family:monospace;font-size:13px}"
                "table{border-collapse:collapse;width:100%}"
                "td{padding:2px 8px;white-space:pre-wrap;border-bottom:1px solid #eee}"
                ".num{width:36px;color:#999;text-align:right}"
                ".prefix{width:20px;color:#999}"
                ".diff-same{background:#fff}"
                ".diff-remove{background:#fee;color:#c00}"
                ".diff-add{background:#efe;color:#080}"
                "</style></head><body>"
                f"<p>相似度: {comparison['similarity']*100:.1f}% | "
                f"新增: +{comparison['summary']['added']} 删除: -{comparison['summary']['removed']}</p>"
                f"<table>{''.join(rows)}</table></body></html>"
            )
        else:
            # Markdown format
            lines = []
            for item in diff_lines:
                prefix = {"same": "  ", "remove": "- ", "add": "+ "}[item["type"]]
                lines.append(f"{prefix}{item['text']}")
            header = (
                f"**相似度**: {comparison['similarity']*100:.1f}% | "
                f"新增: +{comparison['summary']['added']} 删除: -{comparison['summary']['removed']}\n\n"
            )
            return header + "\n".join(lines)

    def change_summary(self, text_a: str, text_b: str) -> Dict:
        """变更摘要（增删改统计 + 关键变化）。"""
        comparison = self.compare(text_a, text_b)
        summary = comparison["summary"]

        # 提取关键变化（新增/删除的内容摘要）
        key_changes = []
        for item in comparison["diff_lines"]:
            if item["type"] == "add":
                key_changes.append(f"+ {item['text'][:50]}")
            elif item["type"] == "remove":
                key_changes.append(f"- {item['text'][:50]}")

        return {
            "added_lines": summary["added"],
            "removed_lines": summary["removed"],
            "changed_lines": summary["total_changed"],
            "similarity": comparison["similarity"],
            "key_changes": key_changes[:10],  # 最多 10 个关键变化
        }

    def export_report(self, text_a: str, text_b: str,
                      format: str = "markdown") -> str:
        """导出对比报告。"""
        comparison = self.compare(text_a, text_b)
        summary = comparison["summary"]

        if format == "markdown":
            report = (
                f"# 文档对比报告\n\n"
                f"## 概览\n\n"
                f"| 指标 | 数值 |\n"
                f"|------|------|\n"
                f"| 相似度 | {comparison['similarity']*100:.1f}% |\n"
                f"| 新增行数 | +{summary['added']} |\n"
                f"| 删除行数 | -{summary['removed']} |\n"
                f"| 变更总行数 | {summary['total_changed']} |\n\n"
                f"## 差异详情\n\n"
            )
            for item in comparison["diff_lines"]:
                prefix = {"same": "  ", "remove": "- ", "add": "+ "}[item["type"]]
                report += f"{prefix}{item['text']}\n"
            return report
        else:
            return self.diff_highlight(text_a, text_b, format="html")


# ---------------------------------------------------------------------------
# 便捷函数
# ---------------------------------------------------------------------------

_comparator = None


def _get() -> DocComparator:
    global _comparator
    if _comparator is None:
        _comparator = DocComparator()
    return _comparator


def compare_documents(text_a: str, text_b: str,
                      label_a: str = "版本A", label_b: str = "版本B") -> Dict:
    return _get().compare(text_a, text_b, label_a, label_b)


def compare_files(file_a: str, file_b: str) -> Dict:
    return _get().compare_files(file_a, file_b)


def diff_highlight(text_a: str, text_b: str, format: str = "markdown") -> str:
    return _get().diff_highlight(text_a, text_b, format)


def change_summary(text_a: str, text_b: str) -> Dict:
    return _get().change_summary(text_a, text_b)


def export_report(text_a: str, text_b: str, format: str = "markdown") -> str:
    return _get().export_report(text_a, text_b, format)
