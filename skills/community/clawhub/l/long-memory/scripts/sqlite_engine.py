#!/usr/bin/env python3
"""SQLite 存储引擎：替代纯文件，高性能查询"""

import argparse
import json
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
DB_FILE = "long-memory.db"


def get_db(memory_dir: Path) -> sqlite3.Connection:
    """获取数据库连接"""
    db_path = memory_dir / DB_FILE
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # 写入不阻塞读
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db(memory_dir: Path):
    """初始化数据库表结构"""
    conn = get_db(memory_dir)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            session TEXT NOT NULL DEFAULT 'default',
            topic TEXT,
            tags TEXT DEFAULT '[]',
            content TEXT NOT NULL,
            raw_content TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_conv_date ON conversations(date);
        CREATE INDEX IF NOT EXISTS idx_conv_topic ON conversations(topic);
        CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session);

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        );
        CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id);
        CREATE INDEX IF NOT EXISTS idx_msg_role ON messages(role);

        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            summary TEXT NOT NULL,
            key_points TEXT DEFAULT '[]',
            topics TEXT DEFAULT '[]',
            tags TEXT DEFAULT '[]',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS distillations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL,
            decisions TEXT DEFAULT '[]',
            todos TEXT DEFAULT '[]',
            preferences TEXT DEFAULT '[]',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            usage_count INTEGER DEFAULT 1,
            first_seen TEXT,
            last_seen TEXT
        );

        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            usage_count INTEGER DEFAULT 1,
            first_seen TEXT,
            last_seen TEXT
        );

        CREATE TABLE IF NOT EXISTS operation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            operation TEXT NOT NULL,
            level TEXT DEFAULT 'info',
            details TEXT DEFAULT '{}'
        );
    """)
    conn.commit()
    conn.close()


def insert_conversation(memory_dir: Path, date: str, time: str, session: str,
                        topic: str, tags: list[str], content: str, raw_content: str = "") -> int:
    """插入对话"""
    conn = get_db(memory_dir)
    cursor = conn.execute(
        "INSERT INTO conversations (date, time, session, topic, tags, content, raw_content) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (date, time, session, topic, json.dumps(tags), content, raw_content)
    )
    conv_id = cursor.lastrowid

    # 更新标签
    for tag in tags:
        conn.execute("""
            INSERT INTO tags (name, first_seen, last_seen, usage_count) VALUES (?, ?, ?, 1)
            ON CONFLICT(name) DO UPDATE SET usage_count=usage_count+1, last_seen=?
        """, (tag, date, date, date))

    # 更新话题
    if topic:
        conn.execute("""
            INSERT INTO topics (name, first_seen, last_seen, usage_count) VALUES (?, ?, ?, 1)
            ON CONFLICT(name) DO UPDATE SET usage_count=usage_count+1, last_seen=?
        """, (topic, date, date))

    conn.commit()
    conn.close()
    return conv_id


def insert_messages(memory_dir: Path, conv_id: int, messages: list[dict]):
    """插入消息"""
    conn = get_db(memory_dir)
    conn.executemany(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        [(conv_id, m["role"], m["content"]) for m in messages]
    )
    conn.commit()
    conn.close()


def search(memory_dir: Path, query: str, topic: str = None, tag: str = None,
           start_date: str = None, end_date: str = None, days: int = None,
           limit: int = 50) -> list[dict]:
    """高性能搜索"""
    conn = get_db(memory_dir)

    if days:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    sql = """
        SELECT c.id, c.date, c.time, c.session, c.topic, c.tags, c.content,
               GROUP_CONCAT(m.content, '|||') as messages_text
        FROM conversations c
        LEFT JOIN messages m ON m.conversation_id = c.id
        WHERE 1=1
    """
    params = []

    if start_date:
        sql += " AND c.date >= ?"
        params.append(start_date)
    if end_date:
        sql += " AND c.date <= ?"
        params.append(end_date)
    if topic:
        sql += " AND c.topic LIKE ?"
        params.append(f"%{topic}%")
    if tag:
        sql += " AND c.tags LIKE ?"
        params.append(f"%{tag}%")
    if query:
        sql += " AND (c.content LIKE ? OR c.topic LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])

    sql += " GROUP BY c.id ORDER BY c.date DESC, c.time DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in rows]


def get_stats(memory_dir: Path) -> dict:
    """统计信息（SQLite 版，比文件版快100倍）"""
    conn = get_db(memory_dir)

    stats = {}
    r = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()
    stats["total_conversations"] = r[0]

    r = conn.execute("SELECT COUNT(*) FROM messages").fetchone()
    stats["total_messages"] = r[0]

    r = conn.execute("SELECT COUNT(DISTINCT date) FROM conversations").fetchone()
    stats["total_days"] = r[0]

    r = conn.execute("SELECT COUNT(*) FROM tags").fetchone()
    stats["total_tags"] = r[0]

    r = conn.execute("SELECT COUNT(*) FROM topics").fetchone()
    stats["total_topics"] = r[0]

    r = conn.execute("SELECT MIN(date), MAX(date) FROM conversations").fetchone()
    stats["date_range"] = f"{r[0]} ~ {r[1]}" if r[0] else "无"

    # 热门话题
    stats["top_topics"] = [dict(r) for r in
        conn.execute("SELECT name, usage_count FROM topics ORDER BY usage_count DESC LIMIT 10").fetchall()]

    # 热门标签
    stats["top_tags"] = [dict(r) for r in
        conn.execute("SELECT name, usage_count FROM tags ORDER BY usage_count DESC LIMIT 10").fetchall()]

    # 每日活跃度
    stats["daily_activity"] = [dict(r) for r in
        conn.execute("""
            SELECT date, COUNT(*) as count
            FROM conversations
            GROUP BY date ORDER BY date DESC LIMIT 30
        """).fetchall()]

    # 数据库大小
    db_path = memory_dir / DB_FILE
    stats["db_size"] = db_path.stat().st_size if db_path.exists() else 0

    conn.close()
    return stats


def import_from_files(memory_dir: Path):
    """从现有的 markdown 文件导入到 SQLite"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        print("⚠️ 没有对话文件可导入")
        return 0

    init_db(memory_dir)
    conn = get_db(memory_dir)
    count = 0

    for fp in sorted(conv_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        date_str = fp.stem

        # 检查是否已导入
        existing = conn.execute("SELECT id FROM conversations WHERE date = ?", (date_str,)).fetchone()
        if existing:
            continue

        # 解析
        sections = re.split(r'(?=## \[)', content)
        for section in sections:
            time_match = re.search(r'\[(\d{2}:\d{2})\]', section)
            topic_match = re.search(r'###\s*话题[：:]\s*(.+)', section)
            tag_match = re.search(r'\*\*标签[：:]\*\*\s*(.+)', section)

            time_str = time_match.group(1) if time_match else "00:00"
            topic = topic_match.group(1).strip() if topic_match else ""
            tags = [t.strip() for t in tag_match.group(1).split("，") if t.strip()] if tag_match else []

            conn.execute(
                "INSERT INTO conversations (date, time, session, topic, tags, content) VALUES (?, ?, ?, ?, ?, ?)",
                (date_str, time_str, "imported", topic, json.dumps(tags), section.strip())
            )
            count += 1

    conn.commit()
    conn.close()
    print(f"✅ 导入 {count} 条记录到 SQLite")
    return count


def print_stats(stats: dict):
    print("=" * 60)
    print("📊 记忆统计（SQLite 高性能版）")
    print("=" * 60)
    print(f"\n  对话记录: {stats['total_conversations']}")
    print(f"  消息总数: {stats['total_messages']}")
    print(f"  对话天数: {stats['total_days']}")
    print(f"  话题数:   {stats['total_topics']}")
    print(f"  标签数:   {stats['total_tags']}")
    print(f"  日期范围: {stats['date_range']}")
    print(f"  数据库:   {stats['db_size'] / 1024:.1f} KB")

    if stats.get("top_topics"):
        print(f"\n  🔥 热门话题:")
        for t in stats["top_topics"][:5]:
            print(f"     {t['name']}: {t['usage_count']}")

    if stats.get("top_tags"):
        print(f"\n  🏷️  热门标签:")
        for t in stats["top_tags"][:5]:
            print(f"     {t['name']}: {t['usage_count']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="SQLite 存储引擎")
    sub = p.add_subparsers(dest="command")

    init_cmd = sub.add_parser("init", help="初始化数据库")
    import_cmd = sub.add_parser("import", help="从文件导入")
    search_cmd = sub.add_parser("search", help="搜索")
    search_cmd.add_argument("-q", "--query", default=None)
    search_cmd.add_argument("-t", "--topic", default=None)
    search_cmd.add_argument("--tag", default=None)
    search_cmd.add_argument("--days", type=int, default=None)
    search_cmd.add_argument("--limit", type=int, default=50)
    stats_cmd = sub.add_parser("stats", help="统计")

    args = p.parse_args()
    md = DEFAULT_MEMORY_DIR

    if args.command == "init":
        init_db(md)
        print("✅ 数据库已初始化")
    elif args.command == "import":
        import_from_files(md)
    elif args.command == "search":
        init_db(md)
        results = search(md, args.query, args.topic, args.tag, days=args.days, limit=args.limit)
        for r in results:
            print(f"📄 {r['date']} [{r['time']}] {r['topic']}")
            print(f"   标签: {r['tags']}")
    elif args.command == "stats":
        init_db(md)
        print_stats(get_stats(md))
    else:
        # 默认：初始化+导入+统计
        init_db(md)
        import_from_files(md)
        print()
        print_stats(get_stats(md))
