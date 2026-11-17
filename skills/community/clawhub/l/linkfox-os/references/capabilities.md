# linkfox-os — Agent Capabilities Reference

This document details the capabilities, sub-functions, and typical prompts for each specialized agent available through the `linkfox-os` async task pipeline.

For quick routing, see the summary table in `SKILL.md`. This file provides the deep reference when you need to understand what each agent can do and how to prompt it effectively.

---

## 1. General Assistant (`default`)

跨境电商运营通用智能助手。拥有全域业务 skill，覆盖平台数据查询、市场分析、选品调研、关键词研究、商品图生成、视频生成、Listing 撰写、知识产权检索等能力。根据用户真实目标自主选择合适的 skill 组合完成任务。

**核心特征**：不是纯 router，会先在主会话给出有用结果、分析或执行计划；复杂任务主动串联多个 skill（如选品 → 关键词验证 → 竞品分析 → 报告输出）。

### 能力覆盖（通过 `linkfox-*` 系列 skill 实现）

| 能力类别 | 覆盖范围 |
|----------|---------|
| 平台数据查询 | Amazon/TikTok/eBay/Walmart/Shopee/Ozon 商品搜索、详情、评论 |
| 市场分析 | 关键词搜索量、竞品格局、价格带、销量趋势 |
| 选品调研 | 关键词选品、条件选品、爆款预测、对标选品 |
| 关键词研究 | SIF 反查、ABA 数据挖掘、流量来源、竞品数量 |
| 商品图生成 | AI 绘图、商品套图、图片裂变 |
| 视频生成 | 图转视频、带货口播、爆款复刻 |
| Listing 撰写 | 标题、五点、描述、Search Terms |
| 知识产权检索 | 外观专利、发明专利、商标、版权、政策合规 |
| 趋势分析 | Google Trends、TikTok 热销榜、亚马逊 BSR |
| 1688 供应链 | 以图搜图、商品榜单、选品库 |
| 实时检索 | 网页搜索（Tavily）、Google AI Mode |
| 数据处理 | 智能数据查询、Excel/PDF 分析、Python 沙箱 |

### 显式工具名识别

用户输入中出现以下工具名时，视为对数据源的显式指代：

`@卖家精灵`、`@Keepa`、`@亚马逊前端`、`@SIF`、`@ABA`、`@智慧芽`、`@睿观`、`@AI绘图`、`@店雷达`

### 典型 Prompt

```
帮我在亚马逊美国站搜索 "wireless earbuds"，返回前 20 条商品数据
```

```
查询 ASIN B0XXXXXXXXX 的 Keepa 价格历史和销量趋势
```

```
用卖家精灵搜索美国站 "yoga mat" 关键词的竞品数据
```

```
帮我在 1688 以图搜图，找这个商品的供应商
```

```
1、在亚马逊美国站搜索 "computer desk"，返回前 2 页商品数据
2、对上一步商品标题分词，统计出现的功能点
3、按功能点统计月销量、月销售额、asin 数
```

### 专业 Agent 推荐触发

当 default agent 完成数据查询或分析后，会根据后续方向推荐切换到专业 Agent：

| 后续方向 | 推荐 Agent |
|---------|-----------|
| 选品/找产品/判断能不能做/预算供应链适配/爆款预测 | `linkfox-product-selection-agent` |
| 市场调研/竞品格局/评论痛点/趋势/合规/IP/关键词 | `linkfox-market-analysis-agent` |
| 标题/五点/A+/描述/Listing 优化/埋词检查 | `linkfox-listing-agent` |
| 主图/场景图/白底图/卖点图/A+ 图/商品图/模特图 | `linkfox-image-agent` |
| 图转视频/口播/TikTok 短视频/视频广告/爆款视频 | `linkfox-video-agent` |

---

## 2. Market Analysis Agent (`linkfox-market-analysis-agent`)

顶级咨询公司级别的亚马逊细分市场分析师。覆盖 5 个分析维度，产出结构化 HTML 报告。拥有 60+ 个可调用 skill。

### 三种分析模式

| 模式 | 适用场景 | 渲染工具 |
|------|---------|---------|
| **编排型分析** | 完整 5 维度 pipeline（市场初步/竞品/评论/关键词/合规全走） | `linkfox-market-html`（全链路渲染） |
| **聚焦分析** | 单维或多维但不完整的针对性分析 | `generate_report.py`（轻量报告） |
| **工具查询型分析** | 纯工具查询 + 用户提到具体分析维度/指标 | `linkfox-report-generator` |

### 分析维度

