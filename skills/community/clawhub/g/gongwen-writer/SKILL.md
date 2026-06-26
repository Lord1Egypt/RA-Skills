---
name: gongwen-writer
description: 政府公文格式文档生成器。支持所有常见文档格式输入（.md .txt .docx .pdf .html .rtf），输出符合国家标准的.docx公文格式。使用场景：产业调研报告、政策分析报告、工作报告等需要严格按照政府公文格式排版的文档。
---

# 公文写作技能

将多种格式文档转换为符合政府公文格式的.docx文档。

## 使用场景
- 产业调研报告
- 政策分析报告
- 工作汇报
- 培训材料

## 支持的输入格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| Markdown | `.md` | 原生支持，#为大标题，##为一级标题，###为二级标题 |
| 纯文本 | `.txt` | 按行解析，通过文本模式自动判断标题层级 |
| Word文档 | `.docx` | 通过段落样式和字号判断标题层级 |
| PDF文档 | `.pdf` | 使用pdfminer.six提取文本，按段落分割 |
| 网页 | `.html` `.htm` | 使用BeautifulSoup解析，h1→标题，h2→一级标题，h3→二级标题 |
| 富文本 | `.rtf` | 使用striprtf提取文本后按段落分割 |

## 使用方法

```bash
# Markdown → .docx
python3 SKILL_DIR/scripts/convert.py <input.md> <output.docx>

# 纯文本 → .docx
python3 SKILL_DIR/scripts/convert.py <input.txt> <output.docx>

# .docx → .docx（重新格式化）
python3 SKILL_DIR/scripts/convert.py <input.docx> <output.docx>

# PDF → .docx
python3 SKILL_DIR/scripts/convert.py <input.pdf> <output.docx>

# HTML → .docx
python3 SKILL_DIR/scripts/convert.py <input.html> <output.docx>

# RTF → .docx
python3 SKILL_DIR/scripts/convert.py <input.rtf> <output.docx>
```

`SKILL_DIR` 为本技能目录的绝对路径。

## 格式规范
详见 references/format-rules.md

## Markdown转换前预处理
Markdown文件需满足：
1. 使用 `##` 作为一级标题（对应一、二、三、）
2. 使用 `###` 作为二级标题（自动转换为（一）（二））
3. 无加粗标记（脚本会自动去除）
4. 无markdown链接标记（脚本会自动去除）
5. 首行以 `#` 开头的为报告大标题（居中显示）
6. **任何段落或标题的开头都不能出现"-"字符**（脚本会自动去除，但请尽量避免）

## 脚本功能
- 自动去除加粗标记 `**...**` 和 `__...__`
- 自动去除markdown链接 `[text](url)`
- 自动将二级标题序号转换为中文数字（（一）（二）...）
- 每个一级标题下的二级标题独立编号
- 段落自动首行缩进、两端对齐
- 英文数字自动使用Times New Roman字体
- 页码自动生成（奇数页右下、偶数页左下，格式 -数字-）
- 落款自动右对齐排版
