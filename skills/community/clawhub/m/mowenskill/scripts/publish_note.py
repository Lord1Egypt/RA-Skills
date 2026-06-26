#!/usr/bin/env python3
"""
墨问笔记发布脚本 — publish_note.py

通过墨问 Open API 创建、编辑笔记或修改笔记设置。
支持本地图片上传和远程图片 URL 上传。

用法:
  # 创建笔记（从 JSON 文件读取内容）
  python publish_note.py --action create --input note.json

  # 创建笔记（从 stdin 读取 JSON）
  echo '{"paragraphs": [...]}' | python publish_note.py --action create

  # 编辑笔记
  python publish_note.py --action edit --note-id NOTE_ID --input note.json

  # 修改笔记设置
  python publish_note.py --action settings --note-id NOTE_ID --privacy rule --no-share

环境变量:
  MOWEN_API_KEY  墨问 API Key（也可通过 --api-key 参数传入）

零第三方依赖，仅使用 Python 标准库。
"""

import argparse
import json
import mimetypes
import os
import sys
import time
import uuid as uuid_mod
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# ── 常量 ─────────────────────────────────────────────────────────────────────

BASE_URL = "https://open.mowen.cn"
API_NOTE_CREATE = "/api/open/api/v1/note/create"
API_NOTE_EDIT = "/api/open/api/v1/note/edit"
API_NOTE_SET = "/api/open/api/v1/note/set"
API_UPLOAD_PREPARE = "/api/open/api/v1/upload/prepare"
API_UPLOAD_URL = "/api/open/api/v1/upload/url"

RATE_LIMIT_DELAY = 1.1  # 秒，略大于 1 以确保不触发限频

# ── HTTP 工具 ─────────────────────────────────────────────────────────────────


def _api_request(api_key: str, path: str, payload: dict) -> dict:
    """向墨问 API 发送 JSON POST 请求并返回响应字典。"""
    url = BASE_URL + path
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace") if e.fp else ""
        try:
            err = json.loads(body_text)
            msg = err.get("message", err.get("msg", body_text))
            code = err.get("code", e.code)
            _die(f"API 错误 (HTTP {e.code}): {msg} (code={code})")
        except (json.JSONDecodeError, ValueError):
            _die(f"HTTP {e.code} — {e.reason}\n{body_text}")
    except URLError as e:
        _die(f"网络错误: {e.reason}")

    # API 成功时直接返回响应体（无 code/data 包装）
    # 错误响应含 code 字段（非 0）
    if "code" in body and body["code"] != 0:
        msg = body.get("message", body.get("msg", "未知错误"))
        _die(f"API 业务错误: {msg} (code={body['code']})")
    return body


def _multipart_upload(endpoint: str, form_fields: dict, file_path: str) -> bytes:
    """使用 multipart/form-data 上传文件到 OSS。"""
    boundary = uuid_mod.uuid4().hex
    body_parts: list[bytes] = []

    # 添加表单字段（按 form_fields 中的顺序）
    field_order = [
        "key", "policy", "callback", "success_action_status",
        "x-oss-signature-version", "x-oss-credential", "x-oss-date",
        "x-oss-signature", "x-oss-meta-mo-uid",
        "x:file_name", "x:file_id", "x:file_uid",
    ]
    for field in field_order:
        if field in form_fields:
            body_parts.append(
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{field}"\r\n\r\n'
                f"{form_fields[field]}\r\n".encode("utf-8")
            )

    # 添加文件字段
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    with open(file_path, "rb") as f:
        file_data = f.read()

    body_parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8")
    )
    body_parts.append(file_data)
    body_parts.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    body = b"".join(body_parts)

    upload_url = endpoint.rstrip("/") + "/"
    req = Request(
        upload_url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=120) as resp:
            return resp.read()
    except HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace") if e.fp else ""
        _die(f"文件投递失败: HTTP {e.code}\n{body_text}")
    except URLError as e:
        _die(f"文件投递网络错误: {e.reason}")


# ── 图片上传 ──────────────────────────────────────────────────────────────────


