# Knowledge Base Format Specification

This document defines the exact format requirements for knowledge base JSON files.

## File Structure

```json
{
  "<filename>": {
    "filename": "<filename>",
    "type": "<filetype>",
    "content": <content>,
    "length": <number>
  },
  ...
}
```

### Required Fields

- `filename`: Original filename (string)
- `type`: File type, one of: `xlsx`, `docx`, `doc` (string)
- `content`: File content (type depends on file type)
- `length`: Content length in bytes (number, optional)

## File Type: xlsx

### Content Format

Text-based representation of Excel with `A1[Value] | B2[Value]` pattern.

### Example

```json
{
  "company_data.xlsx": {
    "filename": "company_data.xlsx",
    "type": "xlsx",
    "content": "=== Sheet: 基本信息\nA1[公司名称] | A2[国寿安保基金管理有限公司]\nA1[法人代表] | A2[邓学芬]\nA1[联系电话] | A2[021-68400800]\nA1[统一社会信用代码] | A2[91310000MA1FK8R90J]\n\n=== Sheet: 财务数据\nA1[年份] | B1[总资产] | C1[净资产]\nA2[2022] | B2[500.23] | C2[300.15]\nA3[2023] | B3[600.45] | C3[350.20]\nA4[2024] | B4[720.80] | C4[420.30]",
    "length": 12345
  }
}
```

### Format Rules

1. **Sheet Declaration**: Start with `=== Sheet: <SheetName> ===`
2. **Cell Format**: `<CellRef>[<Value>]`
3. **Row Separator**: Use ` | ` to separate cells
4. **Value Encoding**: UTF-8 encoded strings
5. **Numeric Values**: Keep as strings (e.g., `"500.23"`)
6. **Empty Cells**: Use empty string or omit cell reference

### Cell Reference Format

- Column: Single letter (A-Z, AA-AZ, etc.)
- Row: Number (1, 2, 3, ...)
- Example: `A1`, `B2`, `AA10`

### Multiple Sheets

Separate with blank line:

```
=== Sheet: Sheet1 ===
A1[Header1] | A2[Value1]

=== Sheet: Sheet2 ===
A1[Header2] | A2[Value2]
```

## File Type: docx

### Content Format

Dictionary containing paragraphs and/or table data.

### Option 1: Paragraphs Array

```json
{
  "document.docx": {
    "filename": "document.docx",
    "type": "docx",
    "content": {
      "paragraphs": [
        "国寿安保基金管理有限公司成立于2013年",
        "法定代表人：邓学芬",
        "注册地址：上海市浦东新区世纪大道1600号"
      ],
      "tables": [
        {
          "headers": ["字段", "值"],
          "rows": [
            ["公司名称", "国寿安保基金管理有限公司"],
            ["注册资本", "12.88亿元"]
          ]
        }
      ]
    },
    "length": 5678
  }
}
```

### Option 2: Field Dictionary

```json
{
  "company_info.docx": {
    "filename": "company_info.docx",
    "type": "docx",
    "content": {
      "公司名称": "国寿安保基金管理有限公司",
      "法定代表人": "邓学芬",
      "联系电话": "021-68400800",
      "传真": "021-68400801",
      "地址": "上海市浦东新区世纪大道1600号陆家嘴世纪金融广场2号楼33层",
      "统一社会信用代码": "91310000MA1FK8R90J",
      "成立时间": "2013年10月",
      "注册资本": "12.88亿元",
      "邮编": "200120"
    },
    "length": 4321
  }
}
```

### Field Extraction Patterns

The system automatically extracts common fields from text:

| Field | Regex Pattern | Example |
|--------|--------------|---------|
| 法人代表 | `法人代表[：:\s]*([^\n\r]{2,10})` | 法人代表：邓学芬 |
| 法定代表人 | `法定代表人[：:\s]*([^\n\r]{2,10})` | 法定代表人：邓学芬 |
| 联系电话 | `(?:联系|业务)电话[：:\s]*([\d\s-]{7,20})` | 联系电话：021-68400800 |
| 传真 | `传真[：:\s]*([\d\s-]{7,20})` | 传真：021-68400801 |
| 地址 | `地址[：:\s]*([^\n\r]{10,100})` | 地址：上海市浦东新区世纪大道1600号... |
| 注册资本 | `注册资本[：:\s]*([\d.]+)` | 注册资本：12.88 |
| 统一社会信用代码 | `统一社会信用代码[：:\s]*([A-Z0-9]{18})` | 统一社会信用代码：91310000MA1FK8R90J |
| 成立时间 | `成立(?:时间|日期)?[：:\s]*(\d{4}年\d{1,2}月)` | 成立时间：2013年10月 |
| 邮编 | `邮编[：:\s]*(\d{6})` | 邮编：200120 |

## File Type: doc

### Content Format

Plain text string.

### Example

```json
{
  "document.doc": {
    "filename": "document.doc",
    "type": "doc",
    "content": "国寿安保基金管理有限公司\n法定代表人：邓学芬\n联系电话：021-68400800\n地址：上海市浦东新区世纪大道1600号",
    "length": 2345
  }
}
```

