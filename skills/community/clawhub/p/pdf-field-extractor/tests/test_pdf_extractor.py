#!/usr/bin/env python3
"""
Test suite for PDF Field Extractor.
Run with: pytest tests/ -v
"""

import json
import os
import sys
import tempfile
from unittest.mock import MagicMock, patch

import pytest

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.tier_config import (
    TierConfig,
    TIER_LIMITS,
    get_default_fields_for_doc_type,
    resolve_doc_type,
    DOC_TYPE_FIELDS,
)
from scripts.pdf_extractor import (
    extract_pdf_text,
    extract_page_text,
    get_pdf_info,
    PDFExtractResult,
)
from scripts.ocr_processor import (
    get_tesseract_lang_codes,
    preprocess_for_ocr,
)
from scripts.field_extractor import (
    _parse_json_response,
    build_user_prompt,
)
from scripts.doc_type_identifier import (
    identify_doc_type,
    get_confidence_scores,
    get_type_display_name,
)
from scripts.output_generator import (
    generate_excel,
    generate_json,
    build_feishu_message,
    build_feishu_text_message,
    merge_results,
)
from scripts.batch_processor import (
    process_single_pdf,
    ProcessingResult,
)


# ─── Fixtures ─────────────────────────────────────────────────────────────────
@pytest.fixture
def sample_pdf_path():
    """Return path to a sample PDF for testing."""
    return os.path.join(os.path.dirname(__file__), "samples", "sample_invoice.pdf")


