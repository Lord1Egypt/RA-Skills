"""JSON repository wrapper around meta.json persistence."""

from __future__ import annotations

import hashlib
import json
import os
from copy import deepcopy

from mg_events.telemetry import record_module_run
from mg_schema import normalize_meta
from mg_utils import load_meta, save_meta, file_lock_acquire


def _hash_meta(meta):
    payload = json.dumps(meta, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()


class MetaJsonRepository:
    """Single write boundary for meta.json-backed workflows."""

    def __init__(self, meta_path, workspace=None, dry_run=False):
        self.meta_path = meta_path
        self.workspace = workspace or self._derive_workspace(meta_path)
        self.dry_run = dry_run

    @staticmethod
    def _derive_workspace(meta_path):
        memory_dir = os.path.dirname(meta_path)
        return os.path.dirname(memory_dir) if os.path.basename(memory_dir) == "memory" else memory_dir

    def load_meta(self, persist=False, _locked=False):
        meta = load_meta(self.meta_path)
        normalized, changed = normalize_meta(meta)
        if persist and changed and not self.dry_run:
            save_meta(self.meta_path, normalized, use_lock=not _locked)
        return normalized

    def save_meta(self, meta, _locked=False):
        normalized, _ = normalize_meta(meta)
        if not self.dry_run:
            save_meta(self.meta_path, normalized, use_lock=not _locked)
        return normalized

    def mutate_meta(self, mutator, context=None):
        with file_lock_acquire(self.meta_path):
            before = self.load_meta(persist=True, _locked=True)
            working = deepcopy(before)
            result = mutator(working)
            after, _ = normalize_meta(working)
            before_hash = _hash_meta(before)
            after_hash = _hash_meta(after)
            changed = before_hash != after_hash
            if changed and not self.dry_run:
                save_meta(self.meta_path, after, use_lock=False)
        return {
            "meta": after,
            "changed": changed,
            "dry_run": self.dry_run,
            "before_hash": before_hash,
            "after_hash": after_hash,
            "context": context or {},
            "result": result,
        }

    def append_event(self, event, context=None):
        payload = deepcopy(event)

        def mutator(meta):
            meta.setdefault("event_log", []).append(payload)
            return payload

        outcome = self.mutate_meta(mutator, context=context)
        return outcome["result"]

    def record_hit(self, module_name, input_count=0, output_count=0, hit=None):
        if not self.workspace:
            return None
        return record_module_run(
            self.workspace,
            module_name,
            input_count=input_count,
            output_count=output_count,
            hit=hit,
        )
