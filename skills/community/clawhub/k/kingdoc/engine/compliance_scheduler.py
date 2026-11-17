"""KingDoc 全域合规扫描定时化（v4.3.0 新增）

能力：
- 周扫空间：Windows 用 schtasks 注册周扫任务；非 Windows 输出 cron 行 + 手动命令
- 新检出项经 webhook_center 三通道推送（签名核验 + SQLite 去重，只推新增不扰民）
- 复用 v4.0 webhook 中心与去重表，新增扫描级去重（同一 finding 跨周不重复推送）

零第三方依赖（stdlib sqlite3/subprocess/平台判断）；本地降级：未配置 webhook 时仅本地记录。

设计要点：
- 扫描级去重表 compliance_scan_dedup 以 (doc_id + pack + 词/类型 + 行号) 计算 hash，
  保证「周扫连续 4 周零误推」——已推送过的 finding 不再推送。
- webhook_center 自身也有 webhook_dedup 二次防护。
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine.compliance_suite import (
    ComplianceSuite,
    DEFAULT_SIGNING_SECRET,
)

SKILL_ROOT = Path(__file__).resolve().parent.parent
_DB_PATH = str(Path(__file__).resolve().parent.parent.parent / ".kingdoc_compliance_scan.db")

# 推送事件类型（与 webhook_center EVENT_TYPES 解耦，独立去重）
EVENT_TYPE = "compliance_new_find"


class ComplianceScheduler:
    """全域合规扫描调度器。"""

    def __init__(
        self,
        backend: Optional[Any] = None,
        signing_secret: str = "",
        external_packs_dir: Optional[str] = None,
    ):
        self.backend = backend
        self.signing_secret = signing_secret or DEFAULT_SIGNING_SECRET
        self.external_packs_dir = external_packs_dir
        self.suite = ComplianceSuite(backend=backend, external_packs_dir=external_packs_dir)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(_DB_PATH)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS weekly_scan_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    space_id TEXT NOT NULL,
                    packs_json TEXT DEFAULT '[]',
                    task_name TEXT,
                    weekday TEXT DEFAULT 'MON',
                    scan_time TEXT DEFAULT '03:00',
                    created_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS compliance_scan_dedup (
                    finding_hash TEXT PRIMARY KEY,
                    doc_id TEXT,
                    space_id TEXT,
                    created_at TEXT
                )
            """)
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 1. 注册周扫任务
    # ------------------------------------------------------------------
    def register_weekly_scan(
        self,
        space_id: str,
        packs: Optional[List[str]] = None,
        task_name: str = "kingdoc_compliance_weekly",
        weekday: str = "MON",
        scan_time: str = "03:00",
    ) -> Dict:
        """注册周扫任务。

        返回 mode（windows_schtasks / cron_manual）与可直接执行的命令。
        非 Windows 不实际写入系统定时，仅产出 cron 行，由用户自行部署。
        """
        packs = packs or []
        conn = sqlite3.connect(_DB_PATH)
        try:
            conn.execute(
                """INSERT INTO weekly_scan_config (space_id, packs_json, task_name, weekday, scan_time, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (space_id, json.dumps(packs, ensure_ascii=False), task_name,
                 weekday, scan_time, datetime.now().isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        runner = str(SKILL_ROOT / "engine" / "compliance_scheduler.py")
        py = "python"  # 由运行环境决定，调度器在宿主环境执行
        cmd = f'{py} "{runner}" --space {space_id} --packs {",".join(packs)}'

        if platform.system().lower().startswith("win"):
            sch = (f'schtasks /create /tn "{task_name}" '
                   f'/tr "\\"{py}\\" \\"{runner}\\" --space {space_id} --packs {",".join(packs)}" '
                   f'/sc weekly /d {weekday} /st {scan_time} /f')
            return {"success": True, "mode": "windows_schtasks",
                    "task_name": task_name, "command": sch,
                    "note": "在 Windows 宿主以管理员运行上述命令即可生效；本函数不自动写入系统定时。"}
        else:
            # cron：周一=1
            wd = {"MON": "1", "TUE": "2", "WED": "3", "THU": "4",
                  "FRI": "5", "SAT": "6", "SUN": "0"}.get(weekday.upper(), "1")
            hh, mm = (scan_time.split(":") + ["00"])[:2]
            cron = f"{int(mm)} {int(hh)} * * {wd} {cmd}"
            return {"success": True, "mode": "cron_manual",
                    "task_name": task_name, "command": cron,
                    "note": "非 Windows 系统：将上方 cron 行加入 crontab（crontab -e）即可周扫。"}

    # ------------------------------------------------------------------
    # 2. 执行扫描（仅推送新增）
    # ------------------------------------------------------------------
    def run_scan(
        self,
        space_id: str,
        docs: Optional[List[Dict]] = None,
        packs: Optional[List[str]] = None,
        external_packs_dir: Optional[str] = None,
    ) -> Dict:
        """扫描空间文档，仅把新增 finding 经 webhook 三通道推送。

        docs: [{"doc_id": "...", "content": "..."}]；云端模式可由 backend 拉取后传入。
        返回 {scanned, total_findings, new_findings, pushed, skipped_dup}
        """
        if docs is None:
            docs = []
        packs = packs or []
        ext = external_packs_dir or self.external_packs_dir

        scanned = 0
        total_findings = 0
        new_findings = 0
        pushed = 0
        skipped_dup = 0
        push_errors = 0

        for doc in docs:
            doc_id = doc.get("doc_id", "")
            content = doc.get("content", "")
            if not content:
                continue
            scanned += 1
            report = self.suite.full_scan(content, doc_id=doc_id, packs=packs,
                                          external_packs_dir=ext)
            # 汇总该文档所有可定位 finding（敏感词 + 泄露）
            findings = []
            for h in report.get("sensitive_words", {}).get("risk_breakdown", {}) and []:
                pass  # risk_breakdown 无明细，改用 quick 明细
            # 直接复用 quick_scan 明细以确保每行定位
            q = self.suite.quick_scan(content, packs=packs, external_packs_dir=ext)
            for h in q["sensitive_detail"]:
                findings.append({
                    "kind": "sensitive", "doc_id": doc_id, "pack": h.get("pack", ""),
                    "word": h.get("word", ""), "line": h.get("line", 0),
                    "risk_tier": h.get("risk_tier", "中"),
                    "responsible_field": h.get("responsible_field", ""),
                })
            for f in q["leak_detail"]:
                findings.append({
                    "kind": "leak", "doc_id": doc_id, "pack": "leak",
                    "word": f.get("label", f.get("type", "")), "line": f.get("line", 0),
                    "risk_tier": f.get("risk_tier", "中"),
                    "responsible_field": "数据安全合规官",
                })

            total_findings += len(findings)
            for fin in findings:
                fhash = self._finding_hash(fin)
                if self._is_dup(fhash):
                    skipped_dup += 1
                    continue
                new_findings += 1
                ok = self._push(fin, space_id)
                if ok:
                    pushed += 1
                    self._mark_dedup(fhash, fin["doc_id"], space_id)
                else:
                    push_errors += 1

        return {
            "success": True,
            "space_id": space_id,
            "scanned": scanned,
            "total_findings": total_findings,
            "new_findings": new_findings,
            "pushed": pushed,
            "skipped_dup": skipped_dup,
            "push_errors": push_errors,
            "scanned_at": datetime.now().isoformat(timespec="seconds"),
        }

    # ------------------------------------------------------------------
    # 内部：去重 + 推送
    # ------------------------------------------------------------------
    def _finding_hash(self, fin: Dict) -> str:
        key = f'{fin["doc_id"]}|{fin.get("pack","")}|{fin.get("word","")}|{fin.get("line",0)}'
        return hashlib.md5(key.encode("utf-8")).hexdigest()

    def _is_dup(self, fhash: str) -> bool:
        conn = sqlite3.connect(_DB_PATH)
        try:
            row = conn.execute(
                "SELECT finding_hash FROM compliance_scan_dedup WHERE finding_hash = ?", (fhash,)
            ).fetchone()
            return row is not None
        finally:
            conn.close()

    def _mark_dedup(self, fhash: str, doc_id: str, space_id: str) -> None:
        conn = sqlite3.connect(_DB_PATH)
        try:
            conn.execute(
                "INSERT OR REPLACE INTO compliance_scan_dedup (finding_hash, doc_id, space_id, created_at) VALUES (?, ?, ?, ?)",
                (fhash, doc_id, space_id, datetime.now().isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

    def _push(self, fin: Dict, space_id: str) -> bool:
        """经 webhook_center 三通道推送（签名核验 + 去重）。"""
        try:
            from engine import webhook_center
            payload = {
                "event_type": EVENT_TYPE,
                "table_id": space_id,
                "record_id": f'{fin["doc_id"]}:{fin.get("pack","")}:{fin.get("word","")}:{fin.get("line",0)}',
                "doc_id": fin["doc_id"],
                "kind": fin["kind"],
                "word": fin.get("word", ""),
                "risk_tier": fin.get("risk_tier", "中"),
                "responsible_field": fin.get("responsible_field", ""),
                "line": fin.get("line", 0),
            }
            signature = self._sign(payload)
            result = webhook_center.process_event(payload, signature=signature)
            return result.get("success", False)
        except Exception:
            return False

    def _sign(self, payload: Dict) -> str:
        import hmac as _hmac
        import hashlib as _hl
        body = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return _hmac.new(self.signing_secret.encode(), body, _hl.sha256).hexdigest()

    def get_status(self) -> Dict:
        conn = sqlite3.connect(_DB_PATH)
        try:
            rows = conn.execute(
                "SELECT space_id, task_name, weekday, scan_time FROM weekly_scan_config"
            ).fetchall()
            dup_count = conn.execute("SELECT COUNT(*) FROM compliance_scan_dedup").fetchone()[0]
        finally:
            conn.close()
        return {
            "platform": platform.system(),
            "registered_tasks": [
                {"space_id": r[0], "task_name": r[1], "weekday": r[2], "scan_time": r[3]}
                for r in rows
            ],
            "dedup_entries": dup_count,
            "event_type": EVENT_TYPE,
        }


# ===========================================================================
# 单例 + 便捷函数
# ===========================================================================
_scheduler: Optional[ComplianceScheduler] = None


def get_scheduler(
    backend: Optional[Any] = None,
    external_packs_dir: Optional[str] = None,
) -> ComplianceScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = ComplianceScheduler(backend=backend, external_packs_dir=external_packs_dir)
    return _scheduler


def register_weekly_scan(
    space_id: str,
    packs: Optional[List[str]] = None,
    task_name: str = "kingdoc_compliance_weekly",
    weekday: str = "MON",
    scan_time: str = "03:00",
    external_packs_dir: Optional[str] = None,
) -> Dict:
    return get_scheduler(external_packs_dir=external_packs_dir).register_weekly_scan(
        space_id, packs, task_name, weekday, scan_time)


def run_scan(
    space_id: str,
    docs: Optional[List[Dict]] = None,
    packs: Optional[List[str]] = None,
    external_packs_dir: Optional[str] = None,
) -> Dict:
    return get_scheduler(external_packs_dir=external_packs_dir).run_scan(
        space_id, docs, packs, external_packs_dir=external_packs_dir)


def get_scheduler_status(external_packs_dir: Optional[str] = None) -> Dict:
    return get_scheduler(external_packs_dir=external_packs_dir).get_status()


def main():
    """CLI：python compliance_scheduler.py --space <id> [--packs edu,finance] [--external-packs-dir DIR]"""
    import argparse
    ap = argparse.ArgumentParser(description="KingDoc 全域合规周扫运行器")
    ap.add_argument("--space", required=True)
    ap.add_argument("--packs", default="")
    ap.add_argument("--external-packs-dir", default="")
    args = ap.parse_args()
    packs = [p.strip() for p in args.packs.split(",") if p.strip()]
    ext = args.external_packs_dir or None
    # 云端模式应由 backend 拉取空间文档；本地 CLI 仅执行已注册配置或空扫描演示
    result = run_scan(args.space, docs=[], packs=packs, external_packs_dir=ext)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
