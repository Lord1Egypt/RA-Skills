#!/usr/bin/env python3
"""
文献管理器 - PDF元数据提取、索引、重命名

用法:
  python3 paper_manager.py index    # 扫描并索引所有PDF
  python3 paper_manager.py rename   # 按规范重命名
  python3 paper_manager.py search <关键词>  # 搜索
  python3 paper_manager.py status   # 查看索引状态

配置:
  配置文件: config.yaml (项目根目录)
  环境变量: PAPERMGR_* (如 PAPERMGR_DATABASE_PATH)
"""

import fitz
import sqlite3
import hashlib
import os
import re
import sys
import json
import glob
from datetime import datetime
from pathlib import Path

# Import configuration
from config import get_config

def get_db():
    """获取数据库连接"""
    cfg = get_config()
    conn = sqlite3.connect(cfg.db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    """初始化数据库（支持schema版本）"""
    conn = get_db()
    
    # Schema版本管理
    SCHEMA_VERSION = 1
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY,
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    current_version = conn.execute("SELECT MAX(version) as v FROM schema_version").fetchone()["v"] or 0
    
    if current_version < 1:
        # v1: 初始schema
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_hash TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                title TEXT,
                authors TEXT,
                doi TEXT,
                year INTEGER,
                journal TEXT,
                abstract TEXT,
                pages INTEGER,
                file_size INTEGER,
                indexed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                renamed INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_doi ON papers(doi);
            CREATE INDEX IF NOT EXISTS idx_year ON papers(year);
            CREATE INDEX IF NOT EXISTS idx_title ON papers(title);
            CREATE INDEX IF NOT EXISTS idx_authors ON papers(authors);
            CREATE INDEX IF NOT EXISTS idx_file_hash ON papers(file_hash);
        """)
        conn.execute("INSERT INTO schema_version (version) VALUES (1)")
    
    # 未来版本的迁移逻辑可以在这里添加
    # if current_version < 2:
    #     # 迁移到v2
    #     ...
    
    conn.commit()
    conn.close()

def extract_meta(pdf_path):
    """从PDF提取元数据"""
    result = {
        "pages": 0, "title": None, "authors": None,
        "doi": None, "year": None, "journal": None, "abstract": None
    }
    try:
        doc = fitz.open(pdf_path)
        result["pages"] = len(doc)
        
        # PDF metadata
        pm = doc.metadata or {}
        if pm.get("title") and len(pm["title"].strip()) > 5:
            result["title"] = pm["title"].strip()[:500]
        if pm.get("author") and len(pm["author"].strip()) > 2:
            result["authors"] = pm["author"].strip()[:500]
        if pm.get("keywords"):
            result["keywords"] = pm["keywords"].strip()
        
        # 从前3页提取文本
        text = ""
        for i in range(min(3, len(doc))):
            text += doc[i].get_text()
        doc.close()
        
        # 提取DOI
        doi_matches = re.findall(r'10\.\d{4,9}/[^\s,;"\']+', text)
        if doi_matches:
            doi_matches.sort(key=len, reverse=True)
            for d in doi_matches:
                if re.match(r'10\.\d{4,9}/\S{4,}', d):
                    result["doi"] = d.rstrip('.')
                    break
        
        # 提取年份
        years = re.findall(r'\b((?:19|20)\d{2})\b', text[:2000])
        if years:
            result["year"] = int(years[0])
        
        # 提取标题
        if not result["title"]:
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            candidates = []
            for l in lines[:20]:
                if len(l) < 15:
                    continue
                if l.startswith('10.'):
                    continue
                if re.match(r'^\d+$', l):
                    continue
                if re.match(r'^(Received|Accepted|Published|Keywords|Abstract|Introduction|DOI|http)', l, re.I):
                    continue
                if '©' in l and len(l) < 80:
                    continue
                candidates.append(l)
            if candidates:
                result["title"] = candidates[0][:500]
        
        # 提取作者
        if not result["authors"]:
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            for i, l in enumerate(lines[:15]):
                if result["title"] and result["title"] in l:
                    if i + 1 < len(lines):
                        author_line = lines[i + 1].strip()
                        if 5 < len(author_line) < 300 and not author_line.startswith('10.'):
                            result["authors"] = author_line[:500]
                            break
        
        # 提取摘要
        abs_match = re.search(
            r'(?:Abstract|ABSTRACT|摘要)[:\s]*\n?(.*?)(?:\n\s*\n|\n\s*(?:Keywords|KEYWORDS|关键词|Introduction|1[\.\s]|引言))',
            text, re.DOTALL | re.IGNORECASE
        )
        if abs_match:
            result["abstract"] = re.sub(r'\s+', ' ', abs_match.group(1).strip())[:1000]
        
        # 提取期刊名
        if result["doi"]:
            pass
        else:
            journal_match = re.search(r'(\w+\s+(?:Journal|Medicine|Surgery|Science|Letters|Biology|Physics|Chemistry|Review|Bio|Clinic))', text[:1000], re.I)
            if journal_match:
                result["journal"] = journal_match.group(1).strip()
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def index_all(progress=True):
    """扫描并索引所有PDF"""
    cfg = get_config()
    papers_dir = cfg.papers_dir
    
    init_db()
    conn = get_db()
    
    indexed = set(row[0] for row in conn.execute("SELECT file_hash FROM papers").fetchall())
    
    pdf_files = glob.glob(os.path.join(papers_dir, "*.pdf"))
    new_count = 0
    skip_count = 0
    error_count = 0
    
    total = len(pdf_files)
    for i, fpath in enumerate(pdf_files):
        if progress and i % 50 == 0:
            print(f"  处理中... {i}/{total}", file=sys.stderr, flush=True)
        
        try:
            with open(fpath, "rb") as f:
                fhash = hashlib.md5(f.read()).hexdigest()
            
            if fhash in indexed:
                skip_count += 1
                continue
            
            meta = extract_meta(fpath)
            fsize = os.path.getsize(fpath)
            
            conn.execute("""
                INSERT OR IGNORE INTO papers (file_hash, filename, filepath, title, authors, doi, year, journal, abstract, pages, file_size)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fhash, os.path.basename(fpath), fpath,
                meta.get("title"), meta.get("authors"), meta.get("doi"),
                meta.get("year"), meta.get("journal"), meta.get("abstract"),
                meta.get("pages", 0), fsize
            ))
            new_count += 1
        except Exception as e:
            error_count += 1
            print(f"  ERROR: {os.path.basename(fpath)}: {e}", file=sys.stderr)
    
    conn.commit()
    conn.close()
    
    print(f"索引完成: 新增 {new_count}, 跳过(已存在) {skip_count}, 错误 {error_count}")
    return new_count

