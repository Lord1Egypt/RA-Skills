"""Unified record entry - dispatch by type to create Notion blocks."""
import os
import re
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from notion_client import api_request, append_blocks, append_to_block, PAGE_ID, get_children, get_last_callout_block, delete_last_block, upload_file


# ---- Rich text helpers ----

RICH_TEXT_CHUNK_SIZE = 1900  # Notion API limit: 2000 chars per rich_text object

def split_rich_text(text, chunk_size=RICH_TEXT_CHUNK_SIZE):
    """Split text into multiple rich_text objects to avoid Notion's 2000-char limit.

    Notion API allows up to 100 rich_text objects per block,
    each with a max of 2000 chars in text.content.
    We use chunk_size=1900 to leave a safety margin.
    """
    if len(text) <= chunk_size:
        return [{"type": "text", "text": {"content": text}}]
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append({"type": "text", "text": {"content": text[i:i + chunk_size]}})
    return chunks


# ---- Block builders ----

def build_paragraph(text):
    """Build a paragraph block with rich_text."""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": split_rich_text(text),
            "color": "default",
        },
    }


def build_callout(emoji, text, color="default", children=None):
    """Build a callout block with optional children for multi-paragraph content.

    Notion API ignores \\n in rich_text content. To display multi-line text
    properly inside a callout, we put the first line/paragraph in the callout's
    own rich_text, and subsequent paragraphs as children paragraph blocks.
    """
    block = {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": emoji},
            "rich_text": split_rich_text(text),
            "color": color,
        },
    }
    if children:
        block["callout"]["children"] = children
    return block


def build_todo(text, checked=False):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": split_rich_text(text),
            "checked": checked,
            "color": "default",
        },
    }


def build_bookmark(url, caption=None):
    """Build a bookmark block. Notion API only supports 'url' and 'caption' fields.

    Note: bookmark block does NOT have a 'rich_text' field like text blocks.
    Use 'caption' (rich_text array) for description text.
    The title/description/thumbnail are auto-fetched by Notion from the URL.
    """
    bookmark_data = {"url": url, "caption": []}
    if caption:
        bookmark_data["caption"] = split_rich_text(caption)
    return {
        "object": "block",
        "type": "bookmark",
        "bookmark": bookmark_data,
    }


def build_heading(level, text):
    return {
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {
            "rich_text": split_rich_text(text),
            "color": "default",
        },
    }


def build_quote_block(text):
    return {
        "object": "block",
        "type": "quote",
        "quote": {"rich_text": split_rich_text(text), "color": "default"},
    }


def build_divider():
    return {"object": "block", "type": "divider", "divider": {}}


def build_bullet(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": split_rich_text(text), "color": "default"},
    }


def build_numbered(text):
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": split_rich_text(text), "color": "default"},
    }


def build_toggle(text, children=None):
    block = {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": split_rich_text(text),
            "color": "default",
        },
    }
    if children:
        block["toggle"]["children"] = children
    return block


def build_image_block(file_upload_id, caption=None):
    """Build an image block using a file_upload ID from Notion's File Upload API.

    After uploading a file via notion-upload, the returned file_id is used
    with type "file_upload" to attach the image to a block.
    """
    image_data = {
        "type": "file_upload",
        "file_upload": {"id": file_upload_id},
    }
    if caption:
        image_data["caption"] = split_rich_text(caption)
    return {
        "object": "block",
        "type": "image",
        "image": image_data,
    }


def build_image_block_external(url, caption=None):
    """Build an image block referencing an external URL."""
    image_data = {
        "type": "external",
        "external": {"url": url},
    }
    if caption:
        image_data["caption"] = split_rich_text(caption)
    return {
        "object": "block",
        "type": "image",
        "image": image_data,
    }


# ---- Type configs ----

