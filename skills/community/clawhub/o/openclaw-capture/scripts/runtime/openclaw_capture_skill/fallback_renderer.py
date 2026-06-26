"""Deterministic Markdown renderer for local preview and no-key environments."""

from __future__ import annotations


class FallbackNoteRenderer:
    def render(self, materials) -> str:
        summary = materials.get("summary", {}) if isinstance(materials, dict) else {}
        evidence = materials.get("evidence", {}) if isinstance(materials, dict) else {}
        title = str(summary.get("title") or "未命名内容").strip()
        conclusion = str(summary.get("conclusion") or "").strip()
        bullets = [str(item).strip() for item in summary.get("bullets", []) if str(item).strip()]
        actions = [str(item).strip() for item in summary.get("follow_up_actions", []) if str(item).strip()]
        quotes = [str(item).strip() for item in summary.get("evidence_quotes", []) if str(item).strip()]
        source_url = str(evidence.get("source_url") or "").strip()

        lines: list[str] = [f"# {title}", ""]
        if conclusion:
            lines.extend(["## 一句话总结", "", conclusion, ""])
        if bullets:
            lines.append("## 关键要点")
            lines.append("")
            lines.extend([f"- {item}" for item in bullets[:8]])
            lines.append("")
        if actions:
            lines.append("## 下一步")
            lines.append("")
            lines.extend([f"- {item}" for item in actions[:6]])
            lines.append("")
        if quotes:
            lines.append("## 关键证据")
            lines.append("")
            lines.extend([f"- {item}" for item in quotes[:8]])
            lines.append("")
        if source_url:
            lines.extend(["## 来源", "", f"- {source_url}", ""])
        return "\n".join(lines).strip() + "\n"

