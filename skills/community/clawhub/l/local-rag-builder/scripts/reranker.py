"""
local-rag-builder 重排序模块（Reranker）
v0.1.0

三种模式：
1. model  — 用 rerank transformer 对检索结果打分排序
2. rule   — 排序规则引擎（权重、时效性、来源优先级等）
3. hybrid — 模型打分 + 规则微调

支持嵌入 rerank 模型 或 自定义排序规则。
"""

import os
import re
import json
from datetime import datetime, timezone
from typing import Optional

from config import load_config


# ==================== 排序规则引擎 ====================

class RerankRule:
    """单条排序规则"""

    def __init__(self, rule_type: str, **params):
        self.type = rule_type  # score_weight | recency | source_weight | boost_keywords
        self.params = params

    def __repr__(self):
        return f"RerankRule({self.type}, {self.params})"


class RuleReranker:
    """规则排序引擎"""

    def __init__(self, rules: list[dict] = None):
        self.rules = self._parse_rules(rules or [])

    def _parse_rules(self, raw_rules: list[dict]) -> list[RerankRule]:
        parsed = []
        for r in raw_rules:
            rtype = r.get("type", "")
            params = {k: v for k, v in r.items() if k != "type"}
            parsed.append(RerankRule(rtype, **params))
        return parsed

    def rerank(self, query: str, docs: list, scores: list[float] = None) -> list:
        """
        对文档排序。
        docs: [Document] 或 [dict]（dict 必须有 content metadata）
        scores: 嵌入检索的分数（可选，用于 score_weight 规则）

        返回排序后的 [(doc, final_score)]
        """
        if not docs:
            return []

        scored = []
        for i, doc in enumerate(docs):
            original_score = scores[i] if scores and i < len(scores) else 0.0
            final_score = self._compute_score(query, doc, original_score)
            scored.append((doc, final_score))

        scored.sort(key=lambda x: -x[1])
        return scored

    def _compute_score(self, query: str, doc, original_score: float) -> float:
        """对单个文档计算综合得分"""
        score = 0.0
        content = doc.page_content if hasattr(doc, "page_content") else (
            doc.get("content", "") if isinstance(doc, dict) else str(doc)
        )
        metadata = doc.metadata if hasattr(doc, "metadata") else (
            doc.get("metadata", {}) if isinstance(doc, dict) else {}
        )

        for rule in self.rules:
            if rule.type == "score_weight":
                emb_weight = rule.params.get("embedding_score", 0.6)
                rerank_weight = rule.params.get("rerank_score", 0.4)
                # 如果没有 rerank 分，只用 embedding 分
                score += original_score * emb_weight

            elif rule.type == "recency":
                field = rule.params.get("field", "updated_at")
                half_life_days = rule.params.get("days_halflife", 30)
                ts = metadata.get(field, "")
                if ts:
                    try:
                        if isinstance(ts, (int, float)):
                            doc_time = datetime.fromtimestamp(ts, tz=timezone.utc)
                        else:
                            doc_time = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                        now = datetime.now(timezone.utc)
                        days_old = (now - doc_time).days
                        score += (0.5 ** (days_old / half_life_days))
                    except (ValueError, TypeError):
                        pass

            elif rule.type == "source_weight":
                sources = rule.params.get("sources", {})
                doc_source = metadata.get("source", "")
                for source_pattern, weight in sources.items():
                    if source_pattern in doc_source:
                        score += weight

            elif rule.type == "boost_keywords":
                keywords = rule.params.get("keywords", [])
                boost = rule.params.get("boost", 1.2)
                content_lower = content.lower()
                for kw in keywords:
                    if kw.lower() in content_lower:
                        score += boost / len(keywords)
                        break

        return score


# ==================== 模型 Reranker ====================

class ModelReranker:
    """用 transformer rerank 模型对检索结果打分排序"""

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self._model = None
        self._tokenizer = None

    def _load_model(self):
        if self._model is not None:
            return

        if not self.model_path:
            cfg = load_config()
            reranker_cfg = cfg.get("reranker", {})
            self.model_path = reranker_cfg.get("model_path", "")

        if not self.model_path or not os.path.exists(self.model_path):
            from utils import MODELS_DIR, find_model_dirs
            models = find_model_dirs(MODELS_DIR)
            if not models:
                raise ValueError("未找到 rerank 模型，请先下载")
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
            raise RuntimeError(f"加载 rerank 模型失败: {e}")

    def rerank(self, query: str, docs: list, top_k: int = None) -> list:
        """
        对文档打分排序。

        返回 [(doc, score)]，按 score 降序。
        """
        if not docs:
            return []

        self._load_model()
        import torch

        if top_k is None:
            cfg = load_config()
            top_k = cfg.get("reranker", {}).get("top_k", 5)

        contents = []
        for doc in docs:
            c = doc.page_content if hasattr(doc, "page_content") else (
                doc.get("content", "") if isinstance(doc, dict) else str(doc)
            )
            contents.append(c)

        pairs = [[query, c] for c in contents]
        inputs = self._tokenizer(
            pairs, padding=True, truncation=True,
            max_length=512, return_tensors="pt"
        ).to(self._model.device)

        with torch.no_grad():
            outputs = self._model(**inputs)
            scores = outputs.logits.squeeze(-1).tolist()

        if isinstance(scores, float):
            scores = [scores]

        scored = list(zip(docs, scores))
        scored.sort(key=lambda x: -x[1])

        return scored[:top_k]


