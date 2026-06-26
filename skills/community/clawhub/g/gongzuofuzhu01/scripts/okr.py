"""
Personal Assistant Skill — OKR Management Module

OKR (Objectives & Key Results) management built on the Database layer.
Supports CRUD, progress tracking with upward propagation, Markdown sync
from Feishu documents, and task-OKR linking.
"""

from __future__ import annotations
import json
import re
from datetime import datetime

from .db import Database

class OKRManager:
    """Manage Objectives, Key Results, and Initiatives in the okr_items table."""

    def __init__(self, db: Database):
        """
        Args:
            db: An initialised Database instance.
        """
        self.db = db

    # ------------------------------------------------------------------
    # CRUD — Create
    # ------------------------------------------------------------------

    def add_objective(
        self,
        title: str,
        description: str = "",
        start_date: str = None,
        end_date: str = None,
        weight: float = 1.0,
    ) -> int:
        """Add an Objective to the top level.

        Returns:
            The id of the new Objective row.
        """
        return self.db.insert("okr_items", {
            "title": title,
            "description": description,
            "obj_type": "objective",
            "start_date": start_date,
            "end_date": end_date,
            "weight": weight,
            "parent_id": None,
        })

    def add_key_result(
        self,
        objective_id: int,
        title: str,
        description: str = "",
        weight: float = 1.0,
    ) -> int:
        """Add a Key Result under an Objective.

        Raises:
            ValueError: If *objective_id* does not reference an existing Objective.
        """
        obj = self.get(objective_id)
        if obj is None or obj["obj_type"] != "objective":
            raise ValueError(f"Objective with id={objective_id} not found")

        return self.db.insert("okr_items", {
            "title": title,
            "description": description,
            "obj_type": "key_result",
            "parent_id": objective_id,
            "weight": weight,
        })

    def add_initiative(
        self,
        kr_id: int,
        title: str,
        description: str = "",
    ) -> int:
        """Add an Initiative under a Key Result.

        Raises:
            ValueError: If *kr_id* does not reference an existing Key Result.
        """
        kr = self.get(kr_id)
        if kr is None or kr["obj_type"] != "key_result":
            raise ValueError(f"Key Result with id={kr_id} not found")

        return self.db.insert("okr_items", {
            "title": title,
            "description": description,
            "obj_type": "initiative",
            "parent_id": kr_id,
        })

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get(self, okr_id: int) -> dict | None:
        """Get a single OKR item by id."""
        return self.db.fetch_one(
            "SELECT * FROM okr_items WHERE id = ?", (okr_id,)
        )

    def list_objectives(self, status: str = "active") -> list[dict]:
        """List all Objectives, optionally filtered by status."""
        return self.db.fetch_all(
            "SELECT * FROM okr_items WHERE obj_type = 'objective' AND status = ? "
            "ORDER BY created_at",
            (status,),
        )

    def list_by_status(self, status: str) -> list[dict]:
        """List all OKR items (any type) with the given status."""
        return self.db.fetch_all(
            "SELECT * FROM okr_items WHERE status = ? ORDER BY obj_type, created_at",
            (status,),
        )

    def get_tree(self) -> list[dict]:
        """Return the full OKR tree: Objective → Key Results → Initiatives.

        Each Objective dict gains a ``key_results`` key (list of dicts),
        and each Key Result dict gains an ``initiatives`` key (list of dicts).
        """
        objectives = self.db.fetch_all(
            "SELECT * FROM okr_items WHERE obj_type = 'objective' ORDER BY created_at"
        )
        all_krs = self.db.fetch_all(
            "SELECT * FROM okr_items WHERE obj_type = 'key_result' ORDER BY created_at"
        )
        all_initiatives = self.db.fetch_all(
            "SELECT * FROM okr_items WHERE obj_type = 'initiative' ORDER BY created_at"
        )

        # Index KRs and Initiatives by parent_id
        kr_by_parent: dict[int, list[dict]] = {}
        for kr in all_krs:
            pid = kr["parent_id"]
            kr_by_parent.setdefault(pid, []).append(kr)

        ini_by_parent: dict[int, list[dict]] = {}
        for ini in all_initiatives:
            pid = ini["parent_id"]
            ini_by_parent.setdefault(pid, []).append(ini)

        # Assemble tree
        tree = []
        for obj in objectives:
            oid = obj["id"]
            krs = kr_by_parent.get(oid, [])
            for kr in krs:
                kr["initiatives"] = ini_by_parent.get(kr["id"], [])
            obj["key_results"] = krs
            tree.append(obj)

        return tree

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update_progress(self, okr_id: int, progress: int) -> None:
        """Update progress (0–100) for an OKR item.

        If the item is a Key Result, recalculate and propagate the
        average progress upward to its parent Objective.
        """
        if not (0 <= progress <= 100):
            raise ValueError("progress must be between 0 and 100")

        item = self.get(okr_id)
        if item is None:
            raise ValueError(f"OKR item with id={okr_id} not found")

        self.db.execute(
            "UPDATE okr_items SET progress = ?, updated_at = datetime('now','localtime') WHERE id = ?",
            (progress, okr_id),
        )

        # If this is a KR, propagate upward to its Objective
        if item["obj_type"] == "key_result" and item["parent_id"] is not None:
            self._sync_parent_progress(item["parent_id"])

    def _sync_parent_progress(self, objective_id: int) -> None:
        """Recalculate an Objective's progress as the average of its child KRs."""
        krs = self.db.fetch_all(
            "SELECT progress FROM okr_items WHERE parent_id = ? AND obj_type = 'key_result'",
            (objective_id,),
        )
        if krs:
            avg_progress = int(sum(kr["progress"] for kr in krs) / len(krs))
        else:
            avg_progress = 0

        self.db.execute(
            "UPDATE okr_items SET progress = ?, updated_at = datetime('now','localtime') WHERE id = ?",
            (avg_progress, objective_id),
        )

    def update_status(self, okr_id: int, status: str) -> None:
        """Set the status of an OKR item.

        Valid statuses: 'active', 'completed', 'cancelled'.
        """
        valid = {"active", "completed", "cancelled"}
        if status not in valid:
            raise ValueError(f"status must be one of {valid}, got '{status}'")

        item = self.get(okr_id)
        if item is None:
            raise ValueError(f"OKR item with id={okr_id} not found")

        self.db.execute(
            "UPDATE okr_items SET status = ?, updated_at = datetime('now','localtime') WHERE id = ?",
            (status, okr_id),
        )

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete(self, okr_id: int) -> None:
        """Delete an OKR item and all its descendants.

        Since the schema uses ON DELETE SET NULL on parent_id (not CASCADE),
        we manually cascade: find all descendants, delete leaves first,
        then delete the target itself.
        """
        item = self.get(okr_id)
        if item is None:
            return  # Idempotent — nothing to delete

        # Collect all descendant ids via BFS
        descendant_ids = []
        queue = [okr_id]
        while queue:
            current = queue.pop(0)
            children = self.db.fetch_all(
                "SELECT id FROM okr_items WHERE parent_id = ?", (current,)
            )
            for child in children:
                cid = child["id"]
                descendant_ids.append(cid)
                queue.append(cid)

        # Delete children first (from deepest to shallowest so FK
        # constraints are never violated)
        for cid in reversed(descendant_ids):
            self.db.delete("okr_items", "id = ?", (cid,))

        # Now delete the target itself
        self.db.delete("okr_items", "id = ?", (okr_id,))

    # ------------------------------------------------------------------
    # Sync from Feishu doc (Markdown)
    # ------------------------------------------------------------------

    def sync_from_doc(self, doc_token: str, doc_content: str) -> dict:
        """Parse Markdown content and sync OKR items to the local database.

        Parsing rules:
        - ``## ...`` (level‑2 heading) → Objective
        - ``### ...`` (level‑3 heading) → Key Result (child of most recent Objective)
        - ``#### ...`` (level‑4 heading) → Initiative (child of most recent KR)
        - ``进度: XX%`` or ``progress: XX%`` → progress value on the current item

        Existing items are matched by *(title, parent_id)* within the same
        *doc_token*.  Items in the database for this *doc_token* that do
        NOT appear in the new content are marked ``completed``.

        Args:
            doc_token: The Feishu document token (stored in source_doc_token).
            doc_content: Markdown string to parse.

        Returns:
            A dict with keys ``added``, ``updated``, ``removed`` (counts).
        """
        parsed_items = self._parse_markdown_okr(doc_content)
        counts = {"added": 0, "updated": 0, "removed": 0}

        # Existing items for this doc_token
        existing = self.db.fetch_all(
            "SELECT * FROM okr_items WHERE source_doc_token = ?", (doc_token,)
        )
        # Build a set of (title, parent_id) pairs for existing items
        existing_pairs: set[tuple[str, int]] = set()
        existing_id_map: dict[tuple[str, int], int] = {}
        for row in existing:
            pair = (row["title"], row["parent_id"])
            existing_pairs.add(pair)
            existing_id_map[pair] = row["id"]

        # Build a staging list ordered by type (objectives first, then KRs, then initiatives)
        staged_objectives = [i for i in parsed_items if i["obj_type"] == "objective"]
        staged_krs = [i for i in parsed_items if i["obj_type"] == "key_result"]
        staged_initiatives = [i for i in parsed_items if i["obj_type"] == "initiative"]

        # Track doc-level parent index → real database id
        doc_idx_to_db_id: dict[int, int] = {}

        # Track which (title, real_parent_id) pairs are covered by the new content
        new_pairs: set[tuple[str, int]] = set()

        # --- Pass 1: Objectives ---
        for item in staged_objectives:
            pair = (item["title"], None)
            db_id = self._upsert_okr_item(
                doc_token=doc_token,
                existing_id_map=existing_id_map,
                item=item,
                pair=pair,
                parent_id=None,
            )
            doc_idx_to_db_id[item["_doc_index"]] = db_id
            new_pairs.add(pair)

            if pair in existing_pairs:
                counts["updated"] += 1
            else:
                counts["added"] += 1

        # --- Pass 2: Key Results ---
        for item in staged_krs:
            parent_db_id = doc_idx_to_db_id.get(item["_doc_parent_index"])
            pair = (item["title"], parent_db_id)
            db_id = self._upsert_okr_item(
                doc_token=doc_token,
                existing_id_map=existing_id_map,
                item=item,
                pair=pair,
                parent_id=parent_db_id,
            )
            doc_idx_to_db_id[item["_doc_index"]] = db_id
            new_pairs.add(pair)

            if pair in existing_pairs:
                counts["updated"] += 1
            else:
                counts["added"] += 1

        # --- Pass 3: Initiatives ---
        for item in staged_initiatives:
            parent_db_id = doc_idx_to_db_id.get(item["_doc_parent_index"])
            pair = (item["title"], parent_db_id)
            db_id = self._upsert_okr_item(
                doc_token=doc_token,
                existing_id_map=existing_id_map,
                item=item,
                pair=pair,
                parent_id=parent_db_id,
            )
            doc_idx_to_db_id[item["_doc_index"]] = db_id
            new_pairs.add(pair)

            if pair in existing_pairs:
                counts["updated"] += 1
            else:
                counts["added"] += 1

        # --- Mark removed items as completed ---
        for pair, item_id in existing_id_map.items():
            if pair not in new_pairs:
                self.db.execute(
                    "UPDATE okr_items SET status = 'completed', updated_at = datetime('now','localtime') WHERE id = ?",
                    (item_id,),
                )
                counts["removed"] += 1

        return counts

    # ------------------------------------------------------------------
    # Sync from Feishu Bitable
    # ------------------------------------------------------------------

    def sync_from_bitable(self, period: str, records: list[dict]) -> dict:
        """Sync OKR items from bitable records into local SQLite.

        Uses ``_upsert_okr_item()`` for each Objective and Key Result.
        Matching key: *(title, parent_id, source_doc_token)* where
        ``source_doc_token = f"bitable:{period}"``.

        Args:
            period: Period identifier (e.g. ``"2026H1"``).
            records: Raw bitable record list as returned by the Feishu API.
                      Each record must contain a ``"fields"`` dict keyed
                      by field_id.

        Returns:
            A dict with keys ``added``, ``updated``, ``removed``,
            ``objectives``, ``key_results``.
        """
        from .okr_sync_bitable import parse_bitable_rows

        source_token = f"bitable:{period}"
        counts = {"added": 0, "updated": 0, "removed": 0,
                  "objectives": 0, "key_results": 0}

        # Parse structured O→KR hierarchy from flat bitable rows
        structured = parse_bitable_rows(records)
        counts["objectives"] = len(structured)

        # Existing items for this source_doc_token
        existing = self.db.fetch_all(
            "SELECT * FROM okr_items WHERE source_doc_token = ?",
            (source_token,),
        )
        existing_id_map: dict[tuple[str, int], int] = {}
        for row in existing:
            pair = (row["title"], row["parent_id"])
            existing_id_map[pair] = row["id"]

        # Track which (title, real_parent_id) pairs are covered by new data
        new_pairs: set[tuple[str, int]] = set()

        # --- Pass 1: Upsert all Objectives ---
        title_to_db_id: dict[str, int] = {}
        for o in structured:
            o_title = o["title"]
            pair = (o_title, None)
            item = {
                "title": o_title,
                "description": "",
                "obj_type": "objective",
                "progress": o.get("progress", 0),
                "extra": o.get("extra", {}),
            }
            db_id = self._upsert_okr_item(
                doc_token=source_token,
                existing_id_map=existing_id_map,
                item=item,
                pair=pair,
                parent_id=None,
            )
            title_to_db_id[o_title] = db_id
            new_pairs.add(pair)

            if pair in existing_id_map:
                counts["updated"] += 1
            else:
                counts["added"] += 1

            # Update status for the Objective
            obj_status = o.get("status", "active")
            self.db.execute(
                "UPDATE okr_items SET status = ?, updated_at = datetime('now','localtime') WHERE id = ?",
                (obj_status, db_id),
            )

        # --- Pass 2: Upsert all Key Results ---
        for o in structured:
            parent_db_id = title_to_db_id.get(o["title"])
            if parent_db_id is None:
                continue
            for kr in o.get("key_results", []):
                kr_title = kr["title"]
                pair = (kr_title, parent_db_id)
                counts["key_results"] += 1

                # Build description from extra fields for completeness
                desc_parts = []
                weight = kr.get("weight")
                if weight:
                    desc_parts.append(f"权重: {weight}%")
                extra = kr.get("extra", {})
                if extra.get("owner"):
                    desc_parts.append(f"负责人: {extra['owner']}")

                item = {
                    "title": kr_title,
                    "description": "; ".join(desc_parts),
                    "obj_type": "key_result",
                    "progress": kr.get("progress", 0),
                    "extra": kr.get("extra", {}),
                }
                db_id = self._upsert_okr_item(
                    doc_token=source_token,
                    existing_id_map=existing_id_map,
                    item=item,
                    pair=pair,
                    parent_id=parent_db_id,
                )
                new_pairs.add(pair)

                if pair in existing_id_map:
                    counts["updated"] += 1
                else:
                    counts["added"] += 1

                # Update status and weight for the KR
                kr_status = kr.get("status", "active")
                self.db.execute(
                    "UPDATE okr_items SET status = ?, weight = ?, updated_at = datetime('now','localtime') WHERE id = ?",
                    (kr_status, weight or 0, db_id),
                )

                # NOTE: O progress uses raw bitable completion value (set in Pass 1).
                # We intentionally do NOT call _sync_parent_progress() here to avoid
                # overwriting the source-of-truth value with a KR average.

        # --- Mark removed items as completed ---
        for pair, item_id in existing_id_map.items():
            if pair not in new_pairs:
                self.db.execute(
                    "UPDATE okr_items SET status = 'completed', updated_at = datetime('now','localtime') WHERE id = ?",
                    (item_id,),
                )
                counts["removed"] += 1

        return counts

    def _upsert_okr_item(
        self,
        doc_token: str,
        existing_id_map: dict,
        item: dict,
        pair: tuple,
        parent_id: int | None,
    ) -> int:
        """Insert or update a single OKR item during sync.

        Returns the database id of the item.
        """
        now = datetime.now().isoformat()
        extra_json = json.dumps(item.get("extra", {}), ensure_ascii=False)
        if pair in existing_id_map:
            # Update
            db_id = existing_id_map[pair]
            self.db.execute(
                "UPDATE okr_items SET description = ?, progress = ?, extra = ?, synced_at = ?, updated_at = datetime('now','localtime') WHERE id = ?",
                (item.get("description", ""), item.get("progress", 0), extra_json, now, db_id),
            )
        else:
            # Insert
            db_id = self.db.insert("okr_items", {
                "title": item["title"],
                "description": item.get("description", ""),
                "obj_type": item["obj_type"],
                "parent_id": parent_id,
                "progress": item.get("progress", 0),
                "extra": extra_json,
                "source_doc_token": doc_token,
                "synced_at": now,
            })
        return db_id

    def _parse_markdown_okr(self, doc_content: str) -> list[dict]:
        """Parse Markdown content into a flat list of OKR item dicts.

        Each dict has:
            title, description, obj_type, progress, _doc_index, _doc_parent_index
        """
        items = []
        # Stack: list of (level, doc_index) — the nesting path
        # level 2 = ##, level 3 = ###, level 4 = ####
        heading_stack: list[tuple[int, int]] = []  # (heading_level, doc_index)

        # Split content into blocks: heading lines + their body text
        # We parse line by line
        lines = doc_content.split("\n")
        current_item = None  # dict being built
        body_lines: list[str] = []

        def _flush_item():
            nonlocal current_item, body_lines
            if current_item is not None:
                body_text = "\n".join(body_lines).strip()
                current_item["description"] = body_text

                # Extract progress from body
                progress = self._extract_progress(body_text)
                current_item["progress"] = progress

                items.append(current_item)
                current_item = None
                body_lines = []

        idx_counter = 0

        for line in lines:
            heading_match = re.match(r"^(#{2,4})\s+(.+)", line)
            if heading_match:
                _flush_item()

                hashes = heading_match.group(1)
                title = heading_match.group(2).strip()
                level = len(hashes)  # 2, 3, or 4

                # Map markdown heading level to OKR type
                type_map = {2: "objective", 3: "key_result", 4: "initiative"}
                obj_type = type_map.get(level)
                if obj_type is None:
                    continue  # Ignore other levels

                # Pop stack until we find a parent at a shallower level
                while heading_stack and heading_stack[-1][0] >= level:
                    heading_stack.pop()

                parent_index = heading_stack[-1][1] if heading_stack else None

                doc_index = idx_counter
                idx_counter += 1
                heading_stack.append((level, doc_index))

                current_item = {
                    "title": title,
                    "obj_type": obj_type,
                    "_doc_index": doc_index,
                    "_doc_parent_index": parent_index,
                }
                body_lines = []
            else:
                body_lines.append(line)

        _flush_item()
        return items

    @staticmethod
    def _extract_progress(text: str) -> int:
        """Extract progress percentage from text using known patterns.

        Supports:
        - ``进度: 75%``
        - ``progress: 60%``
        - ``进度 75%``
        - ``Progress 60%``
        - ``(75%)`` at end of line
        """
        patterns = [
            r"(?:进度|progress)\s*[:：]?\s*(\d{1,3})\s*%",
            r"\((\d{1,3})\s*%\)\s*$",
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                val = int(m.group(1))
                return min(max(val, 0), 100)
        return 0

    # ------------------------------------------------------------------
    # Task linking
    # ------------------------------------------------------------------

    def link_task(self, okr_id: int, task_id: int) -> None:
        """Associate a task with an OKR item.

        Sets the *okr_id* column on the task row.
        """
        self.db.update(
            "tasks",
            {"okr_id": okr_id},
            "id = ?",
            (task_id,),
        )

    def unlink_task(self, task_id: int) -> None:
        """Remove OKR association from a task."""
        self.db.update(
            "tasks",
            {"okr_id": None},
            "id = ?",
            (task_id,),
        )

    def get_linked_tasks(self, okr_id: int) -> list[dict]:
        """Return all tasks linked to a specific OKR item."""
        return self.db.fetch_all(
            "SELECT * FROM tasks WHERE okr_id = ?", (okr_id,)
        )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def progress_summary(self) -> dict:
        """Return an OKR progress summary.

        Returns a dict with:
        - ``total_objectives``: count
        - ``total_key_results``: count
        - ``total_initiatives``: count
        - ``objectives``: list of dicts, each with:
            id, title, status, progress, key_results (list of dicts with
            id, title, progress, linked_task_count)
        """
        tree = self.get_tree()

        total_krs = 0
        total_inis = 0
        objective_summaries = []

        for obj in tree:
            krs = obj.get("key_results", [])
            total_krs += len(krs)

            kr_summaries = []
            for kr in krs:
                inis = kr.get("initiatives", [])
                total_inis += len(inis)
                linked_tasks = self.get_linked_tasks(kr["id"])
                kr_summaries.append({
                    "id": kr["id"],
                    "title": kr["title"],
                    "progress": kr["progress"],
                    "status": kr["status"],
                    "linked_task_count": len(linked_tasks),
                })

            objective_summaries.append({
                "id": obj["id"],
                "title": obj["title"],
                "status": obj["status"],
                "progress": obj["progress"],
                "key_results": kr_summaries,
            })

        return {
            "total_objectives": len(tree),
            "total_key_results": total_krs,
            "total_initiatives": total_inis,
            "objectives": objective_summaries,
        }
