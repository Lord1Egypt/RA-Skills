---
name: pdf-contract-redactor
description: PDF contract redaction tool. Use when the user needs to redact sensitive information from scanned PDF contracts. The tool performs OCR to extract text, identifies field names and their corresponding values, and redacts only the values while keeping field names visible. Supports Alibaba Cloud OCR API for accurate Chinese text recognition.
---

# PDF Contract Redactor

Redact sensitive values from scanned PDF contracts while preserving field names.

## What It Does

1. **OCR Recognition**: Uses Alibaba Cloud OCR to extract text and positions from scanned PDFs
2. **Field-Value Matching**: Finds field names (e.g., "合同金额") and their corresponding values (e.g., "45640元")
3. **Selective Redaction**: Covers only the values with black boxes, keeping field names readable

## Workflow

### Step 1: PDF to Images
Convert PDF pages to high-resolution PNG images (200 DPI) for OCR.

### Step 2: OCR with Alibaba Cloud
Call Alibaba Cloud OCR API to get:
- All text blocks
- Bounding box coordinates for each text block
- Confidence scores

### Step 3: Match Fields to Values
For each field in the field list:
1. Find the field name text block
2. Look for the corresponding value in:
   - **Right side**: Same row, to the right of field name
   - **Below**: Next row, aligned with field name
3. Record field-value pair with both bounding boxes

### Step 4: Generate Redacted PDF
For each matched value:
1. Convert image coordinates to PDF coordinates
2. Draw black rectangle over the value area
3. Keep field name area unchanged

## Field List

The following fields are searched and their values are redacted:

- 法务部归档编号, 归档时间, 申请人工号, 申请人姓名, 申请人部门
- 申请人部门负责人, 所涉项目名称（如有）, 所涉项目编号（如有）
- 对方编号（如有）, 合同编号, 合同名称, 合同甲方名称, 合同乙方名称
- 合同相对方, 相对方所属行业, 相对方是否为世界500强
- 相对方是央企/国企, 相对方是否为涉密单位, 业务类别, 合同类别
- 合同类型, 合同状态, 扫描件状态, 对方是否签章, 我方是否签章
- 销售、采购标的（非一起译填）, 语种, 单价, 合同金额（元）, 币种
- 支付/收款方式, 付款/收款条件, 合同结算周期, 是否使用公司模板
- 用章主体, 印章类型, 签订时间, 合同开始时间, 合同到期时间
- 收支类型, 我方联系人姓名, 我方联系人电话, 对方联系人姓名
- 对方联系人电话, 对方邮寄地址, 归档状态, 开票名称, 开票账号
- 开票银行, 收款名称, 收款账号, 收款银行, 验收时间, 验收标准
- 合同是否自动续期, 合同续期时间, 合同特殊约定
- 协议内是否有结算单, 结算单（如有）内容是否填写

## Usage

### Prerequisites

1. Alibaba Cloud account with OCR service enabled
2. AccessKey ID and AccessKey Secret

### Running the Tool

```bash
python scripts/redact_contract.py <input.pdf> <access_key_id> <access_key_secret> [output.pdf]
```

Example:
```bash
python scripts/redact_contract.py contract.pdf LTAIxxx xxx contract_redacted.pdf
```

### Output

- `<name>_redacted.pdf`: Redacted PDF with values covered
- `<name>_fields.json`: JSON file listing all matched field-value pairs

## Implementation Notes

### OCR API

Uses Alibaba Cloud "通用文字识别-高精度版" (RecognizeAdvanced API):
- Endpoint: `https://ocr.aliyuncs.com`
- Returns text content and quadrilateral coordinates
- Supports automatic rotation detection

### Field-Value Matching Logic

```python
# For a field at (fx0, fy0, fx1, fy1)
# Look for values that are:
# 1. To the right: vx0 > fx1 and |vy0 - fy0| < field_height * 2
# 2. Below: vy0 > fy1 and vx0 >= fx0 - field_width * 0.3
# Choose the closest match
```

### Coordinate Transformation

OCR returns coordinates in image space (200 DPI).
Convert to PDF space (72 DPI) using scale factor: `scale = 72 / 200 = 0.36`

## Dependencies

```bash
pip install pymupdf pillow requests
```

## Error Handling

- If OCR API fails, retry with exponential backoff
- If field not found, skip silently (don't fail entire document)
- If value not found for a field, log warning and continue
