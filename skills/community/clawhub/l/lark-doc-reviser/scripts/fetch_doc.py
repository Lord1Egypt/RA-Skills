#!/usr/bin/env python3
"""
fetch_doc.py - 一键获取飞书文档的完整块结构 + 未解决评论映射

用法:
  python3 fetch_doc.py <doc_url_or_token> [选项]

选项:
  --file-type   文档类型，默认 docx
  --out <path>  写入 JSON 文件（默认只打印到 stdout）

输出 JSON 结构:
  {
    "doc_token": "...",
    "commented_blocks": [   ← 有评论的块 + 指令，Claude 主要读这里
      {
        "block_id": "...",
        "block_type": "text" | "heading2" | "callout" | ...,
        "parent_id": "...",     ← 容器 block（如 callout）的 id
        "full_text": "...",     ← 所有 text_run 拼接
        "elements": [           ← 带样式，编辑时按需传给 PATCH API
          {"text": "...", "bold": true, ...}
        ],
        "comments": [
          {"comment_id": "...", "anchor_text": "...", "instruction": "..."}
        ]
      }
    ],
    "all_blocks": [   ← 全文块列表（精简），按需参考上下文
      {"block_id": "...", "block_type": "...", "parent_id": "...", "full_text": "..."}
    ]
  }
"""
import subprocess
import json
import sys
import argparse

BLOCK_TYPE_NAMES = {
    1: "page", 2: "text", 3: "heading1", 4: "heading2", 5: "heading3",
    6: "heading4", 7: "heading5", 8: "heading6", 9: "heading7",
    10: "heading8", 11: "heading9", 12: "bullet", 13: "ordered",
    14: "code", 15: "quote", 17: "todo", 18: "bitable",
    19: "callout", 22: "divider", 23: "file", 24: "column_set",
    25: "column", 26: "iframe", 27: "image", 31: "table", 32: "table_cell",
}
TEXT_BLOCK_TYPES = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19}


def extract_token(url_or_token: str) -> str:
    if "/" in url_or_token:
        token = url_or_token.rstrip("/").split("/")[-1]
        return token.split("?")[0]
    return url_or_token


# ── API 调用 ──────────────────────────────────────────────────────────────────

def fetch_all_blocks(doc_token: str) -> list:
    all_items = []
    page_token = None
    while True:
        params = {"page_size": 500}
        if page_token:
            params["page_token"] = page_token
        r = subprocess.run(
            ["lark-cli", "api", "GET",
             f"/open-apis/docx/v1/documents/{doc_token}/blocks",
             "--params", json.dumps(params)],
            capture_output=True, text=True,
        )
        data = json.loads(r.stdout)
        all_items.extend(data.get("data", {}).get("items", []))
        if not data.get("data", {}).get("has_more"):
            break
        page_token = data["data"].get("page_token")
    return all_items


def fetch_comments(doc_token: str, file_type: str = "docx") -> list:
    r = subprocess.run(
        ["lark-cli", "drive", "file.comments", "list",
         "--params", json.dumps({
             "file_token": doc_token,
             "file_type": file_type,
             "is_solved": False,
             "user_id_type": "open_id",
         }),
         "--page-all"],
        capture_output=True, text=True,
    )
    data = json.loads(r.stdout)
    return data.get("data", {}).get("items", [])


# ── 数据处理 ──────────────────────────────────────────────────────────────────

def extract_instruction(reply_list: dict) -> str:
    try:
        elements = reply_list["replies"][0]["content"]["elements"]
        return "".join(
            e["text_run"]["text"] for e in elements if e.get("type") == "text_run"
        ).strip()
    except (KeyError, IndexError):
        return ""


def parse_elements(raw_elements: list) -> tuple[list, dict]:
    """
    返回 (slim_elements, comment_id → anchor_text 映射)
    slim_elements 中不含 comment_ids（另外单独处理）
    """
    slim = []
    comment_anchors = {}  # comment_id → anchor text

    for e in raw_elements:
        tr = e.get("text_run", {})
        content = tr.get("content", "")
        if not content:
            continue
        style = tr.get("text_element_style", {})

        elem = {"text": content}
        if style.get("bold"):          elem["bold"] = True
        if style.get("italic"):        elem["italic"] = True
        if style.get("inline_code"):   elem["code"] = True
        if style.get("strikethrough"): elem["strikethrough"] = True

        for cid in style.get("comment_ids", []):
            comment_anchors[cid] = content

        slim.append(elem)

    return slim, comment_anchors


