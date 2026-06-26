# Literature Review API Reference

## 1. Semantic Scholar API

### Endpoint
```
GET https://api.semanticscholar.org/graph/v1/paper/search
```

### Parameters
| 参数 | 类型 | 说明 |
|------|------|------|
| query | string | 搜索主题 |
| limit | int | 返回数量 (默认10, 最大100) |
| offset | int | 分页偏移 |
| fields | string | 返回字段 (title,authors,year,venue,abstract,citationCount,externalIds) |

### Response (paper)
```json
{
  "paperId": "...",
  "title": "...",
  "authors": [{"name": "...", "authorId": "..."}],
  "year": 2024,
  "venue": "...",
  "abstract": "...",
  "citationCount": 100,
  "externalIds": {"DOI": "...", "PMID": "..."}
}
```

### Rate Limit
- 100 requests/5 seconds (无API key)
- 1000 requests/5 seconds (需要API key)

---

## 2. OpenAlex API

### Endpoint
```
GET https://api.openalex.org/works
```

### Parameters
| 参数 | 类型 | 说明 |
|------|------|------|
| search | string | 搜索主题 |
| per-page | int | 每页数量 (默认25, 最大200) |
| filter | string | 过滤条件 |
| sort | string | 排序方式 |

### Response (work)
```json
{
  "id": "https://openalex.org/W...",
  "title": "...",
  "authorships": [{"author": {"display_name": "..."}}],
  "publication_year": 2024,
  "primary_location": {"source": {"display_name": "..."}},
  "abstract": "...",
  "cited_by_count": 100,
  "doi": "https://doi.org/...",
  "pmid": "..."
}
```

### Rate Limit
- 100,000 requests/day (免费)

---

## 3. CrossRef API

### Endpoint
```
GET https://api.crossref.org/works
```

### Parameters
| 参数 | 类型 | 说明 |
|------|------|------|
| query | string | 搜索词 |
| rows | int | 返回数量 (默认20, 最大1000) |
| select | string | 选择字段 |

### Response
```json
{
  "message": {
    "items": [{
      "DOI": "10.xxxx/xxxxx",
      "title": ["..."],
      "author": [{"given": "...", "family": "..."}],
      "published-print": {"date-parts": [[2024]]},
      "container-title": ["..."],
      "type": "journal-article"
    }]
  }
}
```

### Rate Limit
- 50 requests/second

---

## 4. PubMed API (E-utilities)

### Endpoint
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi
```

### Parameters (esearch)
| 参数 | 类型 | 说明 |
|------|------|------|
| db | string | 数据库 (pubmed) |
| term | string | 搜索词 |
| retmax | int | 返回数量 |
| retmode | string | 返回模式 (json) |

### Parameters (esummary)
| 参数 | 类型 | 说明 |
|------|------|------|
| db | string | 数据库 |
| id | string | PubMed ID |
| retmode | string | 返回模式 (json) |

### Rate Limit
- 3 requests/second
- 10 requests/second (with API key)

---

## 5. DataCite API

### Endpoint
```
GET https://api.datacite.org/dois
```

### Parameters
| 参数 | 类型 |说明|
|------|------|------|
| query | string | DOI 查询 |
| rows | int | 返回数量 |

### Response
```json
{
  "data": [{
    "id": "https://doi.org/...",
    "attributes": {
      "titles": [{"title": "..."}],
      "authors": [{"given": "...", "family": "..."}],
      "published": "2024",
      "container-title": ["..."]
    }
  }]
}
```

### Rate Limit
- 30 requests/second

---

## 6. DOI Resolution

### Endpoint (CrossRef)
```
GET https://doi.org/{doi}
```

### Response Headers
- `Content-Type: application/vnd.citationstyles.csl+json`
- `HTTP 200` = 有效
- `HTTP 404` = 未找到
- `HTTP 410` = 已删除

### Validation 逻辑

1. **DOI 格式检查**
   ```python
   import re
   DOI_PATTERN = r'^10\.\d{4,}/[-._;()/:A-Z0-9]+$'
   bool(re.match(DOI_PATTERN, doi, re.IGNORECASE))
   ```

2. **HTTP HEAD 请求** (仅检查有效性，不下载内容)
   ```python
   import requests
   r = requests.head(f"https://doi.org/{doi}", allow_redirects=True, timeout=10)
   r.status_code == 200
   ```

3. **CrossRef API 验证**
   ```python
   r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=10)
   r.status_code == 200 and r.json()["message"]["DOI"]
   ```

---

## 7. 引用格式化格式

### CSL-JSON (通用中间格式)
```json
{
  "type": "article-journal",
  "DOI": "10.1234/example",
  "title": "...",
  "author": [
    {"given": "John", "family": "Doe"},
    {"given": "Jane", "family": "Smith"}
  ],
  "issued": {"date-parts": [[2024, 1, 15]]},
  "container-title": "Nature",
  "volume": "123",
  "issue": "456",
  "page": "789-795"
}
```

### 输出格式对比

| 格式 | 处理方式 |
|------|----------|
| APA 7th | citeproc-py: `apa.csl` |
| MLA 9th | citeproc-py: `mla.csl` |
| Chicago | citeproc-py: `chicago-author-date.csl` |
| IEEE | citeproc-py: `ieee.csl` |
| BibTeX | python: 自定义生成 |
| RIS | python: 自定义生成 |

### BibTeX 示例
```bibtex
@article{doe2024,
  author = {Doe, John and Smith, Jane},
  title = {Example Title},
  journal = {Nature},
  year = {2024},
  volume = {123},
  number = {456},
  pages = {789--795},
  doi = {10.1234/example}
}
```

---

## 8. 完整检索工作流

```
1. 用户输入(query) 
   ↓
2. 并发请求多个源
   - Semantic Scholar (语义检索)
   - OpenAlex (语义检索)
   - CrossRef (精确匹配)
   ↓
3. 合并结果 (按 DOI 去重)
   ↓
4. 验证 DOI 有效性
   - HEAD -> doi.org
   - CrossRef API
   ↓
5. 跨源差异检测
   - 同 DOI 比对 title/authors/year
   - 标记冲突项
   ↓
6. 返回结构化结果
   - papers: 合并去重后的文献列表
   - conflicts: 跨源冲突报告
   - errors: 无效 DOI 列表
```