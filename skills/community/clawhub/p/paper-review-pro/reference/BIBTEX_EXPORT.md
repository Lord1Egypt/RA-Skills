# BibTeX 导出模块

## 功能描述

检阅完成后自动生成 BibTeX 格式文件（`.bib`），方便一键导入 Zotero、Mendeley 等文献管理工具。

## 模块信息

- **模块文件**: `scripts/core/bibtex.py`
- **输出位置**: `~/.openclaw/paper-review-pro/papers/bibtex_{查询关键词}_{时间戳}.bib`

## 使用方式

BibTeX 导出**默认启用**，无需额外参数。

### 禁用 BibTeX 导出
```bash
python scripts/review.py --query "LLM reasoning" --no-bibtex
```

## BibTeX 条目格式

```bibtex
@inproceedings{Vaswani2017AttentionIsAll,
  title = {Attention Is All You Need},
  author = {Vaswani, Ashish and Shazeer, Noam},
  year = {2017},
  booktitle = {NeurIPS 2017},
  note = {CCF-A},
  abstract = {...},
  urldate = {2026-03-29},
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `title` | 论文标题 |
| `author` | 作者列表（英文姓氏在前） |
| `year` | 发表年份 |
| `booktitle` / `journal` | 发表 venue（会议/期刊名称） |
| `note` | CCF 评级注释 |
| `abstract` | 论文摘要（Zotero 可读） |
| `urldate` | 检索日期 |

## 导入 Zotero 步骤

1. 打开 Zotero
2. 文件 → 导入 → 从文件导入
3. 选择生成的 `.bib` 文件
4. 完成导入

## 测试命令

```bash
cd scripts
python core/bibtex.py --title "Test Paper" --authors "John Doe" --year 2025 --publication "CVPR" --ccf-rank A
```

## 注意事项

1. **作者格式**: BibTeX 作者格式假设英文姓名（姓氏在前）。对于中文姓名，可能需要手动调整。

2. **引用键生成**: 系统自动生成引用键（作者 + 年份 + 标题关键词），确保唯一性。

3. **文件命名**: 生成的 `.bib` 文件包含查询关键词和时间戳，便于区分不同检索批次。
