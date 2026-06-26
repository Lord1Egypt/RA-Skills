#!/usr/bin/env python3
"""Static rule/config data for the local redact detector."""

from __future__ import annotations

import re
from typing import Any, Dict, List

SENSITIVE_TYPES = (
    "phone",
    "email",
    "idCard",
    "creditCard",
    "bankCard",
    "address",
    "name",
    "password",
    "apiKey",
    "ipAddress",
    "ssn",
    "passport",
    "dateOfBirth",
)

PROFILE_CHOICES = ("strict", "balanced", "precision")
PROFILE_THRESHOLD_DELTA = {
    "strict": -0.12,
    "balanced": 0.0,
    "precision": 0.10,
}

SCORING_METHOD = "heuristic-v1"
DETECTOR_VERSION = "local-rules-v1"

PLACEHOLDER_MAP = {
    "phone": "PHONE",
    "email": "EMAIL",
    "idCard": "ID_CARD",
    "creditCard": "CREDIT_CARD",
    "bankCard": "BANK_CARD",
    "address": "ADDRESS",
    "name": "NAME",
    "password": "PASSWORD",
    "apiKey": "API_KEY",
    "ipAddress": "IP_ADDRESS",
    "ssn": "SSN",
    "passport": "PASSPORT",
    "dateOfBirth": "DOB",
}

TYPE_LABELS = {
    "phone": "Phone Number",
    "email": "Email",
    "idCard": "ID Card",
    "creditCard": "Credit Card",
    "bankCard": "Bank Card",
    "address": "Address",
    "name": "Name",
    "password": "Password",
    "apiKey": "API Key",
    "ipAddress": "IP Address",
    "ssn": "SSN",
    "passport": "Passport",
    "dateOfBirth": "Date of Birth",
}

HIGH_RISK_TYPES = [
    "idCard",
    "creditCard",
    "bankCard",
    "password",
    "apiKey",
    "ssn",
    "passport",
]
MEDIUM_RISK_TYPES = ["phone", "email", "ipAddress"]

RISK_WEIGHTS = {
    "idCard": 35,
    "ssn": 35,
    "creditCard": 35,
    "bankCard": 30,
    "passport": 30,
    "password": 40,
    "apiKey": 40,
    "phone": 25,
    "email": 15,
    "ipAddress": 20,
    "address": 15,
    "name": 8,
    "dateOfBirth": 12,
}

BASE_CONFIDENCE_BY_TYPE = {
    "apiKey": 0.84,
    "password": 0.82,
    "creditCard": 0.80,
    "bankCard": 0.76,
    "idCard": 0.82,
    "ssn": 0.84,
    "passport": 0.80,
    "phone": 0.74,
    "email": 0.78,
    "ipAddress": 0.74,
    "address": 0.72,
    "name": 0.82,
    "dateOfBirth": 0.78,
}

BASE_THRESHOLDS_BALANCED = {
    "apiKey": 0.45,
    "password": 0.45,
    "creditCard": 0.50,
    "bankCard": 0.50,
    "idCard": 0.55,
    "ssn": 0.55,
    "passport": 0.55,
    "phone": 0.70,
    "email": 0.70,
    "ipAddress": 0.70,
    "dateOfBirth": 0.80,
    "address": 0.80,
    "name": 0.88,
}

CONTEXT_KEYWORDS = {
    "phone": ["phone", "tel", "mobile", "contact", "电话", "手机号", "联系电话"],
    "email": ["email", "mail", "contact", "邮箱", "邮件"],
    "idCard": ["id", "identity", "身份证", "证件", "id card"],
    "creditCard": ["card", "credit", "visa", "mastercard", "银行卡", "信用卡"],
    "bankCard": ["bank", "account", "iban", "银行卡", "开户"],
    "address": ["address", "shipping", "billing", "收货", "地址"],
    "name": ["name", "full name", "contact", "姓名", "联系人", "收件人"],
    "password": ["password", "passwd", "pwd", "credential", "口令", "密码"],
    "apiKey": ["api key", "token", "secret", "bearer", "auth", "密钥"],
    "ipAddress": ["ip", "client", "server", "host", "网关", "地址"],
    "ssn": ["ssn", "social security", "national insurance"],
    "passport": ["passport", "护照"],
    "dateOfBirth": ["dob", "birthday", "born", "出生", "生日"],
}

NEGATIVE_CONTEXT_KEYWORDS = {
    "phone": ["order", "invoice", "ticket", "sku", "serial", "product id"],
    "name": ["test", "sample", "dummy", "测试"],
    "apiKey": ["example", "sample", "dummy"],
    "password": ["example", "sample", "dummy"],
}

