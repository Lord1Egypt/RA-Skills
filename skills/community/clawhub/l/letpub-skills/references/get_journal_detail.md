---
description: 获取期刊详情 - 解析LetPub期刊详情页，提取期刊基本信息、影响因子、分区、审稿速度等
---

# 获取期刊详情

## 功能说明
解析 LetPub 期刊详情页 HTML，提取完整的期刊信息。

## 使用方法

```python
import requests
from letpub_skills import parse_journal_detail, search_journal

# 第1步：通过期刊名称搜索获取 journal_id
results = search_journal("CHEMICAL ENGINEERING SCIENCE")
journal_id = results[0]['id']  # 例如: "1642"

# 第2步：使用 journal_id 获取详情页并解析
url = f"https://letpub.com.cn/index.php?journalid={journal_id}&page=journalapp&view=detail"
response = requests.get(url)
journal = parse_journal_detail(response.text)
```

## 返回字段

| 字段 | 说明 |
|------|------|
| name | 期刊名称 |
| shortname | 期刊简称 |
| letpub_score | LetPub综合评分 |
| score_people | 评分人数 |
| reputation_score | 声誉评分 |
| influence_score | 影响力评分 |
| speed_score | 速度评分 |
| issn | ISSN |
| impact_factor | 最新影响因子 |
| real_time_if | 实时影响因子 |
| self_cite_rate | 自引率 |
| five_year_if | 五年影响因子 |
| jci | JCI期刊引文指标 |
| h_index | h-index |
| cite_score | CiteScore |
| intro | 期刊简介 |
| website | 期刊官网 |
| submission_url | 投稿网址 |
| language_require | 语言要求 |
| open_access | 是否OA开放访问 |
| communication | 通讯地址 |
| publisher | 出版商 |
| field | 涉及的研究方向 |
| country | 出版国家或地区 |
| language | 出版语言 |
| period | 出版周期 |
| start_year | 创刊年份 |
| year_paper | 年文章数 |
| gold_oa | Gold OA文章占比 |
| research_ratio | 研究论文占比 |
| sci_part | WOS期刊SCI分区 |
| warning | 期刊分区表预警名单 |
| ch_sci_2026 | 新锐期刊分区表(2026年3月) |
| ch_sci_2025 | 中科院分区(2025年3月升级版) |
| ch_sci_2023 | 中科院分区(2023年12月升级版) |
| ch_sci_2022 | 中科院分区(2022年12月升级版) |
| sci | 是否SCI收录 |
| scopus | 是否Scopus收录 |
| pmc_url | PMC链接 |
| speed | 平均审稿速度 |
| accept | 平均录用比例 |
| jif_sci_rank | JIF SCI排名 |
| jci_sci_rank | JCI SCI排名 |
| similar_journals | 同类著名期刊 |

## 中科院分区字段结构

```python
{
    "大类学科": "工程技术",
    "小类学科": "ENGINEERING, CHEMICAL工程：化工",
    "Top期刊": True,
    "综述期刊": False,
    "分区": "2区"
}
```

## JIF/JCI SCI排名字段结构

```python
{
    "学科": "ENGINEERING, CHEMICAL",
    "收录子集": "SCIE",
    "分区": "Q2",
    "排名": "55/176",
    "百分位": ""
}
```

## 同类著名期刊字段结构

```python
[
    {
        "name": "Chemical Engineering Journal",
        "journal_id": "1639",
        "h_index": "172",
        "cite_score": "20.60"
    }
]
```
