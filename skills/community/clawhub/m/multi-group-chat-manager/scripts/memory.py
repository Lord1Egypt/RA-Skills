"""
轻量级液态记忆引擎
===================
基于艾宾浩斯遗忘曲线的拟人化记忆系统。
纯 Python 标准库实现，零外部依赖。

核心公式：
  score = e^(-λ * days_passed) + α * log(1 + access_count)
  
  λ（衰减率）= 0.05 —— 遗忘速度
  α（强化系数）= 0.2 —— 每次访问的记忆强化力度
"""

import json
import os
import sys
import time
import math
import hashlib
from pathlib import Path

# ── 从统一配置读取参数 ──
_script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_script_dir))
from config import load as load_config
_cfg = load_config()
LAMBDA_DECAY = _cfg["memory"]["lambda_decay"]
ALPHA_BOOST = _cfg["memory"]["alpha_boost"]
SCORE_THRESHOLD = _cfg["memory"]["score_threshold"]
NEW_MEMORY_SCORE = _cfg["memory"]["new_memory_score"]
AUTO_DECAY_INTERVAL = _cfg["memory"]["auto_decay_interval"]

# 自动衰减标记文件
SKILL_DIR = _script_dir.parent
LAST_DECAY_FILE = os.path.join(str(SKILL_DIR), ".last_decay")


def maybe_auto_decay(fm, force=False):
    """
    检查是否需要执行自动衰减。
    如果距离上次衰减已超过 auto_decay_interval，则执行。
    
    参数:
        fm: FluidMemory 实例
        force: 强制运行，忽略间隔检查
    
    返回:
        {"ran": bool, "archived": int, "message": str}
    """
    now = time.time()
    last = 0.0
    
    if os.path.exists(LAST_DECAY_FILE):
        try:
            with open(LAST_DECAY_FILE, "r") as f:
                last = float(f.read().strip())
        except (OSError, ValueError):
            last = 0.0
    
    elapsed = now - last
    
    if not force and elapsed < AUTO_DECAY_INTERVAL:
        remaining = AUTO_DECAY_INTERVAL - elapsed
        return {
            "ran": False,
            "archived": 0,
            "message": f"距上次衰减 {elapsed:.0f}s，下次在 {remaining:.0f}s 后"
        }
    
    archived = fm.decay_all()
    
    try:
        with open(LAST_DECAY_FILE, "w") as f:
            f.write(str(now))
    except OSError:
        pass
    
    return {
        "ran": True,
        "archived": archived,
        "message": f"衰减完成，归档 {archived} 条记忆"
    }


