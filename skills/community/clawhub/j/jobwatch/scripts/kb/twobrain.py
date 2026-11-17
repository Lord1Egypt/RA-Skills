"""2brain adapter：upload_file 入库 / bot chat 问答 / keyword 图谱。

Base: https://test.2brain.ai/api （课程环境；官方文档写 portal.2brain.ai，但课程账号的 key 只在 test 环境有效）
- POST /kbase/v1/upload_file          上传文档。key 本身绑定知识库（job-hunting），无需 base_id。
                                      multipart 字段：file（二进制）+ file_name（含扩展名）。
                                      支持格式：txt/docx/doc/pdf/pptx/ppt/epub/xlsx/xls/csv —— 无 md，
                                      因此本项目以 .txt 上传 Markdown 内容。限频 100 次/分钟，≤20MB。
                                      响应 {code, msg, data:{file_size, file_type, ocr_num}}，code!=0 为失败。
- POST /bot/chat/v1/chat/completions  对话智能体（OpenAI 兼容；role 仅支持 user）。
- POST /kbase/keywords/keyword_api    关键词图谱，body {"base_id": <int>}。
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import (CONFIG, http_json, multipart_post,  # noqa: E402
                    require_egress_consent)

BASE = CONFIG["twobrain"]["base_url"].rstrip("/")


def _key(name):
    v = os.environ.get(name)
    if not v:
        raise RuntimeError(f"{name} not set in .env")
    return v


def upload_doc(filename, content_md):
    """Upload one doc into the job-hunting KB. Markdown content is sent as .txt.

    文档中认证头写法不一致（curl 示例带 Bearer，参数表/其他示例是裸 key），
    这里先试 Bearer，401 时自动降级为裸 key 重试。
    """
    if not filename.endswith(".txt"):
        filename = filename.rsplit(".", 1)[0] + ".txt"
    require_egress_consent("twobrain", f"an archived job-description document ({filename})")
    key = _key("TWOBRAIN_UPLOAD_KEY")
    status = body = None
    for auth in (f"Bearer {key}", key):
        status, body = multipart_post(
            f"{BASE}/kbase/v1/upload_file",
            fields={"file_name": filename},
            file_field="file",
            filename=filename,
            file_bytes=content_md.encode(),
            content_type="text/plain",
            headers={"Authorization": auth},
        )
        if status != 401:
            break
    if status >= 300:
        raise RuntimeError(f"2brain upload HTTP {status}: {body[:300]!r}")
    resp = json.loads(body)
    if resp.get("code", 0) != 0:
        raise RuntimeError(f"2brain upload failed: code={resp.get('code')} msg={resp.get('msg')}")
    return resp


def ask(question):
    """Ask the conversational bot bound to the KB (带溯源问答)."""
    require_egress_consent("twobrain", "the question you asked, sent to the 2brain bot")
    resp = http_json(
        f"{BASE}/bot/chat/v1/chat/completions",
        method="POST",
        headers={"Authorization": f"Bearer {_key('TWOBRAIN_CHAT_KEY')}"},
        json_body={"messages": [{"role": "user", "content": question}], "stream": False},
        timeout=120,
    )
    return resp["choices"][0]["message"]["content"]


def keyword_graph():
    """Pull the keyword graph of the KB. Needs TWOBRAIN_BASE_ID (integer)."""
    require_egress_consent("twobrain", "a keyword-graph query for your knowledge base id")
    return http_json(
        f"{BASE}/kbase/keywords/keyword_api",
        method="POST",
        headers={"Authorization": f"Bearer {_key('TWOBRAIN_GRAPH_KEY')}"},
        json_body={"base_id": int(_key("TWOBRAIN_BASE_ID"))},
        timeout=60,
    )


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].endswith((".md", ".txt")):
        from pathlib import Path
        p = Path(sys.argv[1])
        print(upload_doc(p.name, p.read_text()))
    elif len(sys.argv) >= 2 and sys.argv[1] == "graph":
        print(json.dumps(keyword_graph(), ensure_ascii=False)[:2000])
    elif len(sys.argv) >= 2:
        print(ask(" ".join(sys.argv[1:])))
    else:
        print("usage: twobrain.py <file.md|file.txt> | graph | <question...>")
