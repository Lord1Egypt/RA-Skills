---
name: literature-search-workflow
description: Standardized literature search workflow integrating tavily-search, pubmed-database, bgpt-paper-search, openalex-database and other academic search skills. Provides complete literature search process from query analysis to literature acquisition.
license: MIT License
metadata:
    skill-author: academic-assistant
    version: 1.0.0
    created: 2026-03-14
---

# Literature Search Workflow

## Overview

标准化文献搜索工作流，整合多个学术搜索技能，提供 6 阶段完整文献搜索流程。

## Workflow Stages

1. **查询分析** (1-2 分钟): 意图识别、关键词提取
2. **初步搜索** (3-5 分钟): tavily-search
3. **深度搜索** (5-10 分钟): PubMed/BGPT/OpenAlex
4. **结果整理** (3-5 分钟): 去重、排序、评估
5. **文献获取** (5-10 分钟): web_fetch 获取全文
6. **输出报告** (2-3 分钟): Markdown/BibTeX

## Usage

```bash
# 学术论文搜索
python literature_search.py "主观幸福感量表 validation" --type academic_paper

# 量表工具搜索
python literature_search.py "SHS scale Chinese validation" --type scale_search

# 综述文献搜索
python literature_search.py "AI psychology review" --type review --max-results 50

# 研究方法搜索
python literature_search.py "experimental design psychology" --type methodology
```

## Search Engines

- **Primary**: tavily-search
- **Fallback**: pubmed-database, bgpt-paper-search, openalex-database
- **Specialized**: research-lookup (方法学)

## Scenarios

| 场景 | 引擎 | 输出 |
|------|------|------|
| academic_paper | tavily-search, pubmed-database, bgpt-paper-search | 论文列表 + 引用 |
| scale_search | tavily-search, pubmed-database | 量表验证报告 |
| review | tavily-search, bgpt-paper-search | 综述文献列表 (50 篇) |
| methodology | research-lookup, tavily-search | 方法学资源列表 |

## Output Format

Markdown report with:
- 搜索摘要
- 关键文献（含 DOI）
- 来源引用
- 全文链接
- BibTeX 引用

## Dependencies

**Required Skills**:
- tavily-search
- web_fetch
- citation-management

**Optional Skills**:
- pubmed-database
- bgpt-paper-search
- openalex-database
- research-lookup

## API Requirements

- **Tavily API**: Required (1000 searches/month free)
- **PubMed API**: Free
- **OpenAlex API**: Free
- **BGPT MCP**: Free 50 searches

## Example Output

```markdown
# 文献搜索结果报告

**查询**: 主观幸福感量表 validation psychometric 2025
**搜索时间**: 2026-03-14 12:38
**数据库**: Tavily, PubMed, BGPT
**结果数量**: 10 篇

## 🔍 关键文献

### 1. Psychometric Evaluation of the Chinese Version of the SHS

**作者**: Cheung F, Lucas RE

**期刊**: Quality of Life Research

**年份**: 2014

**DOI**: 10.1007/s11136-014-0721-1

**样本量**: N = 2,635

**信度**: α = 0.82

**链接**: https://pmc.ncbi.nlm.nih.gov/articles/PMC4107280/

## 📊 文献统计

| 年份 | 数量 | 百分比 |
|------|------|--------|
| 2025 | 3 | 30% |
| 2024 | 2 | 20% |
| 2020-2023 | 3 | 30% |

## 🔗 相关链接

- [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/)
- [ResearchGate](https://www.researchgate.net/)
```

## Quality Assessment

| 指标 | 优秀 | 良好 | 需改进 |
|------|------|------|--------|
| **相关性** | >0.8 | 0.5-0.8 | <0.5 |
| **时效性** | <1 年 | 1-3 年 | >3 年 |
| **权威性** | SCI/SSCI | 核心 | 普通 |
| **完整性** | 全文可获取 | 摘要 | 仅标题 |

## Best Practices

1. **明确查询**: 使用具体关键词，包含时间范围
2. **多轮搜索**: 从广泛到精确，多数据库验证
3. **记录来源**: 保存 DOI，记录访问时间
4. **质量评估**: 检查研究设计、样本量、期刊质量

## References

- Workflow documentation: `workspace/guides/文献搜索工作流_v1.0.md`
- Test report: `reports/文献搜索技能测试报告_20260314.md`