class FluidMemory:
    """
    轻量级液态记忆引擎。
    
    用法:
        fm = FluidMemory("/path/to/storage")
        fm.store("user_123", "喜欢玩空洞骑士", tags=["preferences"])
        results = fm.recall("user_123", query="游戏")
        fm.forget("user_123", keyword="空洞骑士")
        fm.decay_all()  # 定期维护
    """

    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def _filepath(self, user_id: str) -> str:
        return os.path.join(self.storage_dir, f"{user_id}.json")

    def _load(self, user_id: str) -> dict:
        path = self._filepath(user_id)
        if not os.path.exists(path):
            return {"user_id": user_id, "memories": []}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"user_id": user_id, "memories": []}

    def _save(self, user_id: str, data: dict):
        path = self._filepath(user_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _calc_score(self, created_at: float, access_count: int,
                    relevance: float = 1.0) -> float:
        """计算流体分数"""
        days = max(0, (time.time() - created_at) / 86400)
        decay = math.exp(-LAMBDA_DECAY * days)
        freq_boost = ALPHA_BOOST * math.log(1 + access_count)
        return (decay * relevance) + freq_boost

    def _mem_id(self, content: str) -> str:
        """生成唯一记忆 ID"""
        h = hashlib.md5(content.encode("utf-8")).hexdigest()[:8]
        return f"mem_{int(time.time() * 1000)}_{h}"

    # ══════════════════════════════════════════
    # 公开接口
    # ══════════════════════════════════════════

    def store(self, user_id: str, content: str, *,
              tags: list = None, field: str = "") -> str:
        """
        存储一条记忆。
        
        如果内容已存在，刷新其访问计数和分数（强化）。
        返回记忆 ID。
        """
        data = self._load(user_id)
        now = time.time()

        # 去重：如果完全相同的 content 已存在，刷新它
        for mem in data["memories"]:
            if mem["content"] == content:
                mem["last_accessed"] = now
                mem["access_count"] += 1
                mem["score"] = min(1.0, mem.get("score", 0.5) + 0.1)
                mem["status"] = "active"
                self._save(user_id, data)
                return mem["id"]

        # 新记忆
        entry = {
            "id": self._mem_id(content),
            "content": content,
            "tags": tags or [],
            "field": field,
            "created_at": now,
            "last_accessed": now,
            "access_count": 1,
            "score": NEW_MEMORY_SCORE,
            "status": "active",
        }
        data["memories"].append(entry)
        self._save(user_id, data)
        return entry["id"]

    def recall(self, user_id: str, *, query: str = "",
               tags: list = None, field: str = "",
               top_k: int = 5, min_score: float = SCORE_THRESHOLD) -> list:
        """
        唤起记忆——按流体分数排序，返回活跃记忆列表。

        每次调用会自动强化被命中的记忆（访问 +1）。
        分数低于阈值的记忆会被自动归档。
        """
        data = self._load(user_id)
        memories = data.get("memories", [])
        now = time.time()
        changed = False

        scored = []

        for mem in memories:
            if mem.get("status") != "active":
                continue

            # 计算查询相关性
            relevance = 1.0

            if query:
                # 中文匹配：优先用子串匹配，次选字符级重叠
                q_lower = query.lower()
                c_lower = mem["content"].lower()
                if q_lower in c_lower or c_lower in q_lower:
                    relevance = 0.9  # 子串匹配，强相关
                else:
                    # 字符级重叠
                    q_chars = set(q_lower)
                    c_chars = set(c_lower)
                    if q_chars and c_chars:
                        # 去掉空格和标点再算
                        q_clean = {ch for ch in q_chars if ch.strip()}
                        c_clean = {ch for ch in c_chars if ch.strip()}
                        if q_clean and c_clean:
                            overlap = len(q_clean & c_clean) / len(q_clean)
                            relevance = 0.2 + 0.5 * overlap

            if tags:
                mem_tags = set(mem.get("tags", []))
                query_tags = set(tags)
                if mem_tags & query_tags:
                    tag_score = len(mem_tags & query_tags) / max(len(query_tags), 1)
                    relevance = max(relevance, 0.5 + 0.5 * tag_score)

            if field and mem.get("field") == field:
                relevance = max(relevance, 0.8)  # 同字段给予较高分

            final_score = self._calc_score(
                mem["created_at"], mem["access_count"], relevance
            )

            # 强化：每次 recall 增加计数
            mem["access_count"] += 1
            mem["last_accessed"] = now
            mem["score"] = final_score

            if final_score >= min_score:
                scored.append((final_score, mem))
            else:
                # 极低分自动归档
                if final_score < min_score * 0.5:
                    mem["status"] = "archive"
                    changed = True

        if scored or changed:
            self._save(user_id, data)

        scored.sort(key=lambda x: -x[0])
        return [s[1] for s in scored[:top_k]]

    def get_memories_by_field(self, user_id: str, field: str) -> list:
        """
        获取指定字段的所有活跃记忆值（用于构造 structured profile）。
        返回按分数降序排列的 content 列表。
        """
        data = self._load(user_id)
        matched = []
        for mem in data.get("memories", []):
            if mem.get("status") != "active":
                continue
            if mem.get("field") == field:
                now = time.time()
                score = self._calc_score(
                    mem["created_at"], mem["access_count"]
                )
                if score >= SCORE_THRESHOLD:
                    matched.append((score, mem["content"]))
        matched.sort(key=lambda x: -x[0])
        return [m[1] for m in matched]

    def forget(self, user_id: str, keyword: str) -> bool:
        """主动遗忘：归档包含关键词的记忆"""
        data = self._load(user_id)
        found = False
        for mem in data["memories"]:
            if keyword in mem["content"] and mem.get("status") == "active":
                mem["status"] = "archive"
                found = True
        if found:
            self._save(user_id, data)
        return found

    def count_active(self, user_id: str = None) -> int:
        """统计活跃记忆数"""
        if user_id:
            data = self._load(user_id)
            return sum(1 for m in data.get("memories", [])
                       if m.get("status") == "active")
        total = 0
        for fname in os.listdir(self.storage_dir):
            if not fname.endswith(".json"):
                continue
            try:
                with open(os.path.join(self.storage_dir, fname),
                          "r", encoding="utf-8") as f:
                    data = json.load(f)
                total += sum(1 for m in data.get("memories", [])
                             if m.get("status") == "active")
            except (json.JSONDecodeError, OSError):
                continue
        return total

    def decay_all(self) -> int:
        """
        全局衰减扫描：遍历所有记忆，归档低于阈值的条目。
        返回归档条目数。
        """
        archived = 0
        for fname in os.listdir(self.storage_dir):
            if not fname.endswith(".json"):
                continue
            user_id = fname[:-5]
            data = self._load(user_id)
            now = time.time()
            changed = False
            for mem in data.get("memories", []):
                if mem.get("status") != "active":
                    continue
                score = self._calc_score(
                    mem["created_at"], mem["access_count"]
                )
                if score < SCORE_THRESHOLD * 0.5:
                    mem["status"] = "archive"
                    changed = True
                    archived += 1
            if changed:
                self._save(user_id, data)
        return archived

    def get_all_active(self, user_id: str) -> list:
        """
        获取指定用户所有字段的全部活跃记忆（不过滤字段）。
        返回列表，每个元素是完整记忆字典，按分数降序排列。
        """
        data = self._load(user_id)
        now = time.time()
        scored = []
        for mem in data.get("memories", []):
            if mem.get("status") != "active":
                continue
            score = self._calc_score(
                mem["created_at"], mem["access_count"]
            )
            if score >= SCORE_THRESHOLD:
                scored.append((score, mem))
        scored.sort(key=lambda x: -x[0])
        return [s[1] for s in scored]

    def reinforce(self, user_id: str, content_substring: str) -> int:
        """
        根据关键词匹配并强化记忆。
        遍历用户活跃记忆，如果 content 包含 content_substring，
        则增加 access_count、刷新 last_accessed、重算 score。
        返回被强化的记忆数量。
        """
        data = self._load(user_id)
        now = time.time()
        reinforced = 0
        for mem in data.get("memories", []):
            if mem.get("status") != "active":
                continue
            if content_substring.lower() in mem["content"].lower():
                mem["access_count"] += 1
                mem["last_accessed"] = now
                mem["score"] = self._calc_score(
                    mem["created_at"], mem["access_count"]
                )
                reinforced += 1
        if reinforced > 0:
            self._save(user_id, data)
        return reinforced

    @staticmethod
    def _extract_keywords(content: str) -> list:
        """
        从记忆内容中提取有意义的匹配关键词。
        返回多个粒度的关键词（最完整 + 核心名词）。
        覆盖常见中文动作句式和独立名词提取。
        """
        import re

        # 常见中文动作前缀（按长度降序优先匹配）
        # 覆盖：喜欢做某事、正在做某事、经常做某事、想/会/能/在做某事
        prefixes = sorted([
            # 喜欢 + 动词
            "喜欢吃", "喜欢打", "喜欢玩", "喜欢看", "喜欢听",
            "喜欢写", "喜欢画", "喜欢做", "喜欢搞", "喜欢学",
            "喜欢研究", "喜欢创作", "喜欢分享", "喜欢讨论",
            # 正在 + 动词
            "正在自学", "正在学习", "正在玩", "正在做", "正在看",
            "正在写", "正在画", "正在搞", "正在研究",
            # 经常/偶尔 + 动词
            "经常熬夜", "经常玩", "经常打", "经常看", "经常写",
            "经常熬夜打",
            # 单双字前缀（先长后短）
            "喜欢",
            "在自学", "在学习", "在研究", "在开发",
            "在玩", "在打", "在看", "在写", "在画",
            "在做", "在搞", "在学",
            "想要", "希望",
            "正在", "可以", "经常", "偶尔", "总是",
            "推荐了", "分享了一个",
            "自学", "学习", "研究", "开发",
            "玩", "打", "写", "画", "做", "搞", "看", "听",
            "推荐", "分享", "讨论",
            "会", "想", "要", "能", "在",
            "爱玩", "爱吃", "爱打", "爱看", "爱听",
            "爱写", "爱画", "爱做", "爱搞", "爱学",
        ], key=lambda x: -len(x))

        # 常见虚词/标点——去掉不改变语义的部分
        removals = {"的", "和", "与", "了", "着", "过", "就", "还",
                    "，", "、", "。", "！", "？", "：", "；", "…", "～"}

        # 提取所有关键词（多粒度）
        keywords = set()

        # ============ 基础策略

        # 1️⃣ 完整内容本身作为一个关键词
        if len(content) >= 2:
            keywords.add(content)

        # 去掉虚词得到纯骨干文本
        text = "".join(ch for ch in content if ch not in removals)

        # ============ 去前缀策略

        # 2️⃣ 去掉动作前缀，获取核心名词/主题词
        stripped = text
        for p in prefixes:
            if stripped.startswith(p):
                stripped = stripped[len(p):]
                break

        # 3️⃣ 如果没找到前缀，尝试「爱/在」等单字动词剥离
        if stripped == text:
            single_verbs = {"爱", "想", "会", "能", "要", "在",
                           "有", "被", "去", "来", "上", "搞"}
            for sv in single_verbs:
                if stripped.startswith(sv):
                    stripped = stripped[len(sv):]
                    break

        if stripped and len(stripped) >= 2:
            keywords.add(stripped)

        # ============ 英文/数字部分

        # 4️⃣ 提取独立 English/numeric 词
        eng_parts = re.findall(r'[a-zA-Z][a-zA-Z0-9._\-+#]+', content)
        for e in eng_parts:
            if len(e) >= 2:
                keywords.add(e)

        # ============ 中文 n-gram 子串提取（精选版，避免噪音）

        # 5️⃣ 从原内容中提取有语义的 2-4 字中文片段
        #    只取头尾，避免中间段噪音子串占据关键词名额
        chinese_segments = re.findall(r'[\u4e00-\u9fff]{2,}', content)
        for seg in chinese_segments:
            slen = len(seg)
            if slen <= 2:
                keywords.add(seg)
            elif slen <= 4:
                keywords.add(seg)
                for i in range(slen - 1):
                    keywords.add(seg[i:i+2])
            else:  # slen >= 5
                # 头部 2-4 字（动作/描述词）
                for l in range(2, min(5, slen + 1)):
                    keywords.add(seg[:l])
                # 尾部 2-4 字（核心名词短语）
                for l in range(2, min(5, slen + 1)):
                    keywords.add(seg[-l:])

        # 6️⃣ 从 stripped（去前缀核心词）中提取 2 字子串
        #    确保「空洞骑士」→「空洞」「骑士」都被捕获
        chinese_only = re.findall(r'[\u4e00-\u9fff]{2,}', stripped)
        for c in chinese_only:
            if len(c) >= 2 and c not in content:
                keywords.add(c)
            # 从核心词中取 2 字子串
            for i in range(len(c) - 1):
                sub = c[i:i+2]
                keywords.add(sub)

        # 按长度降序，优先返回更长、更独特的关键词
        result = sorted(keywords, key=lambda x: (-len(x), x))
        return result[:10]  # 放宽到 10 个，容纳短关键词爱吃""爱玩"这类不是通用前缀，保留作为完整关键词的一部分
        prefixes = sorted([
            "喜欢玩", "喜欢吃", "喜欢打", "喜欢看", "喜欢听",
            "经常熬夜", "经常", "偶尔", "总是",
            "在自学",
            "想要", "希望",
            "正在", "可以", "推荐了", "分享了一个",
            "会", "想", "要", "能", "在",
            "自学", "学习", "研究", "玩", "打", "写", "做",
            "推荐", "分享", "讨论", "喜欢",
        ], key=lambda x: -len(x))
        # 常见虚词/标点
        removals = {"的", "和", "与", "了", "着", "过", "，", "、", "。", "！", "？"}

        # 常见单字动词（用于二次剥离）
        single_verbs = {"爱", "想", "会", "能", "要", "在", "有", "被", "去", "来", "上"}

        # 提取所有关键词（多粒度）
        keywords = set()

        # 首先，完整内容本身作为一个关键词
        if len(content) >= 2:
            keywords.add(content)

        import re

        # 去掉虚词
        text = "".join(ch for ch in content if ch not in removals)

        # 去掉前缀，获取核心名词
        stripped = text
        for p in prefixes:
            if stripped.startswith(p):
                stripped = stripped[len(p):]
                break

        # 如果还没去掉东西，尝试单字动词剥离
        if stripped == text:
            for sv in single_verbs:
                if stripped.startswith(sv):
                    stripped = stripped[len(sv):]
                    break

        if stripped and len(stripped) >= 2:
            keywords.add(stripped)

        # 从中英文混合中提取独立 English/numeric 词
        eng_parts = re.findall(r'[a-zA-Z][a-zA-Z0-9._-]+', content)
        for e in eng_parts:
            if len(e) >= 2:
                keywords.add(e)

        # 从中文内容中提取可能的二级关键词
        # 规则：去掉常见前缀后，按2字以上取连续中文字符
        # 对于 "玩空洞骑士" → 取 "空洞骑士"
        chinese_only = re.findall(r'[\u4e00-\u9fff]{2,}', stripped)
        for c in chinese_only:
            if len(c) >= 2 and c != stripped:
                # 如果核心词 > 4 个字，尝试提取最后 2-4 个字作为二级关键词
                if len(c) >= 4:
                    for i in range(len(c) - 1, 1, -1):
                        sub = c[-i:]
                        if 2 <= len(sub) <= 4:
                            keywords.add(sub)
                keywords.add(c)

        # 按长度降序，优先返回更独特的长关键词
        result = sorted(keywords, key=lambda x: (-len(x), x))
        return result[:5]  # 最多5个

    def reinforce_by_messages(self, user_id: str, messages: list) -> list:
        """
        根据用户消息列表自动匹配并强化记忆。
        每条记忆提取核心关键词，匹配则强化对应记忆。
        支持交叉匹配：一条消息可强化多条记忆。
        
        参数:
            user_id: 用户 QQ 号
            messages: 消息文本列表
        
        返回:
            [{"content": str, "field": str, "score_after": float}, ...]
        """
        active = self.get_all_active(user_id)
        if not active or not messages:
            return []

        all_text = " ".join(messages).lower()
        results = []

        for mem in active:
            content = mem["content"]
            content_lower = content.lower()

            # 策略1：完整内容子串匹配（适合短句）
            matched = content_lower in all_text

            # 策略2：关键词匹配（适合长句）
            if not matched:
                keywords = self._extract_keywords(content)
                for kw in keywords:
                    kw_lower = kw.lower()
                    if kw_lower in all_text:
                        matched = True
                        break

            # 策略3：字符级重叠度判断（适合长句子中的短关键词）
            if not matched:
                # 对 2-8 字的中短内容，直接检查所有逐字符子串
                # 可以捕获「经常熬夜打游戏」中的「熬夜」
                if 2 <= len(content) <= 8:
                    for i in range(len(content) - 1):
                        for j in range(i + 2, min(i + 5, len(content) + 1)):
                            sub = content[i:j]
                            if len(sub) >= 2 and sub.lower() in all_text:
                                matched = True
                                break
                        if matched:
                            break

            if matched:
                self.reinforce(user_id, content)
                data = self._load(user_id)
                updated = None
                for m in data.get("memories", []):
                    if m["id"] == mem["id"]:
                        updated = m["score"]
                        break
                results.append({
                    "content": content,
                    "field": mem.get("field", ""),
                    "score_after": round(updated or mem["score"], 3),
                    "tags": mem.get("tags", []),
                })

        return results

    def get_all_user_ids(self) -> list:
        """获取所有有记忆的用户 ID 列表"""
        ids = []
        for fname in os.listdir(self.storage_dir):
            if fname.endswith(".json"):
                ids.append(fname[:-5])
        return sorted(ids)


# ══════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    import sys

    # 修复 Windows 编码
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    else:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEMORY_DIR = os.path.join(SKILL_DIR, "profiles", "memory")

    parser = argparse.ArgumentParser(description="液态记忆引擎 CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_store = sub.add_parser("store")
    p_store.add_argument("user_id")
    p_store.add_argument("content")
    p_store.add_argument("--tags", nargs="*", default=[])
    p_store.add_argument("--field", default="")

    p_recall = sub.add_parser("recall")
    p_recall.add_argument("user_id")
    p_recall.add_argument("--query", default="")
    p_recall.add_argument("--tags", nargs="*")
    p_recall.add_argument("--top_k", type=int, default=5)
    p_recall.add_argument("--field", default="")

    p_forget = sub.add_parser("forget")
    p_forget.add_argument("user_id")
    p_forget.add_argument("keyword")

    p_stats = sub.add_parser("stats")
    p_stats.add_argument("--user_id", default="")

    p_decay = sub.add_parser("decay")
    p_decay.add_argument("--force", action="store_true",
                          help="强制运行，忽略自动衰减间隔")

    args = parser.parse_args()

    fm = FluidMemory(MEMORY_DIR)

    if args.cmd == "decay":
        result = maybe_auto_decay(fm, force=args.force)
        print(json.dumps(result, ensure_ascii=False))

    elif args.cmd == "store":
        mid = fm.store(args.user_id, args.content,
                       tags=args.tags, field=args.field)
        print(mid)

    elif args.cmd == "recall":
        results = fm.recall(args.user_id, query=args.query,
                            tags=args.tags, field=args.field,
                            top_k=args.top_k)
        print(json.dumps([{
            "content": r["content"],
            "score": round(r["score"], 3),
            "field": r.get("field", ""),
            "tags": r.get("tags", []),
        } for r in results], ensure_ascii=False, indent=2))

    elif args.cmd == "forget":
        ok = fm.forget(args.user_id, args.keyword)
        print("done" if ok else "not_found")

    elif args.cmd == "stats":
        if args.user_id:
            n = fm.count_active(args.user_id)
            print(json.dumps({"user_id": args.user_id,
                              "active_memories": n},
                             ensure_ascii=False))
        else:
            ids = fm.get_all_user_ids()
            total = sum(fm.count_active(uid) for uid in ids)
            print(json.dumps({
                "total_users": len(ids),
                "total_active_memories": total,
                "users": ids,
            }, ensure_ascii=False, indent=2))

    else:
        parser.print_help()