TYPE_CONFIG = {
    "idea": {"emoji": "💡", "color": "default", "label": "想法"},
    "diary": {"emoji": "📒", "color": "blue", "label": "日记"},
    "todo": {"emoji": "☐", "color": "default", "label": "待办"},
    "done": {"emoji": "✔️", "color": "default", "label": "已完成"},
    "note": {"emoji": "📝", "color": "yellow", "label": "笔记"},
    "question": {"emoji": "❓", "color": "purple", "label": "问题"},
    "quote": {"emoji": "📖", "color": "green", "label": "摘抄"},
    "link": {"emoji": "🔗", "color": "default", "label": "链接"},
    "image": {"emoji": "🖼️", "color": "default", "label": "图片"},
}


def parse_metadata(text):
    """Extract tags (#xxx) and project (/p:xxx) from end of text."""
    tags = []
    project = None

    # Scan from the end of text, line by line
    lines = text.strip().split("\n")
    meta_line_indices = []
    remaining_lines = []

    for i, line in enumerate(lines):
        tokens = line.split()
        is_meta_line = False
        for tok in tokens:
            if tok.startswith("#") or tok.startswith("/p:"):
                is_meta_line = True
                break
        if is_meta_line:
            meta_line_indices.append(i)
        else:
            remaining_lines.append(line)

    # Extract tags and project from meta lines
    meta_text = " ".join(lines[i] for i in meta_line_indices)
    for tok in meta_text.split():
        if tok.startswith("#"):
            tags.append(tok[1:])
        elif tok.startswith("/p:"):
            project = tok[3:]

    clean_text = "\n".join(remaining_lines).strip()
    return clean_text, tags, project


def extract_date_from_block(block):
    """Try to extract YYYY-MM-DD from block text content."""
    block_type = block.get("type", "")
    content = block.get(block_type, {})
    rich = content.get("rich_text", [])
    text = ""
    for item in rich:
        text += item.get("text", {}).get("content", "")
    match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    return match.group(1) if match else None


def check_need_day_separator():
    """Check if the last block on the page is from a different day."""
    data = get_children(page_size=5, silent=True)
    if not data or "results" not in data:
        return False

    today = datetime.now().strftime("%Y-%m-%d")
    for block in reversed(data["results"]):
        block_date = extract_date_from_block(block)
        if block_date:
            return block_date != today
    return False


def is_local_file_path(s):
    """Check if string looks like a local file path."""
    # Windows: C:\... or D:\... etc., or forward slash paths, or relative paths with extensions
    if re.match(r'^[A-Za-z]:[/\\]', s):
        return True
    if s.startswith('./') or s.startswith('../') or s.startswith('~'):
        return True
    # Check if it's a path with a common image extension
    if os.path.isfile(s):
        return True
    return False


def is_image_url(s):
    """Check if string is an HTTP URL pointing to an image."""
    if not s.startswith("http"):
        return False
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg')
    return s.lower().split('?')[0].endswith(image_extensions)


