---
name: keyword-selection-method
description: 关键词选品法：围绕种子词或给定词端到端完成关键词选品+全面竞品数据采集。S1取候选词→S2亚马逊搜索取代表ASIN+卖家精灵反查需供比一刀判淘汰→S3全面数据采集→S4汇总输出。输出按需供比降序的细分市场候选清单。当用户提到关键词选品、选品方法、关键词供需筛选、季节性选品、竞品分析、keyword selection、niche selection时触发。
---

# 关键词选品法

围绕种子词端到端完成关键词选品+全面竞品数据采集，输出按需供比降序的细分市场候选清单。

## 处理模式

- **扩词型**（默认）：仅提供种子词 → 从种子词出发扩展候选关键词
- **验证型**：提供具体关键词列表 → 只验证给定词，跳过扩词

## 执行编排

L1{S1} → L2{S2a} → L2.5{S2a+} → L3{S2b} → L4{S2c} → L5{S3} → L6{S4}

## 流水线总览

| 步骤 | 标题 | 一句话 | 调用 | 依赖 | 用途 | 详情 |
|------|------|--------|------|------|------|------|
| S1 | 取候选词 | 扩词型用建议词扩展；验证型直接用给定词 | linkfox-amazon-suggestion-miner | - | 候选关键词池 | steps/S1.md |
| S2a | 取代表ASIN | 亚马逊前台搜索每个关键词取Top1自然位ASIN | linkfox-amazon-search | S1 | 代表ASIN+标题+价格+主图 | steps/S2.md |
| S2a+ | ASIN频率分析 | 统计ASIN出现频率+市场集中度+广告投手识别+去重 | 内部逻辑 | S2a | 去重省积分+市场集中度+广告投手识别 | steps/S2.md |
| S2b | 查需供比 | 卖家精灵反查ASIN取该词对应的需供比+CPC+垄断率+购买量+购买率+商品数 | linkfox-sellersprite-traffic-keyword | S2a+ | 需求验证+竞争度数据 | steps/S2.md |
| S2c | 一刀判 | 需供比+三因素竞争度综合过滤（优先决策树） | 内部逻辑 | S2b | 淘汰假需求/红海/垄断/数据不足 | steps/S2.md |
| S3 | 全面数据采集 | 并行抓取5维竞品数据（仅deepDiveTopN个词） | 多工具并行 | S2c | 深度竞品分析 | steps/S3.md |
| S4 | 汇总输出 | 合并所有数据输出清单 | 内部逻辑 | S3 | 最终交付物 | steps/S4.md |

## 设计原则：卖家精灵优先

- **需求验证**：卖家精灵 `searches`（月搜索量）> 0 即有需求，无需 ABA 单独验证，**禁止使用 SIF**
- **需供比**：直接用卖家精灵 `supplyDemandRatio` 字段（月搜索量/商品数，越高越好）
- **代表ASIN**：亚马逊前台搜索取Top1自然位ASIN（同时拿到标题+价格+主图）
- **不再依赖ABA做需求验证**：ABA对季节性词淡季返回空，卖家精灵全年有数据
- **数据路径约束**：无直接关键词查询工具，必须走「Amazon搜索 → Top1自然位ASIN → 卖家精灵反查」路径。若候选词未出现在该ASIN的流量词Top100中，则无法获得可靠指标。

## 输入参数

### 基础参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| seedKeyword | 扩词型必填 | - | 种子关键词 |
| keywordList | 验证型必填 | - | 具体关键词列表 |
| marketplace | 否 | US | 站点代码 |
| topN | 否 | 20 | 输出前N个关键词（从保留池中取） |
| deepDiveTopN | 否 | 5 | 对前N个保留词做全面数据采集 |
| filterBroadTerms | 否 | true | 是否过滤宽泛词 |
| profile | 否 | null | 预设模板名：novice/demand-supply/reverse-asin/weighted-score/long-tail |

### Tier-1 核心过滤参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| minPrice | null | 最低价格，低于→放弃-价格过低 |
| maxPrice | null | 最高价格，高于→放弃-价格过高 |
| minSearches | 0 | 最低月搜索量，低于→放弃-需求不足 |
| monopolyThreshold | 0.6 | Top3点击率阈值 |
| monopolyAction | abandon | 垄断处理：abandon(放弃)/watch(观望)/downgrade(评分扣分) |
| redOceanThreshold | 0.1 | 需供比低于此→放弃-红海 |
| watchThreshold | 0.3 | 需供比低于此→观望-竞争激烈 |
| opportunityThreshold | 1.0 | 需供比高于此→可进-机会型 |
| productLowThreshold | 1000 | 商品数低于此=低竞争 |
| productHighThreshold | 5000 | 商品数高于此=高竞争 |
| minPurchases | null | 最低月购买量 |
| minPurchaseRate | null | 最低购买率（0.02=2%） |
| maxCPC | null | 最高CPC（3.0=$3） |

### Tier-2 次要参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| sortBy | sdr | 排序：sdr/score/custom |
| scoreWeights | 见下 | 评分权重，仅sortBy=score时生效 |
| includeWatchlist | true | 输出是否包含"观望"词 |
| riskAppetite | balanced | conservative/balanced/aggressive |
| broadTermBlacklist | [] | 自定义宽泛词黑名单 |
| maxProducts | null | 商品数绝对上限 |

