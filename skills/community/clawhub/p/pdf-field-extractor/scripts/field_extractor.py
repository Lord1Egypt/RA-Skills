#!/usr/bin/env python3
"""
AI-powered field extraction using OpenAI-compatible API.
Model-agnostic: works with any OpenAI-compatible model (GPT-4o, DeepSeek, MiniMax, etc.)
"""

import json
import re
from typing import Any, Dict, List, Optional

import requests

from .tier_config import DOC_TYPE_FIELDS, get_default_fields_for_doc_type


# ─── Default API Configuration ───────────────────────────────────────────────
DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TIMEOUT = 60  # seconds


# ─── System Prompts by Document Type ─────────────────────────────────────────
SYSTEM_PROMPTS = {
    "invoice": """You are an expert at extracting structured information from invoices.
Extract the following fields from the invoice text:
- 发票号 (Invoice Number)
- 日期 (Date)
- 金额 (Amount)
- 买方 (Buyer)
- 卖方 (Seller)
- 商品明细 (Line Items)
- 税率 (Tax Rate)
- 发票代码 (Invoice Code)
- 备注 (Notes)

Return ONLY valid JSON in this exact format:
{
  "发票号": "...",
  "日期": "...",
  "金额": "...",
  "买方": "...",
  "卖方": "...",
  "商品明细": "...",
  "税率": "...",
  "发票代码": "...",
  "备注": "..."
}

If a field is not found, use null. Do not add any explanation.""",

    "contract": """You are an expert at extracting structured information from contracts.
Extract the following fields from the contract text:
- 合同号 (Contract Number)
- 签订日期 (Signing Date)
- 到期日期 (Expiration Date)
- 金额 (Amount)
- 甲方 (Party A)
- 乙方 (Party B)
- 地址 (Address)
- 联系人 (Contact Person)
- 违约条款 (Default Terms)
- 解除条款 (Termination Terms)
- 付款条件 (Payment Terms)

Return ONLY valid JSON in this exact format:
{
  "合同号": "...",
  "签订日期": "...",
  "到期日期": "...",
  "金额": "...",
  "甲方": "...",
  "乙方": "...",
  "地址": "...",
  "联系人": "...",
  "违约条款": "...",
  "解除条款": "...",
  "付款条件": "..."
}

If a field is not found, use null. Do not add any explanation.""",

    "receipt": """You are an expert at extracting structured information from receipts.
Extract the following fields from the receipt text:
- 日期 (Date)
- 金额 (Amount)
- 收款方 (Payee)
- 消费内容 (Items)
- 明细项目 (Line Items)
- 小费 (Tip)

Return ONLY valid JSON in this exact format:
{
  "日期": "...",
  "金额": "...",
  "收款方": "...",
  "消费内容": "...",
  "明细项目": "...",
  "小费": "..."
}

If a field is not found, use null. Do not add any explanation.""",

    "bank_statement": """You are an expert at extracting structured information from bank statements.
Extract the following fields from the bank statement text:
- 日期 (Transaction Date)
- 交易金额 (Transaction Amount)
- 对方账户 (Counterparty Account)
- 余额 (Balance)
- 交易类型 (Transaction Type)
- 摘要 (Summary)

Return ONLY valid JSON in this exact format:
{
  "日期": "...",
  "交易金额": "...",
  "对方账户": "...",
  "余额": "...",
  "交易类型": "...",
  "摘要": "..."
}

If a field is not found, use null. Do not add any explanation.""",

    "license": """You are an expert at extracting structured information from business licenses.
Extract the following fields from the license text:
- 统一社会信用代码 (Unified Social Credit Code)
- 公司名称 (Company Name)
- 法人 (Legal Representative)
- 注册资本 (Registered Capital)
- 注册地址 (Registered Address)
- 经营范围 (Business Scope)

Return ONLY valid JSON in this exact format:
{
  "统一社会信用代码": "...",
  "公司名称": "...",
  "法人": "...",
  "注册资本": "...",
  "注册地址": "...",
  "经营范围": "..."
}

If a field is not found, use null. Do not add any explanation.""",

    "id_card": """You are an expert at extracting structured information from ID cards and passports.
Extract the following fields from the document text:
- 姓名 (Full Name)
- 性别 (Gender)
- 出生日期 (Date of Birth)
- 国籍 (Nationality)
- 证件号码 (Document Number)
- 有效期 (Expiration Date)

Return ONLY valid JSON in this exact format:
{
  "姓名": "...",
  "性别": "...",
  "出生日期": "...",
  "国籍": "...",
  "证件号码": "...",
  "有效期": "..."
}

If a field is not found, use null. Do not add any explanation.""",

    "express": """You are an expert at extracting structured information from express delivery forms.
Extract the following fields from the document text:
- 运单号 (Tracking Number)
- 发件人 (Sender)
- 收件人 (Recipient)
- 地址 (Address)
- 重量 (Weight)
- 运费 (Shipping Cost)

Return ONLY valid JSON in this exact format:
{
  "运单号": "...",
  "发件人": "...",
  "收件人": "...",
  "地址": "...",
  "重量": "...",
  "运费": "..."
}

If a field is not found, use null. Do not add any explanation.""",

    "generic": """You are an expert at extracting structured information from documents.
Extract the key fields from the document text based on the user's request.

Return ONLY valid JSON with the extracted fields.
If a field is not found, use null. Do not add any explanation.""",
}