| 维度 | 典型用户表达 | 可调用工具类别 |
|------|----------|------------|
| **市场初步** | "看这个市场的容量/趋势/竞争" | 卖家精灵市场数据、Keepa 趋势、Google Trends |
| **竞品分析** | "这几个 ASIN 怎么样""竞品的规格/定价/流量" | Amazon 商品详情、Keepa、SIF 流量、卖家精灵竞品反查 |
| **评论分析** | "用户在痛什么""差评集中在哪""用户怎么评价" | Amazon 评论列表、极目舆情 |
| **关键词调研** | "靠哪些词获客""这个词的搜索量/CPC" | SIF 关键词、ABA 查询、Google Trends |
| **合规检测** | "检测专利风险""这个产品有没有侵权" | 睿观检测、智慧芽专利查询 |

### 意图识别优先级

1. 用户提到**具体分析维度/指标**（综合转化率、平均 CPC、点击转化等）→ 优先走工具查询型分析
2. 措辞含"分析/总结/对比/建议/判断"→ 走聚焦分析或工具查询型分析
3. "做完整市场分析/深度分析/从各维度分析"→ 走编排型分析（全链路）
4. 只有"查/获取/列出"等纯取数字眼 → 工具型查询，数据落盘不出报告

### 典型 Prompt

```
对亚马逊美国站 "cat water fountain" 做一个完整的市场分析
```

```
分析 ASIN B0GZSVVBJZ 的差评，提取用户痛点和改良方向
```

```
对比这 5 个竞品 ASIN 的流量结构和关键词布局
```

```
检测这个商品图片是否有外观专利侵权风险
```

```
分析 "portable projector" 关键词的搜索量趋势和竞争格局
```

---

## 3. Product Selection Agent (`linkfox-product-selection-agent`)

跨境电商选品专家，覆盖 Amazon、TikTok Shop、Shopee、Ozon、Walmart、eBay、1688 七大平台。核心价值：约束条件是输入，契合条件、值得做的产品是输出。

### 自有 Skill（四个端到端选品流程）

| Skill | 适用子任务 | 触发短语 |
|-------|-----------|---------|
| `linkfox-keyword-select` | 关键词/搜索词选品（需求端），一个关键词=一个细分市场 | "关键词选品 / 按关键词找市场 / 这个词能做吗 / 哪些词值得做" |
| `linkfox-viral-predict` | 潜在爆款预测，宏观趋势→中观类目→微观产品三维加权打分 | "爆款预测 / 找潜力爆品 / 哪些品会爆 / 蓝海潜力选品" |
| `linkfox-product-condition-selection` | 按产品条件选品（供给端正向筛品），模式化或自定义阈值 | "按条件选品 / 低价长尾 / 销量飙升榜 / 潜力市场" |
| `linkfox-benchmark-product-selection` | 对标选品，锚点为商品ID/链接/主图/关键词/品牌/卖家 | "对标选品 / 按ASIN对标 / 按链接或图找竞品 / 按品牌对标" |

### 按运营方式匹配选品逻辑

| 运营方式 | 选品重点 | 数据支撑 |
|---------|---------|---------|
| 铺货 | 轻小件、低客单、低风险、易批量 Listing | 充分 |
| 精品 | 稳定需求、差异化空间、利润结构、供应链可控 | 充分 |
| 品牌/自有品牌 | 可品牌化、痛点清晰、可系列化、复购粘性 | 待完善（US-centric） |
| 爆品/测品 | 强视觉、3秒看懂、情绪价值、冲动消费、素材空间 | 充分 |
| 平台精细化 | 搜索需求、关键词空间、竞品数量质量、Review 门槛 | 最完整 |
| B2B/批发 | 批量采购、稳定复购、MOQ 阶梯、可定制贴牌 | 仅 1688 供货侧 |

### 共性约束

- 取数预算 **≤7 次 API 调用**
- 原始响应不进上下文（走 `response_io.py` 落盘 + 投影）
- 端到端一次跑完，不分步等"继续"
- 落盘脚本打印完成标志即任务结束

### 典型 Prompt

```
帮我用关键词选品，分析 "insulated water bottle" 这个细分市场值不值得做
```

```
预测美国站未来 3 个月可能爆发的家居小家电品类
```

```
按条件选品：美国站，月销量 500+，评分 4.2 以下，价格 $15-$30，上架 6 个月内
```

```
以 ASIN B0XXXXXXXXX 为标杆，找同品类可切入的差异化方向
```

```
我是铺货模式，预算有限，帮我在 TikTok Shop 美国站找 5 个轻小件低客单产品
```

---

## 4. Listing Agent (`linkfox-listing-agent`)

Amazon Listing 运营官。负责理解用户意图 → 路由到正确执行 skill → 在关键节点产出结构化中间结果 → 最终落盘 HTML 报告。

### 五种模式

