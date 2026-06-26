from __future__ import annotations

import argparse
import math
import platform
import re
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont

# Author: https://github.com/sawyer-shi


FONT_DOWNLOAD_URL = "https://raw.githubusercontent.com/sawyer-shi/mind-map-skill/main/resources/chinese_font.ttc"


PALETTE = [
    "#FF6B6B",
    "#4ECDC4",
    "#45B7D1",
    "#96CEB4",
    "#FECA57",
    "#FF9FF3",
    "#54A0FF",
    "#5F27CD",
    "#00D2D3",
    "#FF9F43",
    "#EE5A24",
    "#0984E3",
]


@dataclass
class Node:
    content: str
    level: int
    children: list["Node"] = field(default_factory=list)
    x: float = 0.0
    y: float = 0.0
    w: float = 0.0
    h: float = 0.0
    depth: int = 0
    color: str = "#333333"
    weight: int = 1
    span: float = 0.0


def _clean_markdown_text(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = text.replace("《", "").replace("》", "")
    text = re.sub(r"\*\*(.*?)\*\*:\s*", r"\1: ", text)
    return text.strip()


def parse_markdown_to_tree(markdown_text: str) -> Node:
    markdown_text = markdown_text.replace("\\n", "\n")
    lines = markdown_text.strip().split("\n")

    roots: list[Node] = []
    stack: list[Node] = []
    last_header_level = 0

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line or line.startswith("```"):
            continue

        level = 0
        content = ""
        is_header = False

        if line.startswith("#"):
            header_count = 0
            for ch in line:
                if ch == "#":
                    header_count += 1
                else:
                    break
            level = header_count
            content = line[header_count:].strip()
            is_header = True
            last_header_level = level
        elif re.match(r"^\s*\d+\.\s+", line):
            leading_spaces = len(line) - len(line.lstrip())
            level = leading_spaces // 2 + 2
            content = re.sub(r"^\s*\d+\.\s*", "", line)
            content = _clean_markdown_text(content)
        elif re.match(r"^\s*[-*+]\s+", line):
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces == 0 and last_header_level > 0:
                level = last_header_level + 1
            else:
                level = leading_spaces // 2 + 2
            content = re.sub(r"^\s*[-*+]\s*", "", line)
            content = _clean_markdown_text(content)
        else:
            continue

        if not content:
            continue

        node = Node(content=content, level=level)
        if not is_header and not re.match(r"^\s*[-*+]\s+", line):
            last_header_level = 0

        while stack and stack[-1].level >= level:
            stack.pop()

        if stack:
            stack[-1].children.append(node)
        else:
            roots.append(node)

        stack.append(node)

    if not roots:
        return Node(content="Mind Map", level=1)
    if len(roots) == 1:
        return roots[0]

    return Node(content="Mind Map", level=1, children=roots)


def tree_depth(node: Node) -> int:
    if not node.children:
        return 1
    return 1 + max(tree_depth(c) for c in node.children)


def all_nodes(node: Node) -> list[Node]:
    out = [node]
    for child in node.children:
        out.extend(all_nodes(child))
    return out


def choose_layout(root: Node) -> str:
    depth = tree_depth(root)
    total_nodes = len(all_nodes(root))
    if depth <= 4 and total_nodes <= 100:
        return "center"
    return "horizontal"


def _get_cached_font_path() -> Path:
    cache_dir = Path.home() / ".cache" / "mind-map-skill"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / "chinese_font.ttc"


def _ensure_cached_font() -> Optional[str]:
    cached = _get_cached_font_path()
    if cached.exists() and cached.stat().st_size > 1024:
        return str(cached)

    try:
        with urllib.request.urlopen(FONT_DOWNLOAD_URL, timeout=8) as resp:
            data = resp.read()
        if len(data) > 1024:
            cached.write_bytes(data)
            return str(cached)
    except Exception:
        return None

    return None


def _first_existing(paths: list[str]) -> Optional[str]:
    for path in paths:
        if Path(path).exists():
            return path
    return None


def _find_system_cjk_font() -> Optional[str]:
    system = platform.system()

    if system == "Windows":
        # Prefer Chinese-friendly fonts on Windows.
        return _first_existing(
            [
                "C:/Windows/Fonts/msyh.ttc",      # Microsoft YaHei
                "C:/Windows/Fonts/msyhbd.ttc",
                "C:/Windows/Fonts/msjh.ttc",      # Microsoft JhengHei
                "C:/Windows/Fonts/simhei.ttf",    # SimHei
                "C:/Windows/Fonts/simsun.ttc",    # SimSun
            ]
        )

    if system == "Darwin":
        # Prefer CJK-capable fonts on macOS.
        return _first_existing(
            [
                "/System/Library/Fonts/PingFang.ttc",
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/System/Library/Fonts/Supplemental/Songti.ttc",
                "/System/Library/Fonts/Supplemental/Heiti SC.ttc",
            ]
        )

    # Linux and other Unix-like systems:
    # 1) WenQuanYi/MicroHei family
    # 2) Noto CJK
    # 3) AR PL fallback
    return _first_existing(
        [
            "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
            "/usr/share/fonts/truetype/arphic/uming.ttc",
            "/usr/share/fonts/truetype/arphic/ukai.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )


def _find_font_path() -> Optional[str]:
    cached = _ensure_cached_font()
    if cached:
        return cached

    return _find_system_cjk_font()


def _font(size: int, font_path: Optional[str]) -> Any:
    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _measure(draw: ImageDraw.ImageDraw, text: str, depth: int, font_path: Optional[str]) -> tuple[float, float]:
    font_size = max(36 - depth * 4, 16)
    font = _font(font_size, font_path)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pad = max(18 - depth * 2, 8)
    return text_w + 2 * pad, text_h + 2 * pad


def _assign_weight(node: Node) -> int:
    if not node.children:
        node.weight = 1
        return 1
    node.weight = sum(_assign_weight(c) for c in node.children)
    return node.weight


def _measure_tree(node: Node, depth: int, draw: ImageDraw.ImageDraw, font_path: Optional[str]) -> None:
    node.depth = depth
    node.w, node.h = _measure(draw, node.content, depth, font_path)
    for child in node.children:
        _measure_tree(child, depth + 1, draw, font_path)


def _check_collision(boxes: list[tuple[float, float, float, float]], x: float, y: float, w: float, h: float, margin: float = 16.0) -> bool:
    left1, right1 = x - w / 2 - margin, x + w / 2 + margin
    top1, bottom1 = y - h / 2 - margin, y + h / 2 + margin
    for bx, by, bw, bh in boxes:
        left2, right2 = bx - bw / 2, bx + bw / 2
        top2, bottom2 = by - bh / 2, by + bh / 2
        if not (left1 > right2 or right1 < left2 or top1 > bottom2 or bottom1 < top2):
            return True
    return False


def _node_diagonal(node: Node) -> float:
    return math.sqrt(node.w * node.w + node.h * node.h)


def _layout_center(root: Node) -> None:
    placed_boxes: list[tuple[float, float, float, float]] = []
    min_radius_by_depth: dict[int, float] = {}

    def layout_recursive(
        node: Node,
        depth: int,
        start_angle: float,
        end_angle: float,
        color: str,
        parent_radius: float,
        parent_diagonal: float,
        root_child_idx: int = 0,
    ) -> None:
        node.depth = depth
        node.color = "#333333" if depth == 0 else color

        if depth == 0:
            node.x, node.y = 0.0, 0.0
            current_radius = 0.0
        else:
            mid_angle = (start_angle + end_angle) / 2.0
            curr_diag = _node_diagonal(node)

            base_min = 110 + (depth - 1) * 120
            hierarchy_min = parent_radius + parent_diagonal / 2 + curr_diag / 2 + 40
            depth_min = min_radius_by_depth.get(depth, 0.0)
            radius_base = max(base_min, hierarchy_min, depth_min)

            if depth == 1:
                radius_base += root_child_idx * 8

            current_radius = radius_base
            placed = False
            step = 18 + depth * 4
            for attempt in range(220):
                test_r = radius_base + attempt * step
                x = math.cos(mid_angle) * test_r
                y = math.sin(mid_angle) * test_r
                if not _check_collision(placed_boxes, x, y, node.w, node.h, margin=14):
                    node.x, node.y = x, y
                    current_radius = test_r
                    placed = True
                    break

            if not placed:
                node.x = math.cos(mid_angle) * current_radius
                node.y = math.sin(mid_angle) * current_radius

            min_radius_by_depth[depth] = max(min_radius_by_depth.get(depth, 0.0), current_radius)

        placed_boxes.append((node.x, node.y, node.w, node.h))

        if not node.children:
            return

        total_weight = max(sum(c.weight for c in node.children), 1)
        cursor = start_angle
        for idx, child in enumerate(node.children):
            sector = (child.weight / total_weight) * (end_angle - start_angle)
            child_color = PALETTE[idx % len(PALETTE)] if depth == 0 else color
            layout_recursive(
                child,
                depth + 1,
                cursor,
                cursor + sector,
                child_color,
                parent_radius=current_radius,
                parent_diagonal=_node_diagonal(node),
                root_child_idx=idx,
            )
            cursor += sector

    layout_recursive(root, 0, -math.pi, math.pi, "#333333", parent_radius=0.0, parent_diagonal=0.0)


def _calc_span(node: Node, v_gap: float = 42.0) -> float:
    own_span = node.h + 24
    if not node.children:
        node.span = own_span
        return node.span
    children_span = sum(_calc_span(c, v_gap) for c in node.children)
    children_span += v_gap * max(len(node.children) - 1, 0)
    node.span = max(own_span, children_span)
    return node.span


def _layout_horizontal(node: Node, depth: int, x: float, y_center: float, color: str) -> None:
    node.depth = depth
    node.color = "#333333" if depth == 0 else color
    node.x, node.y = x, y_center
    if not node.children:
        return

    max_child_w = max(c.w for c in node.children)
    child_x = x + node.w / 2 + max_child_w / 2 + 170

    total = sum(c.span for c in node.children) + 42 * max(len(node.children) - 1, 0)
    top = y_center - total / 2

    for idx, child in enumerate(node.children):
        child_y = top + child.span / 2
        child_color = PALETTE[idx % len(PALETTE)] if depth == 0 else color
        _layout_horizontal(child, depth + 1, child_x, child_y, child_color)
        top += child.span + 42


def _draw_tree(root: Node, out_path: Path) -> None:
    tmp = Image.new("RGB", (8, 8), "white")
    probe = ImageDraw.Draw(tmp)
    font_path = _find_font_path()

    for n in all_nodes(root):
        n.w, n.h = _measure(probe, n.content, n.depth, font_path)

    min_x = min(n.x - n.w / 2 for n in all_nodes(root))
    max_x = max(n.x + n.w / 2 for n in all_nodes(root))
    min_y = min(n.y - n.h / 2 for n in all_nodes(root))
    max_y = max(n.y + n.h / 2 for n in all_nodes(root))

    margin = 120
    width = int(max_x - min_x + 2 * margin)
    height = int(max_y - min_y + 2 * margin)
    width = max(width, 900)
    height = max(height, 700)

    shift_x = margin - min_x
    shift_y = margin - min_y

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    def pxy(n: Node) -> tuple[float, float]:
        return n.x + shift_x, n.y + shift_y

    for n in all_nodes(root):
        sx, sy = pxy(n)
        for c in n.children:
            ex, ey = pxy(c)
            draw.line([(sx, sy), (ex, ey)], fill=c.color, width=max(1, 4 - c.depth))

    for n in all_nodes(root):
        px, py = pxy(n)
        x1, y1 = px - n.w / 2, py - n.h / 2
        x2, y2 = px + n.w / 2, py + n.h / 2
        draw.rounded_rectangle((x1, y1, x2, y2), radius=8, fill="white", outline=n.color, width=3 if n.depth <= 1 else 2)

        font_size = max(36 - n.depth * 4, 16)
        font = _font(font_size, font_path)
        draw.text((px, py), n.content, font=font, fill=n.color, anchor="mm")

    image.save(out_path, "PNG")


def generate_mind_map(
    markdown_content: str,
    layout_type: str = "free",
    filename: Optional[str] = None,
    download_md: bool = False,
    output_dir: str = ".",
) -> dict:
    if not markdown_content or not markdown_content.strip():
        raise ValueError("markdown_content is required")

    layout_type = (layout_type or "free").lower().strip()
    if layout_type not in {"free", "center", "horizontal"}:
        raise ValueError("layout_type must be one of: free, center, horizontal")

    root = parse_markdown_to_tree(markdown_content)
    selected_layout = choose_layout(root) if layout_type == "free" else layout_type

    root.depth = 0
    root.color = "#333333"

    temp_probe = Image.new("RGB", (8, 8), "white")
    probe_draw = ImageDraw.Draw(temp_probe)
    probe_font = _find_font_path()
    _measure_tree(root, 0, probe_draw, probe_font)

    if selected_layout == "center":
        _assign_weight(root)
        _layout_center(root)
    else:
        for n in all_nodes(root):
            n.depth = 0
            n.w, n.h = _measure(probe_draw, n.content, 0, probe_font)
        _calc_span(root)
        _layout_horizontal(root, depth=0, x=0.0, y_center=0.0, color="#333333")

    safe_name = filename.strip() if filename else f"mind_map_{selected_layout}_{int(time.time())}"
    safe_name = re.sub(r"[^\w\-.]", "_", safe_name)
    if not safe_name.lower().endswith(".png"):
        safe_name += ".png"

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / safe_name

    _draw_tree(root, png_path)

    md_path: Optional[Path] = None
    if download_md:
        md_path = png_path.with_suffix(".md")
        md_path.write_text(markdown_content, encoding="utf-8")

    return {
        "success": True,
        "selected_layout": selected_layout,
        "tree_depth": tree_depth(root),
        "total_nodes": len(all_nodes(root)),
        "png_path": str(png_path),
        "md_path": str(md_path) if md_path else None,
    }


def _cli(default_layout: str) -> None:
    parser = argparse.ArgumentParser(description="Generate mind map PNG from markdown text")
    parser.add_argument("--markdown-content", required=True, help="Markdown content")
    parser.add_argument("--layout-type", default=default_layout, choices=["free", "center", "horizontal"])
    parser.add_argument("--filename", default="")
    parser.add_argument("--download-md", action="store_true")
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    result = generate_mind_map(
        markdown_content=args.markdown_content,
        layout_type=args.layout_type,
        filename=args.filename or None,
        download_md=args.download_md,
        output_dir=args.output_dir,
    )
    print(result)


if __name__ == "__main__":
    _cli(default_layout="free")
