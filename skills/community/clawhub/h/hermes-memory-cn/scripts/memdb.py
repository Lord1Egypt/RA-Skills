#!/opt/homebrew/bin/python3.12
"""记忆数据库 - SQLite + sqlite-vec 向量搜索 + FTS5 全文索引
Embedding: shibing624/text2vec-base-chinese (768维, 中文语义模型)
"""

import argparse
import json
import os
import re
import sys
import time
try:
    from pysqlite3 import dbapi2 as sqlite3
except ImportError:
    import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

import numpy as np

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.db")
VEC_DIM = 768

# 本地模型路径（通过curl从hf-mirror.com下载）
_MODEL_PATH = "/Users/dream/.cache/huggingface/hub/models--shibing624--text2vec-base-chinese/snapshots/local"
_model = None


def _get_model():
    global _model
    if _model is None:
        print("⏳ 正在加载 embedding 模型...", file=sys.stderr)
        t0 = time.time()
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(_MODEL_PATH)
        print(f"✅ 模型加载完成 ({time.time()-t0:.1f}s), 维度={_model.get_embedding_dimension()}", file=sys.stderr)
    return _model


def embed(text: str) -> bytes:
    """使用 text2vec-base-chinese 生成 768 维语义向量"""
    model = _get_model()
    vec = model.encode([text], normalize_embeddings=True, show_progress_bar=False)
    return vec[0].astype(np.float32).tobytes()


def embed_batch(texts: List[str]) -> List[bytes]:
    """批量生成向量"""
    model = _get_model()
    vecs = model.encode(texts, normalize_embeddings=True, show_progress_bar=len(texts) > 10,
                        batch_size=64)
    return [v.astype(np.float32).tobytes() for v in vecs]


def cosine_sim(a: bytes, b: bytes) -> float:
    va = np.frombuffer(a, dtype=np.float32)
    vb = np.frombuffer(b, dtype=np.float32)
    return float(np.dot(va, vb))


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    import sqlite_vec
    sqlite_vec.load(conn)
    _init_db(conn)
    return conn