REQUIRED_VALIDATOR_TYPES = {"idCard", "creditCard", "bankCard", "ssn", "passport"}

RULE_KIND_EXACT = "exact"
RULE_KIND_REGEX = "regex"

PLACEHOLDER_PATTERN = re.compile(r"^\[[A-Z_]+_\d+\]$")

BUILTIN_ALLOWLIST_RULES = [
    {
        "type": "*",
        "kind": "regex",
        "value": r"^\[[A-Z_]+_\d+\]$",
    }
]

NAME_STOPWORDS_CN = {
    "测试",
    "管理员",
    "公司",
    "大学",
    "医院",
    "省",
    "市",
    "区",
    "县",
    "路",
    "街",
}
NAME_STOPWORDS_EN = {
    "admin",
    "administrator",
    "root",
    "user",
    "test",
    "company",
    "university",
    "hospital",
    "street",
    "road",
}

NAME_CONTEXT_PATTERNS = [
    {
        "lang": "cn",
        "pattern": re.compile(
            r"(?m)(?:姓名|真实姓名|联系人|收件人|签名|署名|持卡人|开户名)\s*[：:]\s*([\u4e00-\u9fa5·]{2,6})"
        ),
    },
    {
        "lang": "en",
        "pattern": re.compile(
            r"(?m)\b(?i:(?:name|full\s*name|contact|recipient|signed\s*by|cardholder|account\s*holder))\b\s*[:=]\s*([A-Z][a-z]+(?:[ '-][A-Z][a-z]+){1,2})"
        ),
    },
]

REGEX_PATTERNS = [
    {
        "type": "idCard",
        "label": "ID Card",
        "patterns": [
            r"\b[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b",
            r"\b[1-9]\d{5}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}\b",
            r"\b[A-Z]{1,2}\d{6}\([0-9A]\)",
            r"\b[A-Z][12]\d{8}\b",
        ],
    },
    {
        "type": "phone",
        "label": "Phone Number",
        "patterns": [
            r"(?<!\d)(?:(?:\+|00)86[-.\s]?)?1(?:3\d|4[5-79]|5[0-35-9]|6[5-7]|7[0-8]|8\d|9[189])[-.\s]?\d{4}[-.\s]?\d{4}(?!\d)",
            r"(?<!\d)(?:\+?1[-.\s]?)?(?:\([2-9]\d{2}\)|[2-9]\d{2})[-.\s]?[2-9]\d{2}[-.\s]?\d{4}(?:\s?(?:#|x|ext\.?|extension)\s?\d{1,6})?(?!\d)",
            r"(?<!\d)(?:\+44[-.\s]?7\d{3}|0?7\d{3})[-.\s]?\d{3}[-.\s]?\d{3}(?!\d)",
            r"(?<!\d)\+[2-9]\d{1,2}[-.\s]?(?:\(\d{2,4}\)|\d{2,4})[-.\s]?\d{3,4}[-.\s]?\d{3,4}(?!\d)",
            r"(?<!\d)0\d{2,3}[-.\s]\d{7,8}(?!\d)",
        ],
    },
    {
        "type": "email",
        "label": "Email",
        "patterns": [r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"],
    },
    {
        "type": "creditCard",
        "label": "Credit Card",
        "patterns": [
            r"\b4[0-9]{12}(?:[0-9]{3})?\b",
            r"\b(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}\b",
            r"\b3[47][0-9]{13}\b",
            r"\b6(?:011|5[0-9]{2})[0-9]{12}\b",
            r"\b(?:2131|1800|35\d{3})\d{11}\b",
            r"\b62[0-9]{14,17}\b",
            r"\b4[0-9]{3}[-\s][0-9]{4}[-\s][0-9]{4}[-\s][0-9]{4}\b",
            r"\b5[1-5][0-9]{2}[-\s][0-9]{4}[-\s][0-9]{4}[-\s][0-9]{4}\b",
        ],
    },
    {
        "type": "bankCard",
        "label": "Bank Card",
        "patterns": [
            r"\b(?:622|621|620|623|625|626|627|628|629)\d{13,16}\b",
            r"\b[1-9]\d{3}[-\s]\d{4}[-\s]\d{4}[-\s]\d{4,7}\b",
        ],
    },
    {
        "type": "ipAddress",
        "label": "IP Address",
        "patterns": [
            r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
            r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b",
        ],
    },
    {
        "type": "ssn",
        "label": "SSN",
        "patterns": [
            r"\b(?!000|666|9\d{2})[0-8]\d{2}-(?!00)\d{2}-(?!0000)\d{4}\b",
            r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b",
        ],
    },
    {
        "type": "passport",
        "label": "Passport",
        "patterns": [r"\b[EGDSPHegdsph][a-zA-Z]?\d{8}\b", r"\b[A-Z]{2}\d{7}\b"],
    },
    {
        "type": "dateOfBirth",
        "label": "Date of Birth",
        "patterns": [
            r"(?:19[5-9]\d|20[0-2]\d)年(?:0?[1-9]|1[0-2])月(?:0?[1-9]|[12]\d|3[01])日",
            r"(?:生日|出生|DOB|birthday|born)[：:\s]*(?:19[5-9]\d|20[0-2]\d)[-/](?:0?[1-9]|1[0-2])[-/](?:0?[1-9]|[12]\d|3[01])",
        ],
    },
    {
        "type": "apiKey",
        "label": "API Key",
        "patterns": [
            r"\bsk-[a-zA-Z0-9]{20,}\b",
            r"\b[sp]k_(?:live|test)_[a-zA-Z0-9]{20,}\b",
            r"\bAKIA[0-9A-Z]{16}\b",
            r"\bgh[pousr]_[a-zA-Z0-9]{36,}\b",
            r"(?:api[_-]?key|api[_-]?token|access[_-]?token|auth[_-]?token|secret[_-]?key)\s*[:=]\s*[\"']?[a-zA-Z0-9_-]{20,}[\"']?",
            r"\bBearer\s+[a-zA-Z0-9_-]{20,}",
            r"\beyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}",
        ],
    },
    {
        "type": "password",
        "label": "Password",
        "patterns": [
            r"(?:password|passwd|pwd|secret|credential)\s*[:=]\s*[\"']?[^\s\"']{6,64}[\"']?",
            r"--(?:password|passwd|pwd)\s+[\"']?[^\s\"']{6,64}[\"']?",
        ],
    },
    {
        "type": "address",
        "label": "Address",
        "patterns": [
            r"[\u4e00-\u9fa5]{2,}(?:省|自治区)[\u4e00-\u9fa5]{2,}(?:市|自治州|盟)[\u4e00-\u9fa5]{2,}(?:区|县|市|旗)[\u4e00-\u9fa5\d]+(?:路|街|道|巷|弄)[\u4e00-\u9fa5\d]*号?",
            r"\d{1,5}\s+[A-Za-z\s]{2,25}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct|Way|Place|Pl)\.?(?:\s*,?\s*(?:Apt|Suite|Unit|#)\s*\d+)?",
        ],
    },
]

CN_ID_WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
CN_ID_CHECK_DIGITS = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]


