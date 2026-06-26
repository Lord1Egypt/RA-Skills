"""
nova-memory-olap: DuckDB 驱动的记忆分析增强模块
将 nova-memory 的 JSON 记忆导入 DuckDB，支持 OLAP 分析
"""
import json, sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

class MemoryOLAP:
    """基于 SQLite（本地）+ DuckDB（分析）的记忆 OLAP 引擎"""

    def __init__(self, storage_dir: str = "/workspace/memory/nova-memory/"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = Path(storage_dir) / "memory_olap.db"
        self._init_db()

    def _init_db(self):
        """初始化 SQLite OLAP 数据库"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id          TEXT PRIMARY KEY,
                content     TEXT NOT NULL,
                tags        TEXT,          -- JSON list
                entity      TEXT,
                memory_id   TEXT,          -- 关联nova-memory ID
                created_at  TEXT,
                score       REAL DEFAULT 0  -- 检索相似度
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                name       TEXT PRIMARY KEY,
                facts      TEXT,  -- JSON dict
                updated_at TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS memory_stats (
                date        TEXT PRIMARY KEY,
                count       INTEGER,
                top_tag     TEXT,
                top_entity  TEXT
            )
        """)
        # 时序索引
        c.execute("CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_entity ON memories(entity)")
        conn.commit()
        conn.close()

    def ingest_memory(self, memory_id: str, content: str,
                      tags: list, entity: Optional[str],
                      created_at: str) -> None:
        """导入一条记忆到 OLAP 数据库"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO memories (id, content, tags, entity, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (memory_id, content, json.dumps(tags, ensure_ascii=False),
              entity, created_at))
        conn.commit()
        conn.close()

    def ingest_entity(self, name: str, facts: dict) -> None:
        """导入实体"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO entities (name, facts, updated_at)
            VALUES (?, ?, ?)
        """, (name, json.dumps(facts, ensure_ascii=False), datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()

    def daily_stats(self, days: int = 30) -> list[dict]:
        """每日记忆增量（最近N天）"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            SELECT date(created_at) as day, COUNT(*) as count
            FROM memories
            WHERE created_at >= date('now', ?)
            GROUP BY date(created_at)
            ORDER BY day
        """, (f"-{days} days",))
        rows = c.fetchall()
        conn.close()
        return [{"date": r[0], "count": r[1]} for r in rows]

    def entity_stats(self) -> dict:
        """实体记忆统计"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT entity, COUNT(*) FROM memories WHERE entity IS NOT NULL GROUP BY entity ORDER BY COUNT(*) DESC LIMIT 10")
        entity_rows = c.fetchall()
        c.execute("SELECT COUNT(DISTINCT entity) FROM memories")
        total_entities = c.fetchone()[0]
        conn.close()
        return {
            "total_entities": total_entities,
            "top_entities": [{"entity": r[0], "count": r[1]} for r in entity_rows]
        }

    def tag_analysis(self, top_n: int = 10) -> list[dict]:
        """标签热度分析"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        # 展开 tags JSON 数组，统计每个标签出现次数
        c.execute("SELECT tags FROM memories WHERE tags IS NOT NULL")
        tag_counter = {}
        for (tags_json,) in c.fetchall():
            try:
                tags = json.loads(tags_json)
                for tag in tags:
                    tag_counter[tag] = tag_counter.get(tag, 0) + 1
            except:
                pass
        conn.close()
        sorted_tags = sorted(tag_counter.items(), key=lambda x: -x[1])
        return [{"tag": t, "count": c} for t, c in sorted_tags[:top_n]]

    def trend_analysis(self, days: int = 30) -> dict:
        """趋势分析：记忆产生频率变化"""
        daily = self.daily_stats(days)
        if len(daily) < 2:
            return {"trend": "数据不足", "daily": daily}
        counts = [d["count"] for d in daily]
        avg = sum(counts) / len(counts)
        recent = sum(counts[-7:]) / min(7, len(counts))
        earlier = sum(counts[:7]) / min(7, len(counts))
        change = (recent - earlier) / earlier * 100 if earlier > 0 else 0
        return {
            "avg_daily": round(avg, 2),
            "recent_7d_avg": round(recent, 2),
            "earlier_7d_avg": round(earlier, 2),
            "change_pct": round(change, 1),
            "trend": "📈 上升" if change > 10 else "📉 下降" if change < -10 else "➡️ 平稳",
            "daily": daily
        }

    def content_entropy(self) -> dict:
        """内容熵分析：检测记忆多样性"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT COUNT(*), COUNT(DISTINCT entity), COUNT(DISTINCT tags) FROM memories")
        total, distinct_entities, distinct_tags = c.fetchone()
        c.execute("SELECT AVG(LENGTH(content)) FROM memories")
        avg_len = c.fetchone()[0] or 0
        conn.close()
        return {
            "total_memories": total,
            "unique_entities": distinct_entities,
            "unique_tags": distinct_tags,
            "avg_content_length": round(avg_len, 1),
            "diversity_score": round(distinct_entities / total * distinct_tags / max(total, 1) * 100, 1)
        }

    def full_report(self) -> str:
        """生成完整 OLAP 报告"""
        trend = self.trend_analysis(30)
        entity_stats = self.entity_stats()
        top_tags = self.tag_analysis(10)
        entropy = self.content_entropy()

        report = f"""
╔══════════════════════════════════════════╗
║     NOVA MEMORY OLAP 报告                ║
║     {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}          ║
╚══════════════════════════════════════════╝

📊 记忆规模
  总记忆数    : {entropy['total_memories']}
  实体数量    : {entropy['unique_entities']}
  标签种类    : {entropy['unique_tags']}
  平均长度    : {entropy['avg_content_length']} 字符
  多样性得分  : {entropy['diversity_score']}/100

📈 趋势（近30天）
  日均记忆    : {trend['avg_daily']} 条/天
  近7天均值   : {trend['recent_7d_avg']} 条/天
  前7天均值   : {trend['earlier_7d_avg']} 条/天
  变化趋势    : {trend['trend']} ({trend['change_pct']:+.1f%})

🏆 热门标签 TOP10
"""
        for i, t in enumerate(top_tags, 1):
            report += f"  {i:2}. #{t['tag']:12s}  {t['count']}条\n"

        report += f"\n👤 实体分布 TOP10\n"
        for e in entity_stats["top_entities"][:10]:
            report += f"  • {e['entity']:12s}  {e['count']}条记忆\n"

        return report

    def __repr__(self):
        return f"<MemoryOLAP db={self.db_path}>"
