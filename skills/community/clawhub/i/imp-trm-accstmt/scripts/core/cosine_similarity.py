"""
余弦相似度工具
用于智能匹配银行对账单列名与标准字段名称
"""

import re
import math
from typing import List, Dict, Tuple, Optional
from collections import Counter


class CosineSimilarityMatcher:
    """基于余弦相似度的字段匹配器"""

    def __init__(self, threshold: float = 0.75, fallback_threshold: float = 0.6):
        """
        初始化匹配器

        Args:
            threshold: 默认匹配阈值
            fallback_threshold: 备用阈值，当没有高匹配时使用
        """
        self.threshold = threshold
        self.fallback_threshold = fallback_threshold
        self.aliases: Dict[str, List[str]] = {}

    def set_aliases(self, aliases: Dict[str, List[str]]):
        """设置字段别名映射"""
        self.aliases = aliases

    def _tokenize(self, text: str) -> List[str]:
        """
        分词处理

        Args:
            text: 输入文本

        Returns:
            分词后的词列表
        """
        if not text:
            return []

        # 转小写
        text = text.lower()

        # 英文按单词分割
        words = re.findall(r'[a-z]+', text)

        # 中文字符串按字符分割
        chinese_chars = re.findall(r'[一-鿿]', text)

        return words + chinese_chars

    def _compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        """计算词频"""
        if not tokens:
            return {}
        counter = Counter(tokens)
        total = len(tokens)
        return {word: count / total for word, count in counter.items()}

    def _compute_idf(self, corpus: List[List[str]]) -> Dict[str, float]:
        """计算逆文档频率"""
        df: Dict[str, int] = {}
        for tokens in corpus:
            for token in set(tokens):
                df[token] = df.get(token, 0) + 1

        n = len(corpus)
        return {
            token: math.log(n / (doc_freq + 1)) + 1
            for token, doc_freq in df.items()
        }

    def _compute_tfidf(self, tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
        """计算TF-IDF向量"""
        tf = self._compute_tf(tokens)
        return {word: tf_val * idf.get(word, 0) for word, tf_val in tf.items()}

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """计算余弦相似度"""
        # 提取所有词
        all_words = set(vec1.keys()) | set(vec2.keys())

        if not all_words:
            return 0.0

        # 构建向量
        v1 = [vec1.get(word, 0) for word in all_words]
        v2 = [vec2.get(word, 0) for word in all_words]

        # 计算点积和模
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def build_index(self, target_fields: List[str]):
        """
        构建目标字段索引

        Args:
            target_fields: 目标字段列表
        """
        # 展平别名到目标字段
        all_terms = []

        for field in target_fields:
            tokens = self._tokenize(field)
            all_terms.append(tokens)

            # 添加别名
            if field in self.aliases:
                for alias in self.aliases[field]:
                    tokens = self._tokenize(alias)
                    all_terms.append(tokens)

        # 计算IDF
        self.idf = self._compute_idf(all_terms)

        # 存储目标字段的TF-IDF向量
        self.target_vectors: Dict[str, Dict[str, float]] = {}
        for field in target_fields:
            tokens = self._tokenize(field)
            self.target_vectors[field] = self._compute_tfidf(tokens, self.idf)

            if field in self.aliases:
                for alias in self.aliases[field]:
                    tokens = self._tokenize(alias)
                    self.target_vectors[alias] = self._compute_tfidf(tokens, self.idf)

    def match(self, source_field: str) -> Tuple[Optional[str], float]:
        """
        匹配源字段到目标字段

        Args:
            source_field: 源字段名

        Returns:
            (最佳匹配目标字段, 相似度分数)
        """
        if not hasattr(self, 'target_vectors'):
            raise ValueError("Must call build_index() before match()")

        source_tokens = self._tokenize(source_field)
        if not source_tokens:
            return None, 0.0

        source_vector = self._compute_tfidf(source_tokens, self.idf)

        best_match = None
        best_score = 0.0

        for target_field, target_vector in self.target_vectors.items():
            score = self._cosine_similarity(source_vector, target_vector)
            if score > best_score:
                best_score = score
                best_match = target_field

        # 如果最佳匹配低于阈值，检查是否低于备用阈值
        if best_score < self.fallback_threshold:
            return None, best_score

        return best_match, best_score

    def match_all(self, source_fields: List[str]) -> Dict[str, Tuple[Optional[str], float]]:
        """
        批量匹配源字段

        Args:
            source_fields: 源字段列表

        Returns:
            源字段到(目标字段, 相似度)的映射
        """
        return {
            field: self.match(field)
            for field in source_fields
        }


def simple_similarity(str1: str, str2: str) -> float:
    """
    简单的字符串相似度计算（不需要预构建索引）

    Args:
        str1: 字符串1
        str2: 字符串2

    Returns:
        相似度分数 0-1
    """
    if not str1 or not str2:
        return 0.0

    str1_lower = str1.lower()
    str2_lower = str2.lower()

    # 完全匹配
    if str1_lower == str2_lower:
        return 1.0

    # 一个包含另一个
    if str1_lower in str2_lower or str2_lower in str1_lower:
        return 0.8

    # 公共字符比例
    set1 = set(str1_lower)
    set2 = set(str2_lower)
    intersection = set1 & set2
    union = set1 | set2

    if not union:
        return 0.0

    jaccard = len(intersection) / len(union)

    # 加权返回
    return jaccard * 0.6


def match_headers_with_similarity(
    source_headers: List[str],
    target_fields: List[str],
    aliases: Optional[Dict[str, List[str]]] = None,
    threshold: float = 0.75
) -> Dict[str, Optional[str]]:
    """
    使用余弦相似度匹配表头字段

    Args:
        source_headers: 源表头列表
        target_fields: 目标字段列表
        aliases: 字段别名映射
        threshold: 匹配阈值

    Returns:
        源字段到目标字段的映射
    """
    matcher = CosineSimilarityMatcher(threshold=threshold, fallback_threshold=0.5)

    if aliases:
        matcher.set_aliases(aliases)

    # 展平别名到目标字段列表
    expanded_targets = list(target_fields)
    if aliases:
        for field_list in aliases.values():
            expanded_targets.extend(field_list)

    matcher.build_index(expanded_targets)

    result = {}
    for header in source_headers:
        matched_field, score = matcher.match(header)

        # 检查是否需要降级匹配
        if matched_field and score >= threshold:
            # 验证是否在目标字段中（而不是别名中）
            if matched_field not in target_fields:
                # 找到真实的目标字段
                for tf in target_fields:
                    if matched_field in (aliases.get(tf, []) if aliases else []):
                        result[header] = tf
                        break
                else:
                    result[header] = matched_field
            else:
                result[header] = matched_field
        else:
            result[header] = None

    return result


# 预定义的常见银行字段别名
COMMON_BANK_FIELD_ALIASES = {
    "bankaccount_account": ["账号", "银行账号", "账户号码", "账户", "Account", "Account Number", "Account No", "A/C", "客户账号"],
    "bank_seq_no": ["流水号", "交易流水号", "序号", "参考号", "Reference", "Ref No", "Transaction ID", "流水", "唯一流水号", "凭证号", "银行流水号"],
    "tran_date": ["日期", "交易日期", "发生日期", "记账日期", "Date", "Trans Date", "Transaction Date", "Value Date", "交易流水日期"],
    "tran_time": ["交易时间", "交易流水时间", "时间"],
    "dc_flag": ["借贷", "借贷标识", "方向", "收支", "DC", "D/C", "Dr/Cr", "Credit/Debit", "借/贷", "借贷方向", "类型", "收/支"],
    "debitamount": ["支出", "支出金额", "借方", "Debit", "DR", "Withdrawal", "借方发生额", "借方金额", "借方发生", "支出发生额", "支取"],
    "creditamount": ["收入", "收入金额", "贷方", "Credit", "CR", "Deposit", "贷方发生额", "贷方金额", "贷方发生", "存入", "收款"],
    "currency_name": ["币种", "货币", "币别", "Currency", "CCY", "Ccy", "币    种"],
    "tran_amt": ["金额", "交易金额", "发生额", "Amount", "Txn Amount", "Total", "发生金额"],
    "to_acct_no": [
        "对方账号", "对方账户", "收款账号", "Beneficiary Account", "Payee Account",
        "对手账号", "对手账户", "对方卡号", "收款人账号", "付款账号",
        "对方账号/户名", "对方账户/户名"
    ],
    "to_acct_name": [
        "对方户名", "对方名称", "收款人", "Beneficiary", "Payee", "收款方",
        "对手户名", "对手名称", "对方账户名称", "收款人名称", "付款人名称",
        "对方单位名称", "对手公司名称", "对方公司名称"
    ],
    "to_acct_bank_name": ["对方银行", "收款银行", "Beneficiary Bank", "Payee Bank", "对手银行", "对方开户行"],
    "remark": ["摘要", "备注", "说明", "Description", "Narrative", "Details", "交易描述", "交易详情", "详细信息", "附言"],
    "acct_bal": ["余额", "账户余额", "Balance", "Avail Balance", "可用余额", "账户余额", "存款余额", "当前余额"],
    "bankNumber_name": ["开户行", "银行名称", "开户行名称", "Bank Name", "支行名称", "所属银行"]
}