| 模式 | 触发方式 | 调用 Skill |
|------|---------|-----------|
| 对标复刻 (benchmark) | `[modeInstruction:benchmark]` 或 "对标参考竞品/复刻差异化" | `listing-benchmark` |
| 诊断优化 (rewrite) | `[modeInstruction:rewrite]` 或 "诊断/优化这个链接" | `listing-rewrite` |
| 新建 Listing (create) | `[modeInstruction:create]` 或 "基于产品信息新建" | `listing-create` |
| 批量生成 (batch) | `[modeInstruction:batch]` 或 多商品各生成完整 Listing | `listing-batch-replicate` |
| 质量评分 (report) | `[modeInstruction:report]` 或 "检查质量/打分/评估" | `listing-quality-scorer` → `agent-listing-result-html-skill` |

### 生成 Pipeline（L1-L5）

```
L1 输入确认 → L2 商品/竞品信息采集 → L3 关键词矩阵 + 卖点策略 → [交互断点] → L4 文案写作 → L5 质量门 → HTML 报告
```

**关键 Skill 调用链（benchmark 模式为例）**：
```
L2: listing-asin-deep-fetch (竞品详情+变体)
L3: listing-keyword-matrix-build → listing-review-mine(可选) → listing-compliance-scan
L4: listing-title-writer (Title≤75c + Item Highlights≤125c) → listing-bullet-writer
L5: listing-diff-meter → listing-compliance-validator
报告: assemble_report_from_artifacts.py → agent-listing-result-html-skill
```

### 输出规格（Amazon 2026 政策）

| 字段 | 约束 |
|------|------|
| Title | ≤75 字符 |
| Item Highlights | ≤125 字符/条（新增要求） |
| Bullet Points (五点描述) | BAF 五维度结构 |
| Description | A+ compatible |
| Backend Search Terms | 关键词利用率优化 |
| Score Panel | 8 维度评分 + 可执行建议 |

### 多变体生成

`num_variants > 1` 时按 style_angle 循环 writer：功能型、场景型、情感型、礼品型、技术型、性价比型、高端型、极简型。

### 典型 Prompt

```
参考竞品 ASIN B0XXXXXXXXX，为我的产品生成差异化 Listing（美国站英语）
```

```
诊断优化我的 ASIN B0YYYYYYYYY 的 Listing，重点提升关键词覆盖率
```

```
基于以下产品信息新建 Listing：
- 产品名：不锈钢保温杯 500ml
- 卖点：双层真空、24小时保温、食品级304不锈钢、防漏设计
- 目标市场：美国站
```

```
给这个 Listing 打分，检查标题、五点、描述的质量
```

```
批量为这 10 个商品各生成一版完整 Listing，写 3 个风格变体
```

---

## 5. Image Agent (`linkfox-image-agent`)

电商出图总编排。职责：听懂用户出图诉求 → 判定走哪条链路 → 交给对应 skill 执行。自身不出图、不拼 prompt。

### 路由决策（两层判定）

**第一层**：前端显式指定技能 → 按映射表直调
**第二层**：自然语言判断，按优先级命中即停：

1. **人台换模特** → `linkfox-aigc-imagegen-mannequin-to-model`
2. **爆款复刻** → `linkfox-aigc-imagegen-bestseller-replicate`
3. **图片裂变** → `linkfox-aigc-imagegen-image-fission`
4. **操作指令型（创意自足）** → `linkfox-aigc-imagegen`（直走底层）
5. **画面描述型（创意自足）** → `linkfox-aigc-imagegen`（直走底层）
6. **仅类型意图、缺创意方向** → collection（此时判品类：商品系 vs 服饰系）

### 出图能力

| 能力 | 适用场景 | 对应 Skill |
|------|---------|-----------|
| 商品套图 | 主图 + 场景图 + 卖点图 + 特写图 + A+ 图 | `linkfox-aigc-imagegen-product` |
| 服装套图 | 模特图 + 种草图 + 尺码图 + 卖点图 + A+ 图 | `linkfox-aigc-imagegen-cloth` |
| 图片裂变 | 同商品生成 N 张视觉不同的新图（防关联/铺货） | `linkfox-aigc-imagegen-image-fission` |
| 爆款复刻 | 参考竞品图排版，用自己商品图复刻 | `linkfox-aigc-imagegen-bestseller-replicate` |
| 人台换模特 | 把人台/模型架替换成真人模特穿着效果 | `linkfox-aigc-imagegen-mannequin-to-model` |
| 白底图 | Amazon 主图合规白底图 | product/cloth (type=WHITE_BG) |
| 场景图/种草图 | 生活场景图（厨房/户外/健身等） | product/cloth (type=SCENE) |
| 卖点图 | 带文字 overlay 突出功能特性 | product/cloth (type=SELLING_POINT) |
| 特写图 | 材质/纹理细节特写 | product (type=CLOSE_UP) |
| A+ 图 | Premium(1464:600)、Standard(970:600)、Phone(600:450) | product/cloth (type=*_APLUS) |
| 模特图 | 标准电商上身主图 | cloth (type=MODEL_IMAGE) |
| 尺码图 | 尺码表可视化 | cloth (type=SIZE) |

