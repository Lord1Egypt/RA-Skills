---
name: my-pubmed-skill
description: 简易PubMed搜索技能。使用web搜索和API调用检索PubMed文献。当用户要求"搜索PubMed文献"、"查找医学论文"、"医学文献检索"时使用。
---

# My PubMed Search Skill

一个简易的PubMed文献搜索技能，使用多种方法检索PubMed文献。

## 核心功能

### 1. Web搜索
- 使用OpenClaw的web_search/web_fetch工具搜索PubMed网站
- 适用于快速浏览和简单搜索

### 2. API调用
- 使用NCBI E-Utilities API进行结构化检索
- 支持批量获取文献详情
- 支持多种引用格式导出

### 3. 搜索参数
- **时间范围**: 近一年/近三年/近五年/自定义
- **文章类型**: Review/Clinical Trial/Meta-Analysis等
- **语言**: English/Chinese/Japanese
- **可用全文**: Free Full Text/Full Text/Abstract

### 4. 引用格式
- APA
- MLA
- IEEE
- GB/T 7714
- BibTeX

## 使用流程

### 第一步：明确需求
询问用户：
- 研究主题/关键词
- 时间范围（近一年/近三年/不限）
- 需要的结果数量
- 引用格式偏好

### 第二步：执行搜索
根据需求选择方法：
1. **简单搜索** - 使用web_fetch抓取PubMed搜索结果
2. **API搜索** - 运行PowerShell脚本调用PubMed API
   ```powershell
   powershell -File scripts/pubmed_search.ps1 "关键词" 10 apa
   ```

### 第三步：处理结果
提取以下信息：
- 论文标题
- 作者列表
- 发表年份
- PubMed ID (PMID)
- 摘要
- 期刊名称
- DOI

### 第四步：格式化输出
使用模板格式化结果：
- 表格格式 (`templates/results-table.md`)
- 引用格式 (`templates/citation-format.md`)
- 搜索选项 (`templates/search-options.md`)

## 脚本使用

### 基本搜索
```powershell
# 搜索PubMed文献
powershell -File scripts/pubmed_search.ps1 "machine learning" 10 apa
```

### 参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| 第1个 | 搜索关键词 | (必填) |
| 第2个 | 结果数量 | 5 |
| 第3个 | 引用格式 | apa |

### 引用格式
- `apa` - APA格式
- `mla` - MLA格式
- `ieee` - IEEE格式
- `gbt7714` - GB/T 7714格式

## 脚本文件

- `scripts/pubmed_search.ps1` - 主搜索脚本
- `scripts/test_pubmed_api.ps1` - API测试脚本

## 模板文件

- `templates/results-table.md` - 表格格式输出模板
- `templates/citation-format.md` - 引用格式模板
- `templates/search-options.md` - 搜索参数模板

## 参考资料

- `references/pubmed-api.md` - PubMed API使用指南

## 注意事项

1. PubMed API有访问限制（3次/秒，有API key时10次/秒）
2. 重要文献建议用户前往原文核实
3. 搜索结果仅供参考，需结合专业判断
4. 使用API key可提高速率限制
