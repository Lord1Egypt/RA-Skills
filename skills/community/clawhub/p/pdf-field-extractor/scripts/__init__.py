#!/usr/bin/env python3
"""
PDF Field Extractor - AI-powered PDF structured data extraction tool.
"""

from .pdf_extractor import (
    extract_pdf_text,
    extract_page_text,
    extract_tables_from_page,
    get_pdf_info,
    render_page_as_image,
    save_page_as_image,
    PDFExtractResult,
)

from .ocr_processor import (
    ocr_image,
    ocr_image_bytes,
    ocr_pdf_pages,
    preprocess_for_ocr,
    get_ocr_confidence,
)

from .field_extractor import (
    extract_fields,
    extract_fields_batch,
)

from .doc_type_identifier import (
    identify_doc_type,
    get_confidence_scores,
    get_type_display_name,
)

from .output_generator import (
    generate_excel,
    generate_json,
    build_feishu_message,
    build_feishu_text_message,
    merge_results,
)

from .batch_processor import (
    process_single_pdf,
    process_batch,
    run_full_pipeline,
    ProcessingResult,
)

from .tier_config import (
    TierConfig,
    TIER_LIMITS,
    get_default_fields_for_doc_type,
    resolve_doc_type,
    DOC_TYPE_FIELDS,
    DOC_TYPE_ALIASES,
)

__all__ = [
    # PDF extraction
    "extract_pdf_text",
    "extract_page_text",
    "extract_tables_from_page",
    "get_pdf_info",
    "render_page_as_image",
    "save_page_as_image",
    "PDFExtractResult",
    # OCR
    "ocr_image",
    "ocr_image_bytes",
    "ocr_pdf_pages",
    "preprocess_for_ocr",
    "get_ocr_confidence",
    # Field extraction
    "extract_fields",
    "extract_fields_batch",
    # Doc type
    "identify_doc_type",
    "get_confidence_scores",
    "get_type_display_name",
    # Output
    "generate_excel",
    "generate_json",
    "build_feishu_message",
    "build_feishu_text_message",
    "merge_results",
    # Batch
    "process_single_pdf",
    "process_batch",
    "run_full_pipeline",
    "ProcessingResult",
    # Tier
    "TierConfig",
    "TIER_LIMITS",
    "get_default_fields_for_doc_type",
    "resolve_doc_type",
    "DOC_TYPE_FIELDS",
    "DOC_TYPE_ALIASES",
]