def build_user_prompt(doc_type: str, custom_fields: Optional[List[str]] = None) -> str:
    """Build the user prompt for field extraction."""
    if doc_type == "generic" and custom_fields:
        fields_list = ", ".join(custom_fields)
        return f"""Extract the following fields from the document: {fields_list}

Return ONLY valid JSON with those exact field names as keys.
If a field is not found, use null. Do not add any explanation.

Document text:
{{text}}"""
    else:
        return """Extract all relevant information from this document.

Document text:
{text}"""


def extract_fields(
    text: str,
    doc_type: str = "generic",
    custom_fields: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.1,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    Extract structured fields from text using AI.

    Args:
        text: Extracted text from the PDF.
        doc_type: Document type (invoice/contract/receipt/etc.).
        custom_fields: For generic type, list of field names to extract.
        api_key: API key for the AI service. If None, uses env var OPENAI_API_KEY.
        api_base: Base URL for the API. Defaults to OpenAI.
        model: Model name to use. Defaults to gpt-4o.
        temperature: Sampling temperature (0.0 - 1.0).
        timeout: Request timeout in seconds.

    Returns:
        Dictionary of extracted fields.
    """
    if not text or len(text.strip()) < 10:
        return {}

    # Get API credentials
    if api_key is None:
        import os
        api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError(
            "API key is required for field extraction. "
            "Pass api_key or set OPENAI_API_KEY environment variable."
        )

    api_base = api_base or DEFAULT_API_BASE
    model = model or DEFAULT_MODEL

    # Build messages
    system_prompt = SYSTEM_PROMPTS.get(doc_type, SYSTEM_PROMPTS["generic"])
    user_prompt = build_user_prompt(doc_type, custom_fields).format(text=text[:8000])  # Truncate to 8k chars

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Call API
    endpoint = f"{api_base.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise TimeoutError(f"API request timed out after {timeout}s")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")

    result = response.json()

    # Parse response
    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected API response format: {result}")

    # Extract JSON from response
    fields = _parse_json_response(content)

    return fields


def _parse_json_response(content: str) -> Dict[str, Any]:
    """
    Parse JSON from the AI response content.

    Handles cases where the model wraps JSON in markdown code blocks.
    """
    # Try direct JSON parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code block
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find raw JSON object
    json_match = re.search(r"\{[\s\S]*\}", content)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback: return empty dict
    return {}


def extract_fields_batch(
    texts: List[str],
    doc_type: str = "generic",
    custom_fields: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
    max_workers: int = 4,
) -> List[Dict[str, Any]]:
    """
    Extract fields from multiple texts in parallel.

    Note: For high-volume usage, consider implementing async API calls
    or using a queue-based approach.

    Args:
        texts: List of extracted texts from PDFs.
        doc_type: Document type.
        custom_fields: Custom fields for generic type.
        api_key: API key.
        api_base: API base URL.
        model: Model name.
        max_workers: Maximum parallel workers (note: serial execution for simplicity).

    Returns:
        List of field dictionaries.
    """
    results = []
    for text in texts:
        fields = extract_fields(
            text=text,
            doc_type=doc_type,
            custom_fields=custom_fields,
            api_key=api_key,
            api_base=api_base,
            model=model,
        )
        results.append(fields)
    return results
