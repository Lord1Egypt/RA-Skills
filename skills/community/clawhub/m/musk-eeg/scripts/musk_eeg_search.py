#!/usr/bin/env python3
"""
Musk-EEG 检索脚本

两种调用方式：
  1. JSON 模式：
       python musk_eeg_search.py '{"query":"P300", "top_k":3}'
       python musk_eeg_search.py '{"query":"睡眠", "fuzzy":true}'

  2. CLI 直接模式：
       python musk_eeg_search.py --query "epilepsy" --top-k 3
       python musk_eeg_search.py --query "脑电" --fuzzy

数据库查找顺序（全部相对于脚本所在目录）：
  1. ../data/knowledge_new_fixed.db          ← 直接用
  2. ../data/knowledge_new_fixed.db.zip      ← 自动解压后再用
  3. ../../eeg-wiki-rag/data/*.db            ← eeg-wiki-rag 共享只读回退
"""
import sys
import json
import sqlite3
import re
import argparse
import zipfile
from pathlib import Path

# ── 修复 Windows GBK 终端 Unicode 输出问题 ──────────────────
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── 基于脚本所在目录向上查找 data/ ─────────────────────────
# 脚本可能在 scripts/ 子目录，也可能在 skill 根目录
# 向上遍历父目录，直到找到 data/ 目录为止
SCRIPT_PATH = Path(__file__).resolve()
CANDIDATE_DIRS = [SCRIPT_PATH.parent, SCRIPT_PATH.parent.parent, SCRIPT_PATH.parent.parent.parent]

DATA_DIR = None
for d in CANDIDATE_DIRS:
    data_dir = d / "data"
    # 目录存在 + 里面有 db 或 zip 才算有效
    if data_dir.is_dir() and (
        (data_dir / "knowledge_new_fixed.db").exists()
        or (data_dir / "knowledge_new_fixed.db.zip").exists()
    ):
        DATA_DIR = data_dir
        break

if DATA_DIR is None:
    # 最后一搏：更上层目录找（不验证文件存在，由 _init_db_path 报错）
    for parent in SCRIPT_PATH.parents:
        if (parent / "data").is_dir():
            DATA_DIR = parent / "data"
            break

if DATA_DIR is None:
    print("[musk_eeg] 未找到 data/ 目录", file=sys.stderr)
    sys.exit(1)

LOCAL_DB  = DATA_DIR / "knowledge_new_fixed.db"
ZIP_DB    = DATA_DIR / "knowledge_new_fixed.db.zip"
SHARED_DB = (DATA_DIR.parent / "eeg-wiki-rag" / "data"
             / "knowledge_new_fixed.db")

DB_PATH = None


def _init_db_path():
    """查找或解压数据库，优先用本地，其次解压 zip，最后共享回退。"""
    global DB_PATH

    if LOCAL_DB.exists():
        DB_PATH = LOCAL_DB
        return

    if ZIP_DB.exists():
        with zipfile.ZipFile(ZIP_DB, "r") as zf:
            zf.extractall(str(DATA_DIR))
        if LOCAL_DB.exists():
            DB_PATH = LOCAL_DB
            print(
                f"[musk_eeg] zip → db 解压完成 ({LOCAL_DB.stat().st_size // 1024 // 1024} MB)"
                f"  路径: {LOCAL_DB}",
                file=sys.stderr,
            )
            return
        print(f"[musk_eeg] zip 内容异常，缺少 knowledge_new_fixed.db", file=sys.stderr)
        sys.exit(1)

    if SHARED_DB.exists():
        DB_PATH = SHARED_DB
        print(
            f"[musk_eeg] 使用 eeg-wiki-rag 共享数据库: {SHARED_DB}",
            file=sys.stderr,
        )
        return

    print(
        "[musk_eeg] 未找到数据库。\n"
        "请确认 data/ 目录存在 knowledge_new_fixed.db"
        " 或 knowledge_new_fixed.db.zip（会自动解压）。",
        file=sys.stderr,
    )
    sys.exit(1)


_init_db_path()


def _should_fuzzy(q: str) -> bool:
    """中文或短词走模糊搜索；含中文的混合查询也走 fuzzy（中文不分词）。"""
    if re.search(r"[\u4e00-\u9fff]", q):
        return True
    return len(q) < 3 or not re.search(r"[a-zA-Z]{3,}", q)


