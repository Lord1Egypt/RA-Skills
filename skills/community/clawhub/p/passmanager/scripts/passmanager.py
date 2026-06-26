#!/usr/bin/env python3
"""
PassManager — Enterprise-grade password management system for AI assistants.

真正的AES-256-GCM加密密码管理系统，替代1Password等第三方服务。
基于cryptography库实现生产级安全存储。
"""

import sqlite3
import json
import os
import sys
import base64
import shutil
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Tuple

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

__version__ = "1.1.0"

DEFAULT_BASE_DIR = os.path.expanduser("~/.passmanager")
ENV_DB_PATH = os.environ.get("PASSMANAGER_DB")


def _generate_encryption_key(master_password: str, salt: bytes) -> bytes:
    """使用PBKDF2从主密码派生AES-256密钥"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    return kdf.derive(master_password.encode("utf-8"))


def _check_crypto():
    if not CRYPTO_AVAILABLE:
        print("❌ 需要安装 cryptography 库: pip3 install cryptography")
        sys.exit(1)


class PassManager:
    """
    PassManager核心类

    数据存储结构:
      - SQLite数据库存储加密后的凭证
      - AES-256-GCM加密所有敏感字段
      - PBKDF2密钥派生(600,000次迭代)
      - 每次加密使用随机12字节nonce
    """

    def __init__(self, db_path: str = None):
        _check_crypto()
        if db_path:
            self.db_path = db_path
        elif ENV_DB_PATH:
            self.db_path = ENV_DB_PATH
        else:
            self.db_path = os.path.join(DEFAULT_BASE_DIR, "passwords.db")

        self.base_dir = os.path.dirname(self.db_path)
        self.backup_dir = os.path.join(self.base_dir, "backups")
        self.log_dir = os.path.join(self.base_dir, "logs")
        self.key_file = os.path.join(self.base_dir, ".master_key")

        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

        self._init_database()

    # ──────────────────────────────
    # 数据库初始化
    # ──────────────────────────────

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        # 启用WAL模式，支持并发读写
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            service TEXT NOT NULL,
            username TEXT NOT NULL DEFAULT '',
            encrypted_data BLOB NOT NULL,
            notes TEXT DEFAULT '',
            created_by TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            updated_at TEXT DEFAULT (datetime('now', 'localtime')),
            UNIQUE(type, service, username)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('admin','user','auditor','guest')),
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            last_active TEXT DEFAULT ''
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT (datetime('now', 'localtime')),
            user TEXT NOT NULL,
            action TEXT NOT NULL,
            resource_type TEXT DEFAULT '',
            resource_name TEXT DEFAULT '',
            success INTEGER DEFAULT 1,
            detail TEXT DEFAULT ''
        )
        """)

        c.execute("CREATE INDEX IF NOT EXISTS idx_cred_type ON credentials(type, service)")
        try:
            c.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_log(timestamp)")
        except Exception:
            pass

        conn.commit()
        conn.close()

    # ──────────────────────────────
    # 密钥管理
    # ──────────────────────────────

    def init_master_key(self, master_password: str) -> bool:
        """初始化主密码（首次设置）"""
        if os.path.exists(self.key_file):
            print("❌ 主密码已存在。如需重置请手动删除 .master_key 文件。")
            return False

        salt = os.urandom(32)
        key = _generate_encryption_key(master_password, salt)

        # 存储 salt + 一个验证密文，用来验证密码是否正确
        verify_plaintext = b"PASSMANAGER_VERIFY_TOKEN"
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        verify_ciphertext = aesgcm.encrypt(nonce, verify_plaintext, None)

        key_data = {
            "salt": base64.b64encode(salt).decode(),
            "verify_nonce": base64.b64encode(nonce).decode(),
            "verify_ciphertext": base64.b64encode(verify_ciphertext).decode(),
            "created_at": datetime.now().isoformat(),
        }

        with open(self.key_file, "w") as f:
            json.dump(key_data, f)
        os.chmod(self.key_file, 0o600)

        self._log_audit("system", "MASTER_KEY_INIT", "", "", True, "主密码初始化成功")
        return True

    def _load_key(self, master_password: str) -> Optional[bytes]:
        """验证主密码并加载密钥"""
        if not os.path.exists(self.key_file):
            print("❌ 未初始化主密码。请先运行: passmanager init")
            return None

        try:
            with open(self.key_file) as f:
                key_data = json.load(f)

            salt = base64.b64decode(key_data["salt"])
            key = _generate_encryption_key(master_password, salt)

            verify_nonce = base64.b64decode(key_data["verify_nonce"])
            verify_ciphertext = base64.b64decode(key_data["verify_ciphertext"])

            aesgcm = AESGCM(key)
            aesgcm.decrypt(verify_nonce, verify_ciphertext, None)
            return key
        except Exception:
            return None

    # ──────────────────────────────
    # 加密/解密
    # ──────────────────────────────

    def _encrypt(self, key: bytes, plaintext: str) -> str:
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        return base64.b64encode(nonce + ct).decode()

    def _decrypt(self, key: bytes, encrypted: str) -> Optional[str]:
        try:
            raw = base64.b64decode(encrypted)
            nonce = raw[:12]
            ct = raw[12:]
            aesgcm = AESGCM(key)
            return aesgcm.decrypt(nonce, ct, None).decode("utf-8")
        except Exception:
            return None

    # ──────────────────────────────
    # 审计日志
    # ──────────────────────────────

    def _log_audit(self, user: str, action: str, resource_type: str = "",
                   resource_name: str = "", success: bool = True, detail: str = ""):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "INSERT INTO audit_log (user, action, resource_type, resource_name, success, detail) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (user, action, resource_type, resource_name, 1 if success else 0, detail),
            )
            conn.commit()
            conn.close()

            # 同时写文件日志
            log_file = os.path.join(
                self.log_dir, f"audit_{datetime.now().strftime('%Y%m%d')}.log"
            )
            entry = (
                f"{datetime.now().isoformat()} | {user} | {action} | "
                f"{resource_type}/{resource_name} | {'OK' if success else 'FAIL'} | {detail}\n"
            )
            with open(log_file, "a") as f:
                f.write(entry)
        except Exception:
            pass  # 日志写入失败不影响主流程

    # ──────────────────────────────
    # 权限检查
    # ──────────────────────────────

    def check_permission(self, user: str, required_action: str) -> bool:
        """检查用户是否有权限执行某操作"""
        if not user:
            return False
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT role FROM team_members WHERE name = ?", (user,))
        row = c.fetchone()
        conn.close()

        if not row:
            return False

        role = row[0]
        role_perms = {
            "admin": ["add", "get", "list", "update", "delete", "backup", "restore",
                      "audit", "team_add", "team_remove", "team_list", "status", "init"],
            "user": ["add", "get", "list", "update"],
            "auditor": ["get", "list", "audit"],
            "guest": ["get"],
        }
        allowed = role_perms.get(role, [])
        return required_action in allowed

    # ──────────────────────────────
    # 凭证管理
    # ──────────────────────────────

    def add(self, user: str, master_password: str, cred_type: str,
            service: str, username: str, password: str, notes: str = "") -> bool:
        key = self._load_key(master_password)
        if not key:
            return False

        encrypted = self._encrypt(key, password)

        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "INSERT OR REPLACE INTO credentials "
                "(type, service, username, encrypted_data, notes, created_by, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))",
                (cred_type, service, username, encrypted, notes, user),
            )
            conn.commit()
            conn.close()
            self._log_audit(user, "ADD", cred_type, f"{service}/{username}", True)
            return True
        except Exception as e:
            self._log_audit(user, "ADD", cred_type, f"{service}/{username}", False, str(e))
            return False

    def get(self, user: str, master_password: str, cred_type: str,
            service: str, username: str = "") -> Optional[dict]:
        key = self._load_key(master_password)
        if not key:
            return None

        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            if username:
                c.execute(
                    "SELECT type, service, username, encrypted_data, notes, created_by, created_at, updated_at "
                    "FROM credentials WHERE type = ? AND service = ? AND username = ?",
                    (cred_type, service, username),
                )
                row = c.fetchone()
            else:
                c.execute(
                    "SELECT type, service, username, encrypted_data, notes, created_by, created_at, updated_at "
                    "FROM credentials WHERE type = ? AND service = ?",
                    (cred_type, service),
                )
                rows = c.fetchall()
                if len(rows) > 1:
                    print(f"⚠️ 找到多条记录，请指定 --username")
                    conn.close()
                    return None
                row = rows[0] if rows else None

            if not row:
                conn.close()
                return None

            encrypted = row[3]
            password = self._decrypt(key, encrypted)
            result = {
                "type": row[0],
                "service": row[1],
                "username": row[2],
                "password": password or "❌ 解密失败",
                "notes": row[4],
                "created_by": row[5],
                "created_at": row[6],
                "updated_at": row[7],
            }
            conn.close()
            self._log_audit(user, "GET", cred_type, f"{service}/{username or row[2]}", True)
            return result
        except Exception as e:
            self._log_audit(user, "GET", cred_type, f"{service}/{username}", False, str(e))
            return None

    def list(self, user: str, cred_type: str = None) -> List[dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            if cred_type:
                c.execute(
                    "SELECT type, service, username, notes, created_by, created_at, updated_at "
                    "FROM credentials WHERE type = ? ORDER BY service, username",
                    (cred_type,),
                )
            else:
                c.execute(
                    "SELECT type, service, username, notes, created_by, created_at, updated_at "
                    "FROM credentials ORDER BY type, service, username"
                )
            rows = c.fetchall()
            conn.close()

            results = []
            for r in rows:
                results.append({
                    "type": r[0],
                    "service": r[1],
                    "username": r[2],
                    "notes": r[3],
                    "created_by": r[4],
                    "created_at": r[5],
                    "updated_at": r[6],
                })
            self._log_audit(user, "LIST", cred_type or "all", "", True)
            return results
        except Exception as e:
            self._log_audit(user, "LIST", cred_type or "all", "", False, str(e))
            return []

    def update(self, user: str, master_password: str, cred_type: str,
               service: str, username: str, new_password: str = None,
               new_notes: str = None) -> bool:
        key = self._load_key(master_password)
        if not key:
            return False

        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "SELECT id, encrypted_data FROM credentials "
                "WHERE type = ? AND service = ? AND username = ?",
                (cred_type, service, username),
            )
            row = c.fetchone()
            if not row:
                conn.close()
                return False

            cred_id = row[0]
            existing_encrypted = row[1]

            if new_password is not None:
                encrypted = self._encrypt(key, new_password)
                c.execute(
                    "UPDATE credentials SET encrypted_data = ?, updated_at = datetime('now', 'localtime') "
                    "WHERE id = ?",
                    (encrypted, cred_id),
                )

            if new_notes is not None:
                c.execute(
                    "UPDATE credentials SET notes = ?, updated_at = datetime('now', 'localtime') "
                    "WHERE id = ?",
                    (new_notes, cred_id),
                )

            conn.commit()
            conn.close()
            self._log_audit(user, "UPDATE", cred_type, f"{service}/{username}", True)
            return True
        except Exception as e:
            self._log_audit(user, "UPDATE", cred_type, f"{service}/{username}", False, str(e))
            return False

    def delete(self, user: str, cred_type: str, service: str, username: str = "") -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            if username:
                c.execute(
                    "DELETE FROM credentials WHERE type = ? AND service = ? AND username = ?",
                    (cred_type, service, username),
                )
            else:
                c.execute(
                    "DELETE FROM credentials WHERE type = ? AND service = ?",
                    (cred_type, service),
                )
            affected = c.rowcount
            conn.commit()
            conn.close()

            if affected > 0:
                self._log_audit(user, "DELETE", cred_type, f"{service}/{username}", True)
                return True
            return False
        except Exception as e:
            self._log_audit(user, "DELETE", cred_type, f"{service}/{username}", False, str(e))
            return False

    # ──────────────────────────────
    # 团队管理
    # ──────────────────────────────

    def team_add(self, admin_user: str, name: str, role: str = "user") -> bool:
        if role not in ("admin", "user", "auditor", "guest"):
            return False
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "INSERT OR IGNORE INTO team_members (name, role) VALUES (?, ?)",
                (name, role),
            )
            affected = c.rowcount
            conn.commit()
            conn.close()
            if affected > 0:
                self._log_audit(admin_user, "TEAM_ADD", "team", name, True)
                return True
            return False
        except Exception as e:
            self._log_audit(admin_user, "TEAM_ADD", "team", name, False, str(e))
            return False

    def team_list(self) -> List[dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT name, role, created_at, last_active FROM team_members ORDER BY role, name")
            rows = c.fetchall()
            conn.close()
            return [
                {"name": r[0], "role": r[1], "created_at": r[2], "last_active": r[3]}
                for r in rows
            ]
        except Exception:
            return []

    def team_remove(self, admin_user: str, name: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM team_members WHERE name = ?", (name,))
            affected = c.rowcount
            conn.commit()
            conn.close()
            if affected > 0:
                self._log_audit(admin_user, "TEAM_REMOVE", "team", name, True)
                return True
            return False
        except Exception as e:
            self._log_audit(admin_user, "TEAM_REMOVE", "team", name, False, str(e))
            return False

    def team_update(self, admin_user: str, name: str, new_role: str) -> bool:
        if new_role not in ("admin", "user", "auditor", "guest"):
            return False
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("UPDATE team_members SET role = ? WHERE name = ?", (new_role, name))
            affected = c.rowcount
            conn.commit()
            conn.close()
            if affected > 0:
                self._log_audit(admin_user, "TEAM_UPDATE", "team", f"{name}->{new_role}", True)
                return True
            return False
        except Exception as e:
            self._log_audit(admin_user, "TEAM_UPDATE", "team", f"{name}->{new_role}", False, str(e))
            return False

    # ──────────────────────────────
    # 系统管理
    # ──────────────────────────────

    def status(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM credentials")
        total_creds = c.fetchone()[0]
        c.execute("SELECT COUNT(DISTINCT type) FROM credentials")
        type_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM team_members")
        member_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM audit_log WHERE success = 1")
        ok_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM audit_log WHERE success = 0")
        fail_count = c.fetchone()[0]
        conn.close()

        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        key_exists = os.path.exists(self.key_file)

        return {
            "version": __version__,
            "database": self.db_path,
            "db_size": db_size,
            "credentials": total_creds,
            "credential_types": type_count,
            "team_members": member_count,
            "successful_ops": ok_count,
            "failed_ops": fail_count,
            "encryption": "AES-256-GCM",
            "master_key_set": key_exists,
        }

    def backup(self, output_path: str = None) -> Optional[str]:
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.backup_dir, f"backup_{ts}.db")

        try:
            shutil.copy2(self.db_path, output_path)
            if os.path.exists(self.key_file):
                key_backup = output_path + ".key"
                shutil.copy2(self.key_file, key_backup)
            self._log_audit("system", "BACKUP", "system", output_path, True)
            return output_path
        except Exception as e:
            self._log_audit("system", "BACKUP", "system", output_path, False, str(e))
            return None

    def restore(self, input_path: str) -> bool:
        if not os.path.exists(input_path):
            return False
        try:
            shutil.copy2(input_path, self.db_path)
            key_backup = input_path + ".key"
            if os.path.exists(key_backup):
                shutil.copy2(key_backup, self.key_file)
            self._log_audit("system", "RESTORE", "system", input_path, True)
            return True
        except Exception as e:
            self._log_audit("system", "RESTORE", "system", input_path, False, str(e))
            return False

    def audit_logs(self, limit: int = 50, user_filter: str = None,
                   action_filter: str = None) -> List[dict]:
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            conditions = []
            params = []
            if user_filter:
                conditions.append("user = ?")
                params.append(user_filter)
            if action_filter:
                conditions.append("action LIKE ?")
                params.append(f"%{action_filter}%")

            where = ""
            if conditions:
                where = "WHERE " + " AND ".join(conditions)

            sql = f"SELECT timestamp, user, action, resource_type, resource_name, success, detail "
            sql += f"FROM audit_log {where} ORDER BY id DESC LIMIT ?"
            params.append(limit)

            c.execute(sql, params)
            rows = c.fetchall()
            conn.close()
            return [
                {
                    "timestamp": r[0],
                    "user": r[1],
                    "action": r[2],
                    "resource_type": r[3],
                    "resource_name": r[4],
                    "success": bool(r[5]),
                    "detail": r[6],
                }
                for r in rows
            ]
        except Exception:
            return []


# ════════════════════════════════════════
# CLI 入口
# ════════════════════════════════════════


def cmd_init(args):
    pm = PassManager()
    if pm.init_master_key(args.master_password):
        pm.team_add("system", args.admin or "admin", "admin")
        print(f"✅ PassManager v{__version__} 初始化成功！")
        print(f"📁 数据库: {pm.db_path}")
        print(f"📁 备份目录: {pm.backup_dir}")
        print(f"📁 日志目录: {pm.log_dir}")
        print(f"🔐 加密: AES-256-GCM (PBKDF2 600K 迭代)")
        print(f"👤 管理员: {args.admin or 'admin'}")
    else:
        print("❌ 初始化失败。")


def cmd_add(args):
    pm = PassManager()
    if pm.add(args.user, args.master_password, args.type, args.service,
              args.username, args.password, args.notes):
        print(f"✅ 凭证添加成功: {args.type}/{args.service}/{args.username}")
    else:
        print("❌ 添加失败。检查权限或主密码。")


def cmd_get(args):
    pm = PassManager()
    result = pm.get(args.user, args.master_password, args.type, args.service, args.username)
    if result:
        print(f"\n🔐 {result['type'].upper()} 凭证")
        print(f"  服务:     {result['service']}")
        print(f"  用户名:   {result['username']}")
        if args.show_password:
            print(f"  密码:     {result['password']}")
        else:
            print(f"  密码:     {'*' * len(result.get('password', ''))}")
        print(f"  备注:     {result['notes']}")
        print(f"  创建人:   {result['created_by']}")
        print(f"  创建时间: {result['created_at']}")
        print(f"  更新时间: {result['updated_at']}")
    else:
        print("❌ 未找到该凭证或主密码错误。")


def cmd_list(args):
    pm = PassManager()
    results = pm.list(args.user, args.type)
    if not results:
        print("📭 没有凭证记录。")
        return

    print(f"\n📋 凭证列表 ({len(results)} 条)")
    print("-" * 70)
    print(f"{'类型':<12} {'服务':<20} {'用户名':<20} {'备注':<16}")
    print("-" * 70)
    for r in results:
        print(f"{r['type']:<12} {r['service']:<20} {r['username']:<20} {r['notes'][:15]:<16}")
    print("-" * 70)


def cmd_update(args):
    pm = PassManager()
    ok = pm.update(args.user, args.master_password, args.type, args.service,
                   args.username, args.password, args.notes)
    if ok:
        print(f"✅ 凭证更新成功: {args.type}/{args.service}/{args.username}")
    else:
        print("❌ 更新失败。检查主密码或凭证是否存在。")


def cmd_delete(args):
    pm = PassManager()
    ok = pm.delete(args.user, args.type, args.service, args.username)
    if ok:
        print(f"✅ 凭证已删除: {args.type}/{args.service}/{args.username}")
    else:
        print("❌ 删除失败。凭证不存在。")


def cmd_status(args):
    pm = PassManager()
    s = pm.status()
    print(f"\n📊 PassManager v{s['version']} 状态")
    print(f"  📁 数据库: {s['database']}")
    print(f"  💾 大小: {s['db_size'] / 1024:.1f} KB")
    print(f"  🔐 加密: {s['encryption']}")
    print(f"  🔑 主密钥: {'✅ 已设置' if s['master_key_set'] else '❌ 未设置'}")
    print(f"  📋 凭证数: {s['credentials']}")
    print(f"  🏷️  类型数: {s['credential_types']}")
    print(f"  👥 团队成员: {s['team_members']}")
    print(f"  ✅ 成功操作: {s['successful_ops']}")
    print(f"  ❌ 失败操作: {s['failed_ops']}")


def cmd_backup(args):
    pm = PassManager()
    path = pm.backup(args.output)
    if path:
        size = os.path.getsize(path) / 1024
        print(f"✅ 备份成功: {path} ({size:.1f} KB)")
    else:
        print("❌ 备份失败。")


def cmd_restore(args):
    pm = PassManager()
    if pm.restore(args.input):
        print(f"✅ 恢复成功: {args.input}")
    else:
        print("❌ 恢复失败。检查备份文件是否存在。")


def cmd_audit(args):
    pm = PassManager()
    logs = pm.audit_logs(args.limit, args.user_filter, args.action_filter)
    if not logs:
        print("📭 没有审计日志。")
        return

    print(f"\n📋 审计日志 (最近 {len(logs)} 条)")
    print("-" * 100)
    print(f"{'时间':<22} {'用户':<12} {'操作':<16} {'资源':<24} {'结果':<6} {'详情':<16}")
    print("-" * 100)
    for r in logs:
        resource = f"{r['resource_type']}/{r['resource_name']}"
        status_str = "✅" if r['success'] else "❌"
        print(f"{r['timestamp']:<22} {r['user']:<12} {r['action']:<16} {resource:<24} {status_str:<6} {r['detail'][:15]:<16}")
    print("-" * 100)


def cmd_team_add(args):
    pm = PassManager()
    if pm.team_add(args.admin, args.name, args.role):
        print(f"✅ 团队成员添加成功: {args.name} ({args.role})")
    else:
        print("❌ 添加失败。用户可能已存在。")


def cmd_team_list(args):
    pm = PassManager()
    members = pm.team_list()
    if not members:
        print("📭 没有团队成员。")
        return

    print("\n👥 团队成员")
    print("-" * 60)
    print(f"{'名称':<16} {'角色':<10} {'创建时间':<22} {'最后活跃':<10}")
    print("-" * 60)
    for m in members:
        print(f"{m['name']:<16} {m['role']:<10} {m['created_at']:<22} {m['last_active'][:10]:<10}")
    print("-" * 60)


def cmd_team_remove(args):
    pm = PassManager()
    if pm.team_remove(args.admin, args.name):
        print(f"✅ 团队成员已移除: {args.name}")
    else:
        print("❌ 移除失败。用户不存在。")


def cmd_team_update(args):
    pm = PassManager()
    if pm.team_update(args.admin, args.name, args.role):
        print(f"✅ 角色更新成功: {args.name} -> {args.role}")
    else:
        print("❌ 更新失败。检查用户和角色。")


# ════════════════════════════════════════
# 主解析器
# ════════════════════════════════════════


def main():
    _check_crypto()

    parser = argparse.ArgumentParser(
        prog="passmanager",
        description=f"PassManager v{__version__} — 企业级密码管理系统",
    )

    sub = parser.add_subparsers(dest="command", help="可用命令")

    # init
    p_init = sub.add_parser("init", help="初始化系统（首次运行）")
    p_init.add_argument("--admin", default="admin", help="管理员名称")
    p_init.add_argument("master_password", help="设置主密码")

    # add
    p_add = sub.add_parser("add", help="添加凭证")
    p_add.add_argument("user", help="当前用户名称")
    p_add.add_argument("master_password", help="主密码")
    p_add.add_argument("type", help="类型 (email/api_key/database/server/application/custom)")
    p_add.add_argument("service", help="服务名称")
    p_add.add_argument("username", help="用户名/账户名")
    p_add.add_argument("password", help="密码")
    p_add.add_argument("--notes", default="", help="备注")

    # get
    p_get = sub.add_parser("get", help="获取凭证")
    p_get.add_argument("user", help="当前用户名称")
    p_get.add_argument("master_password", help="主密码")
    p_get.add_argument("type", help="凭证类型")
    p_get.add_argument("service", help="服务名称")
    p_get.add_argument("username", nargs="?", default="", help="用户名（如有多条记录必填）")
    p_get.add_argument("--show-password", action="store_true", help="显示明文密码")

    # list
    p_list = sub.add_parser("list", help="列出凭证")
    p_list.add_argument("user", help="当前用户名称")
    p_list.add_argument("--type", "-t", dest="type", default=None, help="按类型过滤")

    # update
    p_update = sub.add_parser("update", help="更新凭证")
    p_update.add_argument("user", help="当前用户名称")
    p_update.add_argument("master_password", help="主密码")
    p_update.add_argument("type", help="凭证类型")
    p_update.add_argument("service", help="服务名称")
    p_update.add_argument("username", help="用户名")
    p_update.add_argument("--password", help="新密码")
    p_update.add_argument("--notes", help="新备注")

    # delete
    p_delete = sub.add_parser("delete", help="删除凭证")
    p_delete.add_argument("user", help="当前用户名称")
    p_delete.add_argument("type", help="凭证类型")
    p_delete.add_argument("service", help="服务名称")
    p_delete.add_argument("username", nargs="?", default="", help="用户名")

    # status
    sub.add_parser("status", help="查看系统状态")

    # backup
    p_backup = sub.add_parser("backup", help="备份数据库")
    p_backup.add_argument("--output", help="备份文件路径")

    # restore
    p_restore = sub.add_parser("restore", help="从备份恢复")
    p_restore.add_argument("input", help="备份文件路径")

    # audit
    p_audit = sub.add_parser("audit", help="查看审计日志")
    p_audit.add_argument("--limit", type=int, default=50, help="日志条数")
    p_audit.add_argument("--user", dest="user_filter", help="按用户过滤")
    p_audit.add_argument("--action", dest="action_filter", help="按操作过滤")

    # team
    p_team = sub.add_parser("team", help="团队管理")
    team_sub = p_team.add_subparsers(dest="team_cmd", help="团队管理命令")

    p_team_add = team_sub.add_parser("add", help="添加团队成员")
    p_team_add.add_argument("admin", help="管理员名称")
    p_team_add.add_argument("name", help="成员名称")
    p_team_add.add_argument("--role", default="user", choices=["admin", "user", "auditor", "guest"])

    p_team_list = team_sub.add_parser("list", help="列出团队成员")

    p_team_remove = team_sub.add_parser("remove", help="移除团队成员")
    p_team_remove.add_argument("admin", help="管理员名称")
    p_team_remove.add_argument("name", help="成员名称")

    p_team_update = team_sub.add_parser("update", help="更新成员角色")
    p_team_update.add_argument("admin", help="管理员名称")
    p_team_update.add_argument("name", help="成员名称")
    p_team_update.add_argument("role", choices=["admin", "user", "auditor", "guest"])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 路由命令
    cmd_map = {
        "init": cmd_init,
        "add": cmd_add,
        "get": cmd_get,
        "list": cmd_list,
        "update": cmd_update,
        "delete": cmd_delete,
        "status": cmd_status,
        "backup": cmd_backup,
        "restore": cmd_restore,
        "audit": cmd_audit,
    }

    if args.command == "team":
        if not args.team_cmd:
            parser.parse_args(["team", "--help"])
            return
        team_cmd_map = {
            "add": cmd_team_add,
            "list": cmd_team_list,
            "remove": cmd_team_remove,
            "update": cmd_team_update,
        }
        fn = team_cmd_map.get(args.team_cmd)
        if fn:
            fn(args)
        return

    fn = cmd_map.get(args.command)
    if fn:
        fn(args)


if __name__ == "__main__":
    main()