def upload_local_image(api_key: str, file_path: str) -> str:
    """本地图片上传（两步流程），返回 fileId。"""
    if not os.path.isfile(file_path):
        _die(f"文件不存在: {file_path}")

    file_size = os.path.getsize(file_path)
    if file_size > 50 * 1024 * 1024:
        _die(f"文件过大 ({file_size / 1024 / 1024:.1f}MB)，本地上传限制 50MB")

    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    if ext not in ("gif", "jpeg", "jpg", "png", "webp"):
        _die(f"不支持的图片格式: .{ext}（仅支持 gif/jpeg/jpg/png/webp）")

    _info(f"[上传] 获取授权: {filename}")
    prepare_data = _api_request(api_key, API_UPLOAD_PREPARE, {
        "fileType": 1,
        "fileName": filename,
    })

    form = prepare_data.get("form", {})
    if not form:
        _die("获取上传授权失败: 未返回 form 数据")

    endpoint = form.pop("endpoint", "")
    if not endpoint:
        _die("获取上传授权失败: 未返回 endpoint")

    file_id = form.get("x:file_id", "")

    time.sleep(RATE_LIMIT_DELAY)

    _info(f"[上传] 投递文件: {filename} -> {endpoint}")
    _multipart_upload(endpoint, form, file_path)

    _info(f"[上传] 完成: fileId={file_id}")
    return file_id


def upload_remote_image(api_key: str, url: str, filename: str = "") -> str:
    """远程图片上传（一步完成），返回 fileId。"""
    _info(f"[上传] 远程上传: {url}")
    payload = {"fileType": 1, "url": url}
    if filename:
        payload["fileName"] = filename

    data = _api_request(api_key, API_UPLOAD_URL, payload)
    file_info = data.get("file", {})
    file_id = file_info.get("fileId", "")
    if not file_id:
        _die(f"远程上传失败: 未返回 fileId\n响应: {json.dumps(data, ensure_ascii=False)}")

    _info(f"[上传] 完成: fileId={file_id}")
    return file_id


def upload_image(api_key: str, image_ref: str) -> str:
    """
    统一图片上传入口。
    - 如果 image_ref 是 URL（http/https 开头），使用远程上传
    - 如果 image_ref 是本地路径，使用本地上传
    - 如果 image_ref 已经是 fileId（不含 / 且不以 http 开头），直接返回
    """
    if image_ref.startswith("http://") or image_ref.startswith("https://"):
        return upload_remote_image(api_key, image_ref)
    elif os.path.sep in image_ref or os.path.exists(image_ref):
        return upload_local_image(api_key, image_ref)
    else:
        # 假定已经是 fileId
        return image_ref


# ── NoteAtom 构建 ─────────────────────────────────────────────────────────────


def _build_text_node(text_item: dict) -> dict:
    """
    构建文本节点。

    text_item 格式:
      { "text": "内容", "bold": true, "highlight": true, "link": "https://..." }
    """
    node = {"type": "text", "text": text_item.get("text", "")}
    marks = []
    if text_item.get("bold"):
        marks.append({"type": "bold"})
    if text_item.get("highlight"):
        marks.append({"type": "highlight"})
    if text_item.get("link"):
        marks.append({"type": "link", "attrs": {"href": text_item["link"]}})
    if marks:
        node["marks"] = marks
    return node


def _build_paragraph(content_items: list) -> dict:
    """构建段落节点。content_items 为文本项列表。"""
    children = []
    for item in content_items:
        if isinstance(item, str):
            children.append({"type": "text", "text": item})
        elif isinstance(item, dict):
            children.append(_build_text_node(item))
    return {"type": "paragraph", "content": children}


