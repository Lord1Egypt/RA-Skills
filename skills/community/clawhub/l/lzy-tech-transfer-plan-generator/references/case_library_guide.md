# 案例库使用指南（41个典型案例）

本技能内置两个数据文件，供运行时空时检索相似案例作参考：

- `case_library.json` — 41个案例完整数据（主库）
- `case_index.json` — 索引（按章节/专题/类型/来源分组）

## 案例构成

| 来源库 | 案例数 | 编号 | 内容 |
|--------|:---:|------|------|
| 北京典型案例集（第一期）2021 | 31 | 1-31 | 改革创新篇(1-8)、能力建设篇(9-17)、落地承接篇(18-31) |
| 全国精选案例 2026 | 10 | 32-41 | 作价入股/技术许可/技术转让/产学研合作/中试基地，含财政部完整会计分录案例 |

## 字段说明

### 通用字段（所有案例）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 案例编号 1-41 |
| case_number | str | "案例N" |
| title | str | 完整标题 |
| chapter_name | str | 改革创新篇/能力建设篇/落地承接篇/全国精选篇 |
| topic_number / topic_name | int/str | 专题编号与名称 |
| organization | str | 实施单位 |
| organization_type | str | 高校/科研院所/医院/企业/服务机构/政府部门 |
| summary | str | 摘要 |
| content | str | 正文 |
| key_measures | list | 关键举措 |
| key_policies | list | 政策依据 |
| tags | list | 标签 |
| first_case | bool | 是否北京/全国首例 |
| library | str | 数据来源库 |

### 全国精选案例扩展字段
| 字段 | 说明 |
|------|------|
| category | 转化模式：作价入股/技术许可/技术转让/产学研合作/中试基地 |
| technology_field | 技术领域：环保技术/生物医药/农业生物技术/新材料/环保装备-AI/多学科/综合 |
| core_technology | 核心技术 |
| partner | 合作方 |
| transaction | 交易信息（valuation评估价值/license_fee许可费/transfer_price转让价/equity_structure股权结构等，单位默认万元） |
| accounting | 会计处理（财政部案例含完整 journal_entries 会计分录） |
| performance | 成果数据（market_share市场占有率/cumulative_contracts累计合同等） |
| source / source_url | 来源与链接 |
| orig_id | 原始编号（CASE-001等） |

## 检索示例（运行时使用）

```python
import json
with open('references/case_library.json', encoding='utf-8') as f:
    cases = json.load(f)

# 按转化模式：找作价入股案例
equity = [c for c in cases if c.get('category') == '作价入股']
# -> 案例32（财政部作价入股+会计分录）、案例35（清华水质指纹，市场占有率80%）

# 按技术领域
medical = [c for c in cases if c.get('technology_field') == '生物医药']
# -> 案例37（厦门大学分枝杆菌试剂盒，里程碑付款超1亿）

# 按主体类型：高校
univ = [c for c in cases if c.get('organization_type') == '高校']

# 按专题（北京库）：收益分配专题
income = [c for c in cases if c.get('topic_number') == 4]

# 全文检索
kw = [c for c in cases if '概念验证' in json.dumps(c, ensure_ascii=False)]
```

## 高频可引用案例速查

| 场景 | 推荐引用 |
|------|---------|
| 作价入股（含会计处理） | 案例32（甲高校废电路板作价入股90万+完整分录） |
| 技术许可 | 案例33（污染场地修复系统许可40万/2年） |
| 技术转让 | 案例34（废电路板专利转让90万） |
| 收益分配制度 | 案例4（北交大）/5（药物所）/6（北医三院） |
| 医工结合 | 案例18（首医"交钥匙"）/19（积水潭）/20（北医三院联盟）/21（朝阳医院） |
| 概念验证中心 | 案例17（清华工研院） |
| 高校技术转移机构 | 案例9（北理工）/10（中科院计算所） |
| 企业承接转化 | 案例29（排水集团红菌）/30（纳通） |
| 全国首例/标杆 | 案例35（清华水质指纹，市场占有率80%）/38（青科大TPI世界首套） |

## 注意事项

- 金额单位默认"万元"（除特别说明）
- 案例32/33/34 为财政部会计司教学用模拟案例（"甲高校"为匿名），会计分录可作财务核算参考
- 北京库案例含「案例启示」字段（insights），可提炼经验做法
