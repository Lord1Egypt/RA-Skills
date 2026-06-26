"""Markdown → DocSpec AST 解析器"""

from markdown_it import MarkdownIt

_md = MarkdownIt("gfm-like")

# 输入体积限制
MAX_MARKDOWN_SIZE = 200 * 1024  # 200KB
MAX_IMAGES = 20
MAX_TABLE_ROWS = 50
MAX_TABLE_COLS = 20


def parse_markdown_to_docspec(markdown: str) -> dict:
    """
    将 Markdown 文本解析为 DocSpec AST。
    """
    if not markdown or not markdown.strip():
        return {"blocks": [], "sections": [], "metadata": {}}

    # 输入体积限制
    if len(markdown.encode("utf-8")) > MAX_MARKDOWN_SIZE:
        markdown = markdown.encode("utf-8")[:MAX_MARKDOWN_SIZE].decode("utf-8", errors="ignore")

    text = markdown.strip()
    metadata = {}

    # 提取 YAML front matter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                metadata = yaml.safe_load(parts[1]) or {}
                text = parts[2].strip()
            except Exception:
                pass

    tokens = _md.parse(text)
    blocks = _tokens_to_blocks(tokens)
    sections = _blocks_to_sections(blocks)

    return {
        "blocks": blocks,
        "sections": sections,
        "metadata": metadata,
    }


def _tokens_to_blocks(tokens: list) -> list[dict]:
    blocks = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token.type == "heading_open":
            level = int(token.tag[1])
            text = _get_heading_text(tokens, i)
            blocks.append({"type": "heading", "level": level, "text": text})
            i = _skip_heading(tokens, i)

        elif token.type == "paragraph_open":
            content_tokens = []
            i += 1
            while i < len(tokens) and tokens[i].type != "paragraph_close":
                content_tokens.append(tokens[i])
                i += 1

            if len(content_tokens) == 1 and content_tokens[0].type == "html_inline":
                content = content_tokens[0].content.strip()
                if content == "<!-- pagebreak -->":
                    blocks.append({"type": "page_break"})
                    continue

            images = _extract_images_deep(content_tokens)
            if images and _is_only_whitespace(content_tokens, images):
                for img in images:
                    blocks.append({"type": "image", **img})
                continue

            text_parts = _extract_text_parts(content_tokens)
            if text_parts:
                runs = _extract_runs_from_children(content_tokens)
                if runs and len(runs) > 1:
                    blocks.append({"type": "paragraph", "runs": runs})
                elif runs and len(runs) == 1:
                    blocks.append({"type": "paragraph", "text": runs[0].get("text", "")})
                    if "bold" in runs[0]:
                        blocks[-1]["bold"] = runs[0]["bold"]
                    if "italic" in runs[0]:
                        blocks[-1]["italic"] = runs[0]["italic"]
                else:
                    text = "".join(tp for tp in text_parts if tp.strip())
                    if text:
                        blocks.append({"type": "paragraph", "text": text})

        elif token.type == "bullet_list_open":
            items, i = _collect_list_items(tokens, i)
            blocks.append({"type": "bullet_list", "items": items})

        elif token.type == "ordered_list_open":
            items, i = _collect_list_items(tokens, i)
            blocks.append({"type": "numbered_list", "items": items})

        elif token.type == "table_open":
            table, i = _parse_table(tokens, i)
            if table:
                blocks.append(table)

        elif token.type == "html_block":
            content = token.content.strip()
            if content == "<!-- pagebreak -->":
                blocks.append({"type": "page_break"})

        elif token.type == "blockquote_open":
            text, i = _collect_blockquote_text(tokens, i)
            blocks.append({"type": "callout", "style": "info", "text": text})

        elif token.type == "hr":
            blocks.append({"type": "hr"})

        elif token.type == "fence":
            # 代码块（含无 info 的 ASCII 图）
            blocks.append({
                "type": "code_block",
                "language": token.info.strip() if token.info else "",
                "code": token.content.rstrip("\n"),
            })

        i += 1

    # 限制图片数量
    image_count = 0
    filtered = []
    for block in blocks:
        if block.get("type") == "image":
            image_count += 1
            if image_count > MAX_IMAGES:
                continue
        filtered.append(block)

    return filtered


def _collect_list_items(tokens: list, start: int) -> tuple[list, int]:
    items = []
    i = start + 1
    while i < len(tokens) and tokens[i].type not in ("bullet_list_close", "ordered_list_close"):
        if tokens[i].type == "list_item_open":
            i += 1
            text = ""
            while i < len(tokens) and tokens[i].type != "list_item_close":
                if tokens[i].type == "inline":
                    text += tokens[i].content
                elif tokens[i].tag in ("h1", "h2", "h3"):
                    text += _get_inline_text(tokens, i)
                    i = _skip_inline_children(tokens, i)
                i += 1
            if text.strip():
                items.append(text.strip())
        i += 1
    return items, i