def build_blocks_for_type(record_type, content):
    """Build Notion blocks for a given type and content."""
    cfg = TYPE_CONFIG.get(record_type, TYPE_CONFIG["idea"])

    if record_type == "todo":
        items = []
        for sep in [", ", ",", "，", "、"]:
            if sep in content:
                items = [x.strip() for x in content.split(sep) if x.strip()]
                break
        if not items:
            items = [content]
        return [build_todo(item, checked=False) for item in items]

    if record_type == "done":
        items = []
        for sep in [", ", ",", "，", "、"]:
            if sep in content:
                items = [x.strip() for x in content.split(sep) if x.strip()]
                break
        if not items:
            items = [content]
        return [build_todo(item, checked=True) for item in items]

    if record_type == "link":
        # Extract URL(s) from content (may include title text)
        url_pattern = r'(https?://[^\s]+)'
        urls = re.findall(url_pattern, content)
        remaining = re.sub(url_pattern, '', content).strip()

        if not urls:
            # No URL found, treat entire content as URL
            url = content.strip()
            if not url.startswith("http"):
                url = f"https://{url}"
            return [build_bookmark(url)]

        # Pure bookmark cards — Notion auto-fetches title & thumbnail
        blocks = []
        for url in urls:
            blocks.append(build_bookmark(url, caption=remaining if remaining else None))

        return blocks

    if record_type == "image":
        path = content.strip()
        if is_image_url(path):
            return [build_image_block_external(path)]
        if is_local_file_path(path):
            # Expand ~ to home directory
            path = os.path.expanduser(path)
            if not os.path.isfile(path):
                print(f"ERROR| 文件不存在: {path}")
                return []
            file_id = upload_file(path)
            if not file_id:
                print("ERROR| 图片上传失败")
                return []
            return [build_image_block(file_id)]
        # Fallback: treat as external URL
        if not path.startswith("http"):
            path = f"https://{path}"
        return [build_image_block_external(path)]

    if record_type in ("idea", "diary", "note", "question", "quote"):
        clean_text, tags, project = parse_metadata(content)

        # Header line: YYYY-MM-DD HH:mm
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Build metadata line
        meta_parts_list = []
        if tags:
            meta_parts_list.append(f"#标签：{' '.join('#' + t for t in tags)}")
        if project:
            meta_parts_list.append(f"/项目：{project}")
        meta_line = " | ".join(meta_parts_list) if meta_parts_list else ""

        # Split content into paragraphs by \n
        # Notion API ignores \n in rich_text, so each paragraph must be a separate block
        lines = clean_text.split("\n")
        paragraphs = [line for line in lines if line.strip()]  # skip blank lines

        # Auto-split long content into multiple callouts
        # Threshold: ~2000 chars per callout (covers most entries in one block)
        # Very long entries (3-4k+) will be split into 2-3 callouts
        CALLOUT_CHAR_LIMIT = 2000
        total_len = sum(len(p) for p in paragraphs)

        if total_len <= CALLOUT_CHAR_LIMIT:
            # Short content: single callout
            children = [build_paragraph(p) for p in paragraphs]
            if meta_line:
                children.append(build_paragraph(meta_line))
            return [build_callout(cfg["emoji"], now_str, cfg["color"], children=children)]
        else:
            # Long content: split into multiple callouts by paragraph boundaries
            callout_blocks = []
            current_paras = []
            current_len = 0

            for p in paragraphs:
                # If adding this paragraph exceeds limit AND we already have content,
                # flush current batch as a callout
                if current_len + len(p) > CALLOUT_CHAR_LIMIT and current_paras:
                    children = [build_paragraph(cp) for cp in current_paras]
                    callout_blocks.append(
                        build_callout(cfg["emoji"], now_str, cfg["color"], children=children)
                    )
                    current_paras = []
                    current_len = 0

                current_paras.append(p)
                current_len += len(p)

            # Flush remaining paragraphs
            if current_paras:
                children = [build_paragraph(cp) for cp in current_paras]
                if meta_line:
                    children.append(build_paragraph(meta_line))
                callout_blocks.append(
                    build_callout(cfg["emoji"], now_str, cfg["color"], children=children)
                )
            # Add metadata to the last callout if not already added
            if meta_line and not callout_blocks:
                # Edge case: no content but metadata
                callout_blocks.append(
                    build_callout(cfg["emoji"], now_str, cfg["color"],
                                  children=[build_paragraph(meta_line)])
                )

            return callout_blocks

    return []


# ---- Main dispatch ----

def parse_format_line(line):
    """Check if a line is a format pattern, return block or None."""
    if line.startswith("* ") and not line.startswith("** ") and not line.startswith("*** "):
        return build_heading(1, line[2:])
    if line.startswith("** ") and not line.startswith("*** "):
        return build_heading(2, line[3:])
    if line.startswith("*** "):
        return build_heading(3, line[4:])
    if line.startswith("> "):
        return build_quote_block(line[2:])
    if line.strip() == "---":
        return build_divider()
    if line.startswith("- "):
        return build_bullet(line[2:])
    # Numbered list: "1. text" or "1) text"
    stripped = line.lstrip()
    if stripped and stripped[0].isdigit():
        m = re.match(r"^(\d+[.)])\s+(.*)", stripped)
        if m:
            return build_numbered(m.group(2))
    return None


