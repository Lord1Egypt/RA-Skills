"""Upload local files to LitMedia OSS and return file url.

Used internally by video_mimic, ai_image, avatar4 and video_gen to auto-upload local paths.
"""

import os
import sys
import time
import random
import hashlib
import requests
import alibabacloud_oss_v2 as oss

from datetime import datetime
from shared.client import LitMediaClient

SUPPORTED_FORMATS = {
    "png", "jpg", "jpeg", "bmp", "webp",
    "mp3", "wav", "m4a",
    "mp4", "avi", "mov",
}


def detect_format(file_path: str) -> str:
    """Return file extension if supported, else raise SystemExit."""
    ext = os.path.splitext(file_path)[1].lstrip(".").lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{ext}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )
    return ext

def get_oss_security_token(client: LitMediaClient | None = None) -> dict:

    if client is None:
        client = LitMediaClient()

    url = f"https://litvideo-api.litmedia.ai/lit-video/get-sls"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Monimaster-Device-Code": "",
        "Monimaster-Api-Version": "",
        "Monimaster-Device-Type": "110"
    }

    params = client.params

    resp = requests.post(url, headers=headers, params=params)
    resp.raise_for_status()
    print(f"{resp.status_code}: {resp.text}")
    return resp.json()

def get_oss_file_path(file_name: str):
    """
    获取存储oss前缀路径
    """
    data_str = datetime.now().strftime("%Y%m%d")
    file_name = os.path.basename(file_name)
    return f'{data_str}/{file_name}'

def put_file(cred_json: dict, file_path: str) -> tuple:

    is_success = False
    sts_access_key_id  = cred_json.get("data").get("aliyun").get("AccessKeyId")
    sts_access_key_secret  = cred_json.get("data").get("aliyun").get("AccessKeySecret")
    sts_security_token  = cred_json.get("data").get("aliyun").get("SecurityToken")
    oss_show_domain = cred_json.get("data").get("aliyun").get("ossShowDomain")
    sts_region = cred_json.get("data").get("aliyun").get("Endpoint")
    oss_bucket = cred_json.get("data").get("aliyun").get("Bucket")

    # 创建静态凭证提供者，显式设置临时访问密钥AccessKey ID和AccessKey Secret，以及STS安全令牌
    credentials_provider = oss.credentials.StaticCredentialsProvider(
        access_key_id=sts_access_key_id,
        access_key_secret=sts_access_key_secret,
        security_token=sts_security_token,
    )

    # 加载SDK的默认配置，并设置凭证提供者
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider

    # 填写Bucket所在地域。以华东1（杭州）为例，Region填写为cn-hangzhou
    if sts_region.startswith("oss-"):
        sts_region = sts_region[len("oss-"):]
    cfg.region = sts_region

    # 使用配置好的信息创建OSS客户端
    client = oss.Client(cfg)

    local_file_path = file_path
    with open(local_file_path, 'rb') as file:
        data = file.read()

    oss_save_path = get_oss_file_path(local_file_path)
    result = client.put_object(oss.PutObjectRequest(
        bucket=oss_bucket,
        key=oss_save_path,
        body=data,
    ))
    if result.status_code == 200:
        is_success = True

    oss_file_url = oss_show_domain + oss_save_path
    # 输出请求的结果状态码、请求ID、内容MD5、ETag、CRC64校验码和版本ID，用于检查请求是否成功
    # print(f'status code: {result.status_code},'
    #       f' request id: {result.request_id},'
    #       f' content md5: {result.content_md5},'
    #       f' etag: {result.etag},'
    #       f' hash crc64: {result.hash_crc64},'
    #       f' version id: {result.version_id},'
    #       f' oss_file_url: {oss_file_url},'
    #       )
    return is_success, oss_file_url


def upload_file(file_path: str, *, quiet: bool = False, client: LitMediaClient | None = None) -> str:
    """Three-step upload: get credential -> PUT to S3 -> verify.

    Returns dict with keys: fileId, fileName, format.
    """
    if not quiet:
        print(f"[1/2] Requesting upload credential ...", file=sys.stderr)

    cred_json = get_oss_security_token(client)

    if not quiet:
        print(f"[2/2] Uploading {os.path.basename(file_path)} to oss...", file=sys.stderr)
    is_success, oss_file_url = put_file(cred_json, file_path)

    if is_success is not True:
        raise RuntimeError("Upload files failed")

    return oss_file_url

def resolve_local_file(file_ref: str, *, quiet: bool = False, client: LitMediaClient | None = None) -> str:
    """If file_ref is a local path, upload it and return fileId. Otherwise pass through."""

    is_url = file_ref.startswith(("http://", "https://"))
    if not is_url:
        if not os.path.exists(file_ref):
            raise FileNotFoundError(f"Local file not found: {file_ref}")

        if not os.path.isfile(file_ref):
            raise ValueError(f"Path is not a file: {file_ref}")

        if not quiet:
            print(f"Detected local file, uploading: {file_ref}", file=sys.stderr)

        fmt = detect_format(file_ref)
        oss_file_url = upload_file(file_ref, quiet=quiet, client=client)
        return oss_file_url

    return file_ref

if __name__ == '__main__':
    pass