### Text Processing

- Use UTF-8 encoding
- Preserve line breaks with `\n`
- Extract fields using regex patterns (see docx section)

## Best Practices

### 1. Field Naming

Use consistent, descriptive field names:

✅ **Good**:
- `法定代表人`
- `联系电话`
- `2024年总资产`
- `注册资本（万元）`

❌ **Avoid**:
- `field1`
- `data1`
- `value`
- `info`

### 2. Value Formatting

- **Numbers**: Keep as strings in JSON
- **Currency**: Include unit (e.g., `"12.88亿元"`, `"500.23万元"`)
- **Dates**: Use consistent format (e.g., `"2024年12月31日"`)
- **Percentages**: Include `%` symbol (e.g., `"15.5%"`)

### 3. Encoding

- Always use UTF-8 encoding
- Validate JSON before use: `python -m json.tool knowledge.json`

### 4. Organization

Group related fields logically:

```json
{
  "basic_info.xlsx": {
    "content": "=== Sheet: 基本信息\nA1[公司名称] | ...\n=== Sheet: 联系信息\nA1[联系电话] | ..."
  }
}
```

### 5. Year-based Data

Include year in field name for automatic matching:

✅ **Good**:
- `2024年总资产`
- `2025年净资产`
- `2023年债券基金规模`

❌ **Avoid**:
- `总资产（2024）`
- `净资产2025`
- `债券基金2023`

## Validation

### Python Validation Script

```python
import json

def validate_kb(kb_path):
    """Validate knowledge base JSON"""
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    errors = []
    
    for filename, data in kb.items():
        # Check required fields
        if 'filename' not in data:
            errors.append(f"{filename}: Missing 'filename'")
        
        if 'type' not in data:
            errors.append(f"{filename}: Missing 'type'")
        
        if 'content' not in data:
            errors.append(f"{filename}: Missing 'content'")
        
        file_type = data.get('type')
        content = data.get('content')
        
        # Validate type-specific format
        if file_type == 'xlsx':
            if not isinstance(content, str):
                errors.append(f"{filename}: xlsx content must be string")
            elif '=== Sheet:' not in content:
                errors.append(f"{filename}: xlsx missing sheet declaration")
        
        elif file_type == 'docx':
            if not isinstance(content, (dict, list)):
                errors.append(f"{filename}: docx content must be dict or list")
        
        elif file_type == 'doc':
            if not isinstance(content, str):
                errors.append(f"{filename}: doc content must be string")
    
    if errors:
        print(f"Found {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ Knowledge base is valid")
        return True

# Usage
validate_kb('knowledge.json')
```

## Example Complete Knowledge Base

```json
{
  "company_basic.xlsx": {
    "filename": "company_basic.xlsx",
    "type": "xlsx",
    "content": "=== Sheet: 基本信息\nA1[公司名称] | A2[国寿安保基金管理有限公司]\nA1[英文名称] | A2[China Life Asset Management Co., Ltd.]\nA1[成立时间] | A2[2013年10月]\nA1[注册资本] | A2[12.88亿元]\nA1[统一社会信用代码] | A2[91310000MA1FK8R90J]",
    "length": 3456
  },
  "company_contact.docx": {
    "filename": "company_contact.docx",
    "type": "docx",
    "content": {
      "法定代表人": "邓学芬",
      "联系电话": "021-68400800",
      "传真": "021-68400801",
      "地址": "上海市浦东新区世纪大道1600号陆家嘴世纪金融广场2号楼33层",
      "邮编": "200120",
      "网站": "www.gsfunds.com"
    },
    "length": 2345
  },
  "financial_data.xlsx": {
    "filename": "financial_data.xlsx",
    "type": "xlsx",
    "content": "=== Sheet: 历年数据\nA1[年份] | B1[总资产] | C1[净资产] | D1[营业收入]\nA2[2022年] | B2[933916042.31] | C2[831322844.2] | D2[957000000]\nA3[2023年] | B3[1172981616.25] | C3[1054030889.87] | D3[1005000000]\nA4[2024年] | B4[1982150027.71] | C4[1856780901.15] | D4[1152000000]",
    "length": 5678
  }
}
```

## Troubleshooting

### Issue: JSON Parse Error

**Error**: `json.decoder.JSONDecodeError`

**Solution**: 
- Ensure file is UTF-8 encoded
- Check for trailing commas
- Validate with online JSON validator

### Issue: No Fields Extracted

**Cause**: Field names don't match regex patterns

**Solution**:
- Use standard field names (see Field Extraction Patterns section)
- Check pattern matching with test script
- Consider adding custom patterns

### Issue: Encoding Issues

**Error**: `UnicodeDecodeError` or `UnicodeEncodeError`

**Solution**:
- Save JSON with UTF-8 encoding
- Use `encoding='utf-8'` when reading/writing
- Avoid BOM (Byte Order Mark) at file start
