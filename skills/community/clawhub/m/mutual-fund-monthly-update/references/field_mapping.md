# 字段映射规则

## 映射原理

AI通过字段名匹配，将模板中的字段名映射到PDF中的对应数据。

---

## 核心指标映射

| 模板字段 | PDF匹配字段（任一） | 数据类型 |
|---------|-------------------|---------|
| 久期 | 久期、组合久期、平均年期、Duration、有效久期、修正久期 | 数值 |
| YTM | 到期收益率、YTM、期满收益率、Yield to Maturity、平均到期收益率 | 百分比 |
| 基金规模 | 基金规模、资产净值、AUM、NAV、基金资产净值 | 数值（亿） |
| 平均评级 | 平均评级、平均信贷质量、Average Rating、信贷质量 | 文本 |
| 平均到期日 | 平均到期日、平均年期、Average Maturity | 数值（年） |
| 持仓数量 | 持仓数量、持仓数目、Number of Holdings | 数值 |
| 发行人数量 | 发行人数量、发行人数目、Number of Issuers | 数值 |

---

## 分布数据映射

### 行业分布

| 模板字段 | PDF匹配字段（任一） |
|---------|-------------------|
| 行业分布 | 行业分布、行业配置、Sector Distribution、Sector Allocation |
| 政府 | 政府、国债、Government、Sovereign |
| 银行 | 银行、Banking、Banks |
| 金融 | 金融、金融服务、Financial Services |
| 能源 | 能源、Energy |
| 通信 | 通信、Telecommunications、Telecom |
| 消费 | 消费、消费品、Consumer |
| 房地产 | 房地产、地产、Real Estate、Property |
| 保险 | 保险、Insurance |
| 公用事业 | 公用事业、公共事业、Utilities |
| 基础物料 | 基础物料、原材料、Basic Materials |
| 其他行业 | 其他行业、Other、Others |

### 地区分布

| 模板字段 | PDF匹配字段（任一） |
|---------|-------------------|
| 地区分布 | 地区分布、地区配置、市场分布、Geographic Distribution |
| 中国内地 | 中国内地、内地、中国大陆、China Mainland |
| 中国香港 | 中国香港、香港、Hong Kong、HK |
| 美国 | 美国、USA、United States |
| 日本 | 日本、Japan |
| 印尼 | 印尼、印度尼西亚、Indonesia |
| 印度 | 印度、India |
| 韩国 | 韩国、南韩、Korea、South Korea |
| 菲律宾 | 菲律宾、Philippines |
| 马来西亚 | 马来西亚、Malaysia |
| 澳大利亚 | 澳大利亚、澳洲、Australia |
| 新加坡 | 新加坡、Singapore |
| 其他地区 | 其他地区、Other Regions |

### 信用评级分布

| 模板字段 | PDF匹配字段（任一） |
|---------|-------------------|
| 信用评级 | 信用评级分布、评级分布、Credit Rating Distribution |
| AAA | AAA、Aaa |
| AA | AA、Aa |
| A | A |
| BBB | BBB、Baa |
| BB | BB、Ba |
| B | B |
| CCC | CCC、Caa |
| 无评级 | 无评级、未评级、Not Rated、NR、Unrated |

---

## 日期识别

### PDF日期格式识别

| PDF格式 | 示例 | 标准化结果 |
|--------|------|----------|
| YYYY年MM月DD日 | 2025年10月31日 | 202510 |
| YYYY.MM.DD | 2025.10.31 | 202510 |
| YYYY/MM/DD | 2025/10/31 | 202510 |
| YYYY-MM | 2025-10 | 202510 |
| MM/DD/YYYY | 10/31/2025 | 202510 |
| Oct 2025 | October 2025 | 202510 |
| 2025年10月 | 2025年10月 | 202510 |

### 模板日期格式适配

| 模板格式 | AI处理 |
|---------|--------|
| 10月 | 匹配月份数字 |
| 202510 | 匹配YYYYMM |
| 2025-10 | 匹配YYYY-MM |
| Oct-25 | 匹配英文月份 |

---

## 基金名称识别

### 识别规则

```
PDF中的基金名称：
- 汇丰亚洲债券基金 → 汇丰亚洲债券
- 摩根亚洲总收益债券基金 → 摩根亚洲总收益
- 博时新兴市场债券基金 → 博时新兴市场

标准化处理：
1. 提取基金名称
2. 去除"基金"、"Fund"等后缀
3. 作为Sheet名称
```

### 同产品判断

```
判断为同一产品的条件：
1. 基金名称相同（去除日期后）
2. 同一股份类别

示例：
- 汇丰亚洲债券基金 10月.pdf
- 汇丰亚洲债券基金 11月.pdf
→ 判断为同一产品，放在同一Sheet
```

---

## 数据格式转换

### 百分比转换

```
PDF数据 → 模板格式

情况1：PDF=5.54，模板=%
  → 输出：5.54%

情况2：PDF=5.54%，模板=小数
  → 输出：0.0554

情况3：PDF=554bp，模板=%
  → 输出：5.54%
```

### 金额转换

```
PDF数据 → 模板格式

情况1：PDF=2,893,380,420，模板=亿
  → 输出：28.93亿

情况2：PDF=28.93亿美元，模板=数字
  → 输出：28.93

情况3：PDF=$2.89B，模板=亿
  → 输出：28.93亿
```

---

## 模糊匹配算法

### 匹配流程

```python
def match_field(template_field, pdf_fields):
    # 1. 完全匹配
    if template_field in pdf_fields:
        return pdf_fields[template_field]
    
    # 2. 去空格/大小写匹配
    normalized = template_field.lower().replace(" ", "")
    for key in pdf_fields:
        if key.lower().replace(" ", "") == normalized:
            return pdf_fields[key]
    
    # 3. 包含匹配
    for key in pdf_fields:
        if template_field in key or key in template_field:
            return pdf_fields[key]
    
    # 4. 同义词匹配
    synonyms = get_synonyms(template_field)
    for key in pdf_fields:
        if any(syn in key for syn in synonyms):
            return pdf_fields[key]
    
    # 5. 未匹配
    return None
```

### 同义词表

```python
synonyms = {
    "久期": ["duration", "久期", "组合久期"],
    "YTM": ["ytm", "yield", "收益率", "到期收益率"],
    "基金规模": ["aum", "nav", "规模", "资产净值"],
    # ... 更多同义词
}
```

---

## 匹配结果标记

### 标记规则

| 匹配状态 | 标记方式 | 说明 |
|---------|---------|------|
| 完全匹配 | 正常显示 | 无需标注 |
| 模糊匹配 | 黄色高亮 | 用户需确认 |
| 未匹配 | 红色高亮 + "N/A" | 用户需手动填充 |
| 多个候选 | 橙色高亮 | AI选择了最佳匹配 |

### 输出说明

```
AI生成Excel后，附带说明：
- 完全匹配：12个字段
- 模糊匹配：3个字段（已黄色标记）
- 未匹配：2个字段（已红色标记，需手动填充）
```
