import os
import time
import uuid

import lancedb
import pyarrow as pa

from config import get_config


VECTOR_DIM = 1024
TABLE_NAME = "memories"


def _ensure_parent(path: str):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def _schema():
    return pa.schema(
        [
            pa.field("id", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), VECTOR_DIM)),
            pa.field("text", pa.string()),
            pa.field("agent_id", pa.string()),
            pa.field("scene", pa.string()),
            pa.field("intent", pa.string()),
            pa.field("metadata_json", pa.string()),
            pa.field("created_at", pa.float64()),
            pa.field("weight", pa.float32()),
        ]
    )


def _esc(s: str) -> str:
    return (s or "").replace("'", "''")


class LanceDBManager:
    def __init__(self):
        cfg = get_config()
        path = (cfg.get("lancedb") or {}).get("path")
        _ensure_parent(path)
        self.db = lancedb.connect(path)
        self.table = self._open_or_create()

    def _open_or_create(self):
        if TABLE_NAME in self.db.table_names():
            tbl = self.db.open_table(TABLE_NAME)
            try:
                field = tbl.schema.field("vector")
                if isinstance(field.type, pa.FixedSizeListType) and field.type.list_size == VECTOR_DIM:
                    return tbl
            except Exception:
                pass
            self.db.drop_table(TABLE_NAME)
        init_row = {
            "id": "__init__",
            "vector": [0.0] * VECTOR_DIM,
            "text": "",
            "agent_id": "__init__",
            "scene": "__init__",
            "intent": "__init__",
            "metadata_json": "{}",
            "created_at": time.time(),
            "weight": 0.0,
        }
        tbl = self.db.create_table(TABLE_NAME, data=[init_row], schema=_schema(), mode="create")
        tbl.delete("id = '__init__'")
        return tbl

    def add(self, vector, text: str, agent_id: str, scene: str, intent: str, metadata_json: str = "{}", weight: float = 1.0):
        mid = str(uuid.uuid4())
        self.table.add(
            [
                {
                    "id": mid,
                    "vector": vector,
                    "text": text,
                    "agent_id": agent_id,
                    "scene": scene,
                    "intent": intent,
                    "metadata_json": metadata_json,
                    "created_at": time.time(),
                    "weight": float(weight),
                }
            ]
        )
        return mid

    def search(self, query_vector, agent_id: str, scene: str, limit: int):
        where = f"agent_id = '{_esc(agent_id)}' AND scene = '{_esc(scene)}'"
        rows = self.table.search(query_vector).where(where).limit(limit).to_list()
        out = []
        for r in rows:
            d = float(r.get("_distance", 0.0))
            out.append(
                {
                    "id": r.get("id"),
                    "text": r.get("text"),
                    "scene": r.get("scene"),
                    "intent": r.get("intent"),
                    "score": 1.0 / (1.0 + d),
                    "created_at": r.get("created_at"),
                }
            )
        return out

    def delete(self, memory_id: str):
        self.table.delete(f"id = '{_esc(memory_id)}'")
