"""
knowledge_bridge.py — 本地化技能: 知识桥
将洞察引擎采集的知识自动导入知识库
"""
import sys, os, json
from pathlib import Path

_SRC = Path(__file__).parent.parent.parent / "db"


def run(query: str = "stats") -> dict:
    """执行知识桥技能
    Args:
        query: ingest | search <term> | stats | backfill | explain <term>
    Returns:
        dict: 操作结果
    """
    sys.path.insert(0, str(_SRC))
    try:
        from knowledge_bridge import (
            ingest_latest_cycle, get_kb_stats, search_knowledge,
            backfill_all_cycles, auto_explain
        )
    except ImportError as e:
        return {"ok": False, "error": f"导入 knowledge_bridge 模块失败: {e}"}

    q = query.strip().lower()

    if q == "ingest":
        n = ingest_latest_cycle()
        return {"ok": True, "action": "ingest", "count": n, "message": f"导入了 {n} 条知识"}

    if q == "stats":
        stats = get_kb_stats()
        return {"ok": True, "action": "stats", "stats": stats}

    if q == "backfill":
        n = backfill_all_cycles()
        return {"ok": True, "action": "backfill", "count": n, "message": f"回溯了 {n} 个周期"}

    if q.startswith("search "):
        term = q[7:]
        results = search_knowledge(term, limit=10)
        return {"ok": True, "action": "search", "query": term, "count": len(results), "results": results}

    if q.startswith("explain "):
        term = q[8:]
        explanation = auto_explain(term)
        return {"ok": True, "action": "explain", "query": term, "explanation": explanation}

    return {"ok": False, "error": f"未知操作: {query}"}


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "stats"
    result = run(q)
    print(json.dumps(result, ensure_ascii=False, indent=2))
