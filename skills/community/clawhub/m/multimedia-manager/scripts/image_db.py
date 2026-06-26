#!/usr/bin/env python3
"""Image Vault database layer — SQLite-backed metadata store."""

import sqlite3
import os
import hashlib
import json
import subprocess
import uuid
from datetime import datetime
from pathlib import Path

def _load_dotenv():
    """Load .env from skill root (one level up from scripts/)."""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

_load_dotenv()

def _load_yaml_config() -> dict:
    """Load config.yaml if available; auto-copy from template on first run."""
    skill_root = os.path.join(os.path.dirname(__file__), "..")
    config_path = os.path.join(skill_root, "config.yaml")
    example_path = os.path.join(skill_root, "config.example.yaml")
    if not os.path.isfile(config_path) and os.path.isfile(example_path):
        import shutil
        shutil.copy2(example_path, config_path)
    if os.path.isfile(config_path):
        try:
            import yaml
            with open(config_path) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            pass
        except Exception:
            pass
    return {}

_yaml_cfg = _load_yaml_config()
_storage_cfg = _yaml_cfg.get("storage", {})
_env_vault = os.environ.get("IMAGE_VAULT_DIR", "")
VAULT_DIR = os.path.expanduser(_env_vault or _storage_cfg.get("vault_dir", "") or "~/.image-vault")
_env_db = os.environ.get("IMAGE_VAULT_DB", "")
DB_PATH = os.path.expanduser(_env_db or _storage_cfg.get("db_path", "") or os.path.join(VAULT_DIR, "image_vault.db"))
ORIGINALS_DIR = os.path.join(VAULT_DIR, "originals")
THUMBNAILS_DIR = os.path.join(VAULT_DIR, "thumbnails")

