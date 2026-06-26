"""TOS 上传工具（精简版，仅 PDF 上传）。

P1 阶段只支持本地 PDF / 远程 URL / tos:// 三种输入；图片、长图智能裁剪等
高级特性留到 P2/P3 再考虑。

接口：
    resolve_input(path_or_url, ...) -> (final_url, meta_dict)
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


DEFAULT_REGION = "cn-beijing"
TOS_REGION_TO_ENDPOINT = {
    "cn-beijing":   "tos-cn-beijing.volces.com",
    "cn-shanghai":  "tos-cn-shanghai.volces.com",
    "cn-guangzhou": "tos-cn-guangzhou.volces.com",
}


class TOSConfigError(RuntimeError):
    """TOS 配置缺失。"""


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


# ---------------------------------------------------------------------------
# 配置读取
# ---------------------------------------------------------------------------

def _credentials() -> Tuple[str, str]:
    ak = os.environ.get("TOS_ACCESS_KEY")
    sk = os.environ.get("TOS_SECRET_KEY")
    if not ak or not sk:
        raise TOSConfigError(
            "TOS_ACCESS_KEY / TOS_SECRET_KEY 未配置（env.sh 或环境变量）。"
            "本地 PDF 必须先上传 TOS 才能调用 LAS。"
        )
    return ak, sk


def _resolve_tos_region(caller_region: str) -> str:
    """TOS 的桶 region 可能与 LAS 算子 region 不同（如桶在 cn-guangzhou，
    LAS 在 cn-beijing）。优先 TOS_REGION 环境变量，回退到 caller 传入。"""
    return os.environ.get("TOS_REGION") or caller_region


def _endpoint(region: str) -> str:
    e = os.environ.get("TOS_ENDPOINT")
    if e:
        return e
    if region not in TOS_REGION_TO_ENDPOINT:
        raise TOSConfigError(f"未知 region: {region}；请用 TOS_ENDPOINT 显式指定")
    return TOS_REGION_TO_ENDPOINT[region]


def _bucket(override: Optional[str] = None) -> str:
    b = override or os.environ.get("TOS_BUCKET")
    if not b:
        raise TOSConfigError("TOS_BUCKET 未配置（env.sh 或 --tos-bucket 参数）")
    return b


def _gen_key(local_path: str, prefix: str = "pdf-finance-parser/uploads") -> str:
    """生成 TOS 对象 key：{prefix}/{timestamp}_{uuid}/{safe_filename}

    文件名 sanitize 成纯 ASCII（LAS 后端 URL parser 不接受中文 key）。
    保留原文件名前缀（取 ASCII 字符）+ 短哈希，便于追溯。
    """
    p = Path(local_path)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:8]
    # 取原文件名的 ASCII 部分作为可读前缀（如 "_9-11"），保留扩展名
    stem_ascii = re.sub(r"[^A-Za-z0-9_.\-]", "", p.stem).strip("._-") or "doc"
    # 原中文名做 hash 保留追溯能力
    name_hash = hashlib.md5(p.name.encode("utf-8")).hexdigest()[:6]
    ext = p.suffix.lower() or ".pdf"
    safe_name = f"{stem_ascii[:32]}_{name_hash}{ext}"
    return f"{prefix.rstrip('/')}/{ts}_{uid}/{safe_name}"


# ---------------------------------------------------------------------------
# 上传
# ---------------------------------------------------------------------------

def upload_pdf(local_path: str, *,
               bucket: Optional[str] = None,
               prefix: str = "pdf-finance-parser/uploads",
               region: str = DEFAULT_REGION) -> str:
    """上传本地 PDF 到 TOS，返回 tos://bucket/key。"""
    try:
        import tos
    except ImportError as e:
        raise TOSConfigError(
            "tos SDK 未安装。请运行: pip install tos\n"
            "或参考: https://www.volcengine.com/docs/6349/74982"
        ) from e

    p = Path(local_path)
    if not p.is_file():
        raise FileNotFoundError(f"本地文件不存在: {local_path}")

    ak, sk = _credentials()
    tos_region = _resolve_tos_region(region)
    ep = _endpoint(tos_region)
    bk = _bucket(bucket)
    key = _gen_key(local_path, prefix)

    client = tos.TosClientV2(ak, sk, ep, tos_region)
    try:
        size_mb = p.stat().st_size / 1024 / 1024
        _log(f"[tos] uploading {p.name} ({size_mb:.2f} MB) -> tos://{bk}/{key}")
        with open(p, "rb") as f:
            client.put_object(bk, key, content=f)
        url = f"tos://{bk}/{key}"
        _log(f"[tos] upload ok")
        return url
    except tos.exceptions.TosClientError as e:
        raise RuntimeError(f"TOS 客户端错误: {e.message}, cause: {e.cause}") from e
    except tos.exceptions.TosServerError as e:
        raise RuntimeError(
            f"TOS 服务端错误: code={e.code}, message={e.message}, "
            f"request_id={e.request_id}, status={e.status_code}"
        ) from e
    finally:
        try:
            client.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# 统一入口
# ---------------------------------------------------------------------------

def _pdf_page_count(file_path: str) -> int:
    """尽力获取 PDF 页数（pypdf > pymupdf）。失败返回 0。"""
    try:
        import pypdf
        with open(file_path, "rb") as f:
            return len(pypdf.PdfReader(f).pages)
    except Exception:
        pass
    try:
        import fitz
        with fitz.open(file_path) as d:
            return len(d)
    except Exception:
        pass
    return 0


def resolve_input(path_or_url: str, *,
                  bucket: Optional[str] = None,
                  prefix: str = "pdf-finance-parser/uploads",
                  region: str = DEFAULT_REGION) -> Tuple[str, Dict[str, Any]]:
    """把用户输入统一解析为 LAS 可接受的 URL。

    返回 (final_url, meta)：
      - 本地 PDF → 上传 TOS，返回 tos://bucket/key, meta={input_type, pages, size_mb}
      - http(s)  → 原样返回, meta={input_type:"remote_url"}
      - tos://   → 原样返回, meta={input_type:"tos_path"}
    """
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url, {"input_type": "remote_url"}
    if path_or_url.startswith("tos://"):
        return path_or_url, {"input_type": "tos_path"}

    p = Path(path_or_url)
    if not p.is_file():
        raise FileNotFoundError(f"路径既不是 URL/tos:// 也不是本地文件: {path_or_url}")
    if p.suffix.lower() != ".pdf":
        raise ValueError(f"P1 阶段仅支持 PDF 输入（图片留到 P2）: {p.suffix}")

    tos_url = upload_pdf(str(p), bucket=bucket, prefix=prefix, region=region)
    return tos_url, {
        "input_type": "local_pdf",
        "pages": _pdf_page_count(str(p)),
        "size_mb": round(p.stat().st_size / 1024 / 1024, 2),
    }
