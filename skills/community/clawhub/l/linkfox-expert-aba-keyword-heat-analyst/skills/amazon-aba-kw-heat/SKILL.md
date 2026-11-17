---
name: amazon-aba-kw-heat
description: "ABA关键词热度分析。支持三种入口：精确词列表、产品图推断搜词、ASIN反查流量词，再批量验证多周SFR。当用户给图/ASIN/词表要热度趋势、多词对比、季节趋势时触发。"
---

# amazon-aba-kw-heat · 关键词热度分析

> ABA **薄场景壳**（Shell A）。取数依赖 L3：`linkfox-aba-data-explorer`。  
> 入口解析可走本 skill `scripts/resolve_entry.py`，或手工编排下游 skill。

## 专家角色

**ABA关键词热度分析师**

## 目标

- 将用户意图变成 **一批精确搜索词**，再拉多周 SFR 做热度验证  
- 支持 **词 / 图 / ASIN** 三种入口  
- 需要可视化时交给 `amazon-aba-kw-heat-report`

## 三种入口（必须支持）

| 入口 | 用户给什么 | 怎么变成 keywords[] | 再做什么 |
|------|------------|---------------------|----------|
| **A. 词表** | 1～N 个精确词 | 直接用 | Shell A 热度 |
| **B. 产品图** | 图片 URL 或本地图 | 多模态推断常用 Amazon 搜词 | Shell A 验证热度 |
| **C. ASIN** | 1～N 个 ASIN | `amazon-aba-asin-reverse` 反查流量词，按 SFR 取 TopN | Shell A 验证热度 |

可组合：图+ASIN+手补词 → 合并去重后再跑热度。

### B. 图 → 搜词（编排）

1. 本地图先上传拿公网 URL：`linkfox-multimodal-recognize-image` → `scripts/upload_image.py`  
2. 识别并**只要搜词 JSON**：  
   `requirement` 固定要求返回  
   `{"product_type","search_keywords":[...],"confidence","notes"}`  
   （英文 Amazon 搜索句式，3～12 个，按可能性排序）  
3. 解析 `search_keywords` → `keywords[]`  
4. 向用户展示「推断词表」后再跑 ABA（可让用户改词）  
5. 调用本壳 Shell A / 或直接 `amazon-aba-kw-heat-report`

脚本一键（推荐）：

```bash
python3 scripts/resolve_entry.py \
  '{"image":"/path/or.png","region":"US","max_keywords":10}'
# 或 imageUrl
```

### C. ASIN → 流量词（编排）

1. 调用 `amazon-aba-asin-reverse`（Shell F）  
   `{"asins":["B0..."],"region":"US","weeks":8,"top_n":30,"order_by":"sfr"}`  
2. 从结果抽 `searchTerm`，按 SFR 升序（越热越前）取 TopN（默认 10～12）  
3. 得到 `keywords[]` → Shell A 热度验证  

```bash
python3 scripts/resolve_entry.py \
  '{"asins":["B01LP0V4JY"],"region":"US","top_n":12}'
```

### A. 词表直跑

```bash
python3 scripts/shell_a.py '{"region":"US","keywords":["yoga mat","exercise mat"],"weeks":52}'
```

## 输入（Shell A 本体）

| 参数 | 必填 | 说明 |
|------|------|------|
| region | 否 | 默认 US |
| keywords | 是* | 精确词；若走图/ASIN 入口则由上游解析填入 |
| weeks | 否 | 默认 12；报告场景建议 80～104 |
| top_k_asin | 否 | 每词 TopK ASIN，默认 0 或 3 |
| preset | 否 | 热度趋势 / 多词对比 / 季节 / 品牌追踪 / 同比季节性对比 等 |
| dedupe | 否 | 默认 identical searchTerm+ASIN keep latest |
| createDownloadUrl | 否 | bool 默认 false |
| yoy_compare | 否 | bool 默认 false；设 true 时拉取去年同期 SFR 做同比季节性对比 |

\* 对用户会话而言：keywords **或** image **或** asins 至少一个。

### Preset（展示场景名）

关键词热度趋势、精确词热度+Top3、多词/批量词表对比、季节节日趋势、品牌词热度追踪、同比季节性对比

## 工作流程（Agent）

1. **判定入口**：纯词 / 图 / ASIN / 混合  
2. **解析 keywords**（`resolve_entry.py` 或手工调多模态 + Shell F）  
3. 展示推断/反查词表；用户有修正则合并  
4. Shell A 拉多周 SFR；提醒 **SFR 越小越热**  
5. **长尾词回退**：若返回 `total=0` 且关键词为长尾词（含修饰词、年份、风格限定等），自动提取核心短词重试：
   - 去掉年份/季节修饰（如 "Summer 2026"）、风格限定（如 "Coquette Style"）、材质描述（如 "Lace Trim"）等
   - 保留品类核心词（如 "babydoll dress"、"bodycon dress"）
   - 用核心短词重新调用 Shell A
   - 输出时必须标注「原词 → 实际查询词」对应关系，明确哪些原词有数据、哪些仍无数据
   - 若核心短词仍无数据，告知用户该词搜索量未达 ABA 收录阈值
6. **同比季节性对比**（用户要求或 `yoy_compare=true` 时）：用相同关键词、相同周数拉取去年同期 SFR 数据，按周对齐做同比对比表，判断季节性走势是否一致：
   - 去年同期日期 = 今年日期 - 365 天（按周对齐）
   - 输出按关键词分组的同比表：每周同时展示去年 SFR、今年 SFR、同比变化百分比
   - 标注每个关键词的季节性判断：一致 / 不一致（去年升温今年掉热等）
   - 同比变化百分比 = (今年SFR - 去年SFR) / 去年SFR × 100%；正数 = 今年更冷（SFR更大），负数 = 今年更热
7. 若要报告/可视化 → `amazon-aba-kw-heat-report`（可直接把 image/asins 传给 report，内置 resolve）  
8. 越界（绝对搜索量/销量/BSR）→ 拒做并导流  

## 输出

- ABA `tables`（searchTerm / reportStartDate / searchFrequencyRank / …）  
- 入口为图/ASIN 时，额外说明 **keywords 来源**（推断 / 反查）  

## 限制 / 边界

- 图推断词 ≠ 真实流量词；**必须以 ABA 验证**，并标注 confidence  
- ASIN 反查依赖该 ASIN 在 ABA 有点击记录；新链/零曝光可能为空  
- 无绝对搜索量/销量/BSR/上架日  
- 站点是参数不是 skill  

## 与其它 skill

| 需求 | 用 |
|------|-----|
| 图理解/上传 | `linkfox-multimodal-recognize-image` |
| ASIN→词 | `amazon-aba-asin-reverse` |
| 热度 HTML 报告（含入口解析） | `amazon-aba-kw-heat-report` |
| 自由 ABA | `linkfox-aba-data-explorer` |

## 契约

工厂 `references/aba-six/contracts/A-amazon-aba-kw-heat.json`
