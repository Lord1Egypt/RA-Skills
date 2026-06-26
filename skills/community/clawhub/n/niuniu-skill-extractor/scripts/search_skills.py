#!/usr/bin/env python3
"""
Search skills in the local skill repository.
Uses simple keyword matching with FTS5-like scoring.

Usage:
  python search_skills.py "query text"
  python search_skills.py "query text" --json
"""

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import List, Dict

SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "skill-extractor" / "skills"
DB_PATH = Path.home() / ".openclaw" / "workspace" / "skills" / "skill-extractor" / "skills.db"

# Stop words for filtering
STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "and", "but", "if", "or", "because", "until", "while",
    "this", "that", "these", "those", "it", "its", "they", "them", "their",
    "what", "which", "who", "whom", "one", "two", "three", "four", "five",
}


def init_db():
    """Initialize SQLite FTS5 database for skill search"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS skills_fts USING fts5(
            name, description, when_to_use, steps, content,
            content_rowid='rowid'
        )
    """)
    
    # Check if we need to index existing skills
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skills_meta (
            rowid INTEGER PRIMARY KEY,
            filename TEXT UNIQUE,
            last_modified REAL
        )
    """)
    conn.commit()
    conn.close()


def index_skill_file(filepath: Path):
    """Index a single skill file into FTS5"""
    content = filepath.read_text(encoding="utf-8")
    
    # Extract frontmatter
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
    
    # Parse frontmatter
    name = re.search(r"name:\s*(.+)", frontmatter).group(1).strip() if re.search(r"name:\s*(.+)", frontmatter) else filepath.stem
    description = re.search(r"description:\s*(.+)", frontmatter).group(1).strip() if re.search(r"description:\s*(.+)", frontmatter) else ""
    
    # Extract markdown sections
    when_to_use = re.search(r"## When to Use\s*\n(.+?)(?=\n##|\n---)", content, re.DOTALL)
    when_to_use = when_to_use.group(1).strip() if when_to_use else ""
    
    steps_match = re.search(r"## Procedure\s*\n(.+?)(?=\n##|\n---)", content, re.DOTALL)
    steps = steps_match.group(1).strip() if steps_match else ""
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT OR REPLACE INTO skills_fts (name, description, when_to_use, steps, content)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, when_to_use, steps, content))
    conn.execute("""
        INSERT OR REPLACE INTO skills_meta (filename, last_modified)
        VALUES (?, ?)
    """, (filepath.name, filepath.stat().st_mtime))
    conn.commit()
    conn.close()


def reindex_all():
    """Reindex all skill files"""
    init_db()
    
    for f in SKILLS_DIR.glob("*.md"):
        try:
            index_skill_file(f)
            print(f"  ✓ indexed: {f.name}")
        except Exception as e:
            print(f"  ✗ {f.name}: {e}")


def search(query: str, limit: int = 5) -> List[Dict]:
    """Search skills using FTS5"""
    init_db()
    
    # Check for new/changed files
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT filename, last_modified FROM skills_meta
    """)
    existing = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    
    for f in SKILLS_DIR.glob("*.md"):
        mtime = f.stat().st_mtime
        if f.name not in existing or existing[f.name] != mtime:
            try:
                index_skill_file(f)
            except:
                pass
    
    # Search with FTS5
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT name, description, when_to_use, content
        FROM skills_fts
        WHERE skills_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    
    results = []
    for row in cursor.fetchall():
        name, description, when_to_use, content = row
        # Extract skill file path
        skill_file = SKILLS_DIR / f"{name}.md"
        if not skill_file.exists():
            skill_file = list(SKILLS_DIR.glob(f"*_{name}*.md"))[0] if list(SKILLS_DIR.glob(f"*_{name}*.md")) else None
        
        results.append({
            "name": name,
            "description": description,
            "when_to_use": when_to_use[:100] + "..." if when_to_use and len(when_to_use) > 100 else when_to_use,
            "file": str(skill_file) if skill_file else None,
        })
    
    conn.close()
    return results


def main():
    parser = argparse.ArgumentParser(description="搜索技能库")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--reindex", action="store_true", help="重新索引所有技能")
    
    args = parser.parse_args()
    
    if args.reindex:
        print("重新索引技能库...")
        reindex_all()
        print("完成!")
        return
    
    results = search(args.query)
    
    if not results:
        print("没有找到相关技能")
        return
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"找到 {len(results)} 个相关技能:\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']}")
            print(f"   描述: {r['description']}")
            print(f"   触发: {r['when_to_use']}")
            print()


if __name__ == "__main__":
    main()
