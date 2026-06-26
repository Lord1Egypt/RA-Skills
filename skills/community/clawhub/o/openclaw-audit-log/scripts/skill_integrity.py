#!/usr/bin/env python3
"""
OpenClaw Skill 文件完整性校验系统
定期对 skill 目录做 hash 校验，检测文件被篡改。
"""

import sys
import json
import hashlib
import os
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

APP_ID = "cli_a92fd77a9af8dcd4"
APP_SECRET = "GjLeLpcUeUe92GCSvFSlxSoKwqHvGXeF"
USER_ID = "ou_24d7f017625dc287e1eb2fa63b4a00ed"

SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
HASH_FILE = Path.home() / ".openclaw" / "audit" / "skill_hashes.json"

# 需要排除的目录/文件（如 node_modules, .git 等）
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".clawhub"}


def get_token():
    req = Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]


def send_alert(token, title: str, detail: str):
    content = (
        f"🔴 **{title}**\n\n"
        f"{detail}\n\n"
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    req = Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps({
            "receive_id": USER_ID,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read()).get("code") == 0
    except Exception:
        return False


def compute_hash(file_path: Path) -> str:
    """计算文件的 SHA256 hash"""
    sha = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception:
        return ""


def scan_skills() -> dict:
    """扫描 skill 目录，返回 {rel_path: hash}"""
    hashes = {}
    for root, dirs, files in os.walk(SKILLS_DIR):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if file.startswith("."):
                continue
            file_path = Path(root) / file
            rel_path = file_path.relative_to(SKILLS_DIR)
            hashes[str(rel_path)] = compute_hash(file_path)

    return hashes


def load_hashes() -> dict:
    if HASH_FILE.exists():
        return json.loads(HASH_FILE.read_text())
    return {}


def save_hashes(hashes: dict, metadata: dict = None):
    HASH_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "hashes": hashes,
        "last_updated": datetime.now().isoformat(),
        **(metadata or {})
    }
    HASH_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def check_integrity(send_notification: bool = True) -> dict:
    """
    检查 skill 文件完整性。
    返回: {changed: [files], new: [files], deleted: [files]}
    """
    current = scan_skills()
    stored = load_hashes()

    current_set = set(current.keys())
    stored_set = set(stored.get("hashes", {}).keys())

    changed = []
    new_files = []
    deleted = []

    # 新增文件
    for f in current_set - stored_set:
        new_files.append(f)

    # 删除文件
    for f in stored_set - current_set:
        deleted.append(f)

    # 修改文件
    for f in current_set & stored_set:
        if current[f] != stored["hashes"].get(f):
            changed.append(f)

    result = {"changed": changed, "new": new_files, "deleted": deleted}

    if (changed or new_files or deleted) and send_notification:
        token = get_token()
        lines = ["🔴 **Skill 文件完整性异常**\n"]

        if new_files:
            lines.append(f"**新增文件** ({len(new_files)}):")
            for f in new_files[:10]:
                lines.append(f"  + {f}")
            if len(new_files) > 10:
                lines.append(f"  ... 还有 {len(new_files) - 10} 个")

        if deleted:
            lines.append(f"\n**删除文件** ({len(deleted)}):")
            for f in deleted[:10]:
                lines.append(f"  - {f}")

        if changed:
            lines.append(f"\n**篡改文件** ({len(changed)}):")
            for f in changed[:10]:
                lines.append(f"  ~ {f}")
            if len(changed) > 10:
                lines.append(f"  ... 还有 {len(changed) - 10} 个")

        lines.append("\n请确认这些变更是否为本人操作。")
        ok = send_alert(token, "Skill 文件完整性异常", "\n".join(lines))
        print(f"完整性告警: {'✅' if ok else '❌'}")

    return result


def update_baseline():
    """更新基准 hash（确认当前文件为可信）"""
    current = scan_skills()
    save_hashes(current, {"note": "手动更新基准hash"})
    print(f"基准已更新: {len(current)} 个文件")


# ========== CLI ==========

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: skill_integrity.py <check|update>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "check":
        result = check_integrity()
        print(f"变更: {len(result['changed'])}")
        print(f"新增: {len(result['new'])}")
        print(f"删除: {len(result['deleted'])}")
        if result["changed"]:
            print("篡改文件:", result["changed"])
        if result["new"]:
            print("新增文件:", result["new"])
        if result["deleted"]:
            print("删除文件:", result["deleted"])
        if not any(result.values()):
            print("✅ 无异常，所有文件完整")

    elif cmd == "update":
        update_baseline()
        print("✅ 基准 hash 已更新")

    elif cmd == "scan":
        hashes = scan_skills()
        print(f"扫描完成: {len(hashes)} 个文件")
        for path, h in sorted(hashes.items())[:10]:
            print(f"  {h[:16]}... {path}")
        if len(hashes) > 10:
            print(f"  ... 还有 {len(hashes) - 10} 个")

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