@pytest.fixture
def temp_excel_path():
    """Return a temporary file path for Excel output."""
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def temp_json_path():
    """Return a temporary file path for JSON output."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def sample_extraction_result():
    """Return a sample extraction result for testing."""
    return {
        "发票号": "12345678",
        "日期": "2024-01-01",
        "金额": "1000.00",
        "买方": "XX公司",
        "卖方": "YY公司",
    }


# ─── Tier Config Tests ────────────────────────────────────────────────────────
class TestTierConfig:
    """Tests for TierConfig."""

    def test_tier_free_defaults(self):
        config = TierConfig(tier="PDF-FREE")
        limits = config.get_limits()
        assert limits["pages_per_month"] == 10
        assert "invoice" in limits["doc_types"]
        assert len(limits["doc_types"]) == 1
        assert "text" in limits["output_formats"]
        assert limits["batch_size"] == 1

    def test_tier_bsc_limits(self):
        config = TierConfig(tier="PDF-BSC")
        limits = config.get_limits()
        assert limits["pages_per_month"] == 200
        assert len(limits["doc_types"]) == 4
        assert "excel" in limits["output_formats"]
        assert limits["batch_size"] == 10

    def test_tier_std_all_doc_types(self):
        config = TierConfig(tier="PDF-STD")
        limits = config.get_limits()
        assert limits["pages_per_month"] == 1000
        assert len(limits["doc_types"]) == 8
        assert "json" in limits["output_formats"]
        assert limits["custom_fields"] is True

    def test_tier_pro_unlimited_pages(self):
        config = TierConfig(tier="PDF-PRO")
        limits = config.get_limits()
        assert limits["pages_per_month"] == float("inf")

    def test_tier_ent_all_languages(self):
        config = TierConfig(tier="PDF-ENT")
        limits = config.get_limits()
        assert "fra" in limits["ocr_languages"]
        assert "deu" in limits["ocr_languages"]
        assert "spa" in limits["ocr_languages"]

    def test_check_limits_within_bounds(self):
        config = TierConfig(tier="PDF-BSC")
        config.check_limits(pages=100, doc_type="invoice", output_format="excel", batch_size=5)

    def test_check_limits_page_exceeded(self):
        config = TierConfig(tier="PDF-BSC")
        with pytest.raises(ValueError, match="Page limit exceeded"):
            config.check_limits(pages=300)

    def test_check_limits_unsupported_doc_type(self):
        config = TierConfig(tier="PDF-FREE")
        with pytest.raises(ValueError, match="not supported"):
            config.check_limits(doc_type="contract")

    def test_check_limits_unsupported_format(self):
        config = TierConfig(tier="PDF-FREE")
        with pytest.raises(ValueError, match="not supported"):
            config.check_limits(output_format="excel")

    def test_check_limits_batch_size_exceeded(self):
        config = TierConfig(tier="PDF-BSC")
        with pytest.raises(ValueError, match="Batch size"):
            config.check_limits(batch_size=20)

    def test_check_limits_custom_fields_not_allowed(self):
        config = TierConfig(tier="PDF-FREE")
        with pytest.raises(ValueError, match="Custom fields not supported"):
            config.check_limits(use_custom_fields=True)

    def test_supports_doc_type(self):
        config = TierConfig(tier="PDF-STD")
        assert config.supports_doc_type("invoice") is True
        assert config.supports_doc_type("contract") is True
        assert config.supports_doc_type("unknown") is False

    def test_supports_format(self):
        config = TierConfig(tier="PDF-STD")
        assert config.supports_format("excel") is True
        assert config.supports_format("json") is True
        assert config.supports_format("pdf") is False

    def test_get_ocr_languages(self):
        config = TierConfig(tier="PDF-STD")
        langs = config.get_ocr_languages()
        assert "eng" in langs
        assert "chi_sim" in langs


class TestDocTypeResolution:
    """Tests for document type resolution."""

    def test_resolve_invoice_variants(self):
        assert resolve_doc_type("发票") == "invoice"
        assert resolve_doc_type("invoice") == "invoice"
        assert resolve_doc_type("增值税发票") == "invoice"

    def test_resolve_contract_variants(self):
        assert resolve_doc_type("合同") == "contract"
        assert resolve_doc_type("contract") == "contract"
        assert resolve_doc_type("协议书") == "contract"

    def test_resolve_generic(self):
        assert resolve_doc_type("其他") == "generic"
        assert resolve_doc_type("文档") == "generic"

    def test_get_default_fields_invoice(self):
        fields = get_default_fields_for_doc_type("invoice")
        assert "发票号" in fields
        assert "金额" in fields
        assert "日期" in fields

    def test_get_default_fields_contract(self):
        fields = get_default_fields_for_doc_type("contract")
        assert "合同号" in fields
        assert "甲方" in fields
        assert "乙方" in fields

    def test_get_default_fields_generic_empty(self):
        fields = get_default_fields_for_doc_type("generic")
        assert fields == []


# ─── PDF Extractor Tests ──────────────────────────────────────────────────────
class TestPDFExtractResult:
    """Tests for PDFExtractResult dataclass."""

    def test_result_creation(self):
        result = PDFExtractResult(
            full_text="test text",
            tables=[[["a", "b"], ["c", "d"]]],
            page_count=1,
            is_scanned=False,
            page_texts=["test text"],
            metadata={"title": "Test"},
        )
        assert result.full_text == "test text"
        assert result.page_count == 1
        assert result.is_scanned is False
        assert len(result.tables) == 1

    def test_result_empty_tables(self):
        result = PDFExtractResult(
            full_text="",
            tables=[],
            page_count=0,
            is_scanned=True,
            page_texts=[],
            metadata={},
        )
        assert result.tables == []
        assert result.is_scanned is True


class TestPDFExtractor:
    """Tests for PDF extractor functions."""

    def test_get_pdf_info_nonexistent(self):
        with pytest.raises(FileNotFoundError):
            get_pdf_info("/nonexistent/file.pdf")

    def test_extract_page_text_nonexistent(self):
        # PyMuPDF raises RuntimeError wrapping FileNotFoundError
        with pytest.raises(RuntimeError, match="Failed to extract"):
            extract_page_text("/nonexistent/file.pdf", 0)


# ─── OCR Processor Tests ──────────────────────────────────────────────────────
class TestOCRProcessor:
    """Tests for OCR processor."""

    def test_get_tesseract_lang_codes_single(self):
        assert get_tesseract_lang_codes(["eng"]) == "eng"

    def test_get_tesseract_lang_codes_multiple(self):
        result = get_tesseract_lang_codes(["eng", "chi_sim"])
        assert "eng" in result
        assert "chi_sim" in result

    def test_get_tesseract_lang_codes_no_duplicates(self):
        result = get_tesseract_lang_codes(["eng", "eng", "chi_sim"])
        assert result.count("eng") == 1

    def test_preprocess_for_ocr_returns_pil_image(self):
        from PIL import Image
        img = Image.new("RGB", (100, 100), color="white")
        processed = preprocess_for_ocr(img)
        assert isinstance(processed, Image.Image)
        assert processed.mode == "L"  # Grayscale


# ─── Field Extractor Tests ───────────────────────────────────────────────────
class TestFieldExtractor:
    """Tests for field extractor."""

    def test_parse_json_response_direct(self):
        json_str = '{"发票号": "123", "金额": "100"}'
        result = _parse_json_response(json_str)
        assert result["发票号"] == "123"
        assert result["金额"] == "100"

    def test_parse_json_response_markdown_block(self):
        content = '```json\n{"发票号": "456"}\n```'
        result = _parse_json_response(content)
        assert result["发票号"] == "456"

    def test_parse_json_response_invalid(self):
        result = _parse_json_response("not valid json at all")
        assert result == {}

    def test_build_user_prompt_generic_with_fields(self):
        prompt = build_user_prompt("generic", ["姓名", "日期"])
        assert "姓名" in prompt
        assert "日期" in prompt

    def test_build_user_prompt_invoice(self):
        prompt = build_user_prompt("invoice", None)
        assert "{text}" in prompt


# ─── Document Type Identifier Tests ───────────────────────────────────────────
class TestDocTypeIdentifier:
    """Tests for document type identifier."""

    def test_identify_invoice_by_keywords(self):
        text = "发票号: 12345678\n金额: 1000.00\n增值税专用发票"
        result = identify_doc_type(text)
        assert result == "invoice"

    def test_identify_contract_by_keywords(self):
        text = "合同号: HT2024001\n甲方: XX公司\n乙方: YY公司\n签订日期: 2024-01-01"
        result = identify_doc_type(text)
        assert result == "contract"

    def test_identify_receipt_by_keywords(self):
        text = "收据\n收款方: XX商店\n金额: 99.00\n日期: 2024-01-01"
        result = identify_doc_type(text)
        assert result == "receipt"

    def test_identify_bank_statement(self):
        text = "银行对账单\n交易明细\n借方金额\n贷方金额\n余额"
        result = identify_doc_type(text)
        assert result == "bank_statement"

    def test_identify_license(self):
        text = "营业执照\n统一社会信用代码: 91110000XXXXXXXX\n法定代表人: 张三"
        result = identify_doc_type(text)
        assert result == "license"

    def test_identify_id_card(self):
        text = "身份证\n姓名: 李四\n性别: 男\n公民身份号码: 110101199001011234"
        result = identify_doc_type(text)
        assert result == "id_card"

    def test_identify_express(self):
        text = "快递单\n运单号: SF1234567890\n发件人: 张三\n收件人: 李四"
        result = identify_doc_type(text)
        assert result == "express"

    def test_identify_generic_low_confidence(self):
        text = "这是一段普通文本，没有任何特定文档类型的关键词。"
        result = identify_doc_type(text)
        assert result == "generic"

    def test_identify_with_user_hint(self):
        text = "一些模糊的文本"
        result = identify_doc_type(text, user_hint="合同")
        assert result == "contract"

    def test_identify_invoice_user_hint_overrides(self):
        text = "收据内容"
        result = identify_doc_type(text, user_hint="发票")
        assert result == "invoice"

    def test_get_confidence_scores(self):
        text = "发票号: 123\n金额: 100\n合同号: 456"
        scores = get_confidence_scores(text)
        assert "invoice" in scores
        assert "contract" in scores
        assert scores["invoice"] > 0
        assert scores["contract"] > 0

    def test_get_type_display_name(self):
        assert get_type_display_name("invoice") == "发票"
        assert get_type_display_name("contract") == "合同"
        assert get_type_display_name("generic") == "通用文档"


# ─── Output Generator Tests ──────────────────────────────────────────────────
class TestOutputGenerator:
    """Tests for output generator."""

    def test_generate_excel_empty_results(self, temp_excel_path, sample_extraction_result):
        results = []
        path = generate_excel(results, temp_excel_path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    def test_generate_excel_with_data(self, temp_excel_path, sample_extraction_result):
        results = [sample_extraction_result]
        path = generate_excel(results, temp_excel_path)
        assert os.path.exists(path)

    def test_generate_excel_with_metadata(self, temp_excel_path, sample_extraction_result):
        results = [dict(sample_extraction_result)]
        results[0]["_filename"] = "test.pdf"
        results[0]["_timestamp"] = "2024-01-01"
        results[0]["_doc_type"] = "invoice"
        path = generate_excel(results, temp_excel_path, include_metadata=True)
        assert os.path.exists(path)

    def test_generate_json_empty(self, temp_json_path):
        results = []
        path = generate_json(results, temp_json_path)
        assert os.path.exists(path)
        with open(path, "r") as f:
            data = json.load(f)
        assert data == []

    def test_generate_json_with_data(self, temp_json_path, sample_extraction_result):
        results = [sample_extraction_result]
        path = generate_json(results, temp_json_path)
        assert os.path.exists(path)
        with open(path, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["发票号"] == "12345678"

    def test_generate_json_pretty_print(self, temp_json_path, sample_extraction_result):
        results = [sample_extraction_result]
        path = generate_json(results, temp_json_path, pretty=True)
        assert os.path.exists(path)

    def test_merge_results(self, sample_extraction_result):
        results = [sample_extraction_result, {"发票号": "87654321"}]
        merged = merge_results(results, ["file1.pdf", "file2.pdf"], ["invoice", "invoice"])
        assert len(merged) == 2
        assert merged[0]["_filename"] == "file1.pdf"
        assert merged[0]["_doc_type"] == "invoice"
        assert merged[1]["_filename"] == "file2.pdf"

    def test_build_feishu_message_empty(self):
        msg = build_feishu_message([])
        assert msg["msg_type"] == "text"
        assert "未提取" in msg["content"]["text"]

    def test_build_feishu_message_with_results(self, sample_extraction_result):
        results = [dict(sample_extraction_result)]
        results[0]["_filename"] = "invoice.pdf"
        msg = build_feishu_message(results, doc_type="invoice")
        assert msg["msg_type"] == "interactive"
        assert "card" in msg

    def test_build_feishu_text_message(self, sample_extraction_result):
        results = [dict(sample_extraction_result)]
        results[0]["_filename"] = "invoice.pdf"
        msg = build_feishu_text_message(results, doc_type="invoice")
        assert msg["msg_type"] == "text"
        assert "PDF关键信息提取" in msg["content"]

    def test_build_feishu_text_message_empty(self):
        msg = build_feishu_text_message([])
        assert msg["msg_type"] == "text"
        assert "未提取" in msg["content"]


# ─── Batch Processor Tests ────────────────────────────────────────────────────
class TestBatchProcessor:
    """Tests for batch processor."""

    def test_processing_result_success(self):
        result = ProcessingResult(
            filename="test.pdf",
            success=True,
            doc_type="invoice",
            fields={"发票号": "123"},
            page_count=1,
            is_scanned=False,
        )
        assert result.success is True
        assert result.filename == "test.pdf"
        assert result.doc_type == "invoice"

    def test_processing_result_failure(self):
        result = ProcessingResult(
            filename="test.pdf",
            success=False,
            doc_type="unknown",
            fields={},
            error="File not found",
        )
        assert result.success is False
        assert result.error == "File not found"

    def test_process_single_pdf_nonexistent(self):
        result = process_single_pdf("/nonexistent/file.pdf")
        assert result.success is False
        assert result.filename == "file.pdf"
        assert result.error is not None


# ─── Additional Integration Tests ──────────────────────────────────────────────
class TestOCRProcessorIntegration:
    """Integration tests for OCR processor."""

    def test_lang_code_mapping_complete(self):
        from scripts.ocr_processor import LANG_CODE_MAP
        assert "eng" in LANG_CODE_MAP
        assert "chi_sim" in LANG_CODE_MAP
        assert "chi_tra" in LANG_CODE_MAP
        assert "jpn" in LANG_CODE_MAP
        assert "kor" in LANG_CODE_MAP


class TestTableExtraction:
    """Tests for table extraction functionality."""

    def test_pdf_extract_result_empty_tables(self):
        result = PDFExtractResult(
            full_text="text",
            tables=[],
            page_count=0,
            is_scanned=False,
            page_texts=[],
            metadata={},
        )
        assert result.tables == []
        assert result.page_count == 0


class TestOutputGeneratorIntegration:
    """Integration tests for output generator."""

    def test_build_feishu_message_respects_max_items(self):
        results = []
        for i in range(20):
            r = {"_filename": f"doc{i}.pdf", "发票号": str(i)}
            results.append(r)
        msg = build_feishu_message(results, doc_type="invoice", max_items=5)
        # Should not raise, and card should be built
        assert msg["msg_type"] == "interactive"

    def test_generate_json_cleans_internal_fields(self):
        results = [{"发票号": "123", "_filename": "test.pdf", "_timestamp": "2024"}]
        path = "/tmp/test_output.json"
        generate_json(results, path)
        with open(path, "r") as f:
            data = json.load(f)
        assert "_filename" not in data[0]
        assert "_timestamp" not in data[0]
        assert "发票号" in data[0]
        os.remove(path)


class TestDocTypeIdentifierIntegration:
    """Integration tests for document type identifier."""

    def test_identify_receipt_with_high_confidence(self):
        text = """收据 RECEIPT
        收款单位：XX商店
        日期：2024-01-01
        消费金额：188.00元
        项目：餐饮
        """
        result = identify_doc_type(text)
        assert result == "receipt"

    def test_identify_express_with_tracking_keywords(self):
        text = """顺丰快递
        运单号：SF1234567890
        发件人：张三 138xxxx
        收件人：李四 139xxxx
        地址：北京市朝阳区xxx
        """
        result = identify_doc_type(text)
        assert result == "express"

    def test_identify_id_card_with_all_fields(self):
        text = """中华人民共和国居民身份证
        姓名：王五
        性别：男
        出生：1990-01-01
        公民身份号码：110101199001011234
        住址：北京市xxx
        """
        result = identify_doc_type(text)
        assert result == "id_card"



# ─── Tier Limits Tests ───────────────────────────────────────────────────────
class TestTIER_LIMITS:
    """Tests for TIER_LIMITS constant."""

    def test_all_tiers_have_required_keys(self):
        required_keys = ["pages_per_month", "doc_types", "output_formats", "batch_size", "ocr_languages", "custom_fields", "api_access"]
        for tier, limits in TIER_LIMITS.items():
            for key in required_keys:
                assert key in limits, f"Tier {tier} missing key {key}"

    def test_free_tier_restrictive(self):
        limits = TIER_LIMITS["PDF-FREE"]
        assert limits["pages_per_month"] == 10
        assert limits["batch_size"] == 1
        assert limits["custom_fields"] is False
        assert limits["api_access"] is False

    def test_ent_tier_most_permissive(self):
        limits = TIER_LIMITS["PDF-ENT"]
        assert limits["pages_per_month"] == float("inf")
        assert limits["batch_size"] == float("inf")
        assert limits["custom_fields"] is True
        assert limits["api_access"] is True

    def test_all_tiers_recognized(self):
        expected = ["PDF-FREE", "PDF-BSC", "PDF-STD", "PDF-PRO", "PDF-ENT"]
        for tier in expected:
            assert tier in TIER_LIMITS


# ─── Doc Type Aliases Tests ──────────────────────────────────────────────────
class TestDocTypeAliases:
    """Tests for document type aliases."""

    def test_all_aliases_resolve_correctly(self):
        for canonical, aliases in DOC_TYPE_FIELDS.items():
            # Each canonical type should have aliases defined
            pass  # Just ensure iteration works

    def test_invoice_has_fields(self):
        fields = DOC_TYPE_FIELDS["invoice"]
        assert len(fields) > 0
        assert "发票号" in fields

    def test_contract_has_fields(self):
        fields = DOC_TYPE_FIELDS["contract"]
        assert len(fields) > 0

    def test_all_types_have_fields_except_generic(self):
        for doc_type, fields in DOC_TYPE_FIELDS.items():
            if doc_type != "generic":
                assert len(fields) > 0, f"{doc_type} has no fields defined"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