SCHEMA_VERSION = 9

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS images (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    filename    TEXT NOT NULL,
    original_path TEXT,
    vault_path  TEXT NOT NULL UNIQUE,
    thumb_path  TEXT,
    file_hash   TEXT NOT NULL,
    file_size   INTEGER,
    width       INTEGER,
    height      INTEGER,
    format      TEXT,
    source      TEXT DEFAULT 'unknown',
    category    TEXT DEFAULT 'uncategorized',
    description TEXT,
    tags        TEXT DEFAULT '[]',
    embedding   TEXT,                      -- reserved for Pro edition
    face_names  TEXT DEFAULT '[]',         -- JSON array of person names
    taken_at    TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    description TEXT,
    cover_image_id INTEGER,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS album_images (
    album_id    INTEGER NOT NULL,
    image_id    INTEGER NOT NULL,
    added_at    TEXT NOT NULL,
    PRIMARY KEY (album_id, image_id),
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS schema_info (
    version INTEGER PRIMARY KEY
);

CREATE INDEX IF NOT EXISTS idx_images_tags ON images(tags);
CREATE INDEX IF NOT EXISTS idx_images_category ON images(category);
CREATE INDEX IF NOT EXISTS idx_images_source ON images(source);
CREATE INDEX IF NOT EXISTS idx_images_created_at ON images(created_at);
CREATE INDEX IF NOT EXISTS idx_images_taken_at ON images(taken_at);
CREATE INDEX IF NOT EXISTS idx_images_file_hash ON images(file_hash);
CREATE INDEX IF NOT EXISTS idx_album_images_image ON album_images(image_id);
"""

MIGRATION_V2 = """
ALTER TABLE images ADD COLUMN embedding TEXT;
ALTER TABLE images ADD COLUMN face_names TEXT DEFAULT '[]';
"""

MIGRATION_V3 = """
ALTER TABLE images ADD COLUMN image_embedding TEXT;
"""

MIGRATION_V4 = """
ALTER TABLE images ADD COLUMN media_type TEXT DEFAULT 'image';
ALTER TABLE images ADD COLUMN duration REAL;
ALTER TABLE images ADD COLUMN cover_path TEXT;
"""

MIGRATION_V5 = """
ALTER TABLE images ADD COLUMN favorite INTEGER DEFAULT 0;
"""

MIGRATION_V6 = """
CREATE TABLE IF NOT EXISTS faces (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id    INTEGER NOT NULL,
    bbox_x      INTEGER,
    bbox_y      INTEGER,
    bbox_w      INTEGER,
    bbox_h      INTEGER,
    crop_path   TEXT,
    embedding   TEXT,
    cluster_id  INTEGER DEFAULT -1,
    person_name TEXT DEFAULT '',
    created_at  TEXT NOT NULL,
    FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_faces_image ON faces(image_id);
CREATE INDEX IF NOT EXISTS idx_faces_cluster ON faces(cluster_id);
"""

MIGRATION_V7 = """
CREATE TABLE IF NOT EXISTS smart_albums (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    icon        TEXT DEFAULT '🔍',
    rules       TEXT NOT NULL DEFAULT '{}',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""

MIGRATION_V8 = """
ALTER TABLE images ADD COLUMN latitude REAL;
ALTER TABLE images ADD COLUMN longitude REAL;
ALTER TABLE images ADD COLUMN location_name TEXT;
ALTER TABLE images ADD COLUMN face_scanned INTEGER DEFAULT 0;
CREATE TABLE IF NOT EXISTS shares (
    id TEXT PRIMARY KEY,
    target_type TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    created_by TEXT DEFAULT 'default',
    expires_at TEXT,
    password TEXT,
    view_count INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_shares_target ON shares(target_type, target_id);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name TEXT,
    role TEXT DEFAULT 'user',
    token TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    image_ids TEXT NOT NULL DEFAULT '[]',
    cover_image_id INTEGER,
    date_range_start TEXT,
    date_range_end TEXT,
    generated_at TEXT NOT NULL
);
"""

MIGRATION_V9 = """
ALTER TABLE images ADD COLUMN deleted_at TEXT;
ALTER TABLE images ADD COLUMN live_photo_video TEXT;

CREATE TABLE IF NOT EXISTS task_queue (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    task_type   TEXT NOT NULL,
    payload     TEXT NOT NULL DEFAULT '{}',
    status      TEXT NOT NULL DEFAULT 'pending',
    priority    INTEGER DEFAULT 0,
    result      TEXT,
    error       TEXT,
    created_at  TEXT NOT NULL,
    started_at  TEXT,
    finished_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON task_queue(status, priority DESC);

CREATE TABLE IF NOT EXISTS config (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

FTS_SETUP = """
CREATE VIRTUAL TABLE IF NOT EXISTS images_fts USING fts5(
    description, tags, filename, face_names,
    content='images', content_rowid='id',
    tokenize='unicode61'
);
"""

FTS_TRIGGERS = """
CREATE TRIGGER IF NOT EXISTS images_ai AFTER INSERT ON images BEGIN
    INSERT INTO images_fts(rowid, description, tags, filename, face_names)
    VALUES (new.id, COALESCE(new.description,''), COALESCE(new.tags,''), COALESCE(new.filename,''), COALESCE(new.face_names,''));
END;
CREATE TRIGGER IF NOT EXISTS images_au AFTER UPDATE ON images BEGIN
    INSERT INTO images_fts(images_fts, rowid, description, tags, filename, face_names)
    VALUES ('delete', old.id, COALESCE(old.description,''), COALESCE(old.tags,''), COALESCE(old.filename,''), COALESCE(old.face_names,''));
    INSERT INTO images_fts(rowid, description, tags, filename, face_names)
    VALUES (new.id, COALESCE(new.description,''), COALESCE(new.tags,''), COALESCE(new.filename,''), COALESCE(new.face_names,''));
END;
CREATE TRIGGER IF NOT EXISTS images_ad AFTER DELETE ON images BEGIN
    INSERT INTO images_fts(images_fts, rowid, description, tags, filename, face_names)
    VALUES ('delete', old.id, COALESCE(old.description,''), COALESCE(old.tags,''), COALESCE(old.filename,''), COALESCE(old.face_names,''));
END;
"""


def get_db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA_SQL)
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version == 0:
        conn.execute("INSERT INTO schema_info(version) VALUES(?)", (SCHEMA_VERSION,))
    if current_version < 2:
        for stmt in MIGRATION_V2.strip().split("\n"):
            stmt = stmt.strip()
            if stmt:
                try:
                    conn.execute(stmt)
                except Exception:
                    pass
        conn.execute("UPDATE schema_info SET version=?", (2,))
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version < 3:
        for stmt in MIGRATION_V3.strip().split("\n"):
            stmt = stmt.strip()
            if stmt:
                try:
                    conn.execute(stmt)
                except Exception:
                    pass
        conn.execute("UPDATE schema_info SET version=?", (3,))
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version < 4:
        for stmt in MIGRATION_V4.strip().split("\n"):
            stmt = stmt.strip()
            if stmt:
                try:
                    conn.execute(stmt)
                except Exception:
                    pass
        conn.execute("UPDATE schema_info SET version=?", (4,))
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version < 5:
        for stmt in MIGRATION_V5.strip().split("\n"):
            stmt = stmt.strip()
            if stmt:
                try:
                    conn.execute(stmt)
                except Exception:
                    pass
        conn.execute("UPDATE schema_info SET version=?", (5,))
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version < 6:
        conn.executescript(MIGRATION_V6)
        conn.execute("UPDATE schema_info SET version=?", (6,))
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version < 7:
        conn.executescript(MIGRATION_V7)
        conn.execute("UPDATE schema_info SET version=?", (7,))
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version < 8:
        for stmt in (s.strip() for s in MIGRATION_V8.strip().split(";") if s.strip()):
            try:
                conn.execute(stmt)
            except Exception:
                pass
        conn.execute("UPDATE schema_info SET version=?", (8,))
    row = conn.execute("SELECT version FROM schema_info LIMIT 1").fetchone()
    current_version = row["version"] if row else 0
    if current_version < 9:
        for stmt in (s.strip() for s in MIGRATION_V9.strip().split(";") if s.strip()):
            try:
                conn.execute(stmt)
            except Exception:
                pass
        conn.execute("UPDATE schema_info SET version=?", (9,))
    try:
        conn.executescript(FTS_SETUP)
        conn.executescript(FTS_TRIGGERS)
        fts_count = conn.execute("SELECT COUNT(*) as c FROM images_fts").fetchone()["c"]
        img_count = conn.execute("SELECT COUNT(*) as c FROM images").fetchone()["c"]
        if fts_count < img_count:
            conn.execute("INSERT INTO images_fts(images_fts) VALUES('rebuild')")
    except Exception:
        pass
    conn.commit()
    conn.close()


def file_hash(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def generate_vault_filename(filepath: str, source: str = "imported") -> str:
    """Generate standardized filename: YYYYMMDD_HHMMSS_<source>_<hash>.<ext>"""
    stat = os.stat(filepath)
    mtime = datetime.fromtimestamp(stat.st_mtime)
    ext = Path(filepath).suffix.lower()
    fhash = file_hash(filepath)
    return f"{mtime.strftime('%Y%m%d_%H%M%S')}_{source}_{fhash}{ext}"


def image_exists(conn: sqlite3.Connection, fhash: str) -> bool:
    row = conn.execute("SELECT id FROM images WHERE file_hash=?", (fhash,)).fetchone()
    return row is not None


def add_image(conn: sqlite3.Connection, **kwargs) -> int:
    now = datetime.now().isoformat()
    kwargs.setdefault("created_at", now)
    kwargs.setdefault("updated_at", now)
    if isinstance(kwargs.get("tags"), list):
        kwargs["tags"] = json.dumps(kwargs["tags"], ensure_ascii=False)

    cols = ", ".join(kwargs.keys())
    placeholders = ", ".join(["?"] * len(kwargs))
    cur = conn.execute(
        f"INSERT INTO images({cols}) VALUES({placeholders})",
        list(kwargs.values()),
    )
    conn.commit()
    return cur.lastrowid


def update_image(conn: sqlite3.Connection, image_id: int, **kwargs):
    kwargs["updated_at"] = datetime.now().isoformat()
    if isinstance(kwargs.get("tags"), list):
        kwargs["tags"] = json.dumps(kwargs["tags"], ensure_ascii=False)
    if isinstance(kwargs.get("face_names"), list):
        kwargs["face_names"] = json.dumps(kwargs["face_names"], ensure_ascii=False)
    sets = ", ".join(f"{k}=?" for k in kwargs)
    conn.execute(f"UPDATE images SET {sets} WHERE id=?", list(kwargs.values()) + [image_id])
    conn.commit()


SYNONYM_GROUPS = [
    {"孩子", "小孩", "儿童", "小朋友", "宝宝", "婴儿", "幼儿", "娃娃", "男孩", "女孩", "少儿"},
    {"海边", "海滩", "沙滩", "大海", "海洋", "海岸", "海浪"},
    {"冰激凌", "冰淇淋", "雪糕", "冰棒"},
    {"风景", "景色", "风光", "美景"},
    {"旅行", "旅游", "出行", "出游"},
    {"动物", "宠物", "小动物", "野生动物"},
    {"城市", "都市", "街道", "街景", "城区"},
    {"天空", "蓝天", "白云", "云彩"},
    {"食物", "美食", "吃", "餐", "饭"},
    {"花", "花朵", "鲜花", "花卉"},
    {"山", "山峰", "山脉", "高山"},
    {"纽约", "New York", "NYC", "曼哈顿", "Manhattan"},
    {"家庭", "家人", "全家", "亲子"},
    {"合照", "合影", "合拍", "集体照"},
    {"运动", "健身", "锻炼", "体育"},
    {"公园", "花园", "园林", "绿地"},
    {"龙虾", "小龙虾", "crawfish", "crayfish"},
    {"猫", "猫咪", "小猫", "喵", "猫猫"},
    {"狗", "狗狗", "小狗", "犬", "汪"},
    {"树", "树木", "大树", "树林", "森林"},
    {"车", "汽车", "轿车", "车辆"},
    {"夜景", "夜晚", "夜间", "灯光"},
    {"日落", "日出", "朝霞", "晚霞", "夕阳"},
    {"水", "湖", "河", "溪", "瀑布", "湖泊", "河流"},
    {"建筑", "大楼", "房子", "楼房", "房屋"},
    {"老虎", "虎", "东北虎", "华南虎", "白虎", "猛虎"},
    {"熊猫", "大熊猫", "国宝", "滚滚"},
    {"大象", "象", "小象", "非洲象", "亚洲象"},
    {"狮子", "雄狮", "母狮", "狮"},
    {"长颈鹿", "鹿"},
    {"斑马", "野马"},
    {"鹦鹉", "鹦"},
    {"鸟", "鸟类", "飞鸟", "小鸟"},
    {"企鹅", "小企鹅"},
    {"猴子", "猴", "猕猴", "金丝猴"},
    {"兔子", "兔", "小兔", "小白兔", "兔兔"},
    {"蝴蝶", "蝶"},
    {"乌龟", "龟", "海龟"},
    {"金鱼", "鱼", "鱼类", "锦鲤"},
    {"蜜蜂", "蜂"},
    {"马", "骏马", "小马", "白马"},
    {"牛", "奶牛", "水牛", "黄牛"},
    {"羊", "绵羊", "山羊", "小羊"},
    {"骆驼", "双峰驼", "单峰驼"},
    {"孔雀", "开屏"},
    {"菊花", "雏菊", "野菊"},
    {"玫瑰", "月季", "蔷薇"},
    {"荷花", "莲花", "睡莲", "荷叶"},
    {"樱花", "樱"},
    {"向日葵", "葵花", "太阳花"},
    {"帆船", "sailing", "扬帆", "航海"},
    {"烟花", "烟火", "焰火", "fireworks"},
]

_SYNONYM_MAP = {}
for group in SYNONYM_GROUPS:
    for word in group:
        _SYNONYM_MAP[word] = group

COMPOUND_EXCLUSIONS = {
    "猫": {"熊猫", "猫科", "猫头鹰", "大熊猫", "小熊猫"},
    "虎": {"壁虎", "马虎"},
    "马": {"骆驼", "马路", "马上", "马虎", "河马", "斑马"},
    "象": {"形象", "景象", "现象", "气象", "想象", "印象", "对象", "抽象"},
    "牛": {"蜗牛", "牛仔"},
    "鹤": {"仙鹤"},
    "鱼": {"鱿鱼"},
    "花": {"花生", "花费", "花岗岩", "花纹"},
    "鸟": {"鸵鸟"},
}


def _expand_synonyms(query: str) -> list:
    """Expand a search query with synonyms. Returns list of all terms to search."""
    query = query.strip()
    if not query:
        return [query]
    terms = {query}
    if query in _SYNONYM_MAP:
        terms.update(_SYNONYM_MAP[query])
    return list(terms)


def _is_excluded(row: dict, search_terms: list, exclusions: set) -> bool:
    """Check if a result should be excluded due to compound word false positives."""
    if not exclusions:
        return False
    tags_str = row.get("tags", "") or ""
    desc = row.get("description", "") or ""
    text = tags_str + " " + desc
    has_direct_match = False
    for term in search_terms:
        if len(term) >= 2 and f'"{term}"' in tags_str:
            has_direct_match = True
            break
    if has_direct_match:
        return False
    for exc in exclusions:
        if exc in text:
            return True
    return False


def _fts_available(conn: sqlite3.Connection) -> bool:
    try:
        conn.execute("SELECT COUNT(*) FROM images_fts").fetchone()
        return True
    except Exception:
        return False


def search_images(conn: sqlite3.Connection, query: str = None, category: str = None,
                  source: str = None, date_from: str = None, date_to: str = None,
                  tags: list = None, limit: int = 100, offset: int = 0,
                  semantic: bool = False) -> list:
    """Flexible search: FTS5 first, LIKE fallback. Re-ranks by cosine when semantic=True."""
    filter_conditions = ["deleted_at IS NULL"]
    filter_params = []

    if category:
        filter_conditions.append("category = ?")
        filter_params.append(category)
    if source:
        filter_conditions.append("source = ?")
        filter_params.append(source)
    if date_from:
        filter_conditions.append("(taken_at >= ? OR created_at >= ?)")
        filter_params.extend([date_from, date_from])
    if date_to:
        filter_conditions.append("(taken_at <= ? OR created_at <= ?)")
        filter_params.extend([date_to, date_to])
    if tags:
        for tag in tags:
            filter_conditions.append("tags LIKE ?")
            filter_params.append(f'%"{tag}"%')

    fetch_limit = max(limit * 3, 300) if (semantic and query) else limit
    results = []

    if query:
        all_terms = _expand_synonyms(query)
        seen_ids = set()
        exclusions = set()
        for term in all_terms:
            exclusions.update(COMPOUND_EXCLUSIONS.get(term, set()))

        if _fts_available(conn):
            try:
                fts_parts = []
                for term in all_terms:
                    words = [w.strip() for w in term.split() if w.strip()]
                    fts_parts.extend(f'"{w}"' for w in words)
                fts_query = " OR ".join(fts_parts)
                fts_sql = "SELECT rowid FROM images_fts WHERE images_fts MATCH ? LIMIT ?"
                fts_rows = conn.execute(fts_sql, (fts_query, max(fetch_limit * 5, 500))).fetchall()
                fts_ids = [r["rowid"] for r in fts_rows]
                if fts_ids:
                    ph = ",".join("?" * len(fts_ids))
                    where_parts = [f"id IN ({ph})"] + filter_conditions
                    where = " AND ".join(where_parts)
                    params = fts_ids + filter_params + [fetch_limit * 2, 0]
                    sql = f"SELECT * FROM images WHERE {where} ORDER BY COALESCE(taken_at, created_at) DESC LIMIT ? OFFSET ?"
                    for r in conn.execute(sql, params).fetchall():
                        d = dict(r)
                        if d["id"] not in seen_ids:
                            if not _is_excluded(d, all_terms, exclusions):
                                seen_ids.add(d["id"])
                                results.append(d)
            except Exception:
                pass

        like_conds = []
        like_params = []
        for term in all_terms:
            tag_exact = f'%"{term}"%'
            q = f"%{term}%"
            like_conds.append("(description LIKE ? OR tags LIKE ? OR filename LIKE ? OR category LIKE ? OR face_names LIKE ?)")
            like_params.extend([q, tag_exact, q, q, q])
        text_cond = "(" + " OR ".join(like_conds) + ")"
        where_parts = [text_cond] + filter_conditions
        where = " AND ".join(where_parts)
        params = like_params + filter_params + [fetch_limit * 2, 0]
        sql = f"SELECT * FROM images WHERE {where} ORDER BY COALESCE(taken_at, created_at) DESC LIMIT ? OFFSET ?"
        for r in conn.execute(sql, params).fetchall():
            d = dict(r)
            if d["id"] not in seen_ids:
                if not _is_excluded(d, all_terms, exclusions):
                    seen_ids.add(d["id"])
                    results.append(d)

        results.sort(key=lambda x: x.get("taken_at") or x.get("created_at", ""), reverse=True)
        if offset > 0:
            results = results[offset:]
    else:
        where = " AND ".join(filter_conditions) if filter_conditions else "1=1"
        params = filter_params + [fetch_limit, offset]
        sql = f"SELECT * FROM images WHERE {where} ORDER BY COALESCE(taken_at, created_at) DESC LIMIT ? OFFSET ?"
        results = [dict(r) for r in conn.execute(sql, params).fetchall()]

    return results[:limit]


def get_all_categories(conn: sqlite3.Connection) -> list:
    rows = conn.execute("SELECT DISTINCT category FROM images WHERE deleted_at IS NULL ORDER BY category").fetchall()
    return [r["category"] for r in rows]


def get_all_tags(conn: sqlite3.Connection, by_frequency: bool = False) -> list:
    rows = conn.execute("SELECT tags FROM images WHERE deleted_at IS NULL").fetchall()
    if by_frequency:
        from collections import Counter
        counter = Counter()
        for r in rows:
            try:
                counter.update(json.loads(r["tags"]))
            except (json.JSONDecodeError, TypeError):
                pass
        return [tag for tag, _ in counter.most_common()]
    all_tags = set()
    for r in rows:
        try:
            all_tags.update(json.loads(r["tags"]))
        except (json.JSONDecodeError, TypeError):
            pass
    return sorted(all_tags)


def get_stats(conn: sqlite3.Connection) -> dict:
    total = conn.execute("SELECT COUNT(*) as c FROM images WHERE deleted_at IS NULL").fetchone()["c"]
    cats = conn.execute("SELECT category, COUNT(*) as c FROM images WHERE deleted_at IS NULL GROUP BY category ORDER BY c DESC").fetchall()
    sources = conn.execute("SELECT source, COUNT(*) as c FROM images WHERE deleted_at IS NULL GROUP BY source ORDER BY c DESC").fetchall()
    return {
        "total": total,
        "categories": {r["category"]: r["c"] for r in cats},
        "sources": {r["source"]: r["c"] for r in sources},
    }


def get_image_by_id(conn: sqlite3.Connection, image_id: int) -> dict | None:
    row = conn.execute("SELECT * FROM images WHERE id=?", (image_id,)).fetchone()
    return dict(row) if row else None


def get_suggest(conn: sqlite3.Connection, prefix: str, limit: int = 10) -> list:
    """Return tag and description matches for autocomplete."""
    suggestions = set()
    p = f"%{prefix}%"
    for row in conn.execute("SELECT tags FROM images WHERE tags LIKE ?", (p,)).fetchall():
        try:
            for t in json.loads(row["tags"]):
                if prefix.lower() in t.lower():
                    suggestions.add(t)
        except (json.JSONDecodeError, TypeError):
            pass
    for row in conn.execute(
        "SELECT DISTINCT description FROM images WHERE description LIKE ? LIMIT 20", (p,)
    ).fetchall():
        desc = row["description"]
        if desc and len(desc) <= 30:
            suggestions.add(desc)
    result = sorted(suggestions, key=lambda s: (not s.lower().startswith(prefix.lower()), len(s)))
    return result[:limit]


def toggle_favorite(conn: sqlite3.Connection, image_id: int) -> bool:
    """Toggle favorite status. Returns new favorite state."""
    img = get_image_by_id(conn, image_id)
    if not img:
        return False
    new_val = 0 if img.get("favorite") else 1
    conn.execute("UPDATE images SET favorite=?, updated_at=? WHERE id=?",
                 (new_val, datetime.now().isoformat(), image_id))
    conn.commit()
    return bool(new_val)


def delete_image(conn: sqlite3.Connection, image_id: int) -> bool:
    """Move to trash (soft delete). Use permanent_delete_image for hard delete."""
    return trash_image(conn, image_id)


def create_album(conn: sqlite3.Connection, name: str, description: str = "") -> int:
    now = datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO albums(name, description, created_at, updated_at) VALUES(?,?,?,?)",
        (name, description, now, now),
    )
    conn.commit()
    return cur.lastrowid


def list_albums(conn: sqlite3.Connection) -> list:
    sql = """SELECT a.*, COUNT(ai.image_id) as image_count
             FROM albums a LEFT JOIN album_images ai ON a.id=ai.album_id
             GROUP BY a.id ORDER BY a.updated_at DESC"""
    return [dict(r) for r in conn.execute(sql).fetchall()]


def get_album_images(conn: sqlite3.Connection, album_id: int) -> list:
    sql = """SELECT i.* FROM images i
             JOIN album_images ai ON i.id=ai.image_id
             WHERE ai.album_id=? ORDER BY COALESCE(i.taken_at, i.created_at) DESC"""
    return [dict(r) for r in conn.execute(sql, (album_id,)).fetchall()]


def add_to_album(conn: sqlite3.Connection, album_id: int, image_id: int):
    now = datetime.now().isoformat()
    conn.execute(
        "INSERT OR IGNORE INTO album_images(album_id, image_id, added_at) VALUES(?,?,?)",
        (album_id, image_id, now),
    )
    conn.execute("UPDATE albums SET updated_at=? WHERE id=?", (now, album_id))
    conn.commit()


def remove_from_album(conn: sqlite3.Connection, album_id: int, image_id: int):
    conn.execute("DELETE FROM album_images WHERE album_id=? AND image_id=?", (album_id, image_id))
    conn.commit()


def backup_db(max_backups: int = 5) -> str:
    """Create a timestamped backup of the database. Keeps at most max_backups copies."""
    import shutil
    import glob as g
    if not os.path.exists(DB_PATH):
        return ""
    backup_dir = os.path.join(VAULT_DIR, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(backup_dir, f"image_vault_{ts}.db")
    conn = get_db()
    bak = sqlite3.connect(dst)
    conn.backup(bak)
    bak.close()
    conn.close()
    backups = sorted(g.glob(os.path.join(backup_dir, "image_vault_*.db")))
    while len(backups) > max_backups:
        os.remove(backups.pop(0))
    return dst


def get_db_size_info() -> dict:
    """Return size information about the database."""
    if not os.path.exists(DB_PATH):
        return {"exists": False}
    size = os.path.getsize(DB_PATH)
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as c FROM images").fetchone()["c"]
    conn.close()
    return {"exists": True, "size_mb": round(size / 1024 / 1024, 2), "total_images": total}


# --- 地理位置 ---
def extract_gps_from_exif(filepath: str) -> tuple[float, float] | None:
    """从图片 EXIF 中提取 GPS 经纬度。返回 (lat, lng) 或 None。"""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        img = Image.open(filepath)
        exif = img._getexif()
        if not exif:
            return None
        gps_ifd = None
        for tag_id, value in exif.items():
            if TAGS.get(tag_id) == "GPSInfo":
                gps_ifd = value
                break
        if not gps_ifd:
            return None
        lat = _convert_to_degrees(gps_ifd.get(2))
        lon = _convert_to_degrees(gps_ifd.get(4))
        if lat is None or lon is None:
            return None
        if lat == 0.0 and lon == 0.0:
            return None
        lat_ref = gps_ifd.get(1, "")
        lon_ref = gps_ifd.get(3, "")
        if lat_ref == "S":
            lat = -lat
        if lon_ref == "W":
            lon = -lon
        return (lat, lon)
    except Exception:
        return None


def _convert_to_degrees(value) -> float | None:
    """Convert GPS DMS to decimal degrees."""
    if not value:
        return None
    try:
        import math
        d, m, s = value
        d, m, s = float(d), float(m), float(s)
        if math.isnan(d) or math.isnan(m) or math.isnan(s):
            return None
        result = d + m / 60 + s / 3600
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    except (TypeError, ValueError):
        return None


def trash_image(conn: sqlite3.Connection, image_id: int) -> bool:
    """软删除：设置 deleted_at 而非真正删除"""
    try:
        conn.execute("UPDATE images SET deleted_at=? WHERE id=? AND deleted_at IS NULL",
                     (datetime.now().isoformat(), image_id))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False


def restore_image(conn: sqlite3.Connection, image_id: int) -> bool:
    """从回收站恢复"""
    try:
        conn.execute("UPDATE images SET deleted_at=NULL WHERE id=?", (image_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False


def get_trash(conn: sqlite3.Connection) -> list:
    """获取回收站中的图片"""
    rows = conn.execute(
        "SELECT * FROM images WHERE deleted_at IS NOT NULL ORDER BY deleted_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def empty_trash(conn: sqlite3.Connection, older_than_days: int = 30) -> int:
    """永久删除回收站中超过指定天数的图片"""
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=older_than_days)).isoformat()
    rows = conn.execute(
        "SELECT id, vault_path, thumb_path, cover_path FROM images WHERE deleted_at IS NOT NULL AND deleted_at < ?",
        (cutoff,),
    ).fetchall()
    count = 0
    for row in rows:
        for p in [row["vault_path"], row["thumb_path"], row["cover_path"]]:
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass
        conn.execute("DELETE FROM album_images WHERE image_id=?", (row["id"],))
        conn.execute("DELETE FROM faces WHERE image_id=?", (row["id"],))
        conn.execute("DELETE FROM images WHERE id=?", (row["id"],))
        count += 1
    conn.commit()
    return count


def permanent_delete_image(conn: sqlite3.Connection, image_id: int) -> bool:
    """从回收站永久删除一张图片"""
    img = get_image_by_id(conn, image_id)
    if not img:
        return False
    for p in [img.get("vault_path"), img.get("thumb_path"), img.get("cover_path")]:
        if p and os.path.exists(p):
            try:
                os.remove(p)
            except OSError:
                pass
    conn.execute("DELETE FROM album_images WHERE image_id=?", (image_id,))
    conn.execute("DELETE FROM faces WHERE image_id=?", (image_id,))
    conn.execute("DELETE FROM images WHERE id=?", (image_id,))
    conn.commit()
    return True


# --- 标签编辑 ---
def add_tag(conn: sqlite3.Connection, image_id: int, tag: str) -> list:
    """给图片添加标签，返回更新后的标签列表"""
    img = get_image_by_id(conn, image_id)
    if not img:
        return []
    try:
        tags = json.loads(img.get("tags") or "[]")
    except (json.JSONDecodeError, TypeError):
        tags = []
    tag = tag.strip()
    if tag and tag not in tags:
        tags.append(tag)
        conn.execute("UPDATE images SET tags=?, updated_at=? WHERE id=?",
                     (json.dumps(tags, ensure_ascii=False), datetime.now().isoformat(), image_id))
        conn.commit()
    return tags


def remove_tag(conn: sqlite3.Connection, image_id: int, tag: str) -> list:
    """移除图片标签，返回更新后的标签列表"""
    img = get_image_by_id(conn, image_id)
    if not img:
        return []
    try:
        tags = json.loads(img.get("tags") or "[]")
    except (json.JSONDecodeError, TypeError):
        tags = []
    tag = tag.strip()
    if tag in tags:
        tags.remove(tag)
        conn.execute("UPDATE images SET tags=?, updated_at=? WHERE id=?",
                     (json.dumps(tags, ensure_ascii=False), datetime.now().isoformat(), image_id))
        conn.commit()
    return tags


# --- 重复检测 ---
def get_config(conn: sqlite3.Connection, key: str, default: str = None) -> str | None:
    """读取配置"""
    try:
        row = conn.execute("SELECT value FROM config WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default
    except Exception:
        return default


def set_config(conn: sqlite3.Connection, key: str, value: str):
    """写入配置"""
    conn.execute("INSERT OR REPLACE INTO config(key, value) VALUES(?, ?)", (key, value))
    conn.commit()


def get_all_config(conn: sqlite3.Connection) -> dict:
    """读取所有配置"""
    try:
        rows = conn.execute("SELECT key, value FROM config").fetchall()
        return {r["key"]: r["value"] for r in rows}
    except Exception:
        return {}


# --- 内存缓存层 ---
import time as _time

_cache = {}
_cache_ttl = {}
CACHE_DEFAULT_TTL = 60


def cache_get(key: str):
    """从缓存读取，过期返回 None"""
    if key in _cache and _cache_ttl.get(key, 0) > _time.time():
        return _cache[key]
    _cache.pop(key, None)
    _cache_ttl.pop(key, None)
    return None


def cache_set(key: str, value, ttl: int = CACHE_DEFAULT_TTL):
    _cache[key] = value
    _cache_ttl[key] = _time.time() + ttl


def cache_invalidate(prefix: str = ""):
    """清除匹配前缀的缓存"""
    if not prefix:
        _cache.clear()
        _cache_ttl.clear()
    else:
        keys = [k for k in _cache if k.startswith(prefix)]
        for k in keys:
            _cache.pop(k, None)
            _cache_ttl.pop(k, None)


# --- Live Photo ---
if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
