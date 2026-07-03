"""
local-rag-builder 路由层模块
v0.2.0

路由架构（直接基于 knowledge_base_manager 的多知识库能力）：

① hardcoded(关键词规则) — 直接用 KB 管理的 auto_classify 查规则
  → 命中 → 直接路由到该 KB
② fallback(语义模型) — query × KB 签名 → 选最佳 KB
  → 命中 → 路由到最佳 KB
③ broadcast — 全量广播所有 KB
  → 兜底

入库和查询共享同一个 FallbackRouter。
"""

import os
import re
import json
from typing import Optional

from config import load_config
from utils import KB_DIR, safe_json_load, safe_json_dump

KB_SIGNATURE_FILE = os.path.join(KB_DIR, "kb_signatures.json")


def _load_signatures():
    return safe_json_load(KB_SIGNATURE_FILE, {})


def _save_signatures(sigs):
    safe_json_dump(sigs, KB_SIGNATURE_FILE)


# ==================== 硬编码路由 ====================

def hardcoded_route(question: str) -> Optional[str]:
    """
    硬编码路由：直接用 knowledge_base_manager.auto_classify()。
    返回命中的 KB 名称，不命中返回 None。

    注意：auto_classify() 在无规则匹配时返回 "default"，
    这里额外验证是否真的有关键词命中。
    """
    from knowledge_base_manager import _load_rules
    rules = _load_rules()
    if not rules:
        return None

    # 快速检查是否有任何关键词命中
    question_lower = question.lower()
    any_hit = False
    for rule in rules.values():
        for kw in rule.get("keywords", []):
            if kw.lower() in question_lower:
                any_hit = True
                break
        if any_hit:
            break

    if not any_hit:
        return None

    from knowledge_base_manager import auto_classify
    return auto_classify(question, rules)


# ==================== 回退语义路由 ====================

class FallbackRouter:
    """回退语义路由：用 rerank 模型对 query 和 KB 签名打分"""

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self._model = None
        self._tokenizer = None

    def _load_model(self):
        if self._model is not None:
            return

        if not self.model_path:
            cfg = load_config()
            router_cfg = cfg.get("router", {})
            fallback_cfg = router_cfg.get("fallback", {})
            self.model_path = fallback_cfg.get("model_path", "")

        if not self.model_path or not os.path.exists(self.model_path):
            from utils import MODELS_DIR, find_model_dirs
            models = find_model_dirs(MODELS_DIR)
            if not models:
                raise ValueError("未找到 rerank/routing 模型")
            self.model_path = models[0]["path"]

        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, local_files_only=True
            )
            self._model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path, local_files_only=True
            ).to(device).eval()
        except Exception as e:
            raise RuntimeError(f"加载路由模型失败: {e}")

    def score(self, query: str, kb_signatures: dict[str, str]) -> dict[str, float]:
        if not kb_signatures:
            return {}
        self._load_model()

        import torch
        pairs = [[query, sig] for sig in kb_signatures.values()]
        inputs = self._tokenizer(
            pairs, padding=True, truncation=True,
            max_length=512, return_tensors="pt"
        ).to(self._model.device)

        with torch.no_grad():
            outputs = self._model(**inputs)
            scores = outputs.logits.squeeze(-1).tolist()

        if isinstance(scores, float):
            scores = [scores]

        kb_names = list(kb_signatures.keys())
        result = {}
        for i, name in enumerate(kb_names):
            result[name] = round(scores[i] if i < len(scores) else 0.0, 4)
        return result

    def route(self, query: str, signatures: dict[str, str],
              threshold: float = None) -> tuple[Optional[str], dict[str, float]]:
        cfg = load_config()
        router_cfg = cfg.get("router", {})
        fallback_cfg = router_cfg.get("fallback", {})
        if threshold is None:
            threshold = fallback_cfg.get("min_score_threshold", 0.3)

        scores = self.score(query, signatures)
        if not scores:
            return None, scores

        best_kb = max(scores, key=scores.get)
        best_score = scores[best_kb]

        if best_score < threshold:
            return None, scores
        return best_kb, scores


# ==================== 全量广播 ====================

def broadcast_route(question: str, kb_names: list[str]) -> list[str]:
    """全量广播：返回所有存在数据的 KB 列表"""
    valid_kbs = []
    for name in kb_names:
        kb_path = os.path.join(KB_DIR, name)
        if os.path.exists(kb_path) and os.listdir(kb_path):
            valid_kbs.append(name)
    return valid_kbs


# ==================== 主路由入口 ====================