def eeg_wiki_search(query: str, top_k: int = 5, fuzzy: bool = False) -> dict:
    """
    检索 EEG 维基百科数据库。

    返回字段：
      query, total, results[{
        title, category, keywords, core_definition,
        mechanism, musk_insight, rank, match_field, source
      }]
    """
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    top_k = min(top_k, 20)
    q = query.strip()

    if not q:
        conn.close()
        return {"query": q, "total": 0, "results": []}

    use_fuzzy = fuzzy or _should_fuzzy(q)

    # ── 修正：fuzzy 路径分词 OR 匹配 ──────────────────────────────────
    if use_fuzzy:
        terms = q.split()
        if len(terms) == 1:
            # 单词：直接 LIKE
            like_q = f"%{terms[0]}%"
            cur.execute(
                f"""SELECT title, keywords, core_definition, mechanism, category,
                           musk_insight, 'fuzzy' AS match_field
                    FROM eeg_wiki_raw
                    WHERE (title LIKE ?
                       OR keywords LIKE ?
                       OR core_definition LIKE ?)
                      AND (keywords IS NOT NULL AND keywords != ''
                        OR core_definition IS NOT NULL AND core_definition != '')
                    LIMIT ?""",
                [like_q, like_q, like_q, top_k],
            )
            rows = cur.fetchall()
        else:
            # 多词：每词独立 OR 匹配，再 UNION 去重
            term_conditions = " OR ".join(
                ["(title LIKE ? OR keywords LIKE ? OR core_definition LIKE ?)"] * len(terms)
            )
            like_args = [f"%{t}%" for t in terms for _ in range(3)]
            cur.execute(
                f"""SELECT DISTINCT title, keywords, core_definition, mechanism,
                                   category, musk_insight, 'fuzzy' AS match_field
                    FROM eeg_wiki_raw
                    WHERE ({term_conditions})
                      AND (keywords IS NOT NULL AND keywords != ''
                        OR core_definition IS NOT NULL AND core_definition != '')
                    LIMIT ?""",
                like_args + [top_k],
            )
            rows = cur.fetchall()
        total = len(rows)

    # ── 修正：FTS 路径支持混合中英文 ─────────────────────────────────
    else:
        en_parts = [t for t in q.split() if re.search(r"[a-zA-Z]{2,}", t)]
        zh_parts = [t for t in q.split() if re.search(r"[\u4e00-\u9fff]", t)]

        if en_parts and zh_parts:
            # 混合：中→fuzzy（LIKE），英→FTS，分开查再合并去重
            en_q = " ".join(en_parts)
            zh_like_args = [f"%{t}%" for t in zh_parts for _ in range(3)]

            # FTS 英文部分（prefix search）
            cur.execute(
                f"""SELECT DISTINCT b.title, b.keywords, b.core_definition,
                                   b.mechanism, b.category, b.musk_insight,
                                   'fts' AS match_field,
                                   -bm25(eeg_wiki) AS sort_rank
                    FROM eeg_wiki
                    JOIN eeg_wiki_raw b ON b.title = eeg_wiki.title
                    WHERE eeg_wiki MATCH '"' || ? || '"*'
                      AND (b.keywords IS NOT NULL AND b.keywords != ''
                        OR b.core_definition IS NOT NULL AND b.core_definition != '')
                    LIMIT ?""",
                [en_q, top_k],
            )
            fts_rows = cur.fetchall()

            # Fuzzy 中文部分
            if zh_like_args:
                term_conditions = " OR ".join(
                    ["(title LIKE ? OR keywords LIKE ? OR core_definition LIKE ?)"] * len(zh_parts)
                )
                cur.execute(
                    f"""SELECT DISTINCT title, keywords, core_definition,
                                       mechanism, category, musk_insight,
                                       'fuzzy' AS match_field, 0.0 AS sort_rank
                        FROM eeg_wiki_raw
                        WHERE ({term_conditions})
                          AND (keywords IS NOT NULL AND keywords != ''
                            OR core_definition IS NOT NULL AND core_definition != '')
                        LIMIT ?""",
                    zh_like_args + [top_k],
                )
                fuzzy_rows = cur.fetchall()
            else:
                fuzzy_rows = []

            # 合并去重（按 title）
            seen = set()
            merged = []
            for r in sorted(fts_rows, key=lambda x: x[-1]) + sorted(fuzzy_rows, key=lambda x: x[-1]):
                if r[0] not in seen:
                    seen.add(r[0])
                    merged.append(r)
            rows = merged[:top_k]

        elif en_parts:
            # 纯英文：FTS BM25
            en_q = " ".join(en_parts)
            cur.execute(
                f"""SELECT b.title, b.keywords, b.core_definition, b.mechanism,
                             b.category, b.musk_insight,
                            -bm25(eeg_wiki) AS sort_rank,
                             'fts' AS match_field
                    FROM eeg_wiki
                    JOIN eeg_wiki_raw b ON b.title = eeg_wiki.title
                    WHERE eeg_wiki MATCH '"' || ? || '"*'
                      AND (b.keywords IS NOT NULL AND b.keywords != ''
                        OR b.core_definition IS NOT NULL AND b.core_definition != '')
                    ORDER BY sort_rank
                    LIMIT ?""",
                [en_q, top_k],
            )
            rows = cur.fetchall()

        else:
            # 纯中文：走 fuzzy（此时 use_fuzzy 应为 True，但兜底）
            zh_q = zh_parts[0] if zh_parts else q
            cur.execute(
                f"""SELECT title, keywords, core_definition, mechanism, category,
                           musk_insight, 'fuzzy' AS match_field
                    FROM eeg_wiki_raw
                    WHERE (title LIKE ? OR keywords LIKE ? OR core_definition LIKE ?)
                      AND (keywords IS NOT NULL AND keywords != ''
                        OR core_definition IS NOT NULL AND core_definition != '')
                    LIMIT ?""",
                [f"%{zh_q}%", f"%{zh_q}%", f"%{zh_q}%", top_k],
            )
            rows = cur.fetchall()

        total = len(rows)

    results = []
    for row in rows:
        if use_fuzzy:
            title, keywords, core_def, mechanism, cat, musk_ins, match_field = row
            rank = 0.0
        else:
            title, keywords, core_def, mechanism, cat, musk_ins, rank, match_field = row

        results.append(
            {
                "title": title,
                "category": cat or "",
                "keywords": keywords or "",
                "core_definition": core_def or "",
                "mechanism": mechanism or "",
                "musk_insight": musk_ins or "",
                "rank": round(float(rank), 3) if rank else 0.0,
                "match_field": match_field,
                "source": "RAG_RETRIEVAL",
            }
        )

    conn.close()
    return {"query": q, "total": total, "results": results}