def rename_all():
    """按规范重命名所有已索引文件"""
    cfg = get_config()
    papers_dir = cfg.papers_dir
    
    conn = get_db()
    papers = conn.execute("SELECT id, filepath, filename, title, year, doi, authors, renamed FROM papers WHERE renamed=0").fetchall()
    
    renamed = 0
    errors = 0
    for p in papers:
        try:
            year = p["year"] or "0000"
            title = p["title"] or os.path.splitext(p["filename"])[0]
            doi = p["doi"] or ""
            
            title = re.sub(r'[\\/:*?"<>|\n\r]', ' ', title)
            title = re.sub(r'\s+', ' ', title).strip()
            if len(title) > 120:
                title = title[:120]
            
            if doi:
                new_name = f"{year}_{title}_{doi.replace('/', '@')}.pdf"
            else:
                new_name = f"{year}_{title}.pdf"
            
            if len(new_name) > 200:
                title = title[:80]
                if doi:
                    new_name = f"{year}_{title}_{doi.replace('/', '@')[:30]}.pdf"
                else:
                    new_name = f"{year}_{title}.pdf"
            
            new_path = os.path.join(papers_dir, new_name)
            
            if os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(p["filepath"]):
                base, ext = os.path.splitext(new_name)
                c = 1
                while os.path.exists(os.path.join(papers_dir, f"{base}_{c}{ext}")):
                    c += 1
                new_path = os.path.join(papers_dir, f"{base}_{c}{ext}")
                new_name = os.path.basename(new_path)
            
            os.rename(p["filepath"], new_path)
            conn.execute("UPDATE papers SET filepath=?, filename=?, renamed=1 WHERE id=?",
                        (new_path, new_name, p["id"]))
            renamed += 1
        except Exception as e:
            errors += 1
            print(f"  RENAME ERROR: {p['filename']}: {e}", file=sys.stderr)
    
    conn.commit()
    conn.close()
    print(f"重命名完成: 成功 {renamed}, 错误 {errors}")