def build_note_atom(api_key: str, input_data: dict) -> dict:
    """
    根据输入数据构建 NoteAtom。

    input_data 格式:
    {
      "paragraphs": [
        "纯文本段落",
        [{"text": "加粗", "bold": true}, "普通文字"],
        {"type": "image", "src": "https://... 或 /path/to/file 或 fileId"},
        {"type": "image", "src": "...", "width": 1080, "height": 720},
        {"type": "heading", "level": 1, "text": "标题"},
        {"type": "blockquote", "text": "引用内容"},
        {"type": "bulletList", "items": ["项目1", "项目2"]},
        {"type": "orderedList", "items": ["项目1", "项目2"]}
      ]
    }
    """
    content_nodes = []
    paragraphs = input_data.get("paragraphs", [])

    for para in paragraphs:
        if isinstance(para, str):
            # 纯文本段落
            content_nodes.append(_build_paragraph([para]))

        elif isinstance(para, list):
            # 富文本段落（文本项列表）
            content_nodes.append(_build_paragraph(para))

        elif isinstance(para, dict):
            node_type = para.get("type", "paragraph")

            if node_type == "image":
                src = para.get("src", "")
                if not src:
                    _warn("跳过无 src 的图片节点")
                    continue
                file_id = upload_image(api_key, src)
                time.sleep(RATE_LIMIT_DELAY)
                img_node = {
                    "type": "image",
                    "attrs": {"uuid": file_id},
                }
                if para.get("width") and para.get("height"):
                    img_node["attrs"]["width"] = str(para["width"])
                    img_node["attrs"]["height"] = str(para["height"])
                    img_node["attrs"]["ratio"] = str(round(
                        para["width"] / para["height"], 2
                    ))
                content_nodes.append(img_node)

            elif node_type == "heading":
                level = str(para.get("level", 1))
                text = para.get("text", "")
                content_nodes.append({
                    "type": "heading",
                    "attrs": {"level": level},
                    "content": [{"type": "text", "text": text}],
                })

            elif node_type in ("blockquote", "quote"):
                text = para.get("text", "")
                content_nodes.append({
                    "type": "quote",
                    "content": [_build_paragraph([text])],
                })

            elif node_type in ("bulletList", "orderedList"):
                items = para.get("items", [])
                list_items = []
                for item_text in items:
                    list_items.append({
                        "type": "listItem",
                        "content": [_build_paragraph([item_text])],
                    })
                content_nodes.append({
                    "type": node_type,
                    "content": list_items,
                })

            elif node_type == "paragraph":
                # 明确的段落类型
                text = para.get("text", "")
                content = para.get("content", [text] if text else [])
                content_nodes.append(_build_paragraph(content))

            elif node_type == "raw":
                # 直接传入原始 NoteAtom 节点
                raw_node = para.get("node")
                if raw_node:
                    content_nodes.append(raw_node)

            else:
                _warn(f"未知节点类型: {node_type}，作为段落处理")
                text = para.get("text", str(para))
                content_nodes.append(_build_paragraph([text]))

    if not content_nodes:
        _die("内容为空，至少需要一个段落")

    return {"type": "doc", "content": content_nodes}


# ── 操作实现 ──────────────────────────────────────────────────────────────────


def action_create(api_key: str, input_data: dict) -> dict:
    """创建笔记。"""
    note_atom = build_note_atom(api_key, input_data)

    # 构建 settings
    settings = {}
    tags = input_data.get("tags", [])
    if tags:
        if len(tags) > 10:
            _warn(f"标签数量 {len(tags)} 超过上限 10，将截断")
            tags = tags[:10]
        for i, tag in enumerate(tags):
            if len(tag) > 30:
                _warn(f"标签 '{tag}' 超过 30 字符，将截断")
                tags[i] = tag[:30]
        settings["tags"] = tags

    if input_data.get("autoPublish") is not None:
        settings["autoPublish"] = bool(input_data["autoPublish"])

    payload = {"body": note_atom}
    if settings:
        payload["settings"] = settings

    _info("[创建] 调用创建 API...")
    data = _api_request(api_key, API_NOTE_CREATE, payload)
    note_id = data.get("noteId", "")
    _info(f"[创建] 成功! noteId={note_id}")
    _info(f"  配额提醒: 创建 API 每日限额 100 次")
    return {"noteId": note_id, "action": "create"}


def action_edit(api_key: str, note_id: str, input_data: dict) -> dict:
    """编辑笔记内容。"""
    if not note_id:
        _die("编辑操作必须提供 --note-id 参数")

    note_atom = build_note_atom(api_key, input_data)

    payload = {
        "noteId": note_id,
        "body": note_atom,
    }

    _info(f"[编辑] 编辑笔记 {note_id}...")
    data = _api_request(api_key, API_NOTE_EDIT, payload)
    _info(f"[编辑] 成功!")
    _info(f"  配额提醒: 编辑 API 每日限额 1000 次")
    _info(f"  ⚠️ 注意: 仅支持编辑通过 API 创建的笔记")
    return {"noteId": note_id, "action": "edit"}


def action_settings(api_key: str, note_id: str, settings: dict) -> dict:
    """修改笔记隐私设置。"""
    if not note_id:
        _die("设置操作必须提供 --note-id 参数")

    privacy_type = settings.get("privacyType")
    if not privacy_type:
        _die("至少需要 --privacy 参数 (public/private/rule)")

    privacy_settings = {"type": privacy_type}

    # rule 类型支持 noShare 和 expireAt
    if privacy_type == "rule":
        rule = {}
        if settings.get("noShare") is not None:
            rule["noShare"] = bool(settings["noShare"])
        if settings.get("expireAt") is not None:
            rule["expireAt"] = str(settings["expireAt"])
        if rule:
            privacy_settings["rule"] = rule

    payload = {
        "noteId": note_id,
        "section": 1,
        "settings": {
            "privacy": privacy_settings,
        },
    }

    _info(f"[设置] 修改笔记 {note_id} 的设置...")
    data = _api_request(api_key, API_NOTE_SET, payload)
    _info(f"[设置] 成功!")
    _info(f"  配额提醒: 设置 API 每日限额 100 次")
    return {"noteId": note_id, "action": "settings"}