def format_text(result: dict) -> str:
    """格式化检索结果（CLI 人工阅读用）。"""
    if not result["results"]:
        return f"❓ 未找到「{result['query']}」相关内容。\n"

    lines = []
    lines.append(f"🔍 检索「{result['query']}」| {result['total']} 条匹配\n" + "=" * 60)

    for i, item in enumerate(result["results"], 1):
        lines.append(f"\n📖 词条 {i}: {item['title']}")
        lines.append(f"   分类: {item['category'] or '未知'}")
        kw = item["keywords"]
        lines.append(f"   关键词: {kw[:150]}{'...' if len(kw) > 150 else ''}")

        cd = item["core_definition"]
        if cd:
            lines.append(f"   定义: {cd[:300]}{'...' if len(cd) > 300 else ''}")

        mech = item["mechanism"]
        if mech:
            lines.append(f"   机制: {mech[:200]}{'...' if len(mech) > 200 else ''}")

        mi = item.get("musk_insight", "")
        if mi:
            lines.append(f"   💡 马斯克视角: {mi[:200]}{'...' if len(mi) > 200 else ''}")

        lines.append(f"   [来源：{item['title']}]")

    lines.append("\n" + "=" * 60)
    lines.append(
        "\n请用马斯克的语气、第一人称，参考以上标注了 [来源：xxx] 的词条内容回答。"
        "只引用检索到的词条，不要掺入你自己的知识。"
    )

    return "\n".join(lines)


def main():
    # ── JSON script 模式 ─────────────────────────────────────
    if len(sys.argv) > 1 and sys.argv[1].startswith("{"):
        try:
            params = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}", file=sys.stderr)
            sys.exit(1)

        query = params.get("query", "")
        top_k = int(params.get("top_k", params.get("limit", 5)))
        fuzzy = bool(params.get("fuzzy", False))

        result = eeg_wiki_search(query, top_k=top_k, fuzzy=fuzzy)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    # ── CLI 模式 ─────────────────────────────────────────────
    else:
        parser = argparse.ArgumentParser(description="Musk-EEG 维基百科检索")
        parser.add_argument("query", nargs="?", default=None)
        parser.add_argument("--query", "-q", dest="query2")
        parser.add_argument("--top-k", "-k", type=int, default=5)
        parser.add_argument("--fuzzy", "-f", action="store_true")
        parser.add_argument("--json", "-j", action="store_true")
        args = parser.parse_args()

        q = args.query or args.query2 or ""
        if not q:
            print("错误：需要传入查询词。", file=sys.stderr)
            sys.exit(1)

        result = eeg_wiki_search(q, top_k=args.top_k, fuzzy=args.fuzzy)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_text(result))


if __name__ == "__main__":
    main()