### 品类判定规则

**仅在确定走 collection 后才判品类**。创意自足（操作指令/完整画面描述）直走底层 `linkfox-aigc-imagegen`，不进 collection、不判品类。

### 支持模型（provider）

| 前端模型名 | 内部代码 |
|-----------|---------|
| LFBanana Pro / 香蕉 Pro | `BANANA_PRO` |
| GPT Image 2 / Img2 | `GPT_2_IMAGE` |
| LFBanana2 / Banana 2 | `BANANA_2` |
| Linkfox-Image-1 | `AIDRAW_EDIT` |
| Wan 2.7 | `WAN2_7` |
| Seedream 5.0 | `SEEDREAM5` |

### 典型 Prompt

```
为这个商品主图生成一套 7 张亚马逊商品图（含白底图、场景图、卖点图、A+ 图）
```

```
把这张人台图换成真人模特穿着效果
```

```
参考这个爆款竞品的主图风格，用我的商品图复刻一套
```

```
对这张商品图做 3 张裂变，风格偏 ins 风
```

```
生成一张卖点图，突出"防水""轻便""大容量"三个核心卖点，比例 1:1
```

---

## 6. Video Agent (`linkfox-video-agent`)

电商视频生成总编排。只路由到三个视频 skill，自己不生成视频、不手写 prompt。

### 三条视频链路

| 链路 | 对应 Skill | 触发信号 |
|------|-----------|---------|
| 爆款视频复刻 | `linkfox-aigc-videogen-viral-replicate` | 给了参考爆款视频 + 商品图，要"复刻/做同款/替换商品" |
| 带货口播 | `linkfox-aigc-videogen-sale` | 要商品口播/真人自拍风带货/TikTok广告/达人种草 |
| 图转视频 | `linkfox-aigc-videogen-image-to-video` | 只想把图片动起来/参考图生视频/首尾帧 |

### 必备入参

**爆款视频复刻**：
- `reference_video_url`：参考视频 http(s) URL（必填）
- `product_image_url`：用户商品图 http(s) URL（必填）
- 可选：`product_name`、`product_desc`、`usp`、`sales_country`、`target_language`、`target_duration`(Auto/5S/10S/15S)

**带货口播**：
- `imageList` 或 `imageUrl`：商品图 http(s) URL（必填）
- `customer_keywords`：商品卖点、痛点（必填）
- `targetAudience`：目标受众（必填）
- `videoDuration`：期望时长（必填）
- 默认：`language`=英语，`salesRegion`=美国
- 流程：先生成 3 套口播方案 → 用户选择 1/2/3 → 生成视频

**图转视频**：
- `entry: "img2video"`（必填）
- 参考图模式：`imageList` 或 `imageUrl`（必填）
- 首尾帧模式：`imageUrl`（必填），可选 `lastFrameImageUrl`
- `videoType`、`videoTime`（必填）
- 模式判断：有 `lastFrameImageUrl` → `first_last_frame`；否则 → `reference`

### 典型 Prompt

```
把这张商品图转成 5 秒的短视频，比例 9:16
```

```
为这个商品生成一段带货口播视频，目标受众是美国 25-35 岁女性，卖点是便携和快速加热，时长 15 秒
```

```
参考这个爆款视频 [URL]，用我的商品图复刻一个同款结构的短视频
```

---

## 跨 Agent 工作流示例

复杂任务可按序串联多个 Agent：

### 从选品到上架

```
Step 1 (选品 Agent): 帮我在美国站找 3 个值得做的 insulated water bottle 细分方向
Step 2 (市场分析 Agent): 对第一步推荐的 Top 1 方向做完整市场分析
Step 3 (Listing Agent): 参考分析中的 Top 3 竞品，为我的产品生成差异化 Listing
Step 4 (图片 Agent): 基于 Listing 卖点生成一套 7 张商品图
Step 5 (视频 Agent): 用商品主图生成一段 15 秒带货口播视频
```

### 竞品情报

```
Step 1 (default): 查询 ASIN B0XXX 的 Keepa 历史数据和 SIF 关键词
Step 2 (市场分析 Agent): 对该 ASIN 所在品类做竞品格局分析
Step 3 (选品 Agent): 基于竞品分析，找该品类的差异化切入机会
```