PENDING_CONTENT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".pending_content.txt")
PENDING_IMAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".pending_image.jpg")


def cmd_record(args):
    cfg = TYPE_CONFIG.get(args.type, TYPE_CONFIG["idea"])
    if args.file_path:
        # Read content from file (avoids shell encoding and variable expansion issues)
        with open(args.file_path, "r", encoding="utf-8") as f:
            full_content = f.read().strip()
    elif args.stdin_content:
        # Read content from stdin to avoid shell variable expansion (e.g. PowerShell $ sign)
        full_content = sys.stdin.read().strip()
    elif args.content:
        full_content = " ".join(args.content)
    elif os.path.exists(PENDING_CONTENT_FILE):
        # Auto-read from pending content file (most reliable for AI callers)
        with open(PENDING_CONTENT_FILE, "r", encoding="utf-8") as f:
            full_content = f.read().strip()
        os.remove(PENDING_CONTENT_FILE)  # Clean up after reading
    else:
        full_content = ""
    blocks = []

    # Check if we need a day separator
    if check_need_day_separator():
        blocks.append(build_divider())

    callout_types = {"idea", "diary", "note", "question", "quote"}

    if args.type in callout_types:
        # Pass entire content directly — no format-line splitting
        blocks.extend(build_blocks_for_type(args.type, full_content))
    else:
        # Multi-line: check each line for format patterns first
        lines = full_content.split("\n")
        content_lines = []
        for line in lines:
            fmt_block = parse_format_line(line)
            if fmt_block is not None:
                # Flush any accumulated content lines as a callout first
                if content_lines:
                    content_text = "\n".join(content_lines)
                    blocks.extend(build_blocks_for_type(args.type, content_text))
                    content_lines = []
                blocks.append(fmt_block)
            else:
                content_lines.append(line)

        # Remaining content lines
        if content_lines:
            blocks.extend(build_blocks_for_type(args.type, "\n".join(content_lines)))

    if not blocks:
        print("OK|没有内容可记录")
        return

    append_blocks(blocks, silent=True)
    type_label = cfg["label"]
    if args.type in ("todo", "done"):
        count = len([b for b in blocks if b.get("type") == "to_do"])
        print(f"OK|已记录到 Notion，共 {count} 条{type_label}")
    else:
        print(f"OK|已记录到 Notion，共 {len(blocks)} 条 ✅")


def cmd_heading(args):
    blocks = [build_heading(args.level, " ".join(args.content))]
    append_blocks(blocks, silent=True)
    print("OK|已记录到 Notion ✅")


def cmd_divider(_args):
    append_blocks([build_divider()], silent=True)
    print("OK|已记录到 Notion ✅")


def cmd_list(args):
    builder = build_bullet if args.kind == "bullet" else build_numbered
    blocks = [builder(text) for text in args.content]
    append_blocks(blocks, silent=True)
    print("OK|已记录到 Notion ✅")


def cmd_toggle(args):
    # JSON input from stdin or args
    if args.content:
        data = json.loads(" ".join(args.content))
    else:
        try:
            data = json.loads(sys.stdin.read())
        except Exception:
            print("ERROR| 无效的 toggle 数据")
            return
    blocks = [build_toggle(data["title"], data.get("children"))]
    append_blocks(blocks, silent=True)
    print("OK|已记录到 Notion ✅")


