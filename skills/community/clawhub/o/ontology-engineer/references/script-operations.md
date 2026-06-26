# Script Operations

## scan_filesystem.py (Mode B/C)

**Input**: Directory path + optional config
**Output**: graph.jsonl (Document + Project entities)

```bash
python scripts/scan_filesystem.py --root <dir> [options]

Options:
  --config <yaml>        Custom namespace rules
  --extract-metadata     Extract author/title from .docx/.pdf
  --dry-run              Stats only, no write
  --output <path>        Custom output path
  --no-dedup             Disable duplicate detection
```

Features:
- Auto-infers namespaces from directory structure (or reads config YAML)
- Skips dependencies, caches, system files via universal patterns
- Lightweight dedup (same filename + same size)
- Optional .docx/.pdf metadata extraction (author/title/subject)
- Cross-platform (Python stdlib only for core; python-docx/PyMuPDF for metadata)

Config format (namespace_rules.yaml, optional):
```yaml
namespace_map:
  MyProjects: work
  Downloads: external/downloads
expand_children:
  - MyProjects
```

Without config: namespaces auto-inferred from project markers (README, package.json, .git).

## scan_directory.py (Mode A)

**Input**: Project root directory
**Output**: scan_result.json (file manifest with P1-P7 priority)

```bash
python scripts/scan_directory.py "<dir>" --output scan_result.json --report
```

Priority classification patterns:
- P1: 数据库设计, 表结构, DB Design, 数据模型, ER图
- P2: 数据字典, 字段定义, 系统清单, 代码表
- P3: 接口说明, API Spec, 报文, 消息格式
- P4-P7: Requirements, architecture, data flow, other

## convert_doc.py (Mode A)

**Input**: Directory or single .doc file
**Output**: .docx files in output directory

```bash
python scripts/convert_doc.py "<input>" --output-dir "<output>" --max-files 100 --scan-result scan_result.json
```

- Windows: COM automation (requires Word)
- Linux: `libreoffice --headless --convert-to docx`
- Sorts by priority if scan_result provided
- Skips already-converted files

## extract_tables.py (Mode A)

**Input**: File or directory + optional scan_result.json
**Output**: extracted_tables.json

```bash
python scripts/extract_tables.py "<input>" --output extracted_tables.json --scan-result scan_result.json
```

Handles .docx (python-docx), .xlsx (openpyxl), .xls (xlrd). Column role detection with longest-keyword-match. Size strategies: full (<5MB), selective (5-20MB), table_priority (20-50MB), sampling (>50MB).

## Word Table Column Role Keywords

```
field_name:    字段名, 字段, 列名, column, field, 英文名
field_name_cn: 中文名, 字段中文, 中文描述, 业务名称
field_type:    类型, 数据类型, type, data type
field_length:  长度, length, size, 精度
nullable:      是否为空, nullable, 是否必填
primary_key:   主键, pk, primary
foreign_key:   外键, fk, foreign, 关联
default_value: 默认值, default, 缺省值
description:   说明, 描述, 备注, comment, 含义, 业务含义
enum_values:   枚举值, 取值范围, 值域, 可选值
```

Table name extraction: Look in preceding paragraphs for `表名：xxx`, `表 1.2 — xxx`, `xxx表结构`, `Table: xxx`.
