#!/usr/bin/env python3
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""jdgold skill 升级检查与执行脚本

用法:
  python3 upgrade.py check              # 检查是否有新版本（静默，输出JSON）
  python3 upgrade.py download           # 下载最新包到临时目录
  python3 upgrade.py apply <tar_path>   # 校验+解压覆盖+更新version.json
  python3 upgrade.py version            # 输出当前本地版本信息

退出码:
  0 = 成功 / 有新版本可用
  1 = 网络错误 / manifest不可达
  2 = SHA256校验失败
  3 = 解压/文件操作失败
  4 = 已是最新版本（check时）
  5 = 参数错误
"""

import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# === 路径约定 ===
SKILL_DIR = Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_DIR / "version.json"


def _read_version() -> dict:
    """读取本地 version.json"""
    if not VERSION_FILE.exists():
        return {"version": "0.0.0", "installed_at": None, "manifest_url": None, "previous_version": None}
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_version(data: dict):
    """写入本地 version.json"""
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _fetch_manifest(manifest_url: str) -> dict:
    """从远端获取 manifest.json"""
    headers = {"User-Agent": "jdgold-upgrade/1.0"}
    claw = os.environ.get("CLAW", "").strip()
    if claw:
        headers["x-claw"] = claw
    req = Request(manifest_url, headers=headers)
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError, TimeoutError) as e:
        print(json.dumps({"error": f"无法访问更新服务: {e}", "code": 1}), file=sys.stdout)
        sys.exit(1)


def _compare_versions(local: str, remote: str) -> int:
    """语义化版本比较: -1=local<remote, 0=相等, 1=local>remote"""
    def to_tuple(v):
        return tuple(int(x) for x in v.split("."))
    l, r = to_tuple(local), to_tuple(remote)
    if l < r:
        return -1
    elif l == r:
        return 0
    return 1


def _sha256_file(filepath: str) -> str:
    """计算文件SHA256"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _download_file(url: str, dest_path: str) -> str:
    """下载文件到指定路径"""
    headers = {"User-Agent": "jdgold-upgrade/1.0"}
    claw = os.environ.get("CLAW", "").strip()
    if claw:
        headers["x-claw"] = claw
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=120) as resp:
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(resp, f)
        return dest_path
    except (URLError, HTTPError, TimeoutError) as e:
        print(json.dumps({"error": f"下载失败: {e}", "code": 1}), file=sys.stdout)
        sys.exit(1)


def cmd_check():
    """检查是否有新版本"""
    local = _read_version()
    manifest_url = local.get("manifest_url")
    if not manifest_url or manifest_url.startswith("__"):
        print(json.dumps({
            "need_upgrade": False,
            "current_version": local["version"],
            "error": "manifest_url 未配置",
            "code": 5
        }, ensure_ascii=False))
        sys.exit(5)

    manifest = _fetch_manifest(manifest_url)
    remote_version = manifest["latest_version"]
    current_version = local["version"]
    cmp = _compare_versions(current_version, remote_version)

    result = {
        "need_upgrade": cmp < 0,
        "current_version": current_version,
        "latest_version": remote_version,
        "changelog_summary": manifest.get("changelog_summary", ""),
        "breaking_changes": manifest.get("breaking_changes", False),
        "upgrade_notice": manifest.get("upgrade_notice", ""),
        "package_size": manifest.get("package", {}).get("size_bytes", 0),
        "released_at": manifest.get("released_at", ""),
        "code": 0 if cmp < 0 else 4
    }
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if cmp < 0 else 4)


