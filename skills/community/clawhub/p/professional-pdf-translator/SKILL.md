---
name: professional-pdf-translator
description: 通用长篇文献/小说多页PDF逐页自动提取、匹配用户提供的本地术语表并翻译追加至DOCX的自动化工作流。适用于任何具有特定受众、包含大量专有名词的长文献、小众长篇小说、学术论文、技术白皮书等PDF翻译场景。用户自行提供原文PDF、专业术语对照表及输出路径。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["python"],
            "python":
              {
                "packages": ["pymupdf", "python-docx"],
                "install": "python -m pip install pymupdf python-docx",
              },
          },
      },
  }
---

# PDF Batch Translator — 通用长篇文献逐页翻译工作流

> **致谢**：本 Skill 的 DOCX 写入模块参考了 [tiangong-wps-word-automation-cn](https://clawhub.com/skill/tiangong-wps-word-automation-cn) (作者: tiangong) 的 Windows COM 自动化思路。如果你还需要 Word/WPS 的批量自动化操作（合并、拆分、导出 PDF 等），推荐安装原 Skill：`clawhub install tiangong-wps-word-automation-cn`。

## 概述

本 Skill 提供一套标准化的长文献 PDF 逐页翻译自动化流水线，核心能力：

- **逐页提取**：从多页 PDF 中按页码逐一提取文本，智能处理双栏排版
- **术语匹配**：根据用户提供的专业术语对照表（支持多个文件），自动识别当前页出现的术语并向翻译模型提供参考
- **动态词库**：每页翻译完成后，自动提取新出现的专有名词（人名、地名、特有概念），追加至专属词表，确保跨页译名一致性
- **富文本写入**：将翻译结果以 Markdown 格式写入 DOCX，自动转换标题层级、粗体、斜体，并支持用户自定义高亮规则

## 适用场景

- 小众长篇小说（如特定圈层的同人/原创作品）
- 学术论文与技术白皮书
- 小众游戏/桌游规则书
- 行业协会标准文档
- 任何以 PDF 流通、包含大量专有术语的长篇文献

## 前置环境要求

- Python 环境需安装依赖：
  ```bash
  python -m pip install pymupdf python-docx
  ```

## 用户需要提供的内容

在启动工作流前，请向用户确认以下信息：

| 必需项 | 说明 |
|--------|------|
| **PDF 路径** | 待翻译的源 PDF 文件绝对路径 |
| **输出 DOCX 路径** | 翻译结果目标 DOCX 文件的绝对路径 |
| **翻译范围** | 起止页码（如第 5 页到第 120 页） |
| **术语对照表** | 一个或多个 `.md` 格式的术语表文件路径，格式为 `English Term: 中文译名`（每行一条） |

| 可选项 | 说明 |
|--------|------|
| **自定义高亮规则** | 一组正则表达式 + 颜色，用于在 DOCX 中对特定文本模式（如数字、公式、代码标识符）进行高亮染色 |
| **翻译风格指令** | 额外的自然语言指令，指导翻译模型的语气、措辞风格（如"学术严谨风格"、"保留口语化表达"、"武侠小说风格"等） |
| **动态专属词表路径** | 动态词表既会被 `append_terms.py` 持续追加新术语，也会作为 `extract_page.py` 的 `--terms` 参数之一参与每页术语匹配，确保跨页译名一致性。默认创建在 PDF 同目录下，文件名为 `{PDF文件名}_专属词表.md` |

### 术语对照表格式要求

术语表应为 Markdown 文件（UTF-8 编码），每行一条术语：

```markdown
# 可选注释行以 # 开头
Ability Score: 属性值
Armor Class: 护甲级
Dexterity Saving Throw: 敏捷豁免
Fireball: 火球术
```

- 以 `#` 开头的行视为注释，不会被匹配
- 匹配逻辑：脚本会提取术语行中的英文单词片段（长度 > 3），若该片段出现在当前页文本中，则整条术语被标记为"匹配"
- 支持多个术语表文件同时使用——适合将"基础通用术语"和"特定章节术语"分开管理

## 执行流程

当用户提供了上述必需信息后，在一个循环中逐页执行以下步骤：

### 步骤 1：提取单页文本与匹配术语

使用本 Skill 内置的 `extract_page.py`：

```bash
python "{baseDir}/scripts/extract_page.py" --pdf "/path/to/document.pdf" --page {page_num} --terms "/path/to/glossary.md" "/path/to/glossary2.md" "{dynamic_glossary_path}"
```

> **注意**：`--terms` 的最后一个参数 `{dynamic_glossary_path}` 是动态专属词表路径。第 1 页时该文件可能不存在（脚本会自动跳过），从第 2 页起，前一页翻译时新提取的专有名词已经在其中，会被一并匹配，确保跨页译名一致性。

脚本输出 JSON：
- `is_empty` (布尔值)：是否为空白页或纯图片页
- `text` (字符串)：提取出的本页原文文本
- `matched_terms` (列表)：本页匹配到的术语条目（来自用户指定的术语表 + 动态词表）

### 步骤 2：执行大模型翻译

- **纯图片页** (`is_empty: true`)：跳过翻译，直接写入 `【第 {page_num} 页】：纯图片页`
- **有文本**：将原文 `text`、匹配术语 `matched_terms`、当前专属词表、以及用户提供的翻译风格指令一并提交给模型翻译

**强制输出格式要求**：
- 仅输出纯中文译文（不附带英文原文）
- 使用 Markdown 标题（`#`、`##`、`###` 等）还原原文层级结构
- 使用 `**粗体**` 和 `*斜体*` 还原原文强调
- 列表项使用 `- ` 或 `1. ` 还原

**动态词库提取**：翻译完成后，要求模型识别本页新出现的专有名词（人名、地名、独特概念、特殊物品等），并使用以下脚本追加：

```bash
python "{baseDir}/scripts/append_terms.py" --file "{dynamic_glossary_path}" --terms "English Name: 中文名" "Another Term: 另一个译名"
```

这确保新词以 UTF-8 编码追加，供下一页翻译时作为上下文参考。注意 `{dynamic_glossary_path}` 与步骤 1 的 `--terms` 最后一个参数相同，因此新追加的术语会在下一页提取时自动被匹配。

### 步骤 3：富文本写入 DOCX

1. 使用 `write` 工具将翻译好的 Markdown 文本存入临时文件（如 `{workdir}/temp_translate.txt`）
2. 执行写入命令：

```bash
python "{baseDir}/scripts/append_docx.py" --docx "/path/to/output.docx" --textfile "{workdir}/temp_translate.txt" --page {page_num}
```

若用户提供了自定义高亮规则，添加 `--highlights` 参数：

```bash
python "{baseDir}/scripts/append_docx.py" --docx "..." --textfile "..." --page {page_num} --highlights "regex1:#RRGGBB" "regex2:#RRGGBB"
```

### 步骤 4：推进下一页

`page_num + 1`，回到步骤 1 重复执行（`--terms` 参数不变，动态词表路径始终包含其中）。随着翻译推进，动态词表会越来越丰富，跨页译名一致性也随之增强。循环直至完成所有页面。完成后向用户报告总页数、跳过的纯图片页数、以及专属词表的最终路径。

## 自定义高亮规则

`append_docx.py` 支持通过 `--highlights` 参数传入自定义高亮规则。每条规则格式为 `正则表达式:颜色HEX`：

```bash
--highlights "DC\s*\d+:#8B0000" "[0-9]+d[0-9]+:#006400"
```

- 正则表达式需符合 Python `re` 语法
- 颜色为 6 位十六进制 RGB（不含 `#` 前缀的格式也可，脚本会自动处理）
- 匹配到的文本将在 DOCX 中被加粗并以指定颜色渲染

不指定 `--highlights` 时，脚本仅处理 Markdown 标准格式（标题、粗体、斜体），不做额外染色。

## 脚本说明

### extract_page.py — 单页文本提取

- 输入：PDF 路径、页码（从 1 开始）、术语表路径列表
- 智能处理双栏排版：检测页面中轴线，分别按垂直位置排序左右栏文本
- 横跨页面宽度 > 65% 的文本块识别为标题/跨栏段落
- 输出：JSON 格式的提取结果与匹配术语

### append_docx.py — Markdown 转 DOCX 追加写入

- 输入：目标 DOCX 路径、包含 Markdown 译文的临时 TXT 文件、页码
- 自动解析 `#` 标题、`**粗体**`、`*斜体*`
- 可选自定义高亮规则
- 每页以灰色斜体分隔线标注原文页码

### append_terms.py — 动态词表追加

- 输入：词表文件路径、要追加的术语列表
- 以 UTF-8 编码追加，避免 GBK 乱码
- 自动创建不存在的目录