def _parse_table(tokens: list, start: int) -> tuple[dict | None, int]:
    headers = []
    rows = []
    i = start + 1

    while i < len(tokens) and tokens[i].type != "table_close":
        if tokens[i].type == "thead_open":
            i += 1
            while i < len(tokens) and tokens[i].type != "thead_close":
                if tokens[i].type == "inline":
                    headers.append(tokens[i].content.strip())
                i += 1
        elif tokens[i].type == "tbody_open":
            i += 1
            while i < len(tokens) and tokens[i].type != "tbody_close":
                if tokens[i].type == "tr_open":
                    i += 1
                    row = []
                    while i < len(tokens) and tokens[i].type != "tr_close":
                        if tokens[i].type == "inline":
                            row.append(tokens[i].content.strip())
                        i += 1
                    if row:
                        rows.append(row)
                else:
                    i += 1
        else:
            i += 1

    if not headers and not rows:
        return None, i
    # 截断超长表格
    headers = headers[:MAX_TABLE_COLS]
    rows = [r[:MAX_TABLE_COLS] for r in rows[:MAX_TABLE_ROWS]]
    return {"type": "table", "headers": headers, "rows": rows}, i


def _collect_blockquote_text(tokens: list, start: int) -> tuple[str, int]:
    text = ""
    i = start + 1
    while i < len(tokens) and tokens[i].type != "blockquote_close":
        if tokens[i].type == "inline":
            text += tokens[i].content
        i += 1
    return text.strip(), i


def _get_heading_text(tokens: list, idx: int) -> str:
    """Extract text from heading: look for inline token after heading_open."""
    j = idx + 1
    while j < len(tokens) and tokens[j].type != "heading_close":
        if tokens[j].type == "inline":
            return tokens[j].content or ""
        j += 1
    return ""


def _skip_heading(tokens: list, idx: int) -> int:
    """Skip past heading_open ... heading_close."""
    j = idx + 1
    while j < len(tokens) and tokens[j].type != "heading_close":
        j += 1
    return j


def _get_inline_text(tokens: list, idx: int) -> str:
    if hasattr(tokens[idx], "children") and tokens[idx].children:
        return "".join(c.content for c in tokens[idx].children if c.type == "text")
    return tokens[idx].content or ""


def _skip_inline_children(tokens: list, idx: int) -> int:
    if hasattr(tokens[idx], "children") and tokens[idx].children:
        return idx
    return idx + 1


def _extract_images_deep(tokens: list) -> list[dict]:
    """Recursively find image tokens, even nested inside inline tokens."""
    images = []
    for t in tokens:
        if t.type == "image":
            caption = t.attrGet("alt") or ""
            if not caption and hasattr(t, "children") and t.children:
                caption = "".join(c.content for c in t.children if c.type == "text")
            images.append({
                "path": t.attrGet("src") or "",
                "caption": caption,
            })
        elif hasattr(t, "children") and t.children:
            images.extend(_extract_images_deep(t.children))
    return images


def _is_only_whitespace(content_tokens: list, images: list) -> bool:
    for t in content_tokens:
        if t.type == "text" and t.content.strip():
            return False
    return len(images) > 0


def _extract_text_parts(tokens: list) -> list[str]:
    parts = []
    for t in tokens:
        if t.type == "text":
            parts.append(t.content)
        elif t.type == "inline":
            parts.append(t.content)
    return parts


def _extract_runs_from_children(children: list) -> list[dict]:
    runs = []
    i = 0
    while i < len(children):
        c = children[i]
        if c.type == "text" and c.content:
            runs.append({"text": c.content})
        elif c.type == "strong_open":
            text = ""
            i += 1
            while i < len(children) and children[i].type != "strong_close":
                if children[i].type == "text":
                    text += children[i].content
                i += 1
            runs.append({"text": text, "bold": True})
        elif c.type == "em_open":
            text = ""
            i += 1
            while i < len(children) and children[i].type != "em_close":
                if children[i].type == "text":
                    text += children[i].content
                i += 1
            runs.append({"text": text, "italic": True})
        elif c.type == "image":
            # Skip image tokens — they're handled separately by _extract_images_deep
            pass
        elif c.type == "inline" and hasattr(c, "children") and c.children:
            runs.extend(_extract_runs_from_children(c.children))
        i += 1
    return runs if runs else None


def _blocks_to_sections(blocks: list) -> list[dict]:
    sections = []
    stack = []

    for block in blocks:
        if block["type"] == "heading":
            new_section = {
                "heading": {"level": block["level"], "text": block["text"]},
                "blocks": [],
                "children": [],
            }
            while stack and stack[-1][0] >= block["level"]:
                stack.pop()
            if stack:
                stack[-1][1]["children"].append(new_section)
            else:
                sections.append(new_section)
            stack.append((block["level"], new_section))
        else:
            if stack:
                stack[-1][1]["blocks"].append(block)
            else:
                if not sections or "blocks" not in sections[-1]:
                    sections.append({"heading": None, "blocks": [block], "children": []})
                else:
                    sections[-1]["blocks"].append(block)

    return sections
