"""TTS-optimized output formatting for podcast-intel."""

from typing import Any, List


def _get(obj: Any, key: str, default: Any = None) -> Any:
    """Access dict keys or object attributes uniformly."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def format_tts_briefing(analyses: List[Any], top_n: int = 5) -> str:
    """
    Format episode analyses into spoken-word briefing text.
    Optimized for text-to-speech readability.
    """
    briefing_text = "Podcast Briefing.\n\n"
    
    # Sort by worth_your_time_score descending
    sorted_analyses = sorted(
        analyses,
        key=lambda a: _get(a, "worth_your_time_score", 0.0),
        reverse=True,
    )[:top_n]
    
    for i, analysis in enumerate(sorted_analyses, 1):
        wyt_percent = int(_get(analysis, "worth_your_time_score", 0.0) * 100)
        show = _get(analysis, "show", "Unknown Show")
        title = _get(analysis, "title", "Untitled")
        novel_minutes = float(_get(analysis, "novel_minutes", 0.0))
        total_minutes = float(_get(analysis, "total_minutes", 0.0))

        briefing_text += f"{i}. {show}: {title}. Worth your time: {wyt_percent} percent.\n"
        
        # Add recommendation summary
        if wyt_percent >= 75:
            briefing_text += f"   Recommendation: Highly recommended. {novel_minutes:.0f} minutes of novel content.\n"
        elif wyt_percent >= 50:
            briefing_text += (
                f"   Recommendation: Recommended. {novel_minutes:.0f} minutes of "
                f"valuable content out of {total_minutes:.0f}.\n"
            )
        else:
            briefing_text += f"   Recommendation: Pass. Minimal novel content or overlaps with recent episodes.\n"

        # Add top segment recommendations
        segments = _get(analysis, "segments_ranked", []) or []
        top_segments = sorted(
            segments,
            key=lambda s: _get(s, "composite_score", 0.0),
            reverse=True,
        )[:2]

        if top_segments:
            briefing_text += f"   Top topics: "
            briefing_text += ", ".join([_get(s, "label", "Unknown topic") for s in top_segments])
            briefing_text += ".\n"

        # Add overlap warnings
        overlaps = _get(analysis, "overlaps", []) or []
        if overlaps:
            briefing_text += f"   Note: Overlaps with other recent episodes on "
            overlap_topics = [_get(o, "topic", "unknown topic") for o in overlaps]
            briefing_text += ", ".join(overlap_topics) + ".\n"

        briefing_text += "\n"

    return briefing_text


def format_markdown_briefing(analyses: List[Any], top_n: int = 5) -> str:
    """Format episode analyses as markdown briefing."""
    markdown = "## 🎧 Podcast Briefing\n\n"
    
    # Sort by worth_your_time_score descending
    sorted_analyses = sorted(
        analyses,
        key=lambda a: _get(a, "worth_your_time_score", 0.0),
        reverse=True,
    )[:top_n]
    
    for analysis in sorted_analyses:
        wyt_percent = int(_get(analysis, "worth_your_time_score", 0.0) * 100)
        show = _get(analysis, "show", "Unknown Show")
        title = _get(analysis, "title", "Untitled")
        novel_minutes = float(_get(analysis, "novel_minutes", 0.0))
        total_minutes = float(_get(analysis, "total_minutes", 0.0))
        
        # Determine emoji based on score
        if wyt_percent >= 75:
            emoji = "🎯"
        elif wyt_percent >= 50:
            emoji = "👍"
        else:
            emoji = "⏸️"
        
        markdown += f"### {emoji} {show}: {title} (WYT: {wyt_percent}%)\n"
        markdown += f"- **Worth listening:** {novel_minutes:.0f} min of {total_minutes:.0f} min total\n"

        # Top segments
        segments = _get(analysis, "segments_ranked", []) or []
        top_segments = sorted(
            segments,
            key=lambda s: _get(s, "composite_score", 0.0),
            reverse=True,
        )[:3]

        if top_segments:
            markdown += "- **Key topics:** "
            markdown += ", ".join([_get(s, "label", "Unknown topic") for s in top_segments])
            markdown += "\n"

        # Segments to skip
        skip_segments = [
            s
            for s in segments
            if "SKIP" in str(_get(s, "listen_recommendation", "")).upper()
        ]
        if skip_segments:
            markdown += "- **Skip:** "
            markdown += ", ".join([_get(s, "label", "Unknown topic") for s in skip_segments[:2]])
            markdown += "\n"

        # Overlaps
        overlaps = _get(analysis, "overlaps", []) or []
        if overlaps:
            markdown += (
                "- **Note:** Overlaps with "
                + ", ".join([_get(o, "overlaps_with_show", "another show") for o in overlaps[:2]])
                + "\n"
            )

        markdown += f"\n{_get(analysis, 'recommendation', '')}\n\n"

    return markdown