def _init_db(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            type TEXT,
            entity TEXT,
            status TEXT DEFAULT 'active',
            severity TEXT,
            source TEXT DEFAULT 'manual',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME,
            metadata JSON
        )
    """)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            content, entity,
            content='memories',
            content_rowid='id'
        )
    """)
    conn.execute(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_vec USING vec0(
            id INTEGER PRIMARY KEY,
            embedding float[{VEC_DIM}]
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_entity TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            to_entity TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(from_entity, relation_type, to_entity)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_relations_from ON relations(from_entity)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_relations_to ON relations(to_entity)")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            type TEXT,
            entity TEXT,
            status TEXT DEFAULT 'archived',
            severity TEXT,
            source TEXT,
            created_at DATETIME,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            metadata JSON
        )
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS mem_insert_fts AFTER INSERT ON memories BEGIN
            INSERT INTO memories_fts(rowid, content, entity) VALUES (new.id, new.content, COALESCE(new.entity, ''));
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS mem_delete_fts AFTER DELETE ON memories BEGIN
            INSERT INTO memories_fts(memories_fts, rowid, content, entity) VALUES('delete', old.id, old.content, COALESCE(old.entity, ''));
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS mem_update_fts AFTER UPDATE ON memories BEGIN
            INSERT INTO memories_fts(memories_fts, rowid, content, entity) VALUES('delete', old.id, old.content, COALESCE(old.entity, ''));
            INSERT INTO memories_fts(rowid, content, entity) VALUES (new.id, new.content, COALESCE(new.entity, ''));
        END
    """)
    conn.commit()


class MemDB:
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        self.conn = conn or get_conn()

    def add(self, content: str, type: Optional[str] = None, entity: Optional[str] = None,
            severity: Optional[str] = None, source: str = "manual",
            expires_at: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> int:
        """添加记忆，自动去重（相似度>0.95则更新）"""
        vec = embed(content)

        rows = self.conn.execute("SELECT id, embedding FROM memories_vec").fetchall()
        for row_id, emb_bytes in rows:
            if emb_bytes and cosine_sim(vec, emb_bytes) > 0.95:
                self.conn.execute("""
                    UPDATE memories SET content=?, updated_at=CURRENT_TIMESTAMP, type=COALESCE(?,type),
                    entity=COALESCE(?,entity), severity=COALESCE(?,severity)
                    WHERE id=?
                """, (content, type, entity, severity, row_id))
                self.conn.execute("UPDATE memories_vec SET embedding=? WHERE id=?", (vec, row_id))
                self.conn.commit()
                return row_id

        cur = self.conn.execute("""
            INSERT INTO memories (content, type, entity, status, severity, source, expires_at, metadata)
            VALUES (?, ?, ?, 'active', ?, ?, ?, ?)
        """, (content, type, entity, severity, source, expires_at, json.dumps(metadata) if metadata else None))
        row_id = cur.lastrowid
        self.conn.execute("INSERT OR REPLACE INTO memories_vec (id, embedding) VALUES (?, ?)", (row_id, vec))
        self.conn.commit()
        return row_id

    def add_batch(self, items: List[Dict[str, Any]]) -> List[int]:
        """批量添加记忆（高效：一次encode）"""
        contents = [item["content"] for item in items]
        vecs = embed_batch(contents)
        ids = []
        for item, vec in zip(items, vecs):
            cur = self.conn.execute("""
                INSERT INTO memories (content, type, entity, status, severity, source, metadata)
                VALUES (?, ?, ?, 'active', ?, ?, ?)
            """, (item["content"], item.get("type"), item.get("entity"),
                  item.get("severity"), item.get("source", "import"),
                  json.dumps(item.get("metadata")) if item.get("metadata") else None))
            row_id = cur.lastrowid
            self.conn.execute("INSERT INTO memories_vec (id, embedding) VALUES (?, ?)", (row_id, vec))
            ids.append(row_id)
        self.conn.commit()
        return ids

    def search(self, query: str, type: Optional[str] = None, status: str = "active",
               entity: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """向量搜索 + 元数据过滤"""
        vec = embed(query)
        sql = "SELECT m.id, m.content, m.type, m.entity, m.status, m.severity, m.source, m.created_at, m.updated_at, m.metadata FROM memories m WHERE 1=1"
        params = []
        if status:
            sql += " AND m.status=?"
            params.append(status)
        if type:
            sql += " AND m.type=?"
            params.append(type)
        if entity:
            sql += " AND m.entity LIKE ?"
            params.append(f"%{entity}%")

        rows = self.conn.execute(sql, params).fetchall()
        results = []
        for row in rows:
            rid = row[0]
            vec_row = self.conn.execute("SELECT embedding FROM memories_vec WHERE id=?", (rid,)).fetchone()
            if vec_row and vec_row[0]:
                score = cosine_sim(vec, vec_row[0])
            else:
                score = 0.0
            results.append({
                "id": rid, "content": row[1], "type": row[2], "entity": row[3],
                "status": row[4], "severity": row[5], "source": row[6],
                "created_at": row[7], "updated_at": row[8], "metadata": row[9],
                "score": score
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def get_by_entity(self, entity: str) -> List[Dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT id, content, type, entity, status, severity, source, created_at, updated_at FROM memories WHERE entity LIKE ? ORDER BY updated_at DESC",
            (f"%{entity}%",)
        ).fetchall()
        return [dict(zip(["id", "content", "type", "entity", "status", "severity", "source", "created_at", "updated_at"], r)) for r in rows]

    def get_by_type(self, type: str, status: str = "active") -> List[Dict[str, Any]]:
        sql = "SELECT id, content, type, entity, status, severity, source, created_at, updated_at FROM memories WHERE type=?"
        params = [type]
        if status:
            sql += " AND status=?"
            params.append(status)
        sql += " ORDER BY updated_at DESC"
        rows = self.conn.execute(sql, params).fetchall()
        return [dict(zip(["id", "content", "type", "entity", "status", "severity", "source", "created_at", "updated_at"], r)) for r in rows]

    def update(self, id: int, **kwargs) -> bool:
        sets = []
        vals = []
        new_content = kwargs.get("content")
        for k in ["content", "type", "entity", "status", "severity", "source", "expires_at", "metadata"]:
            if k in kwargs:
                sets.append(f"{k}=?")
                vals.append(json.dumps(kwargs[k]) if k == "metadata" else kwargs[k])
        if not sets:
            return False
        sets.append("updated_at=CURRENT_TIMESTAMP")
        vals.append(id)
        self.conn.execute(f"UPDATE memories SET {', '.join(sets)} WHERE id=?", vals)
        if new_content:
            vec = embed(new_content)
            self.conn.execute("UPDATE memories_vec SET embedding=? WHERE id=?", (vec, id))
        self.conn.commit()
        return True

    def decay(self, days: int = 30) -> int:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        cur = self.conn.execute(
            "UPDATE memories SET status='expired', updated_at=CURRENT_TIMESTAMP WHERE status='active' AND updated_at < ?",
            (cutoff,)
        )
        self.conn.commit()
        return cur.rowcount

    def archive_expired(self) -> int:
        rows = self.conn.execute(
            "SELECT id, content, type, entity, severity, source, created_at, metadata FROM memories WHERE status='expired'"
        ).fetchall()
        for r in rows:
            self.conn.execute(
                "INSERT OR IGNORE INTO archive (id, content, type, entity, severity, source, created_at, metadata) VALUES (?,?,?,?,?,?,?,?)",
                r
            )
        count = len(rows)
        if count:
            ids = [r[0] for r in rows]
            placeholders = ','.join('?' * count)
            self.conn.execute(f"DELETE FROM memories WHERE id IN ({placeholders})", ids)
            for rid in ids:
                self.conn.execute("DELETE FROM memories_vec WHERE id=?", (rid,))
        self.conn.commit()
        return count

    def export_markdown(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        rows = self.conn.execute(
            "SELECT content, type, entity, status, severity, source, created_at, updated_at FROM memories ORDER BY type, updated_at DESC"
        ).fetchall()
        by_type = {}
        for r in rows:
            t = r[1] or "note"
            by_type.setdefault(t, []).append(r)
        for t, items in by_type.items():
            path = os.path.join(output_dir, f"{t}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# {t}\n\n")
                for item in items:
                    content, _, entity, status, severity, source, created, updated = item
                    date = (created or "")[:10]
                    f.write(f"- [{date}] [{status or 'active'}] {content}")
                    if entity:
                        f.write(f" (实体: {entity})")
                    if severity:
                        f.write(f" [严重度: {severity}]")
                    f.write("\n")
        return list(by_type.keys())

    def import_markdown(self, input_dir: str) -> int:
        """从Markdown文件导入记忆（批量encode以提高效率）"""
        items = []
        if not os.path.isdir(input_dir):
            print(f"目录不存在: {input_dir}")
            return 0

        for fname in os.listdir(input_dir):
            if not fname.endswith(".md"):
                continue
            type_name = fname[:-3]
            filepath = os.path.join(input_dir, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            current_entity = None
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    if line.startswith("## "):
                        current_entity = line[3:].strip()
                    continue

                m = re.match(r"^-?\s*\[([^\]]*)\]\s*\[([^\]]*)\]\s*(.*)", line)
                if m:
                    date_str = m.group(1).strip()
                    status_str = m.group(2).strip().replace("状态:", "").replace("状态：", "")
                    content = m.group(3).strip()
                    severity = None
                    sev_match = re.search(r'\[严重度:\s*(\w+)\]', content)
                    if sev_match:
                        severity = sev_match.group(1)
                        content = content[:sev_match.start()].strip()
                    ent_match = re.search(r'\(实体:\s*([^)]+)\)', content)
                    if ent_match:
                        current_entity = ent_match.group(1)
                        content = content[:ent_match.start()].strip()
                    if content:
                        items.append({"content": content, "type": type_name,
                                      "entity": current_entity, "severity": severity, "source": "import"})
                elif line.startswith("- ") or line.startswith("* "):
                    content = re.sub(r"^[-*]\s*", "", line)
                    if content and len(content) > 3:
                        items.append({"content": content, "type": type_name,
                                      "entity": current_entity, "source": "import"})

        if items:
            self.add_batch(items)
        return len(items)

    # ── Relations ──
    def add_relation(self, from_entity: str, relation_type: str, to_entity: str) -> int:
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO relations (from_entity, relation_type, to_entity) VALUES (?, ?, ?)",
            (from_entity, relation_type, to_entity))
        self.conn.commit()
        if cur.lastrowid:
            return cur.lastrowid
        row = self.conn.execute(
            "SELECT id FROM relations WHERE from_entity=? AND relation_type=? AND to_entity=?",
            (from_entity, relation_type, to_entity)).fetchone()
        return row[0] if row else 0

    def get_relations(self, entity: str, direction: str = "both") -> List[Dict[str, Any]]:
        results = []
        if direction in ("from", "both"):
            rows = self.conn.execute(
                "SELECT id, from_entity, relation_type, to_entity, created_at FROM relations WHERE from_entity=?",
                (entity,)).fetchall()
            results.extend([dict(zip(["id", "from_entity", "relation_type", "to_entity", "created_at"], r)) for r in rows])
        if direction in ("to", "both"):
            rows = self.conn.execute(
                "SELECT id, from_entity, relation_type, to_entity, created_at FROM relations WHERE to_entity=?",
                (entity,)).fetchall()
            results.extend([dict(zip(["id", "from_entity", "relation_type", "to_entity", "created_at"], r)) for r in rows])
        return results

    def get_related(self, entity: str, depth: int = 2) -> List[Dict[str, Any]]:
        visited = set()
        paths = []
        def _walk(current, path, d):
            if d > depth:
                return
            rels = self.conn.execute(
                "SELECT from_entity, relation_type, to_entity FROM relations WHERE from_entity=? OR to_entity=?",
                (current, current)).fetchall()
            for fr, rt, to in rels:
                neighbor = to if fr == current else fr
                direction = "→" if fr == current else "←"
                edge = (fr, rt, to)
                if edge in visited:
                    continue
                visited.add(edge)
                new_path = path + [(fr, rt, to, direction)]
                paths.append({"path": new_path, "endpoint": neighbor, "depth": d})
                if neighbor not in [p for seg in path for p in [seg[0], seg[2]]] + [current]:
                    _walk(neighbor, new_path, d + 1)
        _walk(entity, [], 1)
        return paths

    def delete_relation(self, from_entity: str, relation_type: str, to_entity: str) -> bool:
        cur = self.conn.execute(
            "DELETE FROM relations WHERE from_entity=? AND relation_type=? AND to_entity=?",
            (from_entity, relation_type, to_entity))
        self.conn.commit()
        return cur.rowcount > 0

    def stats(self) -> Dict[str, Any]:
        rows = self.conn.execute(
            "SELECT type, status, COUNT(*) FROM memories GROUP BY type, status ORDER BY type, status"
        ).fetchall()
        result = {}
        total = 0
        for type_, status, cnt in rows:
            key = f"{type_ or 'none'}:{status or 'unknown'}"
            result[key] = cnt
            total += cnt
        result["total"] = total
        return result


def main():
    parser = argparse.ArgumentParser(description="记忆数据库 CLI")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("add", help="添加记忆")
    p.add_argument("content", help="记忆内容")
    p.add_argument("--type", default="note")
    p.add_argument("--entity", default=None)
    p.add_argument("--severity", default=None)
    p.add_argument("--source", default="manual")

    p = sub.add_parser("search", help="搜索记忆")
    p.add_argument("query")
    p.add_argument("--type", default=None)
    p.add_argument("--status", default="active")
    p.add_argument("--entity", default=None)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--format", default="text", choices=["text", "json"])

    p = sub.add_parser("list", help="按类型列出记忆")
    p.add_argument("--type", default=None)
    p.add_argument("--status", default="active")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("decay", help="标记过期记忆")
    p.add_argument("--days", type=int, default=30)

    sub.add_parser("archive", help="归档过期记忆")

    p = sub.add_parser("export", help="导出为Markdown")
    p.add_argument("--dir", default="./entities")

    p = sub.add_parser("import", help="从Markdown导入")
    p.add_argument("--dir", default="./entities")

    sub.add_parser("stats", help="统计")

    p = sub.add_parser("relate", help="添加实体关系")
    p.add_argument("from_entity")
    p.add_argument("relation_type")
    p.add_argument("to_entity")

    p = sub.add_parser("relations", help="查询实体关系")
    p.add_argument("entity")
    p.add_argument("--depth", type=int, default=0)
    p.add_argument("--direction", default="both", choices=["from", "to", "both"])

    p = sub.add_parser("unrelate", help="删除实体关系")
    p.add_argument("from_entity")
    p.add_argument("relation_type")
    p.add_argument("to_entity")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    db = MemDB()

    if args.command == "add":
        rid = db.add(args.content, type=args.type, entity=args.entity,
                     severity=args.severity, source=args.source)
        print(f"✓ 已添加/更新记忆 id={rid}")

    elif args.command == "search":
        results = db.search(args.query, type=args.type, status=args.status,
                            entity=args.entity, limit=args.limit)
        if getattr(args, 'format', 'text') == 'json':
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(f"[{r['score']:.3f}] id={r['id']} [{r['type']}] {r['content'][:80]}")

    elif args.command == "list":
        if args.type:
            items = db.get_by_type(args.type, status=args.status)
        else:
            rows = db.conn.execute(
                "SELECT id, content, type, entity, status, created_at FROM memories WHERE status LIKE ? ORDER BY updated_at DESC LIMIT ?",
                (args.status or "%", args.limit)
            ).fetchall()
            items = [dict(zip(["id", "content", "type", "entity", "status", "created_at"], r)) for r in rows]
        for item in items[:args.limit]:
            print(f"id={item['id']} [{item.get('type','')}] {item['content'][:80]}  ({item.get('created_at','')[:10]})")

    elif args.command == "decay":
        n = db.decay(args.days)
        print(f"✓ 已标记 {n} 条记忆为 expired")

    elif args.command == "archive":
        n = db.archive_expired()
        print(f"✓ 已归档 {n} 条记忆")

    elif args.command == "export":
        types = db.export_markdown(args.dir)
        print(f"✓ 已导出到 {args.dir}/，类型: {', '.join(types)}")

    elif args.command == "import":
        n = db.import_markdown(args.dir)
        print(f"✓ 已导入 {n} 条记忆")

    elif args.command == "relate":
        rid = db.add_relation(args.from_entity, args.relation_type, args.to_entity)
        print(f"✓ 关系已添加 id={rid}: {args.from_entity} ──{args.relation_type}──→ {args.to_entity}")

    elif args.command == "relations":
        if args.depth > 0:
            paths = db.get_related(args.entity, depth=args.depth)
            if not paths:
                print(f"未找到 {args.entity} 的关联实体")
            for p in paths:
                path_str = " → ".join(
                    f"{seg[0]} ──{seg[1]}──{seg[3]} {seg[2]}" for seg in p["path"]
                )
                print(f"[深度{p['depth']}] {path_str}")
        else:
            rels = db.get_relations(args.entity, direction=args.direction)
            if not rels:
                print(f"未找到 {args.entity} 的关系")
            for r in rels:
                arrow = "→" if r["from_entity"] == args.entity else "←"
                if arrow == "→":
                    print(f"  {r['from_entity']} ──{r['relation_type']}──→ {r['to_entity']}")
                else:
                    print(f"  {r['from_entity']} ──{r['relation_type']}──→ {r['to_entity']}  (入边)")

    elif args.command == "unrelate":
        ok = db.delete_relation(args.from_entity, args.relation_type, args.to_entity)
        print(f"✓ 已删除" if ok else "未找到该关系")

    elif args.command == "stats":
        s = db.stats()
        for k, v in s.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
