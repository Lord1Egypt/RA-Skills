

---

skill_name: MyStrDecoder
version: 1.0.0
description: 一个智能的字符串解码工具，专门用于处理包含多层嵌套结构的 JSON 日志文件。它能够自动识别并解码各种编码格式的字符串，将混乱的编码数据还原为可读的文本内容。
author: Your Name
created: 2026-07-02
tags: [json, decoder,log, automation]

---

# 功能描述

## 递归遍历

- 支持任意深度的 JSON 嵌套结构（对象、数组、嵌套对象）

- 深度优先遍历所有节点，不遗漏任何字段

- 保留原始 JSON 结构，仅对字符串值进行处理

## 智能编码识别

自动检测并解码以下常见编码类型：

| 编码类型                 | 示例                          |
| -------------------- | --------------------------- |
| **Unicode 转义**       | `\u4e2d\u6587` → `中文`       |
| **URL 编码**           | `%E4%B8%AD%E6%96%87` → `中文` |
| **Base64**           | `5Lit5paH` → `中文`           |
| **HTML 实体**          | `&#20013;&#25991;` → `中文`   |
| **Hex 编码**           | `e4b8ade69687` → `中文`       |
| **Quoted-Printable** | `=E4=B8=AD=E6=96=87` → `中文` |
| **混合编码**             | 自动识别并递归解码多层编码               |

# 使用前提

1. **Python 环境**：Python 3.6 或更高版本

2. **依赖库**：仅需 Python 标准库（json、sys、os、argparse、typing），无需额外安装

3. **输入文件**：准备好符合 JSON 格式的日志文件 `test_cases.json`

4. **输出目录**：确保输出目录有写入权限

# 

# 使用示例（不等待子进程）

python ./scripts/strDecoder.py -i test_cases.json -o result.json
