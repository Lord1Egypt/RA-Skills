#!/usr/bin/env python3
"""
memory-booster 智能搜索 v4
语义搜索优先（chromadb + sentence-transformers）
索引新鲜度自动检查 + 自动重建
关键词 grep 降级（无索引 / chromadb 不可用时）
输出：按相似度排序，融合语义 + 关键词双重打分
"""
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 国内 HuggingFace 镜像（加速模型下载）
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# 从 config_loader 获取路径
from config_loader import load_config, get_memory_files, get_memory_md_path
MEMORY_DIRS_RAW, CHROMA_DB_DIR = load_config()
MEMORY_DIRS = [Path(d) for d in MEMORY_DIRS_RAW]
INDEX_DIR = Path(CHROMA_DB_DIR)
FRESHNESS_FILE = INDEX_DIR / ".last_indexed"


# ---- 新鲜度检查 ----

def get_latest_file_mtime():
    """返回所有记忆文件中最新的修改时间"""
    latest = None
    for mem_dir in MEMORY_DIRS:
        if not mem_dir.is_dir():
            continue
        for fpath in mem_dir.iterdir():
            if fpath.suffix != ".md":
                continue
            try:
                mtime = fpath.stat().st_mtime
                if latest is None or mtime > latest:
                    latest = mtime
            except OSError:
                continue
    return latest


def check_freshness(verbose=True):
    """
    检查索引是否覆盖了所有记忆文件。
    返回 True 表示索引新鲜，False 表示需要重建。
    """
    if not INDEX_DIR.exists():
        return False

    # 读取上次索引时间戳
    last_indexed = 0
    if FRESHNESS_FILE.exists():
        try:
            last_indexed = float(FRESHNESS_FILE.read_text().strip())
        except (ValueError, IOError):
            last_indexed = 0

    latest_mtime = get_latest_file_mtime()
    if latest_mtime is None:
        return True  # 没有记忆文件，视为新鲜

    if latest_mtime > last_indexed:
        if verbose:
            newest = datetime.fromtimestamp(latest_mtime).strftime("%Y-%m-%d %H:%M")
            indexed = datetime.fromtimestamp(last_indexed).strftime("%Y-%m-%d %H:%M") if last_indexed else "从未"
            print(f"⚠️  索引已过期！最新文件: {newest}，索引时间: {indexed}")
            print(f"   自动重建索引...")
        return False

    return True


def write_freshness_timestamp():
    """写入当前时间戳到 .last_indexed"""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().timestamp()
    FRESHNESS_FILE.write_text(str(now))


def auto_rebuild_index(verbose=True):
    """自动重建索引（调用 index_memory.py）"""
    index_script = Path(__file__).parent / "index_memory.py"
    if not index_script.exists():
        if verbose:
            print(f"⚠️  index_memory.py 不存在: {index_script}")
        return False

    if verbose:
        print(f"🔄 自动重建语义索引...")

    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, str(index_script), "--force"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            write_freshness_timestamp()
            if verbose:
                # 提取关键输出行
                for line in result.stdout.splitlines():
                    if "索引完成" in line or "chunks" in line:
                        print(f"  ✅ {line.strip()}")
            return True
        else:
            if verbose:
                print(f"  ⚠️ 索引重建失败: {result.stderr[:200]}")
            return False
    except Exception as e:
        if verbose:
            print(f"  ⚠️ 索引重建异常: {e}")
        return False


# ---- 语义搜索 ----

