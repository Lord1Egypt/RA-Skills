#!/usr/bin/env python3
"""
wechat_voice_extractor.py — 微信语音一键提取工具

自动完成：解密微信数据库 → 列出群聊/联系人 → 提取指定人的语音 → 输出 silk 文件

前置条件：
  1. 微信 3.9.x PC 版已登录且正在运行
  2. 手机聊天记录已迁移到 PC（设置 → 聊天记录管理 → 导入与导出 → 导出到电脑）
  3. pip install pywxdump

用法：
  # 交互模式：自动引导选择群聊和目标人
  python wechat_voice_extractor.py --interactive

  # 列出所有群聊
  python wechat_voice_extractor.py --list-groups

  # 列出指定群聊的成员及语音数量
  python wechat_voice_extractor.py --group "家庭群名称"

  # 提取指定人的语音
  python wechat_voice_extractor.py --group "家庭群名称" --person "备注或昵称" --outdir ./voices/
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 默认工作目录
WORK_DIR = os.path.join(PROJECT_ROOT, "wxdump_work")


# ── 微信信息获取 ──────────────────────────────────────────────────────────────

def get_wechat_info() -> Optional[dict]:
    """获取运行中的微信信息（密钥、数据目录）。"""
    try:
        from pywxdump import get_wx_info
        results = get_wx_info()
        if not results:
            return None
        # 取第一个有效结果
        for info in results:
            if info.get("key") and info["key"] != "None":
                return info
        # key 为空但有 wx_dir 的也返回（可能需要 patch）
        return results[0] if results else None
    except ImportError:
        print("[x] pywxdump not installed: pip install pywxdump")
        return None


def find_wx_dir() -> Optional[str]:
    """查找微信数据目录。"""
    info = get_wechat_info()
    if info and info.get("wx_dir"):
        wx_dir = info["wx_dir"]
        # 找到具体的 wxid 目录
        if os.path.isdir(wx_dir):
            for d in os.listdir(wx_dir):
                if d.startswith("wxid_") and os.path.isdir(os.path.join(wx_dir, d, "Msg")):
                    return os.path.join(wx_dir, d)
        return wx_dir
    # 默认路径
    default = os.path.expanduser(r"~\Documents\WeChat Files")
    if os.path.isdir(default):
        for d in os.listdir(default):
            if d.startswith("wxid_") and os.path.isdir(os.path.join(default, d, "Msg")):
                return os.path.join(default, d)
    return None


# ── 数据库解密 ────────────────────────────────────────────────────────────────

def decrypt_databases(wx_dir: str, key: str, out_dir: str) -> list:
    """解密微信数据库。返回已解密的数据库列表。"""
    from pywxdump import decrypt

    db_dir = os.path.join(wx_dir, "Msg", "Multi")
    msg_dir = os.path.join(wx_dir, "Msg")
    os.makedirs(out_dir, exist_ok=True)

    decrypted = []

    # 解密 MediaMSG（语音数据）和 MSG（消息记录）
    for src_dir in [db_dir, msg_dir]:
        if not os.path.isdir(src_dir):
            continue
        for fname in os.listdir(src_dir):
            if not fname.endswith(".db"):
                continue
            if fname.endswith(("-shm", "-wal")):
                continue
            if "MediaMSG" in fname or ("MSG" in fname and "FTS" not in fname) or fname == "MicroMsg.db":
                src = os.path.join(src_dir, fname)
                dst = os.path.join(out_dir, fname)
                if os.path.exists(dst) and os.path.getsize(dst) > 0:
                    decrypted.append(dst)
                    continue
                try:
                    decrypt(key, src, dst)
                    if os.path.getsize(dst) > 0:
                        decrypted.append(dst)
                except Exception as e:
                    pass  # 部分数据库可能解密失败，跳过

    return decrypted


# ── 群聊和联系人查询 ──────────────────────────────────────────────────────────

def list_groups(decrypted_dir: str) -> list:
    """列出所有群聊及其名称。"""
    micro_db = os.path.join(decrypted_dir, "MicroMsg.db")
    if not os.path.exists(micro_db):
        return []

    conn = sqlite3.connect(micro_db)
    try:
        rows = conn.execute('''
            SELECT UserName, NickName FROM Contact
            WHERE UserName LIKE "%@chatroom" AND NickName != ""
            ORDER BY NickName
        ''').fetchall()
        return [{"id": r[0], "name": r[1]} for r in rows]
    except Exception:
        return []
    finally:
        conn.close()


def find_group(decrypted_dir: str, keyword: str) -> Optional[dict]:
    """按关键词搜索群聊。"""
    groups = list_groups(decrypted_dir)
    for g in groups:
        if keyword in g["name"]:
            return g
    return None


def list_voice_senders(decrypted_dir: str, group_id: str) -> list:
    """列出群聊中所有发送过语音的人及其语音数量。"""
    micro_db = os.path.join(decrypted_dir, "MicroMsg.db")

    # 收集语音消息的发送者
    sender_counts = {}
    for db_name in _find_msg_dbs(decrypted_dir):
        db_path = os.path.join(decrypted_dir, db_name)
        try:
            conn = sqlite3.connect(db_path)
            rows = conn.execute('''
                SELECT StrContent, BytesExtra, IsSender FROM MSG
                WHERE StrTalker = ? AND Type = 34
            ''', (group_id,)).fetchall()
            for content, extra, is_sender in rows:
                wxid = _extract_sender(content, extra, is_sender)
                if wxid:
                    sender_counts[wxid] = sender_counts.get(wxid, 0) + 1
            conn.close()
        except Exception:
            continue

    # 解析昵称
    result = []
    if os.path.exists(micro_db):
        conn = sqlite3.connect(micro_db)
        for wxid, count in sorted(sender_counts.items(), key=lambda x: -x[1]):
            row = conn.execute(
                'SELECT NickName, Remark FROM Contact WHERE UserName = ?', (wxid,)
            ).fetchone()
            nick = row[0] if row else ""
            remark = row[1] if row and row[1] else ""
            display = remark or nick or wxid
            result.append({"wxid": wxid, "name": display, "nickname": nick, "remark": remark, "count": count})
        conn.close()
    else:
        for wxid, count in sorted(sender_counts.items(), key=lambda x: -x[1]):
            result.append({"wxid": wxid, "name": wxid, "nickname": "", "remark": "", "count": count})

    return result


def _extract_sender(content: str, extra: bytes, is_sender: int) -> str:
    """从消息中提取发送者 wxid。"""
    # 语音消息的 XML 中有 fromusername
    if content:
        m = re.search(r'fromusername="([^"]+)"', content)
        if m:
            return m.group(1)
    # 文字消息从 BytesExtra 提取
    if extra:
        wxids = re.findall(rb'wxid_[a-z0-9]+', extra)
        if wxids:
            return wxids[0].decode()
    return ""


def _find_msg_dbs(decrypted_dir: str) -> list:
    """查找所有 MSG 数据库。"""
    return sorted([
        f for f in os.listdir(decrypted_dir)
        if re.match(r'MSG\d+\.db$', f) and os.path.getsize(os.path.join(decrypted_dir, f)) > 0
    ])


def _find_media_dbs(decrypted_dir: str) -> list:
    """查找所有 MediaMSG 数据库。"""
    return sorted([
        f for f in os.listdir(decrypted_dir)
        if re.match(r'MediaMSG\d+\.db$', f) and os.path.getsize(os.path.join(decrypted_dir, f)) > 0
    ])


# ── 语音提取 ──────────────────────────────────────────────────────────────────

def extract_voices(
    decrypted_dir: str,
    group_id: str,
    target_wxids: set,
    output_dir: str,
) -> dict:
    """提取目标人的所有语音文件。"""
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: 收集目标人的语音 MsgSvrID + 元信息
    voice_svrids = {}
    for db_name in _find_msg_dbs(decrypted_dir):
        db_path = os.path.join(decrypted_dir, db_name)
        try:
            conn = sqlite3.connect(db_path)
            rows = conn.execute('''
                SELECT MsgSvrID, CreateTime, StrContent FROM MSG
                WHERE StrTalker = ? AND Type = 34
            ''', (group_id,)).fetchall()
            for svrid, ts, content in rows:
                m = re.search(r'fromusername="([^"]+)"', content or "")
                if m and m.group(1) in target_wxids:
                    dur_m = re.search(r'voicelength="(\d+)"', content or "")
                    dur_ms = int(dur_m.group(1)) if dur_m else 0
                    voice_svrids[svrid] = {"ts": ts, "dur_ms": dur_ms}
            conn.close()
        except Exception:
            continue

    # Step 2: 从 MediaMSG 用 Reserved0 = MsgSvrID 提取音频
    extracted = 0
    total_dur_ms = 0
    for db_name in _find_media_dbs(decrypted_dir):
        db_path = os.path.join(decrypted_dir, db_name)
        try:
            conn = sqlite3.connect(db_path)
            rows = conn.execute('SELECT Reserved0, Buf FROM Media WHERE Buf IS NOT NULL').fetchall()
            for r0, buf in rows:
                if r0 in voice_svrids and buf and len(buf) > 100:
                    info = voice_svrids[r0]
                    dt = datetime.fromtimestamp(info["ts"]).strftime("%Y%m%d_%H%M%S")
                    dur_s = info["dur_ms"] / 1000
                    fname = f"voice_{dt}_{dur_s:.0f}s.silk"
                    with open(os.path.join(output_dir, fname), "wb") as f:
                        f.write(buf)
                    extracted += 1
                    total_dur_ms += info["dur_ms"]
            conn.close()
        except Exception:
            continue

    return {
        "total_found": len(voice_svrids),
        "extracted": extracted,
        "total_duration_seconds": total_dur_ms / 1000,
    }


# ── 交互模式 ──────────────────────────────────────────────────────────────────

def interactive_mode(out_base: str):
    """交互式引导用户完成语音提取。"""
    print("=" * 60)
    print("  Memorial Voice Extractor - WeChat")
    print("=" * 60)

    # Step 1: 获取微信信息
    print("\n[1/5] Detecting WeChat...")
    info = get_wechat_info()
    if not info:
        print("[x] WeChat not detected. Please ensure:")
        print("  - WeChat 3.9.x PC version is running and logged in")
        print("  - pip install pywxdump")
        return

    key = info.get("key")
    wx_dir = find_wx_dir()
    if not key or key == "None" or not wx_dir:
        print(f"[x] Cannot get decryption key (version: {info.get('version', '?')})")
        print("  WeChat 4.x is not supported by pywxdump yet.")
        print("  Please install WeChat 3.9.x from:")
        print("  https://github.com/tom-snow/wechat-windows-versions/releases/tag/v3.9.9.43")
        return

    print(f"  WeChat version: {info.get('version', '?')}")
    print(f"  Data directory: {wx_dir}")

    # Step 2: 解密数据库
    print("\n[2/5] Decrypting databases...")
    decrypt_dir = os.path.join(out_base, "decrypted")
    dbs = decrypt_databases(wx_dir, key, decrypt_dir)
    print(f"  Decrypted {len(dbs)} databases")

    # Step 3: 列出群聊
    print("\n[3/5] Finding group chats...")
    groups = list_groups(decrypt_dir)
    if not groups:
        print("[x] No group chats found")
        return

    print(f"  Found {len(groups)} groups:")
    for i, g in enumerate(groups[:20], 1):
        print(f"    {i}. {g['name']}")
    if len(groups) > 20:
        print(f"    ... and {len(groups) - 20} more")

    # 用户选择群聊（在 Claude Code 环境中通过参数传入）
    print("\n  [Next] Use --group 'keyword' to select a group")
    print("  Example: python wechat_voice_extractor.py --group '家' --outdir ./voices/")


def extract_mode(group_keyword: str, person_keyword: str, out_base: str, outdir: str):
    """自动提取模式。"""
    # 获取微信信息
    info = get_wechat_info()
    if not info:
        print("[x] WeChat not detected")
        return

    key = info.get("key")
    wx_dir = find_wx_dir()
    if not key or key == "None" or not wx_dir:
        print("[x] Cannot get decryption key")
        return

    # 解密
    decrypt_dir = os.path.join(out_base, "decrypted")
    dbs = decrypt_databases(wx_dir, key, decrypt_dir)
    print(f"[ok] {len(dbs)} databases decrypted")

    # 查找群聊
    group = find_group(decrypt_dir, group_keyword)
    if not group:
        print(f"[x] Group not found: '{group_keyword}'")
        print("Available groups:")
        for g in list_groups(decrypt_dir)[:15]:
            print(f"  {g['name']}")
        return

    print(f"[ok] Group: {group['name']} ({group['id']})")

    # 列出语音发送者
    senders = list_voice_senders(decrypt_dir, group["id"])
    if not senders:
        print("[x] No voice messages found in this group")
        return

    if not person_keyword:
        print(f"\nVoice message senders ({len(senders)}):")
        for s in senders:
            print(f"  {s['name']}: {s['count']} messages")
        print("\n  [Next] Add --person 'name' to extract")
        return

    # 查找目标人（支持多个 wxid，如同一人有多个账号）
    target_wxids = set()
    for s in senders:
        if person_keyword in s["name"] or person_keyword in s["nickname"] or person_keyword in s["remark"]:
            target_wxids.add(s["wxid"])

    if not target_wxids:
        print(f"[x] Person not found: '{person_keyword}'")
        print("Available senders:")
        for s in senders:
            print(f"  {s['name']}: {s['count']} messages")
        return

    total_msgs = sum(s["count"] for s in senders if s["wxid"] in target_wxids)
    print(f"[ok] Target: {person_keyword} ({len(target_wxids)} wxid(s), {total_msgs} voice messages)")

    # 提取语音
    print(f"\n[extracting] ...")
    stats = extract_voices(decrypt_dir, group["id"], target_wxids, outdir)

    print(f"\n[ok] Extracted {stats['extracted']}/{stats['total_found']} voice files")
    print(f"  Total duration: {stats['total_duration_seconds']:.0f}s ({stats['total_duration_seconds']/60:.1f} min)")
    print(f"  Output: {outdir}")

    if stats["total_duration_seconds"] >= 180:
        print(f"\n  [next] python voice_preprocessor.py --dir {outdir} --outdir ./processed/")
    elif stats["total_duration_seconds"] >= 30:
        print(f"\n  [next] python voice_preprocessor.py --dir {outdir} --outdir ./processed/")
        print(f"  (Audio < 3 min, voice quality may be limited)")
    else:
        print(f"\n  [!] Audio too short ({stats['total_duration_seconds']:.0f}s), consider collecting more")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="WeChat voice extractor - one-click extraction from WeChat databases",
    )
    parser.add_argument("--interactive", action="store_true",
                        help="Interactive guided mode")
    parser.add_argument("--list-groups", action="store_true",
                        help="List all group chats")
    parser.add_argument("--group", help="Group chat name keyword")
    parser.add_argument("--person", help="Target person name/remark keyword")
    parser.add_argument("--outdir", default="./voices_raw",
                        help="Output directory for voice files")
    parser.add_argument("--workdir", default=WORK_DIR,
                        help="Working directory for decrypted databases")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode(args.workdir)
    elif args.list_groups:
        info = get_wechat_info()
        if not info:
            print("[x] WeChat not detected")
            return
        decrypt_dir = os.path.join(args.workdir, "decrypted")
        key = info.get("key", "")
        wx_dir = find_wx_dir()
        if key and key != "None" and wx_dir:
            decrypt_databases(wx_dir, key, decrypt_dir)
        for g in list_groups(decrypt_dir):
            print(f"  {g['name']}")
    elif args.group:
        extract_mode(args.group, args.person or "", args.workdir, args.outdir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