### 综合评分公式

scoreWeights 默认值：`{"sdr": 0.35, "searches": 0.25, "purchaseRate": 0.20, "monopolyPenalty": 0.15, "cpcPenalty": 0.05}`

公式（各维度先归一化到0-1）：
```
score = w_sdr × norm(SDR) + w_searches × norm(log(搜索量)) + w_purchaseRate × norm(购买率)
        - w_monopoly × norm(垄断率) - w_cpc × norm(CPC)
```

### 预设模板

| 模板名 | 适用场景 | 核心配置 |
|--------|----------|----------|
| novice | 新手保守型 | minSearches=3000, monopolyThreshold=0.55, redOceanThreshold=1.0, minPurchaseRate=0.03, includeWatchlist=false |
| demand-supply | 需供比核心漏斗型 | minSearches=2000, monopolyThreshold=0.50, redOceanThreshold=0.8, minPurchaseRate=0.04, maxCPC=1.5, sortBy=custom |
| reverse-asin | 反查竞品精准型 | minSearches=1500, monopolyThreshold=0.45, redOceanThreshold=1.0, minPurchaseRate=0.06, maxCPC=1.2, sortBy=score, scoreWeights={purchaseRate:0.35} |
| weighted-score | 成熟加权评分型 | minPrice=18, maxPrice=55, minSearches=3000, monopolyThreshold=0.48, monopolyAction=demote, redOceanThreshold=0.6, sortBy=score |
| long-tail | 长尾猎人型 | minSearches=300, maxSearches=10000, monopolyThreshold=0.40, redOceanThreshold=3.0, minPurchaseRate=0.08, maxCPC=0.9, minTokenCount=3 |

## 输出字段

| 字段 | 来源 | 说明 |
|------|------|------|
| rank | S4排序 | 排名（按sortBy参数排序，仅保留池） |
| platform | 固定 | 平台/站点 |
| keyword | S1 | 关键词 |
| demandSignal | S2b | 需求信号（基于月搜索量分级） |
| priceBand | S2a | 价格带（来自代表ASIN价格） |
| funnelConclusion | S2c | 漏斗结论（可进/观望/放弃+原因） |
| suggestedAction | S2c | 建议动作 |
| sortBasis | S4 | 排序依据（需供比值或综合评分） |
| score | S4 | 综合评分（仅sortBy=score时有值，0-10分） |
| filterTrace | S4 | 过滤标注（如"价格$26.99 ✓ \| 搜索量45,906 ✓ \| 综合分8.4"） |
| representativeProduct | S2a | 代表商品（ASIN+标题+价格+主图） |
| competition | S2c | 竞争度（低/中/高） |
| cpc | S2b | PPC竞价/CPC |
| purchases | S2b | 月购买量 |
| purchaseRate | S2b | 购买率 |
| products | S2b | 商品数（三因素之一） |

## 漏斗过滤规则（S2c 一刀判 · 优先决策树）

按以下顺序判断，**第一个命中的条件即生效**：

1. **Amazon搜索无结果（无ASIN）** → 放弃-无搜索结果
2. **候选词未出现在代表ASIN的卖家精灵流量词Top100中** → 放弃-数据不足
3. **卖家精灵无数据或 searches == 0** → 放弃-假需求
4. **filterBroadTerms == true 且（关键词 == 种子词 或 is_broad(关键词)）** → 放弃-词过于宽泛
   - `is_broad` 启发式：token数 ≤ 1，或明显无产品修饰词的宽泛词
   - **验证型**下对用户明确给出的词更宽容（不因 == seed 而自动放弃）
5. **垄断率（Top3点击率） > monopolyThreshold** → **放弃-垄断**（一票否决）
6. **需供比 < redOceanThreshold** → 放弃-红海
7. **竞争度 == 高**（见下方决策树） → 观望-竞争激烈
8. **需供比 < 0.3** → 观望-竞争激烈
9. **0.3 ≤ 需供比 ≤ 1.0** → 可进-供需平衡
10. **需供比 > 1.0** → 可进-机会型

> 淘汰词（所有「放弃」）保留在附录，标注原因（数据诚信原则）。
> **可进 + 观望** = 保留池，按需供比降序排序后取 `deepDiveTopN` 进入S3，最终 `topN` 也从此池输出。

## 竞争度三因素决策树（完整优先逻辑）

```text
if 垄断率 > monopolyThreshold:
    竞争度 = 高          # 头部锁定（已在漏斗第5步直接放弃）
elif 商品数 > 5000 and 需供比 < 1:
    竞争度 = 高          # 红海，供过于求
elif 商品数 > 5000 and 需供比 >= 1:
    竞争度 = 中          # 需求大但竞争者多
elif 1000 <= 商品数 <= 5000 and 需供比 > 1:
    竞争度 = 中          # 有机会，差异化切入
elif 商品数 < 1000 and 需供比 > 1:
    竞争度 = 低          # 蓝海，优先切入
else:                     # 其余情况（商品数中低 + 需供比 ≤1）
    if 需供比 < 0.3:
        竞争度 = 高
    else:
        竞争度 = 中
```

## 数据诚信原则

- 缺字段标注「未返回」，严禁编造销量/利润/趋势数字
- 淘汰词保留并标注原因
- S3仅对deepDiveTopN个词做全面采集，其余标注"未深度采集"
