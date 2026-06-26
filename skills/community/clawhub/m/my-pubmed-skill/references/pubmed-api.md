# PubMed API使用指南

## 官方API

### 1. E-Utilities API
- **URL**: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- **无需API key**，但有速率限制（3次/秒）

### 2. PubMed API (需要API key)
- **URL**: https://www.ncbi.nlm.nih.gov/research/pubmed-api/
- **速率限制**: 10次/秒（有API key）

## 基本API调用

### 搜索文献
```bash
# 使用curl
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=CRISPR&retmax=10"
```

### 获取文献详情
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=12345678&rettype=abstract"
```

## 示例Python代码

```python
import requests
import json

def search_pubmed(query, limit=10):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": limit,
        "retmode": "json"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_pubmed_details(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return None
```

## 速率限制

- **无API key**: 3次/秒
- **有API key**: 10次/秒
- **建议**: 添加延迟，避免触发限制

## 获取API key

1. 注册NCBI账号：https://www.ncbi.nlm.nih.gov/
2. 进入Account Settings → API Key Management
3. 生成API key
4. 在代码中添加：
   ```python
   headers = {"api-key": "your_api_key"}
   ```

## 常见问题

### 1. 403错误
- 检查API key是否正确
- 检查速率限制

### 2. XML解析错误
- 使用XML解析库（如xml.etree.ElementTree）
- 或使用JSON格式（retmode=json）

### 3. 网络连接问题
- 添加超时设置
- 使用代理（如果需要）
