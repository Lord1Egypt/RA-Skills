#!/usr/bin/env python3
"""
Tier configuration and usage limits for PDF Field Extractor.
Token prefixes: PDF-FREE / PDF-BSC / PDF-STD / PDF-PRO / PDF-ENT
"""

from dataclasses import dataclass
from typing import List, Optional


# ─── Tier Limits ───────────────────────────────────────────────────────────────
TIER_LIMITS = {
    "PDF-FREE": {
        "pages_per_month": 10,
        "doc_types": ["invoice"],
        "output_formats": ["text"],
        "batch_size": 1,
        "ocr_languages": ["eng"],
        "custom_fields": False,
        "api_access": False,
    },
    "PDF-BSC": {
        "pages_per_month": 200,
        "doc_types": ["invoice", "receipt", "license", "id_card"],
        "output_formats": ["excel", "text"],
        "batch_size": 10,
        "ocr_languages": ["eng", "chi_sim"],
        "custom_fields": False,
        "api_access": False,
    },
    "PDF-STD": {
        "pages_per_month": 1000,
        "doc_types": ["invoice", "receipt", "license", "id_card", "contract", "bank_statement", "express", "generic"],
        "output_formats": ["excel", "json", "text"],
        "batch_size": 50,
        "ocr_languages": ["eng", "chi_sim", "chi_tra", "jpn", "kor"],
        "custom_fields": True,
        "api_access": False,
    },
    "PDF-PRO": {
        "pages_per_month": float("inf"),
        "doc_types": ["invoice", "receipt", "license", "id_card", "contract", "bank_statement", "express", "generic"],
        "output_formats": ["excel", "json", "text"],
        "batch_size": float("inf"),
        "ocr_languages": ["eng", "chi_sim", "chi_tra", "jpn", "kor"],
        "custom_fields": True,
        "api_access": True,
    },
    "PDF-ENT": {
        "pages_per_month": float("inf"),
        "doc_types": ["invoice", "receipt", "license", "id_card", "contract", "bank_statement", "express", "generic"],
        "output_formats": ["excel", "json", "text"],
        "batch_size": float("inf"),
        "ocr_languages": ["eng", "chi_sim", "chi_tra", "jpn", "kor", "fra", "deu", "spa", "por", "rus"],
        "custom_fields": True,
        "api_access": True,
    },
}

# ─── Document Type Mapping ──────────────────────────────────────────────────────
DOC_TYPE_ALIASES = {
    "invoice": ["发票", "invoice", "增值税发票", "普通发票", "电子发票"],
    "contract": ["合同", "contract", "协议书", "agreement"],
    "receipt": ["收据", "receipt", "小票", "凭据"],
    "bank_statement": ["银行对账单", "bank_statement", "银行流水", "对账单"],
    "license": ["营业执照", "license", "经营许可证"],
    "id_card": ["身份证", "id_card", "护照", "passport", "证件"],
    "express": ["快递单", "express", "物流单", "运单", "shipping"],
    "generic": ["通用", "generic", "其他", "文档", "document"],
}

DOC_TYPE_FIELDS = {
    "invoice": ["发票号", "日期", "金额", "买方", "卖方", "商品明细", "税率", "发票代码", "备注"],
    "contract": ["合同号", "签订日期", "到期日期", "金额", "甲方", "乙方", "地址", "联系人", "违约条款", "解除条款", "付款条件"],
    "receipt": ["日期", "金额", "收款方", "消费内容", "明细项目", "小费"],
    "bank_statement": ["日期", "交易金额", "对方账户", "余额", "交易类型", "摘要"],
    "license": ["统一社会信用代码", "公司名称", "法人", "注册资本", "注册地址", "经营范围"],
    "id_card": ["姓名", "性别", "出生日期", "国籍", "证件号码", "有效期"],
    "express": ["运单号", "发件人", "收件人", "地址", "重量", "运费"],
    "generic": [],  # 用户自定义
}


@dataclass
class TierConfig:
    """Tier configuration for PDF Field Extractor."""
    tier: str = "PDF-FREE"

    def get_limits(self) -> dict:
        """Return the limits for the current tier."""
        return TIER_LIMITS.get(self.tier, TIER_LIMITS["PDF-FREE"])

    def check_limits(
        self,
        pages: int = 0,
        doc_type: Optional[str] = None,
        output_format: Optional[str] = None,
        batch_size: Optional[int] = None,
        use_custom_fields: bool = False,
    ) -> None:
        """
        Check if the requested usage exceeds tier limits.
        Raises ValueError if any limit is exceeded.
        """
        limits = self.get_limits()

        # Check page limit
        if pages > limits["pages_per_month"]:
            raise ValueError(
                f"Page limit exceeded: {pages} pages requested, "
                f"limit is {limits['pages_per_month']} pages/month for {self.tier}"
            )

        # Check document type
        if doc_type is not None and doc_type not in limits["doc_types"]:
            raise ValueError(
                f"Document type '{doc_type}' not supported in {self.tier}. "
                f"Supported types: {limits['doc_types']}"
            )

        # Check output format
        if output_format is not None and output_format not in limits["output_formats"]:
            raise ValueError(
                f"Output format '{output_format}' not supported in {self.tier}. "
                f"Supported formats: {limits['output_formats']}"
            )

        # Check batch size
        if batch_size is not None and batch_size > limits["batch_size"]:
            raise ValueError(
                f"Batch size {batch_size} exceeds limit of {limits['batch_size']} "
                f"for {self.tier}"
            )

        # Check custom fields
        if use_custom_fields and not limits["custom_fields"]:
            raise ValueError(
                f"Custom fields not supported in {self.tier}. "
                f"Upgrade to Standard or higher."
            )

    def supports_doc_type(self, doc_type: str) -> bool:
        """Check if this tier supports the given document type."""
        return doc_type in self.get_limits()["doc_types"]

    def supports_format(self, fmt: str) -> bool:
        """Check if this tier supports the given output format."""
        return fmt in self.get_limits()["output_formats"]

    def get_ocr_languages(self) -> List[str]:
        """Get the list of OCR languages supported by this tier."""
        return self.get_limits()["ocr_languages"]


def get_default_fields_for_doc_type(doc_type: str) -> List[str]:
    """Return the default extraction fields for a document type."""
    return DOC_TYPE_FIELDS.get(doc_type, [])


def resolve_doc_type(doc_type_input: str) -> str:
    """Resolve a user-input doc type string to a canonical type."""
    doc_type_input_lower = doc_type_input.lower().strip()
    for canonical, aliases in DOC_TYPE_ALIASES.items():
        if doc_type_input_lower in [a.lower() for a in aliases] or doc_type_input_lower == canonical:
            return canonical
    return "generic"
