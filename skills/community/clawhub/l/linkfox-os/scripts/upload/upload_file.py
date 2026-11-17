#!/usr/bin/env python3
"""upload_file: 把本地文件上传到 linkfox-os 使用的 S3 桶（中国区，STS 直传），
返回给 agent 一个 sandbox 内可直接引用的 file:///root/... 虚拟路径。

用法:
    python upload_file.py <local_path> [--kind image|doc|video]

流程:
    1. POST /agent-studio/task/getUploadCredentials    → 拿 STS 临时凭证
    2. 手写 SigV4 直 PUT 到  https://<bucket>.s3.<region>.amazonaws.com.cn/temp/YYYY/MM/<uuid>.<ext>
    3. POST /agent-studio/task/getFileVirtualPath      → 换 file:///root/... 虚拟路径

stdout 仅输出单个 JSON 对象:
    {
      "url":          "file:///root/.linkfox/workspaces/.../<uuid>.jpg",   # 给下一步 prompt 用
      "s3PreviewUrl": "https://<bucket>.s3.<region>.amazonaws.com.cn/temp/...",
      "fileName":     "product.jpg",
      "mimeType":     "image/jpeg",
      "size":         123456,
      "kind":         "image"                                              # 可选
    }
stderr 走人类可读进度。

依赖: LINKFOXAGENT_API_KEY / LINKFOXAGENT_BASE_URL（跟其它 linkfox-os 脚本一致）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid

# Windows 控制台默认 GBK 无法输出 utf-8 JSON，显式切成 utf-8
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from upload_common import (  # noqa: E402
    agent_post,
    build_signed_put_request,
    guess_mime_type,
    make_object_key,
    put_to_s3,
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Upload a local file to linkfox-os S3 and return file:// virtual path."
    )
    parser.add_argument("local_path", help="本地文件绝对路径")
    parser.add_argument(
        "--kind",
        choices=("image", "doc", "video"),
        default=None,
        help="产物类型标注（不影响上传，仅回显方便下游），可省略",
    )
    args = parser.parse_args(argv)

    local_path = os.path.abspath(args.local_path)
    if not os.path.isfile(local_path):
        print(f"[upload_file] 文件不存在: {local_path}", file=sys.stderr)
        return 2

    file_name = os.path.basename(local_path)
    with open(local_path, "rb") as f:
        body = f.read()
    size = len(body)
    mime = guess_mime_type(local_path)

    print(
        f"[upload_file] 本地: {local_path} ({size} bytes, {mime}) → 申请上传凭证",
        file=sys.stderr,
    )

    # Step 1: 拿 STS 凭证
    creds = agent_post("/agent-studio/task/getUploadCredentials")
    for k in ("region", "bucket", "accessKeyId", "secretAccessKey", "sessionToken"):
        if not creds.get(k):
            print(
                f"[upload_file] getUploadCredentials 返回缺字段 {k}: {creds}",
                file=sys.stderr,
            )
            return 3

    key = make_object_key(file_name, uuid.uuid4().hex)
    print(f"[upload_file] 对象 key: {key} → SigV4 PUT S3", file=sys.stderr)

    # Step 2: SigV4 直传
    url, headers = build_signed_put_request(
        region=creds["region"],
        bucket=creds["bucket"],
        key=key,
        body=body,
        content_type=mime,
        access_key_id=creds["accessKeyId"],
        secret_access_key=creds["secretAccessKey"],
        session_token=creds["sessionToken"],
    )
    put_to_s3(url, headers, body)
    print("[upload_file] S3 上传完成 → 换虚拟路径", file=sys.stderr)

    # Step 3: 换 file:///root/... 虚拟路径
    vp = agent_post("/agent-studio/task/getFileVirtualPath", {"key": key})
    virtual = vp.get("fileUri") or ""
    if not virtual:
        print(
            f"[upload_file] getFileVirtualPath 未返回 fileUri: {vp}", file=sys.stderr
        )
        return 4

    preview = f"https://{creds['bucket']}.s3.{creds['region']}.amazonaws.com.cn/{key}"
    out = {
        "url": virtual,
        "s3PreviewUrl": preview,
        "fileName": file_name,
        "mimeType": mime,
        "size": size,
    }
    if args.kind:
        out["kind"] = args.kind
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"[upload_file] 失败: {e}", file=sys.stderr)
        sys.exit(1)
