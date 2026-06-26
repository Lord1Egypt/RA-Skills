#!/usr/bin/env python3
"""
patch_blocks.py - 批量精准更新飞书文档 block 的文本内容

用法:
  python3 patch_blocks.py <doc_token> <patches.json>
  python3 patch_blocks.py <doc_token> -          # 从 stdin 读取

patches.json 格式（元素列表完整替换目标 block 的 elements）:
[
  {
    "block_id": "doxcnXXXXXX",
    "elements": [
      {"text": "普通文字"},
      {"text": "加粗文字", "bold": true},
      {"text": "代码", "code": true},
      {"text": "斜体", "italic": true}
    ]
  },
  ...
]

注意：elements 列表会完整替换 block 的现有内容，请确保包含所有文字片段。
"""
import subprocess
import json
import sys


def elem_to_api(e: dict) -> dict:
    """将精简格式的 element 转为 API 所需的 text_element 格式"""
    style = {}
    if e.get("bold"):        style["bold"] = True
    if e.get("italic"):      style["italic"] = True
    if e.get("code"):        style["inline_code"] = True
    if e.get("strikethrough"): style["strikethrough"] = True
    if e.get("underline"):   style["underline"] = True

    text_run = {"content": e["text"]}
    if style:
        text_run["text_element_style"] = style

    return {"text_run": text_run}


def build_batch_request(patches: list) -> dict:
    """将 patches 列表转为 batch_update API 的请求体"""
    requests = []
    for p in patches:
        requests.append({
            "block_id": p["block_id"],
            "update_text_elements": {
                "elements": [elem_to_api(e) for e in p["elements"]]
            }
        })
    return {"requests": requests}


def patch_blocks(doc_token: str, patches: list) -> dict:
    """调用 batch_update API，返回响应"""
    body = build_batch_request(patches)

    result = subprocess.run(
        ["lark-cli", "api", "PATCH",
         f"/open-apis/docx/v1/documents/{doc_token}/blocks/batch_update",
         "--data", json.dumps(body)],
        capture_output=True, text=True,
    )

    # 过滤 lark-cli 的 WARN 行
    stdout = "\n".join(
        line for line in result.stdout.splitlines()
        if not line.startswith("[lark-cli]")
    )
    return json.loads(stdout) if stdout.strip() else {"error": result.stderr}


def main():
    if len(sys.argv) < 3:
        print("用法: python3 patch_blocks.py <doc_token> <patches.json | ->",
              file=sys.stderr)
        sys.exit(1)

    doc_token = sys.argv[1]
    patches_arg = sys.argv[2]

    if patches_arg == "-":
        patches = json.load(sys.stdin)
    else:
        with open(patches_arg, encoding="utf-8") as f:
            patches = json.load(f)

    if not patches:
        print("[WARN] patches 为空，无需调用 API", file=sys.stderr)
        sys.exit(0)

    print(f"[INFO] 准备更新 {len(patches)} 个 block...", file=sys.stderr)
    resp = patch_blocks(doc_token, patches)

    if resp.get("code") == 0:
        updated = len(resp.get("data", {}).get("blocks", []))
        print(f"[OK] 成功更新 {updated} 个 block", file=sys.stderr)
    else:
        print(f"[ERROR] {resp}", file=sys.stderr)

    print(json.dumps(resp, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
