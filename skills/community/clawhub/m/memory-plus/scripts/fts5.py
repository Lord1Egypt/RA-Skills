"""
FTS5 全文搜索 — SQLite 内置，无需外部依赖

功能：
1. 自动建 FTS5 virtual table（如果不存在）
2. 增量更新：每次 store_memory 时同步写入 FTS5
3. 搜索：MATCH 查询 + BM25 排序
4. 降级：如果 FTS5 不可用，静默跳过
"""
import os
import re
import sqlite3
from pathlib import Path
from typing import Optional, List
from .config import MEMORY_DIR

# FTS5 数据库（放在记忆目录旁边）
FTS_DB = MEMORY_DIR.parent / "fts5_index.db"


def _get_fts_conn() -> sqlite3.Connection:
    """获取 FTS5 连接"""
    conn = sqlite3.connect(str(FTS_DB), check_same_thread=False)
    # FTS5 不支持 WAL，会导致 "no such table" 错误
    conn.execute("PRAGMA journal_mode=DELETE")
    return conn


def init_fts():
    """初始化 FTS5 表"""
    conn = _get_fts_conn()
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            path,
            content,
            date
        )
    """)
    conn.commit()
    conn.close()


def sync_file_to_fts(file_path: str, content: str, date: str):
    """同步单条记忆到 FTS5（store_memory 时调用）

    注意：content 是本次要存储的新内容，但文件可能包含旧内容。
    策略：删掉该文件所有旧记录，重新从文件读取完整内容索引。
    """
    try:
        mf = Path(file_path)
        if not mf.exists():
            return

        full_content = mf.read_text(encoding="utf-8")

        conn = _get_fts_conn()

        # 删掉该文件所有旧记录
        conn.execute("DELETE FROM memories_fts WHERE path = ?", (file_path,))

        # 从文件重新索引所有段落
        for para in full_content.split("\n"):
            para = para.strip()
            if len(para) < 5:
                continue
            para = re.sub(r"^[-*]\s+", "", para).strip()
            if para:
                conn.execute(
                    "INSERT INTO memories_fts(path, content, date) VALUES (?, ?, ?)",
                    (str(mf), para, date)
                )

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"    [FTS5同步错误] {e}")


def build_fts_index():
    """全量重建 FTS5 索引（首次启用时调用）"""
    if not MEMORY_DIR.exists():
        print("记忆目录不存在，跳过 FTS5 索引构建")
        return

    conn = _get_fts_conn()
    count = 0

    for mf in MEMORY_DIR.glob("*.md"):
        try:
            date = mf.stem  # YYYY-MM-DD
            content = mf.read_text(encoding="utf-8")
            # 分段插入
            for para in content.split("\n"):
                para = para.strip()
                if len(para) < 5:
                    continue
                para = re.sub(r"^[-*]\s+", "", para).strip()
                if para:
                    conn.execute(
                        "INSERT INTO memories_fts(path, content, date) VALUES (?, ?, ?)",
                        (str(mf), para, date)
                    )
                    count += 1
        except Exception as e:
            print(f"    [FTS5索引错误] {mf}: {e}")

    conn.commit()
    conn.close()
    print(f"FTS5 索引构建完成: {count} 条记录")


def search_fts(query: str, limit: int = 10) -> List[dict]:
    """
    FTS5 全文搜索

    使用 BM25 排序，支持：
    - 短语搜索: "hello world"
    - AND/OR: hello AND world
    - 前缀: hello*
    """
    if not query or not query.strip():
        return []

    # 预处理 query（处理特殊字符）
    query = query.strip()
    query = re.sub(r'[""\'*]', ' ', query)
    query = ' OR '.join(query.split())

    try:
        conn = _get_fts_conn()

        # 尝试 MATCH 查询
        try:
            cursor = conn.execute("""
                SELECT path, content, date, bm25(memories_fts) as score
                FROM memories_fts
                WHERE memories_fts MATCH ?
                ORDER BY score
                LIMIT ?
            """, (query, limit))
            rows = cursor.fetchall()
        except Exception:
            # MATCH 语法错误，使用 LIKE 降级
            like_pattern = f"%{query.replace(' ', '%')}%"
            cursor = conn.execute("""
                SELECT path, content, date, 0.0 as score
                FROM memories_fts
                WHERE content LIKE ?
                ORDER BY date DESC
                LIMIT ?
            """, (like_pattern, limit))
            rows = cursor.fetchall()

        conn.close()

        results = []
        seen = set()
        for path, content, date, score in rows:
            if content in seen:
                continue
            seen.add(content)
            results.append({
                "chunk": content,
                "date": date,
                "file": path,
                "fts_score": score,
                "source": "fts5"
            })

        return results

    except Exception as e:
        print(f"    [FTS5搜索错误] {e}")
        return []


def rerank_with_fts(jaccard_results: List[dict], query: str, top_n: int = 5) -> List[dict]:
    """
    用 FTS5 对 Jaccard 结果重排

    Jaccard 结果 + FTS5 BM25 分 → 混合分数
    混合分数 = jaccard_score * 0.6 + fts_score_normalized * 0.4
    """
    if not jaccard_results or not query.strip():
        return jaccard_results[:top_n]

    try:
        fts_results = search_fts(query, limit=len(jaccard_results) * 2)
        if not fts_results:
            return jaccard_results[:top_n]

        # 建 FTS 分数表
        fts_map = {r["chunk"]: r["fts_score"] for r in fts_results}

        # 找 max/min fts_score 用于归一化
        fts_scores = [v for v in fts_map.values() if v != 0]
        if fts_scores:
            fts_max = max(fts_scores)
            fts_min = min(fts_scores)
        else:
            fts_max = fts_min = 1

        # 混合打分
        for r in jaccard_results:
            chunk = r["chunk"]
            fts_score = fts_map.get(chunk, 0)
            if fts_max != fts_min:
                fts_norm = (fts_score - fts_min) / (fts_max - fts_min)
            else:
                fts_norm = 0.5

            # jaccard_score 归一化（因为 Jaccard 通常很小）
            jaccard_norm = r.get("score", 0) * 5  # 放大便于比较
            r["hybrid_score"] = jaccard_norm * 0.6 + fts_norm * 0.4

        jaccard_results.sort(key=lambda x: x.get("hybrid_score", 0), reverse=True)

    except Exception as e:
        print(f"    [FTS5重排错误] {e}")

    return jaccard_results[:top_n]


# 初始化（在模块首次导入时）
try:
    init_fts()
except Exception as e:
    print(f"    [FTS5初始化错误] {e}")
