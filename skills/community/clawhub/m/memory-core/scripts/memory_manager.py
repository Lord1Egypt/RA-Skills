import json

from config import get_config
from db_lance import LanceDBManager
from embedding import get_embedding


def classify(text: str):
    t = (text or "").lower()
    scene = "general"
    if any(w in t for w in ["python", "java", "code", "bug", "api", "framework", "library", "git", "npm", "pip"]):
        scene = "coding"
    elif any(w in t for w in ["wow", "warcraft", "game", "dps", "tank", "healer", "魔兽", "游戏"]):
        scene = "game"
    elif any(w in t for w in ["eat", "food", "sleep", "movie", "music", "life", "吃饭", "睡觉"]):
        scene = "life"
    elif any(w in t for w in ["work", "meeting", "project", "deadline", "pmo", "hr", "工作", "会议"]):
        scene = "work"

    intent = "statement"
    if "?" in text or any(w in t for w in ["what", "how", "why", "who", "when", "什么", "怎么", "为什么"]):
        intent = "query"
    if any(w in t for w in ["remember", "save", "store", "note", "记住", "保存"]):
        intent = "instruction"
    if any(w in t for w in ["forget", "删除", "忘记"]):
        intent = "forget"
    return intent, scene


def _read_openclaw_agent_model(agent_id: str) -> str:
    try:
        import os

        p = os.path.expanduser("~/.openclaw/openclaw.json")
        with open(p, "r") as f:
            cfg = json.load(f) or {}
        agents = (((cfg.get("agents") or {}).get("list")) or [])
        for a in agents:
            if (a or {}).get("id") == agent_id:
                return (((a.get("model") or {}).get("primary")) or "")
    except Exception:
        return ""
    return ""


def _infer_tier(agent_id: str, default_tier: str) -> str:
    m = (_read_openclaw_agent_model(agent_id) or "").lower()
    if not m:
        return default_tier or "medium"
    if any(k in m for k in ["claude", "k2p5", "m2.5", "opus", "sonnet"]):
        return "large"
    if any(k in m for k in ["flash", "mini", "glm-4-flash"]):
        return "small"
    if any(k in m for k in ["coder", "32b", "qwen2.5-coder"]):
        return "medium"
    if any(k in m for k in ["deepseek", "v3.2", "v3"]):
        return "medium"
    return default_tier or "medium"


class MemoryManager:
    def __init__(self):
        self.db = LanceDBManager()

    def ingest(self, agent_id: str, text: str):
        intent, scene = classify(text)
        vector = get_embedding(text)
        mid = self.db.add(vector, text, agent_id, scene, intent, metadata_json=json.dumps({}), weight=1.0)
        return {"status": "stored", "id": mid, "tags": {"intent": intent, "scene": scene}}

    def retrieve(self, agent_id: str, query: str, scene: str = ""):
        _, inferred_scene = classify(query)
        target_scene = scene or inferred_scene
        if not target_scene:
            target_scene = "general"
        cfg = get_config()
        mem_cfg = cfg.get("memory") or {}
        limit = int((cfg.get("lancedb") or {}).get("max_results") or 5)
        vector = get_embedding(query)
        if target_scene == "general":
            target_scene = inferred_scene or "general"
        memories = self.db.search(vector, agent_id, target_scene, limit)
        min_score = float(mem_cfg.get("min_score") or 0)
        if min_score > 0:
            memories = [m for m in memories if float(m.get("score") or 0) >= min_score]

        per_limit = int(mem_cfg.get("max_chars_per_memory") or 0)
        total_limit = int(mem_cfg.get("max_total_chars") or 0)
        if mem_cfg.get("auto_budget", True):
            tiers = mem_cfg.get("tiers") or {}
            tier = _infer_tier(agent_id, str(mem_cfg.get("default_tier") or "medium"))
            tier_cfg = (tiers.get(tier) or {}) if isinstance(tiers, dict) else {}
            per_limit = int(tier_cfg.get("max_chars_per_memory") or per_limit)
            total_limit = int(tier_cfg.get("max_total_chars") or total_limit)
        if per_limit > 0 or total_limit > 0:
            budget = total_limit if total_limit > 0 else None
            for m in memories:
                t = (m.get("text") or "")
                if per_limit > 0 and len(t) > per_limit:
                    m["text"] = t[:per_limit] + "…"
                    m["text_truncated"] = True
                else:
                    m["text"] = t
                    m["text_truncated"] = False
                if budget is None:
                    continue
                if budget <= 0:
                    m["text"] = ""
                    m["text_truncated"] = True
                    continue
                if len(m["text"]) > budget:
                    m["text"] = m["text"][:budget] + "…"
                    m["text_truncated"] = True
                budget -= len(m["text"])
        return {"query": query, "scene": target_scene, "memories": memories}

    def forget(self, memory_id: str):
        self.db.delete(memory_id)
        return {"status": "deleted", "id": memory_id}
