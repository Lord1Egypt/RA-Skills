#!/usr/bin/env python3
"""
Document type identification for PDF Field Extractor.
Uses keyword matching and AI-assisted classification.
"""

import re
from typing import Optional

from .tier_config import DOC_TYPE_ALIASES, resolve_doc_type


# ─── Keyword Patterns for Each Document Type ──────────────────────────────────
TYPE_PATTERNS = {
    "invoice": [
        r"发票", r"invoice", r"增值税", r"价税合计", r"发票代码", r"发票号码",
        r"销方", r"购方", r"开票日期", r"专用发票", r"普通发票", r"电子发票",
        r"tax invoice", r"billing", r"receipt invoice",
    ],
    "contract": [
        r"合同", r"contract", r"协议书", r"agreement", r"甲方", r"乙方",
        r"签订日期", r"到期日", r"有效期", r"违约", r"解除条款", r"付款条件",
        r"合同号", r"contract no", r"party a", r"party b",
    ],
    "receipt": [
        r"收据", r"receipt", r"小票", r"凭据", r"消费", r"付款凭证",
        r"流水号", r"交易金额", r"收款方", r"消费明细",
    ],
    "bank_statement": [
        r"银行对账单", r"bank statement", r"银行流水", r"对账单",
        r"交易明细", r"余额", r"借方", r"贷方", r"对方账户", r"摘要",
        r"account statement", r"transactions",
    ],
    "license": [
        r"营业执照", r"license", r"经营许可证", r"统一社会信用代码",
        r"法定代表人", r"注册资本", r"注册地址", r"经营范围",
        r"business license", r"registration",
    ],
    "id_card": [
        r"身份证", r"id card", r"passport", r"护照", r"证件号码",
        r"姓名", r"性别", r"出生", r"国籍", r"有效期",
        r"公民身份号码", r"居民身份证",
    ],
    "express": [
        r"快递单", r"运单", r"物流单", r"shipping", r"express",
        r"发件人", r"收件人", r"寄件人", r"收件人", r"快递公司",
        r"运单号", r"tracking", r"delivery",
    ],
}


def identify_doc_type(text: str, user_hint: Optional[str] = None) -> str:
    """
    Identify the document type from extracted text.

    Priority:
    1. User hint (if provided)
    2. Keyword pattern matching
    3. Default to "generic"

    Args:
        text: Extracted text from the PDF.
        user_hint: Optional user-provided hint (e.g., "发票", "合同").

    Returns:
        Canonical document type string.
    """
    # Priority 1: User hint
    if user_hint:
        resolved = resolve_doc_type(user_hint)
        if resolved != "generic":
            return resolved

    # Priority 2: Keyword pattern matching
    text_lower = text.lower()

    scores = {}
    for doc_type, patterns in TYPE_PATTERNS.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 1
        if score > 0:
            scores[doc_type] = score

    if scores:
        # Return the type with the highest score
        best_type = max(scores, key=scores.get)
        # Only return if confidence is reasonable (at least 2 matches)
        if scores[best_type] >= 2:
            return best_type

    return "generic"


def get_confidence_scores(text: str) -> dict:
    """
    Get confidence scores for all document types.

    Args:
        text: Extracted text from the PDF.

    Returns:
        Dictionary mapping document type to confidence score (0.0 - 1.0).
    """
    text_lower = text.lower()
    total_patterns = sum(len(patterns) for patterns in TYPE_PATTERNS.values())

    scores = {}
    for doc_type, patterns in TYPE_PATTERNS.items():
        matched = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matched += 1
        scores[doc_type] = matched / len(patterns) if patterns else 0.0

    return scores


def get_type_display_name(doc_type: str) -> str:
    """Get the display name for a document type."""
    display_names = {
        "invoice": "发票",
        "contract": "合同",
        "receipt": "收据",
        "bank_statement": "银行对账单",
        "license": "营业执照",
        "id_card": "身份证/护照",
        "express": "快递单",
        "generic": "通用文档",
    }
    return display_names.get(doc_type, doc_type)