def slim_block(b: dict) -> dict:
    """将 raw block 精简，返回 None 表示跳过（page root）"""
    btype = b.get("block_type", 999)
    if btype == 1:
        return None  # page root，跳过

    bid = b.get("block_id", "")
    parent = b.get("parent_id", "")
    type_name = BLOCK_TYPE_NAMES.get(btype, f"type_{btype}")

    base = {"block_id": bid, "block_type": type_name, "parent_id": parent}

    if btype == 22:  # divider
        return base
    if btype == 27:  # image
        return {**base, "image_token": b.get("image", {}).get("token", "")}

    if btype in TEXT_BLOCK_TYPES:
        # 找到含 elements 的字段（text/heading1/bullet/…）
        text_data = next(
            (b[k] for k in ("text", "heading1", "heading2", "heading3",
                            "heading4", "heading5", "heading6", "heading7",
                            "heading8", "heading9", "bullet", "ordered",
                            "code", "quote", "todo")
             if k in b and b[k]),
            {}
        )
        raw_elems = text_data.get("elements", [])
        slim_elems, comment_anchors = parse_elements(raw_elems)

        if slim_elems:
            base["elements"] = slim_elems
            base["full_text"] = "".join(e["text"] for e in slim_elems)
        base["_comment_anchors"] = comment_anchors  # 临时字段，后续剔除
        return base

    return base


def build_output(raw_blocks: list, raw_comments: list) -> dict:
    # 1. 精简所有 block
    slim_blocks = [slim_block(b) for b in raw_blocks]
    slim_blocks = [b for b in slim_blocks if b is not None]

    # 2. 汇总 comment_id → anchor_text（来自各 block 的临时字段）
    block_by_id = {}
    comment_to_block = {}  # comment_id → block
    for b in slim_blocks:
        block_by_id[b["block_id"]] = b
        for cid, anchor in b.pop("_comment_anchors", {}).items():
            comment_to_block[cid] = {"block": b, "anchor": anchor}

    # 3. 构建 comment_id → instruction 映射
    comment_instructions = {}
    for item in raw_comments:
        cid = item.get("comment_id", "")
        instruction = extract_instruction(item.get("reply_list", {}))
        comment_instructions[cid] = instruction

    # 4. 合并：找出有评论的 block，附上 comments 列表
    commented_map = {}  # block_id → enriched block
    for cid, info in comment_to_block.items():
        b = info["block"]
        bid = b["block_id"]
        instruction = comment_instructions.get(cid, "")

        if bid not in commented_map:
            # 复制 block，加 comments 列表
            cb = {k: v for k, v in b.items()}
            cb["comments"] = []
            commented_map[bid] = cb

        commented_map[bid]["comments"].append({
            "comment_id": cid,
            "anchor_text": info["anchor"],
            "instruction": instruction,
        })

    commented_blocks = list(commented_map.values())

    # 5. all_blocks 去掉 elements（太长），只保留 block_id/type/parent/full_text
    all_blocks = [
        {k: v for k, v in b.items() if k != "elements"}
        for b in slim_blocks
    ]

    return {
        "doc_token": "",  # 由 main 填入
        "commented_blocks": commented_blocks,
        "all_blocks": all_blocks,
    }


# ── 主程序 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="飞书文档一键拉取：块结构 + 评论映射")
    parser.add_argument("doc", help="飞书文档 URL 或 token")
    parser.add_argument("--file-type", default="docx")
    parser.add_argument("--out", default=None, help="写入 JSON 文件路径")
    args = parser.parse_args()

    token = extract_token(args.doc)

    print("[INFO] 拉取文档块结构...", file=sys.stderr)
    raw_blocks = fetch_all_blocks(token)
    print(f"[INFO] 共 {len(raw_blocks)} 个 block", file=sys.stderr)

    print("[INFO] 拉取未解决评论...", file=sys.stderr)
    raw_comments = fetch_comments(token, args.file_type)
    print(f"[INFO] 共 {len(raw_comments)} 条未解决评论", file=sys.stderr)

    result = build_output(raw_blocks, raw_comments)
    result["doc_token"] = token
    print(f"[INFO] 有评论的块：{len(result['commented_blocks'])} 个", file=sys.stderr)

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[INFO] 已写入 {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
