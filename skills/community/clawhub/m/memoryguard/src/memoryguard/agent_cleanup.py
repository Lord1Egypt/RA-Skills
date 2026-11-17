"""v3.2 Agent 残留清理：标记 / 归档 / 恢复 / 历史。

安全边界：
- 不提供删除按钮
- 归档是移动到 .memoryguard/cleanup/archived-agents/，可恢复
- 标记卸载只是写入 uninstalled.json，扫描时跳过
- 所有操作写入 ledger.jsonl
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schema_v3 import stable_hash


class AgentCleanup:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.root = self.workspace / ".memoryguard" / "cleanup"
        self.ledger_path = self.root / "ledger.jsonl"
        self.uninstalled_path = self.root / "uninstalled.json"
        self.archived_dir = self.root / "archived-agents"

    def _ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.archived_dir.mkdir(parents=True, exist_ok=True)

    def mark_uninstalled(self, product: str, dir_path: str = "",
                         reason: str = "") -> dict[str, Any]:
        """标记产品为已卸载。后续扫描会跳过。"""
        self._ensure_dirs()
        data = {"products": []}
        if self.uninstalled_path.exists():
            try:
                data = json.loads(self.uninstalled_path.read_text(encoding="utf-8"))
            except ValueError:
                data = {"products": []}
        products = set(data.get("products", []))
        products.add(product)
        data["products"] = sorted(products)
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.uninstalled_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_ledger("mark_uninstalled", product, dir_path, reason, {})
        return {"ok": True, "product": product, "marked_uninstalled": True}

    def unmark_uninstalled(self, product: str) -> dict[str, Any]:
        """取消已卸载标记。"""
        self._ensure_dirs()
        if not self.uninstalled_path.exists():
            return {"ok": True, "product": product, "marked_uninstalled": False}
        data = json.loads(self.uninstalled_path.read_text(encoding="utf-8"))
        products = set(data.get("products", []))
        products.discard(product)
        data["products"] = sorted(products)
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.uninstalled_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_ledger("unmark_uninstalled", product, "", "", {})
        return {"ok": True, "product": product, "marked_uninstalled": False}

    def archive_agent_dir(self, product: str, dir_path: str,
                          reason: str = "") -> dict[str, Any]:
        """归档 Agent 目录：移动到 .memoryguard/cleanup/archived-agents/。

        可恢复。不删除。
        """
        self._ensure_dirs()
        src = Path(dir_path)
        if not src.exists():
            return {"error": f"dir not found: {dir_path}"}
        archive_id = stable_hash("archive", product, str(src), datetime.now(timezone.utc).isoformat())
        dest = self.archived_dir / archive_id / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        manifest = {
            "archive_id": archive_id,
            "product": product,
            "original_path": str(src),
            "archived_path": str(dest),
            "archived_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
        }
        manifest_path = self.archived_dir / archive_id / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_ledger("archive", product, str(src), reason, {
            "archive_id": archive_id,
            "archived_path": str(dest),
        })
        return {"ok": True, "archive_id": archive_id, "manifest": manifest}

    def restore_archived(self, archive_id: str) -> dict[str, Any]:
        """从归档恢复 Agent 目录到原位置。"""
        archive_root = self.archived_dir / archive_id
        manifest_path = archive_root / "manifest.json"
        if not manifest_path.exists():
            return {"error": f"archive not found: {archive_id}"}
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        archived_path = Path(manifest["archived_path"])
        original_path = Path(manifest["original_path"])
        if original_path.exists():
            return {"error": f"original path already exists: {original_path}"}
        original_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(archived_path), str(original_path))
        manifest["restored_at"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_ledger("restore", manifest["product"], str(original_path), "", {
            "archive_id": archive_id,
        })
        return {"ok": True, "archive_id": archive_id, "restored_to": str(original_path)}

    def list_archives(self) -> list[dict[str, Any]]:
        """列出所有归档。"""
        if not self.archived_dir.exists():
            return []
        archives = []
        for sub in self.archived_dir.iterdir():
            if not sub.is_dir():
                continue
            manifest_path = sub / "manifest.json"
            if not manifest_path.exists():
                continue
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                archives.append(manifest)
            except ValueError:
                continue
        return archives

    def list_cleanup_history(self) -> list[dict[str, Any]]:
        """读取 cleanup ledger。"""
        if not self.ledger_path.exists():
            return []
        history = []
        for line in self.ledger_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                history.append(json.loads(line))
            except ValueError:
                continue
        return history

    def _append_ledger(self, action: str, product: str, dir_path: str,
                       reason: str, detail: dict[str, Any]) -> None:
        self._ensure_dirs()
        event = {
            "event_id": stable_hash("cleanup_event", action, product, dir_path,
                                     datetime.now(timezone.utc).isoformat()),
            "action": action,
            "product": product,
            "dir_path": dir_path,
            "reason": reason,
            "detail": dict(detail),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
