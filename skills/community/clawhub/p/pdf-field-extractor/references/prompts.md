# AI Field Extraction Prompt Templates

## System Prompts by Document Type

### Invoice (发票)
```
You are an expert at extracting structured information from invoices.
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

If a field is not found, use null. Do not add any explanation.
```

### Contract (合同)
```
You are an expert at extracting structured information from contracts.
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

If a field is not found, use null. Do not add any explanation.
```

### Generic (Custom Fields)
```
You are an expert at extracting structured information from documents.
Extract the key fields from the document text based on the user's request.

Return ONLY valid JSON with the extracted fields.
If a field is not found, use null. Do not add any explanation.

Document text:
{text}
```

## API Configuration

### Recommended Models
- **GPT-4o**: Best quality, higher cost
- **GPT-4o-mini**: Good quality, lower cost
- **DeepSeek-V3**: Cost-effective, good for structured extraction
- **MiniMax**: Good performance, competitive pricing

### Temperature
- Recommended: 0.1 (low temperature for consistent extraction)
- Range: 0.0 - 0.3

### Max Tokens
- Recommended: 2048
- For complex documents with many fields: 4096

### API Base URLs
- OpenAI: `https://api.openai.com/v1`
- Azure OpenAI: `https://{resource}.openai.azure.com/openai/deployments/{deployment}/chat/completions`
- Custom (DeepSeek, etc.): Configurable

## Error Handling

### Common Errors
1. **API Key missing**: Raise ValueError with instructions
2. **API Timeout**: Raise TimeoutError after configurable seconds
3. **API Error**: Raise RuntimeError with response details
4. **Invalid JSON Response**: Attempt parsing from markdown block, fallback to empty dict
