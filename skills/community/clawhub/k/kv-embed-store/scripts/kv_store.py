#!/usr/bin/env python3
"""Key-embedding value store with multi-alias support and auto-deduplication."""

import argparse
import json
import os
import sys
import time
from typing import Optional

import numpy as np
import requests


def get_api_key() -> str:
    """Resolve API key from env or common locations."""
    key = os.environ.get("SILICONFLOW_API_KEY")
    if key:
        return key
    # Try reading from file
    keyfile = os.path.expanduser("/userdata/硅基流动api-key")
    if os.path.exists(keyfile):
        return open(keyfile).read().strip()
    raise RuntimeError(
        "SILICONFLOW_API_KEY not set. Set env var or place key at /userdata/硅基流动api-key"
    )


BASE_URL = os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
MODEL = os.environ.get("EMBED_MODEL", "BAAI/bge-m3")
DEFAULT_THRESHOLD = 0.85


def embed(texts: list[str], api_key: str) -> np.ndarray:
    """Get embeddings from SiliconFlow API."""
    resp = requests.post(
        f"{BASE_URL}/embeddings",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": MODEL, "input": texts, "encoding_format": "float"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    embeddings = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
    return np.array(embeddings, dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Cosine similarity between a (n,d) and b (m,d). Returns (n,m)."""
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return a_norm @ b_norm.T


class KVEmbedStore:
    def __init__(self, path: str, threshold: float = DEFAULT_THRESHOLD):
        self.path = path
        self.threshold = threshold
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path) as f:
                d = json.load(f)
            # Convert embeddings back to numpy
            for key, vec in d.get("embeddings", {}).items():
                d["embeddings"][key] = np.array(vec, dtype=np.float32)
            return d
        return {"entries": {}, "embeddings": {}, "config": {}}

    def _save(self):
        d = {
            "entries": self.data["entries"],
            "embeddings": {k: v.tolist() for k, v in self.data["embeddings"].items()},
            "config": {"threshold": self.threshold, "model": MODEL},
        }
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)

    @property
    def api_key(self) -> str:
        return get_api_key()

    def _next_id(self) -> str:
        existing = [int(k[1:]) for k in self.data["entries"] if k.startswith("e")]
        return f"e{max(existing, default=0) + 1}"

    def _search_keys(self, query_vec: np.ndarray, top_k: int = 10) -> list[dict]:
        """Search keys by embedding similarity. Returns [{key, score}, ...]."""
        if not self.data["embeddings"]:
            return []
        keys = list(self.data["embeddings"].keys())
        vecs = np.stack([self.data["embeddings"][k] for k in keys])
        sims = cosine_similarity(query_vec.reshape(1, -1), vecs)[0]
        indices = np.argsort(sims)[::-1][:top_k]
        return [{"key": keys[i], "score": float(sims[i])} for i in indices]

    def put(self, key: str, value: any, force: bool = False) -> dict:
        """Insert or update a key-value pair with auto-dedup."""
        # Embed the key
        key_vec = embed([key], self.api_key)[0]

        if not force and self.data["embeddings"]:
            # Search for existing similar keys
            candidates = self._search_keys(key_vec, top_k=5)
            best = candidates[0] if candidates else None

            if best and best["score"] >= 0.95:
                # Auto-merge: add alias to existing entry
                entry_id = self._entry_id_for_key(best["key"])
                if entry_id:
                    entry = self.data["entries"][entry_id]
                    if key not in entry["aliases"]:
                        entry["aliases"].append(key)
                    entry["data"] = value
                    entry["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                    self.data["embeddings"][key] = key_vec
                    self._save()
                    return {
                        "action": "merged",
                        "entry_id": entry_id,
                        "matched_key": best["key"],
                        "score": best["score"],
                        "aliases": entry["aliases"],
                    }
            elif best and best["score"] >= self.threshold:
                # Ambiguous: return candidates for caller to decide
                candidates_with_entries = []
                for c in candidates:
                    if c["score"] >= self.threshold:
                        eid = self._entry_id_for_key(c["key"])
                        if eid:
                            candidates_with_entries.append({
                                **c,
                                "entry_id": eid,
                                "aliases": self.data["entries"][eid]["aliases"],
                            })
                if candidates_with_entries:
                    return {
                        "action": "ambiguous",
                        "key": key,
                        "candidates": candidates_with_entries,
                        "hint": "Use --force to create new, or 'merge' command to merge",
                    }

        # Create new entry
        entry_id = self._next_id()
        self.data["entries"][entry_id] = {
            "aliases": [key],
            "data": value,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self.data["embeddings"][key] = key_vec
        self._save()
        return {"action": "created", "entry_id": entry_id, "aliases": [key]}

    def _entry_id_for_key(self, key: str) -> Optional[str]:
        for eid, entry in self.data["entries"].items():
            if key in entry["aliases"]:
                return eid
        return None

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search by embedding similarity, return entries."""
        query_vec = embed([query], self.api_key)[0]
        candidates = self._search_keys(query_vec, top_k=max(top_k * 3, 10))
        seen = set()
        results = []
        for c in candidates:
            eid = self._entry_id_for_key(c["key"])
            if eid and eid not in seen:
                seen.add(eid)
                entry = self.data["entries"][eid]
                results.append({
                    "entry_id": eid,
                    "score": c["score"],
                    "matched_key": c["key"],
                    "aliases": entry["aliases"],
                    "data": entry["data"],
                    "updated_at": entry.get("updated_at", entry.get("created_at")),
                })
                if len(results) >= top_k:
                    break
        return results

    def get(self, key: str) -> Optional[dict]:
        """Exact key lookup."""
        eid = self._entry_id_for_key(key)
        if eid:
            entry = self.data["entries"][eid]
            return {
                "entry_id": eid,
                "aliases": entry["aliases"],
                "data": entry["data"],
                "updated_at": entry.get("updated_at", entry.get("created_at")),
            }
        return None

    def list_keys(self) -> list[dict]:
        """List all entries with their aliases."""
        return [
            {
                "entry_id": eid,
                "aliases": entry["aliases"],
                "updated_at": entry.get("updated_at", entry.get("created_at")),
                "data_preview": str(entry["data"])[:80],
            }
            for eid, entry in self.data["entries"].items()
        ]

    def remove(self, key: str) -> dict:
        """Remove a key-alias. Removes entry only if no aliases left."""
        eid = self._entry_id_for_key(key)
        if not eid:
            return {"error": f"Key '{key}' not found"}
        entry = self.data["entries"][eid]
        if key in entry["aliases"]:
            entry["aliases"].remove(key)
        if key in self.data["embeddings"]:
            del self.data["embeddings"][key]

        if not entry["aliases"]:
            del self.data["entries"][eid]
            self._save()
            return {"action": "deleted_entry", "entry_id": eid}

        self._save()
        return {
            "action": "removed_alias",
            "entry_id": eid,
            "removed_key": key,
            "remaining_aliases": entry["aliases"],
        }

    def merge(self, key_a: str, key_b: str) -> dict:
        """Merge two entries by their keys. key_b's aliases and embedding move to key_a's entry."""
        eid_a = self._entry_id_for_key(key_a)
        eid_b = self._entry_id_for_key(key_b)
        if not eid_a:
            return {"error": f"Key '{key_a}' not found"}
        if not eid_b:
            return {"error": f"Key '{key_b}' not found"}
        if eid_a == eid_b:
            return {"error": "Keys already in same entry"}

        entry_a = self.data["entries"][eid_a]
        entry_b = self.data["entries"][eid_b]

        # Move aliases
        entry_a["aliases"].extend(entry_b["aliases"])
        # Move embeddings (re-key to entry_a)
        for alias in entry_b["aliases"]:
            if alias in self.data["embeddings"]:
                # No-op, embeddings stay keyed by alias text
                pass
        # Remove merged entry
        del self.data["entries"][eid_b]
        entry_a["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        self._save()
        return {
            "action": "merged",
            "target_entry": eid_a,
            "merged_entry": eid_b,
            "aliases": entry_a["aliases"],
        }

    def dedup(self, threshold: Optional[float] = None, apply: bool = False) -> list[dict]:
        """Full scan for duplicate entries. Returns merge suggestions."""
        if threshold is None:
            threshold = self.threshold
        suggestions = []
        entry_ids = list(self.data["entries"].keys())
        for i in range(len(entry_ids)):
            for j in range(i + 1, len(entry_ids)):
                eid_a, eid_b = entry_ids[i], entry_ids[j]
                entry_a = self.data["entries"][eid_a]
                entry_b = self.data["entries"][eid_b]
                # Compare first alias embeddings
                ka = entry_a["aliases"][0]
                kb = entry_b["aliases"][0]
                if ka not in self.data["embeddings"] or kb not in self.data["embeddings"]:
                    continue
                va = self.data["embeddings"][ka]
                vb = self.data["embeddings"][kb]
                sim = float(cosine_similarity(va.reshape(1, -1), vb.reshape(1, -1))[0][0])
                if sim >= threshold:
                    suggestions.append({
                        "entry_a": eid_a,
                        "entry_b": eid_b,
                        "key_a": ka,
                        "key_b": kb,
                        "score": sim,
                    })
                    if apply:
                        self.merge(ka, kb)
        if apply:
            self._save()
        return suggestions


def main():
    parser = argparse.ArgumentParser(description="Key-embedding value store")
    parser.add_argument("--store", default="data/kv_store.json", help="Store file path")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    sub = parser.add_subparsers(dest="command", required=True)

    # put
    p = sub.add_parser("put")
    p.add_argument("key")
    p.add_argument("value", help="JSON value string")
    p.add_argument("--force", action="store_true")

    # search
    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("-k", "--top-k", type=int, default=5)

    # get
    p = sub.add_parser("get")
    p.add_argument("key")

    # list
    sub.add_parser("list")

    # remove
    p = sub.add_parser("remove")
    p.add_argument("key")

    # merge
    p = sub.add_parser("merge")
    p.add_argument("key_a")
    p.add_argument("key_b")

    # dedup
    p = sub.add_parser("dedup")
    p.add_argument("--apply", action="store_true")

    args = parser.parse_args()
    store = KVEmbedStore(args.store, threshold=args.threshold)

    if args.command == "put":
        try:
            value = json.loads(args.value)
        except json.JSONDecodeError:
            value = args.value
        result = store.put(args.key, value, force=args.force)
    elif args.command == "search":
        result = store.search(args.query, top_k=args.top_k)
    elif args.command == "get":
        result = store.get(args.key)
        if result is None:
            print(json.dumps({"error": f"Key '{args.key}' not found"}, ensure_ascii=False))
            sys.exit(1)
    elif args.command == "list":
        result = store.list_keys()
    elif args.command == "remove":
        result = store.remove(args.key)
    elif args.command == "merge":
        result = store.merge(args.key_a, args.key_b)
    elif args.command == "dedup":
        result = store.dedup(apply=args.apply)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
