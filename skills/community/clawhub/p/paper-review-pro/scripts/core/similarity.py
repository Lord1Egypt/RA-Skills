"""
语义相似度模块（字符串 + 模糊匹配版｜修正版）
"""

import re
from difflib import SequenceMatcher


class SimilarityModel:
    def __init__(self):
        pass

    # =========================
    # 🔹 工具函数
    # =========================
    def tokenize(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9 ]", " ", text)
        return text.split()

    def fuzzy_ratio(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def ngram_overlap(self, query_tokens, text_tokens, n=2):
        """
        计算 n-gram 命中（用于短语近似）
        """
        def get_ngrams(tokens, n):
            return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))

        q_ngrams = get_ngrams(query_tokens, n)
        t_ngrams = get_ngrams(text_tokens, n)

        if not q_ngrams:
            return 0

        return len(q_ngrams & t_ngrams) / len(q_ngrams)

    # =========================
    # 🔹 核心评分函数
    # =========================
    def compute_score(self, query, title, abstract):
        # 处理 None 值
        title = title or ""
        abstract = abstract or ""
        
        query_lower = query.lower()
        title_lower = title.lower()
        abstract_lower = abstract.lower()

        score = 0.0

        q_tokens = self.tokenize(query)
        t_tokens = self.tokenize(title)
        a_tokens = self.tokenize(abstract)

        # =========================
        # 1️⃣ 完整短语匹配（最重要）
        # =========================
        if query_lower in title_lower:
            score += 2.0
        elif query_lower in abstract_lower:
            score += 1.2

        # =========================
        # 2️⃣ 核心关键词匹配（强化）
        # =========================
        # 提取 query 中的实词（过滤停用词）
        stop_words = {"the", "a", "an", "for", "with", "based", "using", "via", "and", "or", "of", "in", "on", "to"}
        core_keywords = [t for t in q_tokens if t not in stop_words and len(t) > 3]
        
        # 每个核心关键词在标题中出现都给予高分
        for kw in core_keywords:
            if kw in title_lower:
                score += 0.8
            if kw in abstract_lower:
                score += 0.4

        # =========================
        # 3️⃣ token覆盖率（核心）
        # =========================
        overlap_title = len(set(q_tokens) & set(t_tokens)) / (len(q_tokens) + 1e-6)
        overlap_abstract = len(set(q_tokens) & set(a_tokens)) / (len(q_tokens) + 1e-6)

        score += 0.6 * overlap_title
        score += 0.4 * overlap_abstract

        # =========================
        # 4️⃣ n-gram（短语近似）
        # =========================
        score += 0.5 * self.ngram_overlap(q_tokens, t_tokens, n=2)
        score += 0.3 * self.ngram_overlap(q_tokens, a_tokens, n=2)

        # =========================
        # 5️⃣ 标题强化
        # =========================
        score *= 1.3

        return score

    # =========================
    # 🔹 外部接口（不变）
    # =========================
    def compute(self, query, papers, use_authority: bool = False, authority_weight: float = 0.3):
        """
        计算论文相似度分数
        
        参数:
            query: 查询字符串
            papers: 论文列表
            use_authority: 是否考虑权威度分数（默认 False）
            authority_weight: 权威度分数权重（0.0-1.0，默认 0.3）
        
        返回:
            papers: 添加了 sim 字段的论文列表
        """
        for p in papers:
            title = p.get("title", "")
            abstract = p.get("abstract", "")
            
            # 基础相关度分数
            base_sim = float(self.compute_score(query, title, abstract))
            p["sim"] = base_sim
            
            # 如果使用权威度，且论文有 authority_score 字段
            if use_authority and "authority_score" in p:
                authority_score = p.get("authority_score", 0.3)
                # 综合分数 = 相关度 * (1 - weight) + 权威度 * weight
                # 将 base_sim 归一化到 0-1 范围（假设 base_sim 最大约为 5.0）
                normalized_sim = min(base_sim / 5.0, 1.0)
                combined_score = normalized_sim * (1 - authority_weight) + authority_score * authority_weight
                p["sim_combined"] = combined_score
                p["sim_base"] = base_sim
                p["authority_score"] = authority_score
        
        return papers
    
    def compute_with_authority(self, query, papers, authority_weight: float = 0.3):
        """
        便捷方法：计算考虑权威度的综合分数
        
        参数:
            query: 查询字符串
            papers: 论文列表（应已包含 authority_score 字段）
            authority_weight: 权威度权重（默认 0.3）
        
        返回:
            papers: 添加了综合分数的论文列表
        """
        return self.compute(query, papers, use_authority=True, authority_weight=authority_weight)