def semantic_search(query, days=14, top_k=10, auto_rebuild=True):
    """使用 chromadb 语义搜索，返回 (results, model_available)"""
    try:
        import chromadb
    except ImportError:
        return None, False

    if not INDEX_DIR.exists():
        # 索引不存在，尝试自动构建
        if auto_rebuild:
            auto_rebuild_index()
        if not INDEX_DIR.exists():
            return None, False

    # 检查新鲜度，过期则自动重建
    if auto_rebuild and not check_freshness(verbose=True):
        auto_rebuild_index()

    try:
        client = chromadb.PersistentClient(path=str(INDEX_DIR))
        collection = client.get_collection("workbuddy_memory")
    except Exception:
        if auto_rebuild:
            auto_rebuild_index()
            try:
                client = chromadb.PersistentClient(path=str(INDEX_DIR))
                collection = client.get_collection("workbuddy_memory")
            except Exception:
                return None, False
        else:
            return None, False

    if collection.count() == 0:
        return None, False

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return None, False

    # 加载模型（轻量，CPU 友好）
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query], show_progress_bar=False)

    # 计算日期截止
    cutoff = (datetime.now() - timedelta(days=days))
    cutoff_str = cutoff.strftime("%Y-%m-%d")

    # 搜索（取 top_k*3，后面过滤日期）
    results_raw = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=min(top_k * 3, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    # 整理结果
    results = []
    if results_raw["ids"] and results_raw["ids"][0]:
        for doc_id, doc, meta, dist in zip(
            results_raw["ids"][0],
            results_raw["documents"][0],
            results_raw["metadatas"][0],
            results_raw["distances"][0]
        ):
            date = meta.get("date", "unknown")
            # 日期过滤（MEMORY.md 不限制日期）
            if meta.get("file") != "MEMORY.md" and date != "unknown":
                try:
                    if datetime.strptime(date, "%Y-%m-%d") < cutoff:
                        continue
                except ValueError:
                    pass

            # 相似度转得分（cosine distance → 0-100 分）
            similarity = max(0, 1 - dist)  # cosine: dist 0=identical, dist 2=opposite
            score = int(similarity * 100)

            results.append({
                "file": meta.get("file", "unknown"),
                "score": score,
                "match": doc[:150].strip(),
                "context": doc[:300].strip(),
                "source": "semantic",
                "chunk_idx": meta.get("chunk_idx", 0)
            })

    # 去重 + 按得分排序 + 限制 top_k
    seen = set()
    deduped = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        key = (r["file"], r["chunk_idx"])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
            if len(deduped) >= top_k:
                break

    return deduped, True


# ---- 关键词 grep（降级方案） ----

def keyword_search(query, days=14, top_k=8):
    """关键词 grep 搜索，语义搜索不可用时使用"""
    results = []
    cutoff = datetime.now() - timedelta(days=days)

    keywords = [kw.strip() for kw in query.split() if kw.strip()]
    if not keywords:
        keywords = [query]

    patterns = [re.compile(re.escape(kw), re.IGNORECASE) for kw in keywords]
    scanned_files = set()

    for mem_dir in [d for d in MEMORY_DIRS if d.is_dir()]:
        for fpath in sorted(mem_dir.iterdir()):
            fname = fpath.name
            if not fname.endswith(".md") or fname in scanned_files:
                continue
            scanned_files.add(fname)

            if fname != "MEMORY.md":
                try:
                    fdate = datetime.strptime(fname.replace(".md", ""), "%Y-%m-%d")
                    if fdate < cutoff:
                        continue
                except ValueError:
                    pass

            try:
                with open(fpath, "r") as f:
                    lines = f.read().split("\n")
            except Exception:
                continue

            matched_lines = []
            keyword_hits = set()
            for i, line in enumerate(lines):
                for j, pat in enumerate(patterns):
                    if pat.search(line):
                        matched_lines.append(i)
                        keyword_hits.add(j)

            if not matched_lines:
                continue

            score = len(keyword_hits) * 10 + len(matched_lines)
            best_idx = matched_lines[0]
            ctx_start = max(0, best_idx - 2)
            ctx_end = min(len(lines), best_idx + 3)
            ctx = "\n".join(lines[ctx_start:ctx_end]).strip()

            results.append({
                "file": fname,
                "score": score,
                "match": lines[best_idx].strip()[:150],
                "context": ctx[:300],
                "source": "keyword"
            })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]


# ---- 融合搜索 ----

def search(query, days=14, top_k=10, auto_rebuild=True):
    """融合搜索：语义优先 → 关键词降级"""
    # 尝试语义搜索
    sem_results, sem_available = semantic_search(query, days, top_k, auto_rebuild=auto_rebuild)

    if sem_results:
        return True, sem_results

    # 降级到关键词搜索
    kw_results = keyword_search(query, days, top_k)
    return False, kw_results


# ---- CLI ----

def main():
    if len(sys.argv) < 2:
        print("用法: search_memory.py <查询> [天数] [--no-semantic] [--no-rebuild]")
        sys.exit(1)

    query = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 14
    no_semantic = "--no-semantic" in sys.argv
    no_rebuild = "--no-rebuild" in sys.argv

    if no_semantic:
        results = keyword_search(query, days)
        used_semantic = False
    else:
        used_semantic, results = search(query, days, auto_rebuild=not no_rebuild)

    if not results:
        print(f"未找到与「{query}」相关的记忆")
        return

    mode = "🧠 语义" if used_semantic else "🔤 关键词"
    print(f"{mode}搜索找到 {len(results)} 条与「{query}」相关的结果\n")

    for i, r in enumerate(results):
        tag = "长期记忆" if r["file"] == "MEMORY.md" else "日记"
        print(f"#{i+1} [{tag}] {r['file']} (相似度:{r['score']}%)")
        print(f"   匹配: {r['match'][:150]}")
        print("-" * 60)


if __name__ == "__main__":
    main()
