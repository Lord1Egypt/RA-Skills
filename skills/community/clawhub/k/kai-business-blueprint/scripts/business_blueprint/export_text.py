from __future__ import annotations


def estimate_svg_text_width(text: str, font_size: float = 11) -> float:
    width = 0.0
    for ch in text:
        if ch in " \t":
            width += font_size * 0.32
        elif ch in "ilI1|!.,:;'`":
            width += font_size * 0.34
        elif ch.isascii():
            width += font_size * (0.68 if ch.isupper() else 0.56)
        else:
            width += font_size * 0.96
    return width


def wrap_text_to_width(
    text: str,
    max_px: float,
    font_size: float = 11,
    max_lines: int | None = 2,
    ellipsize: bool = True,
) -> list[str]:
    if not text:
        return [""]

    lines: list[str] = []
    current: list[str] = []
    current_px = 0.0
    line_limit = max_lines if max_lines is not None else float("inf")

    for ch in text:
        if ch in "\n\r":
            if current:
                lines.append("".join(current).strip())
                current = []
                current_px = 0.0
            continue
        ch_px = estimate_svg_text_width(ch, font_size=font_size)
        if current and current_px + ch_px > max_px:
            lines.append("".join(current).strip())
            current = [ch]
            current_px = ch_px
            if len(lines) >= line_limit:
                break
        else:
            current.append(ch)
            current_px += ch_px

    if len(lines) < line_limit and current:
        lines.append("".join(current).strip())

    lines = [line for line in lines if line]
    if not lines:
        return [text.strip() or text]

    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]

    consumed = "".join(lines)
    if ellipsize and len(consumed) < len(text):
        lines[-1] = lines[-1].rstrip("，、。：:；;,. ") + "…"
    return lines


def wrap_timeline_text(
    text: str,
    max_units: int = 22,
    max_lines: int | None = 2,
    ellipsize: bool = True,
) -> list[str]:
    """Wrap mixed CJK/ASCII text into short lines for timeline cards."""
    return wrap_text_to_width(
        text,
        max_px=max_units * 5.6,
        font_size=11,
        max_lines=max_lines,
        ellipsize=ellipsize,
    )