# ==================== 混合 Reranker ====================

class HybridReranker:
    """模型打分 + 规则微调"""

    def __init__(self, model_path: str = None, rules: list[dict] = None):
        self.model_reranker = ModelReranker(model_path)
        self.rule_reranker = RuleReranker(rules)

    def rerank(self, query: str, docs: list, top_k: int = None) -> list:
        """
        先用模型打分，再用规则微调排序。

        返回 [(doc, model_score, final_score)]
        """
        if not docs:
            return []

        if top_k is None:
            cfg = load_config()
            top_k = cfg.get("reranker", {}).get("top_k", 5)

        # 模型打分
        model_results = self.model_reranker.rerank(query, docs, top_k=len(docs))
        model_docs = [d for d, _ in model_results]
        model_scores = [s for _, s in model_results]

        # 规则微调
        rule_results = self.rule_reranker.rerank(query, model_docs, model_scores)

        # 合并分数
        combined = []
        for i, (doc, rule_score) in enumerate(rule_results):
            ms = model_scores[i] if i < len(model_scores) else 0.0
            combined.append((doc, ms, rule_score))

        return combined[:top_k]


# ==================== 统一 Reranker 入口 ====================

class Reranker:
    """
    统一 Reranker 入口。
    根据 config.reranker.mode 自动选择：
    - "model"   → ModelReranker
    - "rule"    → RuleReranker
    - "hybrid"  → HybridReranker
    """

    def __init__(self, config: dict = None):
        self.cfg = config or load_config()
        self._reranker = None

    def _get_reranker(self):
        if self._reranker is not None:
            return self._reranker

        rerank_cfg = self.cfg.get("reranker", {})
        mode = rerank_cfg.get("mode", "model")
        model_path = rerank_cfg.get("model_path", "")
        rules = rerank_cfg.get("sort_rules", [])

        if mode == "model":
            self._reranker = ModelReranker(model_path)
        elif mode == "rule":
            self._reranker = RuleReranker(rules)
        elif mode == "hybrid":
            self._reranker = HybridReranker(model_path, rules)
        else:
            self._reranker = ModelReranker(model_path)

        return self._reranker

    def rerank(self, query: str, docs: list, top_k: int = None) -> list:
        """统一 rerank 接口"""
        try:
            actual = self._get_reranker()
            if isinstance(actual, RuleReranker):
                # RuleReranker 第三参数是 scores，不是 top_k
                return actual.rerank(query, docs, None)[:top_k]
            return actual.rerank(query, docs, top_k)
        except Exception as e:
            # 出错时按原序返回（降级保底）
            if top_k:
                return [(d, 0.0) for d in docs[:top_k]]
            return [(d, 0.0) for d in docs]


# ==================== CLI ====================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Reranker 测试工具")
    parser.add_argument("--query", type=str, help="查询文本")
    parser.add_argument("--docs", type=str, nargs="+", help="待排序文档")
    parser.add_argument("--mode", type=str, default="model", choices=["model", "rule", "hybrid"],
                        help="rerank 模式")
    parser.add_argument("--top-k", type=int, default=5, help="返回条数")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--list-rules", action="store_true", dest="list_rules", help="显示当前排序规则")

    args = parser.parse_args()

    if args.list_rules:
        cfg = load_config()
        rules = cfg.get("reranker", {}).get("sort_rules", [])
        print("当前排序规则:")
        if rules:
            for i, r in enumerate(rules):
                print(f"  {i+1}. {r}")
        else:
            print("  （未配置）")

    elif args.query and args.docs:
        from langchain_core.documents import Document
        docs = [Document(page_content=d) for d in args.docs]

        cfg = load_config()
        cfg.setdefault("reranker", {})
        cfg["reranker"]["mode"] = args.mode

        reranker = Reranker(cfg)
        results = reranker.rerank(args.query, docs, args.top_k)

        if args.json:
            output = []
            for doc, score in results:
                output.append({
                    "content": doc.page_content[:100] if hasattr(doc, "page_content") else str(doc)[:100],
                    "score": round(score, 4),
                })
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"Rerank 结果 (mode={args.mode}):")
            for i, (doc, score) in enumerate(results):
                content = (doc.page_content if hasattr(doc, "page_content") else str(doc))[:80]
                print(f"  #{i+1} [{score:.4f}] {content}...")
    else:
        parser.print_help()
