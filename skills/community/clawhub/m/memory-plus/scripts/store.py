"""
存储记忆 - 三层存储：文件 + Milvus + 知识图谱

1. 文件存储：~/.openclaw/workspace/memory-workflow-data/memories/YYYY-MM-DD.md
2. Milvus 向量存储：需要 embedding 模型生成向量
3. 知识图谱：SQLite KG，提取实体+关系三元组
"""
import os
import re
import json
import uuid
import math
from pathlib import Path
from datetime import datetime
from typing import Optional
from .config import MEMORY_DIR

# KG 路径
MEMORY_WORKFLOW_DATA = os.environ.get(
    "MEMORY_WORKFLOW_DATA",
    str(Path.home() / ".openclaw" / "workspace" / "memory-workflow-data")
)
KG_DIR = os.path.join(MEMORY_WORKFLOW_DATA, "knowledge-graph")
KG_DB = os.path.join(KG_DIR, "kg.db")
os.makedirs(KG_DIR, exist_ok=True)
os.makedirs(MEMORY_DIR, exist_ok=True)

# Milvus 配置
MILVUS_HOST = os.environ.get('MILVUS_HOST', 'host.docker.internal')
MILVUS_PORT = os.environ.get('MILVUS_PORT', '19530')

# Embedding 服务（宿主机的 bge-m3）
EMBEDDING_URL = os.environ.get('EMBEDDING_URL', 'http://172.17.0.1:18779/v1/embeddings')
EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'bge-m3')

# Ollama 配置（用于 KG 三元组提取）
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434")

JIEBA_AVAILABLE = False
try:
    import jieba
    import jieba.posseg as pseg
    JIEBA_AVAILABLE = True
except ImportError:
    pass