def cmd_image(args):
    """Upload an image and append to Notion page."""
    path = " ".join(args.path)
    blocks = []

    if check_need_day_separator():
        blocks.append(build_divider())

    if is_image_url(path):
        blocks.append(build_image_block_external(path, caption=args.caption))
    elif is_local_file_path(path):
        path = os.path.expanduser(path)
        if not os.path.isfile(path):
            print(f"ERROR| 文件不存在: {path}")
            return
        file_id = upload_file(path)
        if not file_id:
            print("ERROR| 图片上传失败")
            return
        blocks.append(build_image_block(file_id, caption=args.caption))
    else:
        # Try as URL
        if not path.startswith("http"):
            path = f"https://{path}"
        blocks.append(build_image_block_external(path, caption=args.caption))

    if blocks:
        append_blocks(blocks, silent=True)
        # Clean up pending image file if it was the source
        src_path = os.path.abspath(path)
        if os.path.abspath(PENDING_IMAGE_FILE) == src_path:
            try:
                os.remove(PENDING_IMAGE_FILE)
            except OSError:
                pass
        print("OK|已记录图片到 Notion ✅")


def cmd_caption(args):
    """Append content to the last callout block on the page."""
    # Read content
    if args.file_path:
        with open(args.file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    elif args.stdin_content:
        content = sys.stdin.read().strip()
    elif args.content:
        content = " ".join(args.content).strip()
    elif os.path.exists(PENDING_CONTENT_FILE):
        with open(PENDING_CONTENT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        os.remove(PENDING_CONTENT_FILE)
    else:
        content = ""

    if not content:
        print("OK|没有内容可追加")
        return

    # Find the last callout block
    last_callout = get_last_callout_block()
    if not last_callout:
        print("ERROR| Notion 页面上没有记录，无法追加")
        return

    block_id = last_callout["id"]

    # Build paragraph children — prefix with ↳ to show it's a follow-up
    paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
    children = []
    for i, p in enumerate(paragraphs):
        if i == 0:
            children.append(build_paragraph(f"↳ {p}"))
        else:
            children.append(build_paragraph(p))

    append_to_block(block_id, children, silent=True)
    print("OK|已追加到上一条记录 ✅")


def cmd_undo(_args):
    delete_last_block()


def main():
    parser = argparse.ArgumentParser(description="Unified Notion record entry")
    sub = parser.add_subparsers(dest="command")

    # record command
    p = sub.add_parser("record")
    p.add_argument("--type", required=True)
    p.add_argument("--stdin-content", action="store_true", dest="stdin_content",
                   help="Read content from stdin instead of args (avoids shell variable expansion)")
    p.add_argument("--file", dest="file_path", default=None,
                   help="Read content from file (avoids shell encoding issues)")
    p.add_argument("content", nargs="*")
    p.set_defaults(func=cmd_record)

    # heading command
    p = sub.add_parser("heading")
    p.add_argument("--level", type=int, default=2)
    p.add_argument("content", nargs="+")
    p.set_defaults(func=cmd_heading)

    # divider command
    p = sub.add_parser("divider")
    p.set_defaults(func=cmd_divider)

    # list command
    p = sub.add_parser("list")
    p.add_argument("--kind", choices=["bullet", "number"], default="bullet")
    p.add_argument("content", nargs="+")
    p.set_defaults(func=cmd_list)

    # toggle command
    p = sub.add_parser("toggle")
    p.add_argument("content", nargs="*")
    p.set_defaults(func=cmd_toggle)

    # image command
    p = sub.add_parser("image")
    p.add_argument("--caption", default=None, help="Optional caption for the image")
    p.add_argument("path", nargs="+", help="Local file path or URL of the image")
    p.set_defaults(func=cmd_image)

    # caption command — append to last callout
    p = sub.add_parser("caption")
    p.add_argument("--stdin-content", action="store_true", dest="stdin_content",
                   help="Read content from stdin")
    p.add_argument("--file", dest="file_path", default=None,
                   help="Read content from file")
    p.add_argument("content", nargs="*", help="Content to append")
    p.set_defaults(func=cmd_caption)

    # undo command
    p = sub.add_parser("undo")
    p.set_defaults(func=cmd_undo)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    try:
        args.func(args)
    except Exception as e:
        print(f"ERROR| 操作失败: {e}")


if __name__ == "__main__":
    main()