def _compile_patterns() -> List[Dict[str, Any]]:
    compiled: List[Dict[str, Any]] = []
    for entry in REGEX_PATTERNS:
        stype = entry["type"]
        flags = re.IGNORECASE if stype in {"dateOfBirth", "password", "apiKey"} else 0
        compiled.append(
            {
                "type": stype,
                "label": entry["label"],
                "patterns": [re.compile(pattern, flags) for pattern in entry["patterns"]],
            }
        )
    return compiled


COMPILED_PATTERNS = _compile_patterns()


__all__ = [
    "BASE_CONFIDENCE_BY_TYPE",
    "BASE_THRESHOLDS_BALANCED",
    "BUILTIN_ALLOWLIST_RULES",
    "CN_ID_CHECK_DIGITS",
    "CN_ID_WEIGHTS",
    "COMPILED_PATTERNS",
    "CONTEXT_KEYWORDS",
    "DETECTOR_VERSION",
    "HIGH_RISK_TYPES",
    "MEDIUM_RISK_TYPES",
    "NAME_CONTEXT_PATTERNS",
    "NAME_STOPWORDS_CN",
    "NAME_STOPWORDS_EN",
    "NEGATIVE_CONTEXT_KEYWORDS",
    "PLACEHOLDER_MAP",
    "PLACEHOLDER_PATTERN",
    "PROFILE_CHOICES",
    "PROFILE_THRESHOLD_DELTA",
    "REGEX_PATTERNS",
    "REQUIRED_VALIDATOR_TYPES",
    "RISK_WEIGHTS",
    "RULE_KIND_EXACT",
    "RULE_KIND_REGEX",
    "SCORING_METHOD",
    "SENSITIVE_TYPES",
    "TYPE_LABELS",
]