def route_query(question: str) -> dict:
    """
    完整路由流程：
    ① hardcoded(query) — 命中则直接路由
    ② fallback(query × KB签名) — 命中则路由到最佳 KB
    ③ broadcast — 全量广播所有 KB
    """
    from knowledge_base_manager import list_knowledge_bases
    cfg = load_config()
    router_cfg = cfg.get("router", {})

    # ① 硬编码路由
    hc_result = hardcoded_route(question)
    if hc_result:
        return {"kb_names": [hc_result], "method": "hardcoded", "kb_scores": None}

    # ② 回退语义路由
    fallback_enabled = router_cfg.get("fallback", {}).get("enabled", True)
    if fallback_enabled:
        signatures = _load_signatures()
        if signatures:
            try:
                fallback = FallbackRouter()
                best_kb, scores = fallback.route(question, signatures)
                if best_kb:
                    return {"kb_names": [best_kb], "method": "fallback", "kb_scores": scores}
            except (ValueError, RuntimeError):
                pass  # 模型未就绪，降级到 broadcast

    # ③ 全量广播
    all_kbs = list(list_knowledge_bases().keys())
    broadcast_kbs = broadcast_route(question, all_kbs)
    return {"kb_names": broadcast_kbs, "method": "broadcast", "kb_scores": None}


# ==================== KB 签名自动归纳 ====================

def _build_signature_from_texts(texts: list[str], max_chars: int = 500) -> str:
    """
    从文本列表提取签名：词频统计（排除停用词）+ 代表性片段
    """
    combined = " ".join(texts)
    tokens = re.findall(r'[\w\u4e00-\u9fff]+', combined.lower())
    stop_words = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
        "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
        "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那", "吗",
        "把", "被", "让", "给", "为", "所", "以", "能", "于", "之", "与",
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "can",
        "could", "may", "might", "shall", "should", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "this", "that", "these", "those", "it", "its",
    }
    freq = {}
    for t in tokens:
        if len(t) < 2 or t in stop_words:
            continue
        freq[t] = freq.get(t, 0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: -x[1])
    top_words = [w for w, _ in sorted_words[:30]]
    signature = " ".join(top_words)

    excerpt_parts = []
    for t in texts[:3]:
        excerpt_parts.append(t[:100].strip())
    excerpt = " ".join(excerpt_parts)

    full = f"{signature} {excerpt}"
    return full[:max_chars]


def induce_kb_signature(kb_name: str, chunks: list = None) -> str:
    """
    自动归纳 KB 签名。
    chunks 为可选（入库时直接传入），否则从 Chroma 读取。
    """
    from knowledge_base_manager import _load_index

    if chunks is None:
        try:
            from langchain_chroma import Chroma
            from rag_core import get_embeddings

            index = _load_index()
            if kb_name not in index:
                return ""
            persist_dir = index[kb_name]["path"]
            if not os.path.exists(persist_dir) or not os.listdir(persist_dir):
                return ""

            embeddings = get_embeddings(kb_name=kb_name)
            vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
            try:
                all_docs = vectorstore.get()
                texts = all_docs.get("documents", [])
            except Exception:
                all_docs = vectorstore.similarity_search("", k=20)
                texts = [d.page_content for d in all_docs]
        except Exception:
            texts = []
    else:
        texts = [c.page_content if hasattr(c, "page_content") else str(c) for c in chunks]

    if not texts:
        return ""
    return _build_signature_from_texts(texts)


def update_kb_signature(kb_name: str, chunks: list = None):
    """更新指定 KB 的签名（入库时自动调用）"""
    sig = induce_kb_signature(kb_name, chunks)
    if not sig:
        return
    sigs = _load_signatures()
    sigs[kb_name] = {
        "signature": sig,
        "updated_at": str(__import__("datetime").datetime.now()),
        "auto_updated": True,
    }
    _save_signatures(sigs)


def list_kb_signatures() -> dict:
    return _load_signatures()


def rebuild_all_signatures():
    """重建所有 KB 签名"""
    from knowledge_base_manager import list_knowledge_bases
    kbs = list_knowledge_bases()
    for kb_name in kbs:
        try:
            update_kb_signature(kb_name)
        except Exception as e:
            print(f"  [!] 重建签名失败 {kb_name}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="路由层管理工具")
    parser.add_argument("--route", type=str, help="测试路由")
    parser.add_argument("--signatures", action="store_true", help="列出 KB 签名")
    parser.add_argument("--rebuild-signatures", action="store_true", dest="rebuild", help="重建所有 KB 签名")
    parser.add_argument("--update-signature", type=str, dest="update_sig", help="更新指定 KB 签名")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.signatures:
        sigs = list_kb_signatures()
        if args.json:
            print(json.dumps(sigs, ensure_ascii=False, indent=2))
        else:
            print(f"KB 签名 ({len(sigs)}):")
            for name, info in sigs.items():
                print(f"  {name}: {info.get('signature', '')[:80]}...")

    elif args.rebuild:
        rebuild_all_signatures()
        print("[OK] 所有 KB 签名已重建")

    elif args.update_sig:
        update_kb_signature(args.update_sig)
        sigs = list_kb_signatures()
        info = sigs.get(args.update_sig, {})
        print(f"[OK] 签名已更新: {info.get('signature', '')[:100]}...")

    elif args.route:
        result = route_query(args.route)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"路由结果:")
            print(f"  方法: {result['method']}")
            print(f"  目标 KB: {result['kb_names']}")
            if result.get("kb_scores"):
                print(f"  得分: {result['kb_scores']}")
    else:
        parser.print_help()