# ── 工具函数 ──────────────────────────────────────────────────────────────────


def _info(msg: str):
    print(f"[mowen] {msg}", file=sys.stderr)


def _warn(msg: str):
    print(f"[mowen] ⚠️  {msg}", file=sys.stderr)


def _die(msg: str):
    print(f"[mowen] ❌ {msg}", file=sys.stderr)
    sys.exit(1)


# ── CLI 入口 ──────────────────────────────────────────────────────────────────


def parse_args():
    parser = argparse.ArgumentParser(
        description="墨问笔记发布工具 — 创建、编辑笔记或修改笔记设置",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建笔记
  python publish_note.py --action create --input note.json

  # 创建笔记（stdin）
  echo '{"paragraphs":["Hello World"],"tags":["test"],"autoPublish":true}' | python publish_note.py --action create

  # 编辑笔记
  python publish_note.py --action edit --note-id NOTE_ID --input note.json

  # 修改设置
  python publish_note.py --action settings --note-id NOTE_ID --privacy public

输入 JSON 格式（create/edit）:
  {
    "paragraphs": [
      "纯文本段落",
      [{"text": "加粗", "bold": true}, "普通"],
      {"type": "image", "src": "https://example.com/img.jpg"},
      {"type": "image", "src": "/path/to/local.jpg", "width": 1080, "height": 720},
      {"type": "heading", "level": 1, "text": "标题"},
      {"type": "blockquote", "text": "引用"},
      {"type": "bulletList", "items": ["项1", "项2"]}
    ],
    "tags": ["标签1", "标签2"],
    "autoPublish": true
  }
""",
    )

    parser.add_argument(
        "--action",
        required=True,
        choices=["create", "edit", "settings"],
        help="操作类型: create=创建笔记, edit=编辑笔记, settings=修改设置",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("MOWEN_API_KEY", ""),
        help="墨问 API Key（默认读取 MOWEN_API_KEY 环境变量）",
    )
    parser.add_argument(
        "--note-id",
        default="",
        help="笔记 ID（edit 和 settings 操作必填）",
    )
    parser.add_argument(
        "--input",
        default="",
        help="输入 JSON 文件路径（不指定时从 stdin 读取）",
    )

    # settings 操作的参数
    settings_group = parser.add_argument_group("settings 操作参数")
    settings_group.add_argument(
        "--privacy",
        choices=["public", "private", "rule"],
        help="隐私类型: public=公开, private=仅自己可见, rule=自定义规则",
    )
    settings_group.add_argument(
        "--no-share",
        action="store_true",
        default=None,
        help="禁止分享（仅 rule 模式）",
    )
    settings_group.add_argument(
        "--expire-at",
        type=int,
        help="过期时间（Unix 时间戳，秒；0=永不过期；仅 rule 模式）",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # 校验 API Key
    api_key = args.api_key
    if not api_key:
        _die(
            "未提供 API Key。请通过 --api-key 参数或 MOWEN_API_KEY 环境变量设置。\n"
            "获取方式: 墨问小程序 → 我的 → 设置 → 开放平台 → 创建 API Key"
        )

    action = args.action

    if action in ("create", "edit"):
        # 读取输入 JSON
        if args.input:
            if not os.path.isfile(args.input):
                _die(f"输入文件不存在: {args.input}")
            with open(args.input, "r", encoding="utf-8") as f:
                input_data = json.load(f)
        else:
            _info("从 stdin 读取 JSON 输入...")
            raw = sys.stdin.read()
            if not raw.strip():
                _die("stdin 无输入数据")
            input_data = json.loads(raw)

        if action == "create":
            result = action_create(api_key, input_data)
        else:
            result = action_edit(api_key, args.note_id, input_data)

    elif action == "settings":
        settings = {}
        if args.privacy is not None:
            settings["privacyType"] = args.privacy
        if args.no_share:
            settings["noShare"] = True
        if args.expire_at is not None:
            settings["expireAt"] = args.expire_at

        result = action_settings(api_key, args.note_id, settings)

    # 输出结果 JSON 到 stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