# ===== KG 工具函数 =====
def kg_get_conn():
    import sqlite3
    conn = sqlite3.connect(KG_DB, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def kg_init(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            entity_type TEXT,
            created_at TEXT DEFAULT (date('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_id INTEGER NOT NULL REFERENCES kg_entities(id),
            to_id INTEGER NOT NULL REFERENCES kg_entities(id),
            rel TEXT NOT NULL,
            time TEXT,
            session TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_rel ON kg_edges(rel)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_from ON kg_edges(from_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_to ON kg_edges(to_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_entities_name ON kg_entities(name)")
    conn.commit()


def kg_get_or_create(conn, name):
    name = name.strip()
    cur = conn.execute("SELECT id FROM kg_entities WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur = conn.execute("INSERT INTO kg_entities (name) VALUES (?)", (name,))
    conn.commit()
    return cur.lastrowid


def kg_insert_edge(conn, from_name, rel, to_name, session_id=None):
    from_id = kg_get_or_create(conn, from_name)
    to_id = kg_get_or_create(conn, to_name)
    conn.execute(
        "INSERT INTO kg_edges (from_id, to_id, rel, time, session) VALUES (?, ?, ?, ?, ?)",
        (from_id, to_id, rel, datetime.now().strftime("%Y-%m-%d"), session_id)
    )
    conn.commit()


# ===== 三元组提取 =====
def extract_triples_via_llm(text: str):
    """调用 Ollama LLM 提取三元组"""
    prompt = f"""从以下文本中抽取实体和关系，输出JSON数组格式，每条记录包含 from、rel、to。

文本：{text}

要求：
- 只提取有意义的实体关系，最多5条
- 实体名称简洁，如"发哥"、"龙虾平台"
- 关系动词简洁，如"拥有"、"完成"、"讨论了"
- 只输出JSON数组，不要其他内容

输出："""
    try:
        from urllib.request import Request, urlopen
        data = json.dumps({
            "model": "hoangquan456/qwen3-nothink:4b",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }).encode("utf-8")
        req = Request(
            OLLAMA_URL + "/api/chat",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result.get("message", {}).get("content", "").strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find('[')
            end = content.rfind(']')
            if start != -1 and end != -1 and start < end:
                return json.loads(content[start:end+1])
    except Exception as e:
        print(f"    [LLM错误] {e}")
    return None


REL_WORDS = sorted([
    '雇佣了', '拥有了', '创建了', '搭建了', '完成了', '属于',
    '雇佣', '拥有', '创建', '搭建', '完成', '属于', '使用', '是'
], key=len, reverse=True)


def extract_triples_rule(text: str):
    """基于规则的三元组提取"""
    triples = []
    for rel in REL_WORDS:
        if rel in text:
            parts = text.split(rel)
            if len(parts) >= 2:
                from_name = parts[0].strip()
                to_name = rel.join(parts[1:]).strip()
                if len(from_name) >= 2 and len(to_name) >= 2:
                    triples.append({"from": from_name, "rel": rel, "to": to_name})
    return triples[:5]


def extract_triples(text: str):
    """提取三元组，LLM优先，规则降级"""
    triples = extract_triples_via_llm(text)
    if triples and isinstance(triples, list) and len(triples) > 0:
        valid = [t for t in triples if isinstance(t, dict) and t.get("from") and t.get("rel") and t.get("to")]
        if valid:
            return valid, "llm"
    rule_triples = extract_triples_rule(text)
    if rule_triples:
        return rule_triples, "rule"
    return [], "none"


# ===== 文件去重检查 =====
def get_existing_chunks() -> list[str]:
    """获取所有已有记忆片段（用于去重）"""
    chunks = []
    if not MEMORY_DIR.exists():
        return chunks
    for mf in MEMORY_DIR.glob("*.md"):
        try:
            content = mf.read_text(encoding="utf-8")
            for line in content.split("\n"):
                line = line.strip()
                if len(line) > 10:
                    line = re.sub(r"^[-*]\s+", "", line).strip()
                    if line:
                        chunks.append(line)
        except Exception:
            continue
    return chunks


def _ngram(text: str, n: int = 2) -> set:
    """字符级 N-gram"""
    return {text[i:i+n] for i in range(len(text) - n + 1)}


def _jaccard_ngram(text1: str, text2: str, n: int = 2) -> float:
    """基于字符 N-gram 的 Jaccard 相似度"""
    ng1 = _ngram(text1.lower(), n)
    ng2 = _ngram(text2.lower(), n)
    if not ng1 or not ng2:
        return 0.0
    return len(ng1 & ng2) / len(ng1 | ng2) if len(ng1 | ng2) > 0 else 0.0


def check_duplicate(new_content: str, threshold: float = 0.85) -> bool:
    """检查新内容是否与已有记忆重复（字符 N-gram Jaccard）"""
    if not new_content.strip():
        return False
    for existing in get_existing_chunks():
        score = _jaccard_ngram(new_content, existing, n=2)
        if score > threshold:
            return True
    return False


# ===== 主存储函数 =====
def store_memory(content: str, tags: list = None, session_id: str = None) -> dict:
    """
    存储单条记忆到三层存储

    Returns:
        {"file": str, "date": str, "tags": list, "skipped": bool, "reason": str,
         "kg_triples": int, "milvus_id": str}
    """
    if not content or not content.strip():
        return {
            "file": None, "date": "", "tags": tags or [],
            "skipped": True, "reason": "内容为空",
            "kg_triples": 0, "milvus_id": None
        }

    # 1. 文件去重检查
    if check_duplicate(content):
        return {
            "file": None,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tags": tags or [],
            "skipped": True,
            "reason": "内容已存在，跳过存储",
            "kg_triples": 0,
            "milvus_id": None
        }

    today = datetime.now().strftime("%Y-%m-%d")
    mf = MEMORY_DIR / f"{today}.md"
    tag_str = f"[{', '.join(tags)}] " if tags else ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"## {timestamp}\n- {tag_str}{content}\n"

    # 2. 写入文件
    with open(mf, "a", encoding="utf-8") as f:
        f.write(entry)

    # 2.5 同步到 FTS5 索引
    try:
        from .fts5 import sync_file_to_fts, init_fts
        init_fts()  # 确保表存在
        sync_file_to_fts(str(mf), content, today)
    except Exception as e:
        print(f"    [FTS5同步错误] {e}")

    result = {
        "file": str(mf),
        "date": today,
        "tags": tags or [],
        "skipped": False,
        "kg_triples": 0,
        "milvus_id": None
    }

    # 3. 提取三元组并存入 KG
    try:
        triples, method = extract_triples(content)
        if triples:
            conn = kg_get_conn()
            kg_init(conn)
            for t in triples:
                kg_insert_edge(conn, t["from"], t["rel"], t["to"], session_id)
            conn.close()
            result["kg_triples"] = len(triples)
    except Exception as e:
        print(f"    [KG错误] {e}")

    # 4. 存入 Milvus（先查重）
    try:
        if not check_milvus_duplicate(content):
            embedding = get_embedding(content)
            if embedding:
                result["milvus_id"] = store_to_milvus(content, embedding)
        else:
            result["milvus_id"] = None
            result["skipped"] = True
            result["reason"] = (result.get("reason") or "") + " | Milvus已存在，跳过"
    except Exception as e:
        print(f"    [Milvus存储错误] {e}")

    return result


def check_milvus_duplicate(content: str) -> bool:
    """检查 Milvus 是否已有相同内容（精确匹配）"""
    try:
        from pymilvus import Collection, connections
        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT, alias='default')
        collection = Collection('memory_workflow')
        collection.load()
        results = collection.query(
            expr=f'content == "{content}"',
            output_fields=['id'],
            limit=1
        )
        return len(results) > 0
    except Exception:
        return False


def get_embedding(text: str) -> Optional[list[float]]:
    """调用 bge-m3 获取文本向量"""
    try:
        from urllib.request import Request, urlopen
        data = json.dumps({
            "model": EMBEDDING_MODEL,
            "input": text
        }).encode("utf-8")
        req = Request(
            EMBEDDING_URL,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            embedding = result["data"][0]["embedding"]
            return embedding
    except Exception as e:
        print(f"    [Embedding错误] {e}")
        return None


def store_to_milvus(text: str, vector: list[float], metadata: dict = None) -> Optional[str]:
    """存入 Milvus"""
    try:
        from pymilvus import Collection, connections
        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT, alias='default')
        collection = Collection('memory_workflow')
        collection.load()

        entity_id = str(uuid.uuid4())
        entity = {
            "id": entity_id,
            "vector": vector,
            "content": text,
            "topic": metadata.get("topic", "") if metadata else "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parent_id": metadata.get("parent_id", "") if metadata else "",
            "chunk_index": metadata.get("chunk_index", 0) if metadata else 0,
        }

        collection.insert([entity])
        collection.flush()
        return entity_id
    except Exception as e:
        print(f"    [Milvus错误] {e}")
        return None