def cmd_download():
    """下载最新包到临时目录"""
    local = _read_version()
    manifest_url = local.get("manifest_url")
    if not manifest_url or manifest_url.startswith("__"):
        print(json.dumps({"error": "manifest_url 未配置", "code": 5}, ensure_ascii=False))
        sys.exit(5)

    manifest = _fetch_manifest(manifest_url)
    pkg = manifest["package"]
    pkg_url = pkg["url"]

    # 下载到临时目录
    tmp_dir = tempfile.mkdtemp(prefix="jdgold-upgrade-")
    filename = f"jdgold-{manifest['latest_version']}.zip"
    dest = os.path.join(tmp_dir, filename)

    print(json.dumps({"status": "downloading", "url": pkg_url, "dest": dest}, ensure_ascii=False), file=sys.stderr)
    _download_file(pkg_url, dest)

    # SHA256校验
    actual_hash = _sha256_file(dest)
    expected_hash = pkg["sha256"]
    if actual_hash != expected_hash:
        os.unlink(dest)
        print(json.dumps({
            "error": "SHA256校验失败",
            "expected": expected_hash,
            "actual": actual_hash,
            "code": 2
        }, ensure_ascii=False))
        sys.exit(2)

    result = {
        "status": "downloaded",
        "path": dest,
        "version": manifest["latest_version"],
        "sha256": actual_hash,
        "size_bytes": os.path.getsize(dest),
        "code": 0
    }
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)


def cmd_apply(tar_path: str):
    """解压覆盖+更新version.json"""
    if not os.path.isfile(tar_path):
        print(json.dumps({"error": f"文件不存在: {tar_path}", "code": 3}, ensure_ascii=False))
        sys.exit(3)

    local = _read_version()
    manifest_url = local.get("manifest_url")
    manifest = _fetch_manifest(manifest_url) if manifest_url and not manifest_url.startswith("__") else None

    # 解压新版本
    try:
        with zipfile.ZipFile(tar_path, "r") as zf:
            # 安全检查：防止路径穿越
            for name in zf.namelist():
                if name.startswith("/") or ".." in name:
                    print(json.dumps({"error": f"不安全的压缩包路径: {name}", "code": 3}, ensure_ascii=False))
                    sys.exit(3)
            zf.extractall(str(SKILL_DIR))
    except (zipfile.BadZipFile, OSError) as e:
        print(json.dumps({"error": f"解压失败: {e}", "code": 3}, ensure_ascii=False))
        sys.exit(3)

    # 更新 version.json
    new_version = manifest["latest_version"] if manifest else "unknown"
    now = datetime.now(timezone(timedelta(hours=8))).isoformat()
    _write_version({
        "version": new_version,
        "installed_at": now,
        "manifest_url": manifest_url,
        "previous_version": local["version"]
    })

    # 验证关键文件
    critical_files = ["SKILL.md", "scripts/jos.py", "scripts/bff_client.py"]
    missing = [f for f in critical_files if not (SKILL_DIR / f).exists()]
    if missing:
        print(json.dumps({
            "error": f"升级后缺失关键文件: {missing}",
            "code": 3
        }, ensure_ascii=False))
        sys.exit(3)

    # 清理临时下载文件
    try:
        os.unlink(tar_path)
        os.rmdir(os.path.dirname(tar_path))
    except OSError:
        pass

    result = {
        "status": "upgraded",
        "previous_version": local["version"],
        "current_version": new_version,
        "code": 0
    }
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)


def cmd_version():
    """输出当前版本信息"""
    local = _read_version()
    print(json.dumps(local, ensure_ascii=False))
    sys.exit(0)


def main():
    if len(sys.argv) < 2:
        print(f"用法: python3 {sys.argv[0]} <check|download|apply|version>")
        sys.exit(5)

    action = sys.argv[1]

    if action == "check":
        cmd_check()
    elif action == "download":
        cmd_download()
    elif action == "apply":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "apply 需要指定 tar.gz 路径", "code": 5}, ensure_ascii=False))
            sys.exit(5)
        cmd_apply(sys.argv[2])
    elif action == "version":
        cmd_version()
    else:
        print(json.dumps({"error": f"未知命令: {action}", "code": 5}, ensure_ascii=False))
        sys.exit(5)


if __name__ == "__main__":
    main()
