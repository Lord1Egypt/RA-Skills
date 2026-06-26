#!/usr/bin/env python3
"""
Batch processing for PDF Field Extractor.
Handles multiple PDFs simultaneously with progress tracking.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from .pdf_extractor import extract_pdf_text, PDFExtractResult
from .ocr_processor import ocr_pdf_pages
from .field_extractor import extract_fields
from .doc_type_identifier import identify_doc_type
from .output_generator import generate_excel, generate_json, merge_results
from .tier_config import TierConfig, resolve_doc_type


@dataclass
class ProcessingResult:
    """Result of processing a single PDF."""
    filename: str
    success: bool
    doc_type: str
    fields: Dict[str, Any]
    error: Optional[str] = None
    page_count: int = 0
    is_scanned: bool = False


def process_single_pdf(
    pdf_path: str,
    doc_type_hint: Optional[str] = None,
    custom_fields: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
    ocr_languages: Optional[List[str]] = None,
) -> ProcessingResult:
    """
    Process a single PDF file end-to-end.

    Args:
        pdf_path: Path to the PDF file.
        doc_type_hint: User hint for document type.
        custom_fields: Custom fields for generic type.
        api_key: API key for AI extraction.
        api_base: API base URL.
        model: Model name.
        ocr_languages: Languages for OCR.

    Returns:
        ProcessingResult with extracted fields or error.
    """
    filename = os.path.basename(pdf_path)

    try:
        # Step 1: Extract text
        extract_result = extract_pdf_text(pdf_path)
        page_count = extract_result.page_count
        is_scanned = extract_result.is_scanned
        text = extract_result.full_text

        # Step 2: OCR if scanned
        if is_scanned and extract_result.page_count > 0:
            langs = ocr_languages or ["eng"]
            ocr_texts = ocr_pdf_pages(pdf_path, languages=langs, preprocess=True)
            text = "\n".join(ocr_texts)

        # Step 3: Identify document type
        if doc_type_hint:
            doc_type = resolve_doc_type(doc_type_hint)
        else:
            doc_type = identify_doc_type(text)

        # Step 4: Extract fields with AI
        if api_key:
            fields = extract_fields(
                text=text,
                doc_type=doc_type,
                custom_fields=custom_fields,
                api_key=api_key,
                api_base=api_base,
                model=model,
            )
        else:
            # Without API key, return raw text info
            fields = {
                "文档类型": doc_type,
                "页数": page_count,
                "是否扫描件": is_scanned,
                "文本长度": len(text),
                "文本预览": text[:500] if text else "",
            }

        return ProcessingResult(
            filename=filename,
            success=True,
            doc_type=doc_type,
            fields=fields,
            page_count=page_count,
            is_scanned=is_scanned,
        )

    except Exception as e:
        return ProcessingResult(
            filename=filename,
            success=False,
            doc_type="unknown",
            fields={},
            error=str(e),
        )


def process_batch(
    pdf_files: List[str],
    doc_type: Optional[str] = None,
    custom_fields: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
    max_workers: int = 4,
    tier_config: Optional[TierConfig] = None,
) -> List[Dict[str, Any]]:
    """
    Process multiple PDF files in batch.

    Args:
        pdf_files: List of PDF file paths.
        doc_type: Document type (applies to all files if specified).
        custom_fields: Custom fields for generic type.
        api_key: API key for AI extraction.
        api_base: API base URL.
        model: Model name.
        max_workers: Maximum parallel workers.
        tier_config: Tier configuration for limit checking.

    Returns:
        List of result dictionaries suitable for output generation.
    """
    # Check tier limits
    total_pages = 0
    if tier_config:
        for pdf_path in pdf_files:
            try:
                info = _get_pdf_page_count_estimate(pdf_path)
                total_pages += info.get("page_count", 1)
            except Exception:
                total_pages += 1  # Assume 1 page if can't determine

        tier_config.check_limits(pages=total_pages, batch_size=len(pdf_files))

    results = []
    errors = []

    # Process in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_single_pdf,
                pdf_path,
                doc_type,
                custom_fields,
                api_key,
                api_base,
                model,
            ): pdf_path
            for pdf_path in pdf_files
        }

        for future in as_completed(futures):
            pdf_path = futures[future]
            try:
                result = future.result()
                results.append(result)
                if not result.success:
                    errors.append(f"{result.filename}: {result.error}")
            except Exception as e:
                errors.append(f"{os.path.basename(pdf_path)}: {str(e)}")

    # Build output dictionaries
    output_results = []
    for result in results:
        output_dict = dict(result.fields)
        output_dict["_filename"] = result.filename
        output_dict["_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output_dict["_doc_type"] = result.doc_type
        output_dict["_page_count"] = result.page_count
        output_dict["_is_scanned"] = result.is_scanned
        output_results.append(output_dict)

    return output_results


def _get_pdf_page_count_estimate(pdf_path: str) -> Dict[str, Any]:
    """Get estimated page count without full extraction."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        count = len(doc)
        doc.close()
        return {"page_count": count}
    except Exception:
        return {"page_count": 1}


def run_full_pipeline(
    pdf_files: List[str],
    output_excel: Optional[str] = None,
    output_json: Optional[str] = None,
    doc_type: Optional[str] = None,
    custom_fields: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
    tier: str = "PDF-FREE",
    send_feishu: bool = False,
) -> Dict[str, Any]:
    """
    Run the complete PDF extraction pipeline.

    Args:
        pdf_files: List of PDF file paths.
        output_excel: Optional path to save Excel output.
        output_json: Optional path to save JSON output.
        doc_type: Document type hint.
        custom_fields: Custom fields for generic type.
        api_key: API key for AI extraction.
        api_base: API base URL.
        model: Model name.
        tier: Subscription tier for limit checking.
        send_feishu: Whether to return Feishu message content.

    Returns:
        Dictionary with results and output paths.
    """
    tier_config = TierConfig(tier=tier)

    # Process batch
    results = process_batch(
        pdf_files=pdf_files,
        doc_type=doc_type,
        custom_fields=custom_fields,
        api_key=api_key,
        api_base=api_base,
        model=model,
        max_workers=4,
        tier_config=tier_config,
    )

    # Determine output paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_path = output_excel or f"pdf_extraction_results_{timestamp}.xlsx"
    json_path = output_json or f"pdf_extraction_results_{timestamp}.json"

    # Generate outputs
    if tier_config.supports_format("excel"):
        generate_excel(results, excel_path)

    if tier_config.supports_format("json"):
        generate_json(results, json_path)

    # Build Feishu message if requested
    feishu_msg = None
    if send_feishu:
        from .output_generator import build_feishu_text_message
        feishu_msg = build_feishu_text_message(results, doc_type or "generic")

    return {
        "results": results,
        "total_files": len(results),
        "successful": sum(1 for r in results if not r.get("_error")),
        "failed": sum(1 for r in results if r.get("_error")),
        "excel_path": excel_path if tier_config.supports_format("excel") else None,
        "json_path": json_path if tier_config.supports_format("json") else None,
        "feishu_message": feishu_msg,
    }
