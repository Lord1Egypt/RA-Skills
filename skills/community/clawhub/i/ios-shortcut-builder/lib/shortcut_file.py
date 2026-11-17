#!/usr/bin/env python3
"""shortcut_file.py — 读一个 .shortcut：本地文件或 iCloud 分享链接。

两种输入形态，内容完全不同：
  - iCloud 链接 → 拉下来的是**未签名** bplist，没有证书，但读得到快捷指令名
  - 本地已签名文件 → AEA1 容器，证书链在里面，但 Linux 上解不开内容

所以「能不能读到 CA 名」取决于用户发的是哪种，不能假定。
"""
from __future__ import annotations

import json
import os
import plistlib
import re
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ICLOUD_RE = re.compile(r"/shortcuts/(?:api/records/)?([0-9A-Fa-f]{8,})")
MAGIC_AEA = b"AEA1"
MAGIC_BPLIST = b"bplist00"


def is_url(s: str) -> bool:
    return s.startswith(("http://", "https://"))


def _safe(name: str) -> str:
    s = re.sub(r'[\\/:*?"<>|\s]+', "_", name).strip("_")
    return s[:60] or "shortcut"


def fetch_icloud(url: str, dest_dir: Path) -> tuple[Path, str]:
    """从 iCloud 分享链接拉取。返回 (本地路径, 分享名)。"""
    m = ICLOUD_RE.search(url)
    if not m:
        raise ValueError(
            "链接里没找到快捷指令 ID。\n"
            "  正确形态：https://www.icloud.com/shortcuts/1a2b3c4d5e6f...")
    sid = m.group(1)
    api = f"https://www.icloud.com/shortcuts/api/records/{sid}"
    req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise ValueError(
            f"拉取失败：HTTP {e.code}。\n"
            "  链接多半已失效，或作者取消了分享。让他重新在快捷指令 App 里"
            "「分享 → 拷贝 iCloud 链接」再发一次")
    except Exception as e:
        raise ValueError(f"拉取失败：{e}")
    fields = data.get("fields", {})
    try:
        dl = fields["shortcut"]["value"]["downloadURL"]
    except KeyError:
        raise ValueError("iCloud 返回里没有下载地址（链接可能失效或需要登录）")
    name = (fields.get("name", {}) or {}).get("value") or sid
    dest = Path(dest_dir) / f"{_safe(name)}.shortcut"
    urllib.request.urlretrieve(dl, dest)
    return dest, name


def kind(path: Path) -> str:
    raw = Path(path).read_bytes()[:8]
    if raw[:4] == MAGIC_AEA:
        return "signed"
    if raw[:8] == MAGIC_BPLIST or raw[:5] == b"<?xml":
        return "unsigned"
    return "unknown"


def workflow_name(path: Path) -> str | None:
    """从未签名 bplist 里读快捷指令名；已签名件在 Linux 上读不到。"""
    if kind(path) != "unsigned":
        return None
    try:
        d = plistlib.loads(Path(path).read_bytes())
    except Exception:
        return None
    return d.get("WFWorkflowName") or None


def materialize(source: str, tmpdir: str | None = None) -> tuple[Path, str | None, str | None]:
    """统一入口：本地路径或 URL → (本地路径, iCloud 分享名, 错误说明)。"""
    if is_url(source):
        d = Path(tmpdir or tempfile.mkdtemp(prefix="sc-adopt-"))
        d.mkdir(parents=True, exist_ok=True)
        try:
            p, name = fetch_icloud(source, d)
            return p, name, None
        except Exception as e:
            return Path(), None, str(e)
    p = Path(os.path.expanduser(source))
    if not p.is_file():
        return p, None, f"找不到文件：{p}"
    return p, None, None


# ---------------- 证书链（签名件里嵌的那几张 DER） ----------------

def extract_chain(path: Path) -> list[bytes]:
    """从 AEA1 签名件里把证书链原样取出来。纯 Python 解头，不需要 aea 工具。"""
    import struct
    raw = Path(path).read_bytes()
    if raw[:4] != MAGIC_AEA:
        return []
    try:
        n = struct.unpack("<I", raw[8:12])[0]
        meta = plistlib.loads(raw[12:12 + n])
        return list(meta.get("SigningCertificateChain") or [])
    except Exception:
        return []


def cert_subject(der: bytes) -> str:
    import subprocess
    r = subprocess.run(["openssl", "x509", "-inform", "DER", "-noout",
                        "-subject", "-nameopt", "utf8"],
                       input=der, capture_output=True)
    s = r.stdout.decode("utf-8", "replace").strip()
    return s[len("subject="):] if s.startswith("subject=") else s


def cert_cn(der: bytes) -> str:
    return cert_subject(der).split("CN=")[-1].strip()


def is_apple_cert(der: bytes) -> bool:
    return "Apple" in cert_subject(der)


def own_ca(chain: list[bytes]) -> bytes | None:
    """挑出签名者自己的 CA 证书（跳过 Apple 根证书和 xxx Signing 那张）。"""
    for der in chain:
        if is_apple_cert(der):
            continue
        if cert_cn(der).endswith(" Signing"):
            continue
        return der
    return None
