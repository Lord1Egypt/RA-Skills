# 数据收集指南

## UniProt REST API

### 搜索语法

```
基础搜索:
  https://rest.uniprot.org/uniprotkb/search?query={查询}&format=json&size={数量}

常用查询字段:
  文本搜索: "protein name"          # 自由文本
  基因名: gene:NAME                # 基因名称
  物种: organism_id:TAXON_ID       # NCBI 分类ID
  长度: length:[MIN TO MAX]        # 序列长度范围
  已审: reviewed:true              # Swiss-Prot only
```

### 示例查询

```python
import requests

def search_uniprot(query, size=500):
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {"query": query, "format": "json", "size": size}
    resp = requests.get(url, params=params, timeout=120)
    return resp.json().get("results", [])

# 搜索 imine reductase
results = search_uniprot('"imine reductase"', size=500)

# 提取信息
for r in results:
    acc = r["primaryAccession"]
    org = r.get("organism", {}).get("scientificName", "?")
    seq = r.get("sequence", {}).get("value", "")
    print(f"{acc} | {org} | {len(seq)}aa")
```

### 下载 FASTA

```python
def fetch_fasta(accession):
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"
    return requests.get(url, timeout=30).text
```

### 质量过滤

| 条件 | 推荐值 |
|------|--------|
| 序列长度 | 150-600 aa（酶典型范围） |
| 来源 | reviewed=true 优先 |
| 去重 | 按 accession 去重 |
| 物种覆盖 | 选代表性物种（非冗余） |

### 输出格式

```json
[
  {
    "accession": "A1B8Z0",
    "entry_name": "A1B8Z0_PARDE",
    "organism": "Paracoccus denitrificans",
    "protein_name": "Imine reductase",
    "sequence": "MVLSPADKTN...",
    "length": 320
  }
]
```

```fasta
>A1B8Z0|Paracoccus denitrificans|Imine reductase
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH
...
```
