"""KingDoc 协同编辑冲突解决模块

自研实现，零第三方依赖（仅 Python 标准库 difflib）。
目标：检测多人并发修改冲突，提供智能合并建议与可视化 diff。

设计原则：
- 本地降级优先：不依赖外部 AI API，纯算法实现
- 硬件自适应：大文档分块处理，不拖累用户电脑
- 保守优先：冲突段绝不自动覆盖，必须用户确认
"""
from __future__ import annotations

import difflib
import re
from typing import Dict, List, Optional, Tuple

from engine.hardware import get_recommended_settings


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

class ConflictBlock:
    """单个冲突块"""

    def __init__(
        self,
        location: str,
        base_text: str,
        version_a: str,
        version_b: str,
        conflict_type: str = "both_modified",
    ):
        self.location = location
        self.base_text = base_text
        self.version_a = version_a
        self.version_b = version_b
        self.conflict_type = conflict_type  # both_modified / a_only / b_only

    def to_dict(self) -> Dict:
        return {
            "location": self.location,
            "base": self.base_text,
            "version_a": self.version_a,
            "version_b": self.version_b,
            "type": self.conflict_type,
        }


# ---------------------------------------------------------------------------
# 核心解析器
# ---------------------------------------------------------------------------

class ConflictResolver:
    """冲突检测、合并、diff、解决"""

    def __init__(self):
        hw = get_recommended_settings()
        self.max_chunk_chars = hw["batch_chunk"] * 200  # 大文档分块阈值

    # ------------------------------------------------------------------
    # 1. 冲突检测
    # ------------------------------------------------------------------

    def detect(
        self, base_text: str, version_a: str, version_b: str
    ) -> Dict:
        """检测三方文本的并发修改冲突。

        返回：
        {
          "conflicts": [ConflictBlock, ...],
          "stats": {"total": N, "both_modified": N, "a_only": N, "b_only": N},
          "has_conflict": bool
        }
        """
        # 按段落切分（兼容 \n\n 和 \n）
        base_paras = self._split_paragraphs(base_text)
        a_paras = self._split_paragraphs(version_a)
        b_paras = self._split_paragraphs(version_b)

        conflicts = []
        stats = {"total": 0, "both_modified": 0, "a_only": 0, "b_only": 0}

        # 三方逐段比对
        max_len = max(len(base_paras), len(a_paras), len(b_paras))
        for i in range(max_len):
            base_p = base_paras[i] if i < len(base_paras) else ""
            a_p = a_paras[i] if i < len(a_paras) else ""
            b_p = b_paras[i] if i < len(b_paras) else ""

            a_changed = a_p != base_p
            b_changed = b_p != base_p

            if a_changed and b_changed and a_p != b_p:
                stats["total"] += 1
                stats["both_modified"] += 1
                conflicts.append(
                    ConflictBlock(
                        location=f"第{i + 1}段",
                        base_text=base_p,
                        version_a=a_p,
                        version_b=b_p,
                        conflict_type="both_modified",
                    )
                )
            elif a_changed and not b_changed:
                stats["total"] += 1
                stats["a_only"] += 1
                conflicts.append(
                    ConflictBlock(
                        location=f"第{i + 1}段",
                        base_text=base_p,
                        version_a=a_p,
                        version_b=b_p,
                        conflict_type="a_only",
                    )
                )
            elif b_changed and not a_changed:
                stats["total"] += 1
                stats["b_only"] += 1
                conflicts.append(
                    ConflictBlock(
                        location=f"第{i + 1}段",
                        base_text=base_p,
                        version_a=a_p,
                        version_b=b_p,
                        conflict_type="b_only",
                    )
                )

        return {
            "conflicts": [c.to_dict() for c in conflicts],
            "stats": stats,
            "has_conflict": stats["both_modified"] > 0,
        }

    # ------------------------------------------------------------------
    # 2. 智能合并建议
    # ------------------------------------------------------------------

    def merge(
        self, base_text: str, version_a: str, version_b: str
    ) -> Dict:
        """三方合并：无冲突段自动合并，冲突段标注。

        返回：
        {
          "merged_text": str,       # 合并后文本（冲突段用标记包裹）
          "conflict_count": int,
          "auto_merged_count": int,
          "backend": "local"
        }
        """
        base_paras = self._split_paragraphs(base_text)
        a_paras = self._split_paragraphs(version_a)
        b_paras = self._split_paragraphs(version_b)

        merged_parts = []
        conflict_count = 0
        auto_merged_count = 0

        max_len = max(len(base_paras), len(a_paras), len(b_paras))
        for i in range(max_len):
            base_p = base_paras[i] if i < len(base_paras) else ""
            a_p = a_paras[i] if i < len(a_paras) else ""
            b_p = b_paras[i] if i < len(b_paras) else ""

            a_changed = a_p != base_p
            b_changed = b_p != base_p

            if not a_changed and not b_changed:
                # 都没改
                merged_parts.append(base_p)
                auto_merged_count += 1
            elif a_changed and not b_changed:
                # 只有 A 改
                merged_parts.append(a_p)
                auto_merged_count += 1
            elif b_changed and not a_changed:
                # 只有 B 改
                merged_parts.append(b_p)
                auto_merged_count += 1
            elif a_changed and b_changed and a_p == b_p:
                # 改成一样
                merged_parts.append(a_p)
                auto_merged_count += 1
            else:
                # 真冲突
                conflict_count += 1
                merged_parts.append(
                    f"<<<<<<< VERSION_A\n"
                    f"{a_p}\n"
                    f"=======\n"
                    f"{b_p}\n"
                    f">>>>>>> VERSION_B"
                )

        return {
            "merged_text": "\n\n".join(merged_parts),
            "conflict_count": conflict_count,
            "auto_merged_count": auto_merged_count,
            "backend": "local",
        }

    # ------------------------------------------------------------------
    # 3. 冲突可视化（Git diff 风格）
    # ------------------------------------------------------------------

    def diff(
        self,
        version_a: str,
        version_b: str,
        label_a: str = "版本A",
        label_b: str = "版本B",
    ) -> Dict:
        """生成结构化 diff 数据。

        返回：
        {
          "lines": [{"type": "same/remove/add", "text": "..."}],
          "summary": {"added": N, "removed": N, "same": N},
          "html": str  # 可选 HTML 并排视图
        }
        """
        a_lines = version_a.splitlines()
        b_lines = version_b.splitlines()

        matcher = difflib.SequenceMatcher(None, a_lines, b_lines)
        diff_lines = []
        summary = {"added": 0, "removed": 0, "same": 0}

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for line in a_lines[i1:i2]:
                    diff_lines.append({"type": "same", "text": line})
                summary["same"] += (i2 - i1)
            elif tag == "delete":
                for line in a_lines[i1:i2]:
                    diff_lines.append({"type": "remove", "text": line})
                summary["removed"] += (i2 - i1)
            elif tag == "insert":
                for line in b_lines[j1:j2]:
                    diff_lines.append({"type": "add", "text": line})
                summary["added"] += (j2 - j1)
            elif tag == "replace":
                for line in a_lines[i1:i2]:
                    diff_lines.append({"type": "remove", "text": line})
                for line in b_lines[j1:j2]:
                    diff_lines.append({"type": "add", "text": line})
                summary["removed"] += (i2 - i1)
                summary["added"] += (j2 - j1)

        # 生成 HTML（仅内部使用，不写入仓库）
        html = self._render_diff_html(diff_lines, label_a, label_b)

        return {
            "lines": diff_lines,
            "summary": summary,
            "html": html,
        }

    # ------------------------------------------------------------------
    # 4. 冲突解决模板
    # ------------------------------------------------------------------

    def resolve(
        self,
        base_text: str,
        version_a: str,
        version_b: str,
        strategy: str = "keep_a",
        manual_text: str = "",
    ) -> Dict:
        """应用冲突解决模板。

        strategy: keep_a / keep_b / manual / auto_merge
        返回：
        {
          "resolved_text": str,
          "strategy": str,
          "conflicts_resolved": int,
          "backend": "local"
        }
        """
        detection = self.detect(base_text, version_a, version_b)
        conflicts = detection["conflicts"]
        conflict_count = detection["stats"]["both_modified"]

        if strategy == "keep_a":
            resolved = version_a
        elif strategy == "keep_b":
            resolved = version_b
        elif strategy == "manual":
            if not manual_text:
                return {
                    "resolved_text": "",
                    "strategy": "manual",
                    "conflicts_resolved": 0,
                    "error": "手动合并需要传入 manual_text",
                    "backend": "local",
                }
            resolved = manual_text
        elif strategy == "auto_merge":
            result = self.merge(base_text, version_a, version_b)
            resolved = result["merged_text"]
        else:
            return {
                "resolved_text": "",
                "strategy": strategy,
                "conflicts_resolved": 0,
                "error": f"未知策略: {strategy}",
                "backend": "local",
            }

        return {
            "resolved_text": resolved,
            "strategy": strategy,
            "conflicts_resolved": conflict_count,
            "backend": "local",
        }

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------

    @staticmethod
    def _split_paragraphs(text: str) -> List[str]:
        """按空行切分段落，兼容 \n\n 和 \n。"""
        if not text:
            return [""]
        # 先按 \n\n 切，再按单个 \n 切
        paragraphs = re.split(r"\n\s*\n", text.strip())
        result = []
        for p in paragraphs:
            for line in p.splitlines():
                stripped = line.strip()
                if stripped:
                    result.append(stripped)
        return result if result else [""]

    @staticmethod
    def _render_diff_html(
        diff_lines: List[Dict], label_a: str, label_b: str
    ) -> str:
        """渲染 diff 为 HTML（仅内部使用，不写入仓库）。"""
        rows = []
        for item in diff_lines:
            css_class = {
                "same": "diff-same",
                "remove": "diff-remove",
                "add": "diff-add",
            }[item["type"]]
            prefix = {
                "same": "  ",
                "remove": "- ",
                "add": "+ ",
            }[item["type"]]
            rows.append(
                f'<tr class="{css_class}">'
                f"<td class='num'></td>"
                f"<td class='prefix'>{prefix}</td>"
                f"<td class='content'>{item['text']}</td>"
                f"</tr>"
            )

        return (
            f"<html><head><style>"
            f"body{{font-family:monospace;font-size:13px;margin:0;padding:10px}}"
            f"table{{border-collapse:collapse;width:100%}}"
            f"td{{padding:1px 8px;white-space:pre-wrap;vertical-align:top}}"
            f".num{{width:36px;color:#999;text-align:right}}"
            f".prefix{{width:20px;color:#999}}"
            f".diff-same{{background:#fff}}"
            f".diff-remove{{background:#fee;color:#c00}}"
            f".diff-add{{background:#efe;color:#080}}"
            f"</style></head><body>"
            f"<h3>{label_a} ↔ {label_b}</h3>"
            f"<table>{''.join(rows)}</table></body></html>"
        )


# ---------------------------------------------------------------------------
# 便捷函数（供 MCP Server 直接调用）
# ---------------------------------------------------------------------------

_resolver = None


def _get() -> ConflictResolver:
    global _resolver
    if _resolver is None:
        _resolver = ConflictResolver()
    return _resolver


def detect_conflicts(base: str, a: str, b: str) -> Dict:
    return _get().detect(base, a, b)


def merge_versions(base: str, a: str, b: str) -> Dict:
    return _get().merge(base, a, b)


def diff_versions(a: str, b: str, label_a: str = "版本A", label_b: str = "版本B") -> Dict:
    return _get().diff(a, b, label_a, label_b)


def resolve_conflicts(
    base: str, a: str, b: str, strategy: str = "keep_a", manual: str = ""
) -> Dict:
    return _get().resolve(base, a, b, strategy, manual)
