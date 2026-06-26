"""
词频逆文档频率向量索引 (TF-IDF NLP Index)
用于处理自然语言，匹配最合适的技能。
"""
import math
from collections import defaultdict, Counter
from typing import List, Tuple

class TFIDFIndex:
    """轻量级 TF-IDF 向量索引"""
    def __init__(self):
        self.documents = {} # 文档内容库
        self.document_tokens = {} # 分词结果库
        self.word_document_count = defaultdict(int) # 词频 (文档频次)
        self.total_documents = 0 # 总文档数

    def _tokenize(self, text: str) -> List[str]:
        """简单分词器，按字拆分并转小写"""
        return [char.lower() for char in text if char.strip()]

    def add_skill(self, skill_id: str, description: str):
        """添加技能描述到索引"""
        tokens = self._tokenize(description)
        self.documents[skill_id] = description
        self.document_tokens[skill_id] = tokens
        self.total_documents += 1

        # 记录包含该词的文档数量，用于计算逆文档频率
        unique_tokens = set(tokens)
        for token in unique_tokens:
            self.word_document_count[token] += 1

    def match(self, query: str, top_k: int = 1) -> List[Tuple[str, float]]:
        """计算余弦相似度并返回最匹配技能"""
        if self.total_documents == 0:
            return []

        query_tokens = self._tokenize(query)
        query_counter = Counter(query_tokens)

        scores = defaultdict(float)

        # 遍历所有文档，计算相似度得分
        for skill_id, tokens in self.document_tokens.items():
            if not tokens:
                continue
                
            skill_counter = Counter(tokens)
            score = 0.0

            for token, q_count in query_counter.items():
                if token in skill_counter:
                    # 词频 (Term Frequency)
                    tf = skill_counter[token] / len(tokens)
                    # 逆文档频率 (Inverse Document Frequency)
                    idf = math.log(self.total_documents / (1 + self.word_document_count[token]))
                    # 累加权重得分
                    score += q_count * (tf * idf)

            scores[skill_id] = score

        # 按得分从高到低排序
        sorted_skills = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        # 仅返回得分大于0的技能
        return [(skill_id, score) for skill_id, score in sorted_skills[:top_k] if score > 0]