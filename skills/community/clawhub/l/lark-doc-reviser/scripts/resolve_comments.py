#!/usr/bin/env python3
"""
resolve_comments.py - 批量将飞书文档评论标记为已解决

用法:
  python3 resolve_comments.py <doc_token> <comment_id> [comment_id ...]
  python3 resolve_comments.py <doc_token> -         # 从 stdin 读取 JSON 数组

stdin 格式:
  ["7623820156610809026", "7623821400884645044"]
"""
import subprocess
import json
import sys


def resolve_comment(doc_token: str, comment_id: str) -> dict:
    """调用 API 将单条评论标记为已解决"""
    result = subprocess.run(
        ["lark-cli", "api", "PATCH",
         f"/open-apis/drive/v1/files/{doc_token}/comments/{comment_id}",
         "--params", '{"file_type": "docx"}',
         "--data", '{"is_solved": true}'],
        capture_output=True, text=True,
    )
    stdout = "\n".join(
        line for line in result.stdout.splitlines()
        if not line.startswith("[lark-cli]")
    )
    return json.loads(stdout) if stdout.strip() else {"error": result.stderr}


def main():
    if len(sys.argv) < 3:
        print("用法: python3 resolve_comments.py <doc_token> <comment_id ...| ->",
              file=sys.stderr)
        sys.exit(1)

    doc_token = sys.argv[1]

    if sys.argv[2] == "-":
        comment_ids = json.load(sys.stdin)
    else:
        comment_ids = sys.argv[2:]

    if not comment_ids:
        print("[WARN] 没有评论需要解决", file=sys.stderr)
        sys.exit(0)

    print(f"[INFO] 准备解决 {len(comment_ids)} 条评论...", file=sys.stderr)

    ok_count = 0
    for cid in comment_ids:
        resp = resolve_comment(doc_token, cid)
        if resp.get("code") == 0:
            print(f"[OK] 评论 {cid} 已解决", file=sys.stderr)
            ok_count += 1
        else:
            print(f"[ERROR] 评论 {cid}: {resp}", file=sys.stderr)

    print(f"[INFO] 共解决 {ok_count}/{len(comment_ids)} 条评论", file=sys.stderr)


if __name__ == "__main__":
    main()