def search(keyword):
    """搜索论文"""
    conn = get_db()
    query = f"%{keyword}%"
    rows = conn.execute("""
        SELECT title, authors, year, doi, journal, pages, filename 
        FROM papers 
        WHERE title LIKE ? OR authors LIKE ? OR doi LIKE ? OR abstract LIKE ? OR journal LIKE ?
        ORDER BY year DESC
    """, (query, query, query, query, query)).fetchall()
    conn.close()
    
    if not rows:
        print(f"没有找到与 '{keyword}' 相关的论文")
        return
    
    print(f"找到 {len(rows)} 篇相关论文:\n")
    for i, r in enumerate(rows, 1):
        print(f"{i}. [{r['year'] or '?'}] {r['title'] or '未知标题'}")
        if r['authors']:
            print(f"   作者: {r['authors'][:100]}")
        if r['doi']:
            print(f"   DOI: {r['doi']}")
        print(f"   文件: {r['filename']}")
        print()

def status():
    """查看索引状态"""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    with_title = conn.execute("SELECT COUNT(*) FROM papers WHERE title IS NOT NULL").fetchone()[0]
    with_doi = conn.execute("SELECT COUNT(*) FROM papers WHERE doi IS NOT NULL").fetchone()[0]
    renamed = conn.execute("SELECT COUNT(*) FROM papers WHERE renamed=1").fetchone()[0]
    years = conn.execute("SELECT year, COUNT(*) as cnt FROM papers WHERE year IS NOT NULL GROUP BY year ORDER BY year DESC LIMIT 10").fetchall()
    conn.close()
    
    print(f"索引状态:")
    print(f"  总数: {total}")
    print(f"  有标题: {with_title}")
    print(f"  有DOI: {with_doi}")
    print(f"  已重命名: {renamed}")
    if years:
        print(f"  年份分布:")
        for y in years:
            print(f"    {y['year']}: {y['cnt']}篇")

def get_abstract(paper_id):
    """获取某篇论文的摘要"""
    conn = get_db()
    row = conn.execute("SELECT title, abstract FROM papers WHERE id=?", (paper_id,)).fetchone()
    conn.close()
    if row and row["abstract"]:
        print(f"标题: {row['title']}")
        print(f"摘要: {row['abstract']}")
    else:
        print("未找到摘要")

USAGE = """文献管理器 - PDF元数据提取、索引、重命名

用法:
  python3 paper_manager.py index    # 扫描并索引所有PDF
  python3 paper_manager.py rename   # 按规范重命名
  python3 paper_manager.py search <关键词>  # 搜索
  python3 paper_manager.py status   # 查看索引状态
  python3 paper_manager.py abstract <id>  # 查看摘要

配置:
  - config.yaml (项目根目录)
  - 环境变量 PAPERMGR_* (如 PAPERMGR_DATABASE_PATH)
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "index":
        index_all()
    elif cmd == "rename":
        rename_all()
    elif cmd == "search":
        search(" ".join(sys.argv[2:]))
    elif cmd == "status":
        status()
    elif cmd == "abstract":
        get_abstract(int(sys.argv[2]))
    else:
        print(f"未知命令: {cmd}")
        print(USAGE)
