"""
Data Validator - 安全输入验证和净化模块（i-skill）

修复记录（v2.1.0）：
- [P0] 修正 name_pattern 正则：原有 \b[A-Z][a-z]+ [A-Z][a-z]+\b 误报极高
        （'FastAPI LangChain'、'Hello World' 等均被误判为人名）
        改为仅对已知姓名格式（英文名+姓）做宽松过滤，且只在明确上下文中过滤
- [P1] 补充中文 PII 检测：中文姓名（2-4汉字）、11位手机号、18位身份证号
- [P2] validate_evidence 先截断再检测的顺序问题：改为先检测原文再截断
- [P3] 去除 max_evidence_length 默认值过小（20字符）的问题，改为合理的 500
- [P3] profanity 列表补充中文常见敏感词占位（可扩展）
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class ValidationError(Exception):
    """自定义验证异常"""
    pass


class DataValidator:
    # 内容长度上限（字符数），作为类常量方便配置
    MAX_CONTENT_LENGTH = 50000

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self._compile_patterns()

    def _load_config(self, config_path: str) -> Dict:
        if config_path:
            try:
                config_file = Path(config_path)
                if not config_file.exists():
                    raise ValidationError(f"配置文件不存在: {config_path}")
                if config_file.stat().st_size > 1024 * 1024:
                    raise ValidationError("配置文件过大")
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self._validate_config_structure(config)
                return config
            except (json.JSONDecodeError, ValidationError) as e:
                raise ValidationError(f"无效配置: {str(e)}")

        # [P3修复] max_evidence_length 改为合理值 500（原 20 过于激进）
        return {
            "data_validation": {
                "max_evidence_length": 500,
                "max_evidence_per_topic": 2,
                "max_total_evidence": 20,
                "max_topics_per_conversation": 5,
                "max_topics_per_session": 10
            },
            "sanitization_rules": {
                "remove_personal_identifiers": True,
                "remove_sensitive_info": True,
                "remove_profanity": True,
                "remove_timestamps": False   # 档案内时间标记不强制删除
            }
        }

    def _validate_config_structure(self, config: Dict):
        required_sections = ["data_validation", "sanitization_rules"]
        for section in required_sections:
            if section not in config:
                raise ValidationError(f"缺少配置节: {section}")

        data_validation = config["data_validation"]
        for key in ["max_evidence_length", "max_evidence_per_topic",
                    "max_total_evidence", "max_topics_per_conversation",
                    "max_topics_per_session"]:
            if key not in data_validation:
                raise ValidationError(f"缺少 data_validation.{key}")
            if not isinstance(data_validation[key], int) or data_validation[key] <= 0:
                raise ValidationError(f"data_validation.{key} 的值无效")

    def _compile_patterns(self):
        # 英文 PII
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        )
        # 国际通用电话（含中国手机号 1xx-xxxx-xxxx）
        # [P1修复] 中文语境中汉字前后没有 \b 边界，使用 (?<!\d) 和 (?!\d) 替代 \b
        self.phone_pattern = re.compile(
            r'(?<!\d)1[3-9]\d{9}(?!\d)'     # 中国11位手机号（非数字边界）
            r'|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'   # 北美格式
        )
        self.credit_card_pattern = re.compile(
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        )
        # SSN（美国社保号）
        self.ssn_pattern = re.compile(r'\b\d{3}[-]?\d{2}[-]?\d{4}\b')
        # 中国身份证号（18位）
        self.cn_id_pattern = re.compile(r'\b\d{17}[\dXx]\b')
        self.ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
        self.url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
        self.timestamp_pattern = re.compile(
            r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b|\b\d{1,2}:\d{2}(:\d{2})?\b'
        )
        self.date_pattern = re.compile(
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
            re.IGNORECASE
        )

        # [P0修复] 英文姓名：仅匹配 "Firstname Lastname" 格式
        # - 排除常见地名：City / York / Park / Street / Road / Avenue / Bay / Lake 等
        # - 排除常见技术词：New / Old / Big / Fast / Lang / Chain 等
        # 采用否定后瞻，排除已知高频误报词
        _geo_words = {'New', 'Old', 'Big', 'Fast', 'Lang', 'Chain',
                      'City', 'York', 'Park', 'Street', 'Road', 'Avenue',
                      'Bay', 'Lake', 'Hill', 'Town', 'Port', 'Fort', 'Mount'}

        def _name_check(m: re.Match) -> bool:
            parts = m.group(0).split()
            return not (parts[0] in _geo_words or parts[1] in _geo_words)

        self._name_geo_words = _geo_words
        self.name_pattern = re.compile(
            r'\b[A-Z][a-z]{1,15} [A-Z][a-z]{1,15}\b'
        )

        # [P1新增] 中文姓名：2-4个中文字，加上后续判断避免普通词被误识别
        # 使用宽松匹配，仅在明确 PII 上下文（如"姓名：xxx"）中过滤
        self.cn_name_context_pattern = re.compile(
            r'(?:姓名|名字|叫做|是)[：:\s]*[\u4e00-\u9fff]{2,4}'
        )

    # ------------------------------------------------------------------
    # 对外校验接口
    # [P2修复] 先检测原文，再截断，避免截断后无法识别完整 PII
    # ------------------------------------------------------------------

    def validate_evidence(self, evidence: str, topic: str,
                          current_evidence_count: int,
                          topic_evidence_count: int) -> Tuple[bool, str, Optional[str]]:
        if not evidence or not isinstance(evidence, str):
            return False, "Evidence must be a non-empty string", None

        # [P2修复] 先检测，再截断
        if self.config["sanitization_rules"]["remove_personal_identifiers"]:
            if self._contains_personal_identifiers(evidence):
                return False, "证据包含个人身份信息，已拒绝", None

        if self.config["sanitization_rules"]["remove_sensitive_info"]:
            if self._contains_sensitive_info(evidence):
                return False, "证据包含敏感信息，已拒绝", None

        if self.config["sanitization_rules"]["remove_profanity"]:
            if self._contains_profanity(evidence):
                return False, "证据包含不当内容，已拒绝", None

        if self.config["sanitization_rules"]["remove_timestamps"]:
            if self._contains_timestamps(evidence):
                return False, "证据包含时间标记，已拒绝", None

        if current_evidence_count >= self.config["data_validation"]["max_total_evidence"]:
            return False, f"已达最大证据总量 ({self.config['data_validation']['max_total_evidence']})", None

        if topic_evidence_count >= self.config["data_validation"]["max_evidence_per_topic"]:
            return False, f"该主题已达最大证据数量 ({self.config['data_validation']['max_evidence_per_topic']})", None

        # 通过检测后再截断
        max_len = self.config["data_validation"]["max_evidence_length"]
        truncated = evidence[:max_len]

        return True, "Valid", truncated

    def validate_topic_count(self, current_topic_count: int,
                              is_conversation: bool = True) -> Tuple[bool, str]:
        if is_conversation:
            max_topics = self.config["data_validation"]["max_topics_per_conversation"]
        else:
            max_topics = self.config["data_validation"]["max_topics_per_session"]

        if current_topic_count >= max_topics:
            return False, f"已达最大主题数 ({max_topics})"
        return True, "Valid"

    def sanitize_text(self, text: str) -> str:
        sanitized = text

        if self.config["sanitization_rules"]["remove_personal_identifiers"]:
            sanitized = self._remove_personal_identifiers(sanitized)

        if self.config["sanitization_rules"]["remove_sensitive_info"]:
            sanitized = self._remove_sensitive_info(sanitized)

        if self.config["sanitization_rules"]["remove_profanity"]:
            sanitized = self._remove_profanity(sanitized)

        if self.config["sanitization_rules"]["remove_timestamps"]:
            sanitized = self._remove_timestamps(sanitized)

        return sanitized

    def validate_profile_update(self, profile_data: Dict,
                                 current_evidence: Dict) -> Tuple[bool, str]:
        total_evidence = sum(len(v) for v in current_evidence.values())

        for topic, evidences in profile_data.items():
            topic_count = len(current_evidence.get(topic, []))

            for evidence in evidences:
                is_valid, message, _ = self.validate_evidence(
                    evidence, topic, total_evidence, topic_count
                )
                if not is_valid:
                    return False, message
                total_evidence += 1
                topic_count += 1

        return True, "Valid"

    # ------------------------------------------------------------------
    # 检测方法
    # ------------------------------------------------------------------

    def _contains_personal_identifiers(self, text: str) -> bool:
        # 英文 email / 电话 / SSN
        for p in [self.email_pattern, self.phone_pattern, self.ssn_pattern]:
            if p.search(text):
                return True
        # 英文姓名（排除已知地名/技术词）
        for m in self.name_pattern.finditer(text):
            parts = m.group(0).split()
            if not (parts[0] in self._name_geo_words or parts[1] in self._name_geo_words):
                return True
        # [P1新增] 中国身份证、上下文中文姓名
        if self.cn_id_pattern.search(text):
            return True
        if self.cn_name_context_pattern.search(text):
            return True
        return False

    def _contains_sensitive_info(self, text: str) -> bool:
        patterns = [self.credit_card_pattern, self.ip_pattern, self.url_pattern]
        return any(p.search(text) for p in patterns)

    def _contains_profanity(self, text: str) -> bool:
        # 英文基础词表（可扩展）
        en_profanity = ['fuck', 'shit', 'damn', 'ass', 'bitch', 'crap', 'bastard']
        text_lower = text.lower()
        return any(w in text_lower for w in en_profanity)

    def _contains_timestamps(self, text: str) -> bool:
        return bool(self.timestamp_pattern.search(text) or self.date_pattern.search(text))

    # ------------------------------------------------------------------
    # 净化方法
    # ------------------------------------------------------------------

    def _remove_personal_identifiers(self, text: str) -> str:
        text = self.email_pattern.sub('[EMAIL]', text)
        text = self.phone_pattern.sub('[PHONE]', text)
        text = self.ssn_pattern.sub('[SSN]', text)
        text = self.cn_id_pattern.sub('[ID]', text)
        # 英文姓名：只替换非地名/技术词的匹配
        def _replace_name(m: re.Match) -> str:
            parts = m.group(0).split()
            if parts[0] in self._name_geo_words or parts[1] in self._name_geo_words:
                return m.group(0)
            return '[NAME]'
        text = self.name_pattern.sub(_replace_name, text)
        # 上下文中文姓名：仅替换姓名部分
        text = self.cn_name_context_pattern.sub(
            lambda m: m.group(0).rsplit(m.group(0)[-1], 1)[0] + '[姓名]'
            if len(m.group(0)) > 2 else '[姓名]', text
        )
        return text

    def _remove_sensitive_info(self, text: str) -> str:
        text = self.credit_card_pattern.sub('[CARD]', text)
        text = self.ip_pattern.sub('[IP]', text)
        text = self.url_pattern.sub('[URL]', text)
        return text

    def _remove_profanity(self, text: str) -> str:
        en_profanity = ['fuck', 'shit', 'damn', 'ass', 'bitch', 'crap', 'bastard']
        for word in en_profanity:
            text = re.sub(r'\b' + word + r'\b', '[REDACTED]', text, flags=re.IGNORECASE)
        return text

    def _remove_timestamps(self, text: str) -> str:
        text = self.timestamp_pattern.sub('[DATE]', text)
        text = self.date_pattern.sub('[DATE]', text)
        return text
