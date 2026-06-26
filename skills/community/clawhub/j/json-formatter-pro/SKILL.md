---
name: json-formatter-pro
description: Format and validate JSON files with pretty-printing, indentation control, key sorting, and validation modes supporting stdin, stdout, and file I/O.
version: v1.0.0
tags: json-formatter, json-validation, developer-tools
---

# json-formatter-pro

## Usage Scenarios

### Scenario 1: Format a JSON File with Proper Indentation
**User input:** "Format this JSON file with 4-space indentation"
**Expected output:** The tool reads `input.json`, applies 4-space indentation, and outputs the formatted JSON to stdout or a specified output file.

### Scenario 2: Validate JSON Syntax
**User input:** "Check if my config.json has valid JSON syntax"
**Expected output:** The tool validates the file and returns "Valid JSON" or an error message with the line number of the syntax issue.

### Scenario 3: Format and Sort Keys Alphabetically
**User input:** "I want this JSON formatted with sorted keys"
**Expected output:** The tool reads the JSON file, formats it with default 2-space indentation, sorts all keys alphabetically, and outputs the result.
### Scenario 4: API返回的数据太乱了要格式化
**User input:** "后端给了一个API返回的JSON数据，字符串一长串看了头晕，帮我格式化成可读的格式，顺便检查一下语法对不对。"
**Expected output:** 接收原始JSON字符串：1）进行语法验证并指出错误位置（如多余的逗号、未闭合的引号、不合法的数值）；2）输出格式化后的JSON（缩进2空格/4空格可选）；3）如果支持，还可提供JSON路径查询、键值对统计和一键复制功能。支持嵌套最大深度检测，避免循环引用导致的卡顿。

## Description

A utility skill for formatting JSON files with proper indentation and validating JSON syntax. Supports reading from files or stdin, outputting to files or stdout.

## Usage

```bash
# Format a JSON file (pretty-print to stdout)
python ~/.openclaw/skills/json-formatter-pro/json_formatter.py format input.json

# Format and save to a new file
python ~/.openclaw/skills/json-formatter-pro/json_formatter.py format input.json -o output.json

# Validate JSON syntax without formatting
python ~/.openclaw/skills/json-formatter-pro/json_formatter.py validate input.json

# Read from stdin, format and output to stdout
cat input.json | python ~/.openclaw/skills/json-formatter-pro/json_formatter.py format -

# Validate JSON from stdin
cat input.json | python ~/.openclaw/skills/json-formatter-pro/json_formatter.py validate -
```

## Options

- `format`: Pretty-print JSON with proper indentation
- `validate`: Check if JSON is valid without formatting output
- `-o, --output`: Specify output file (default: stdout)
- `-i, --indent`: Number of spaces for indentation (default: 2)
- `--sort-keys`: Sort JSON keys alphabetically

## Examples

```bash
# Format with 4-space indentation
python ~/.openclaw/skills/json-formatter-pro/json_formatter.py format data.json -i 4

# Format and sort keys
python ~/.openclaw/skills/json-formatter-pro/json_formatter.py format data.json --sort-keys

# Validate a JSON file
python ~/.openclaw/skills/json-formatter-pro/json_formatter.py validate config.json
# Output: Valid JSON or error message with line number
```

## Exit Codes

- `0`: Success
- `1`: Invalid JSON syntax
- `2`: File not found or permission error
- `3`: Other error
