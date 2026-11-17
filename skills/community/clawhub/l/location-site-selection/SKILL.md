---
name: restaurant-site-selection-roi
display_name: 餐饮选址决策与ROI分析系统
description: |
  资深商业地产数据分析师视角的餐饮商铺量化评估与决策工具。融合 Reilly 零售引力定律、
  Hotelling 区位模型、TQI 客流质量指数与 GIS 逻辑，并深度调用地图 MCP（如腾讯地图 MCP）
  采集人流量代理、竞品分布、消费水平与商业密度，输出数据驱动的品类选址建议，
  以及面向决策人的专业 Markdown 报告（含可视化）。
  当用户提及"商铺评估"、"开店测算"、"选址"、"雷利定律"、"商圈吸客力"、"投资回报"、
  "Reilly"、"Hotelling"、"GIS"、"断裂点"、"客流质量"、"地图"、"人流量"、"竞品分布"、
  "消费水平"、"商业密度"、"品类选择"、"选址决策报告"等关键词时触发。
  基于结构化 JSON（位置/客流/竞争/财务 + 可选地图MCP采集），调用 scripts 下引擎输出：
  商圈断裂点与捕获面积、TQI 修正有效客流、三情景财务预测与回本周期置信区间、
  数据驱动的品类推荐排序，以及谈判筹码。内置消防/排烟/产权一票否决（Red Flag）。
version: 3.0.0
agent_created: true
author: WorkBuddy
tags:
  - 餐饮选址
  - 零售选址
  - 地图MCP
  - 人流量测量
  - 商圈价值
  - Reilly定律
  - Hotelling模型
  - GIS商圈分析
  - ROI测算
  - 品类推荐
  - 决策报告
  - 雷利定律
  - 断点分析
---

# 餐饮选址决策与 ROI 分析系统 v3.0.0

## 角色设定

以「资深商业地产数据分析师」身份执行。不输出"感觉"，而是基于人口统计学与空间经济学的
**置信区间**做量化评估。核心工具：Reilly's Law（雷利零售引力定律）、Hotelling's Location
Model（霍特林区位模型）、TQI（Traffic Quality Index 客流质量指数）与 GIS 逻辑
（Buffer Zone、Network Analysis、Catchment Area）。

**v3.0 新增能力**：深度联动地图 MCP 采集结构化空间数据（人流量代理 / 竞品分布 / 消费水平 /
商业密度），并基于数据给出**餐饮品类选址建议**与**决策人级 Markdown 报告**。

## 适用场景（触发条件）

用户提出以下任意意图时激活：

- 评估某餐饮铺位的商圈吸客力与断裂点（Reilly）
- 量化客流质量（可视性衰减 + 物理阻抗）并预测翻台/客单
- 基于竞品距离与规模测算分流率（Hotelling）
- 输出三情景（乐观/中性/悲观）财务预测与回本周期置信区间
- **测量目标区域人流量 / 商业密度（调用地图 MCP）**
- **评估周边商圈价值：竞品分布、消费水平、商业密度**
- **基于数据给出餐饮品类选择建议**
- 需要带 GIS 术语的专业决策报告与租约谈判筹码
- 存在消防/排烟/产权硬伤时的"一票否决"判定

## 使用指南

### 1. 功能说明

本 Skill 面向餐饮 / 零售商铺选址决策，提供以下能力：

- **地图 MCP 数据采集**：调用已连接的地图 MCP（如腾讯地图 MCP）测量目标区域人流量代理、竞品分布、消费水平、商业密度与路网可达性（详见 `references/map_mcp_guide.md`）。
- **Reilly 零售引力定律**：计算断裂点（Breaking Point）与核心商圈半径、有效捕获面积（Catchment Area）。
- **TQI 客流质量指数**：可视衰减 × 物理阻抗，将"通过人流"折算为"进店人流"。
- **Hotelling 区位模型**：基于竞品距离与规模测算分流率，量化竞争影响。
- **三情景财务 + 置信区间**：乐观 / 中性 / 悲观营收与回本周期，输出风险等级。
- **数据驱动品类推荐**：基于商圈类型 / 消费水平 / 商业密度 / 竞争强度 / TQI / 合规硬伤，给出餐饮品类评分排序与回避清单。
- **决策人 Markdown 报告**：七节结构化报告（含客流漏斗、回本区间等 ASCII 可视化与行动清单）。
- **Red Flag 一票否决**：命中消防 / 排烟 / 产权 / 排污硬伤直接终止。

### 2. 使用方法

**方式一 · 对话触发（推荐）**
直接对 AI 描述选址需求，例如："帮我评估 XX 路这个铺位，做茶饮合不合适？""测量一下这个商圈的竞品分布和人流量"。命中关键词（选址 / 雷利定律 / 商圈吸客力 / 置信区间 / 人流量 / 品类选择 / 选址决策报告 等）即触发；AI 会引导补全信息并自动跑完工作流，最终输出 Markdown 决策报告。

**方式二 · 本地脚本直跑（可选，便于批处理 / 二次开发）**

```bash
# 1) 量化分析（Reilly / TQI / Hotelling / 三情景）
python scripts/roi_calculator.py --json input.json      # 自定义输入
python scripts/roi_calculator.py --demo                 # 内置示例

# 2) 品类推荐
python scripts/category_recommender.py --json feats.json
python scripts/category_recommender.py --demo

# 3) 生成决策人 Markdown 报告（整合 1+2 + 可选地图数据）
python scripts/report_generator.py --json input.json --map-json map_data.json --out report.md
python scripts/report_generator.py --demo --map-json examples/demo_map_data.json --out examples/decision_report_demo.md
```

> 脚本仅依赖 Python **标准库**（argparse / json / math / re / datetime / os / sys），**无需任何第三方包**，Python 3.8+ 即可运行。

**地图 MCP 前置**：若要用到真实空间数据，请先在连接器面板将 `tencent-map`（或等效地图 MCP）状态置为 **connected**；未连接时按降级策略以人工估算推进，并在报告中明确标注。

### 3. 参数描述（输入 JSON）

以下为 `roi_calculator.py` 的输入 schema，缺失项由 `references/benchmarks.md` 基准估算（`*` 为可选）：

| 字段路径 | 类型 | 必填 | 说明 | 示例 / 缺省 |
| :--- | :--- | :--- | :--- | :--- |
| `project` | string | 是 | 项目名（报告标题用） | `"新店001"` |
| `category` | string | * | 品类，决定捕获率基准（正餐/快餐/茶饮/火锅/烘焙…） | `"正餐"` |
| `location.address` | string | * | 地址（供地图 MCP 地理编码） | `"XX路XX号"` |
| `location.longitude` / `latitude` | number | * | 经纬度（有则跳过地理编码） | `121.47 / 31.23` |
| `location.scale_sqm` | number | 是 | 本店营业面积，作为 Reilly 吸引力 Sa | `150` |
| `location.visibility_angle` | number | * | 门头可视角度（度），决定可视衰减 | `45`（缺省 90） |
| `location.foot_traffic.weekday_noon` | number | 是 | 工作日午市过点人流 | `2500` |
| `location.foot_traffic.weekday_night` | number | 是 | 工作日晚市过点人流 | `800` |
| `location.foot_traffic.weekend_avg` | number | 是 | 周末平均过点人流 | `1800` |
| `impedance` | array | * | 物理阻抗标签：`step`/`median`/`low_ceiling`/`pillar`/`bad_parking` | `["step"]` |
| `competition[].name` | string | 是 | 竞品名 | `"竞品A"` |
| `competition[].distance_m` | number | 是 | 本店与竞品间距（米） | `50` |
| `competition[].scale_sqm` | number | * | 竞品面积（吸引力 Sb） | `150`（缺省同本店） |
| `financials.rent_monthly` | number | 是 | 月租金 | `50000` |
| `financials.deposit_terms` | string | 是 | 押付条款，解析为 首期租金 = 月租×(押+付) | `"3押1付"` |
| `financials.renovation_cost` | number | 是 | 装修设备投入 | `300000` |
| `financials.transfer_fee` | number | * | 转让费 | `0` |
| `financials.avg_check` | number | 是 | 客单价 | `45` |
| `financials.cogs_ratio` | number | 是 | 食材成本率 | `0.35` |
| `financials.opex_ratio` | number | 是 | 运营费用率（占营收） | `0.25` |
| `red_flags` | array | * | 合规硬伤：`no_fume`/`no_vent`/`fire_hazard`/`no_sewage`/`unknow_title` 等 | `[]` |

完整 JSON 示例：

```json
{
  "project": "新店001",
  "category": "正餐",
  "location": {
    "address": "XX路XX号",
    "longitude": 121.47, "latitude": 31.23,
    "scale_sqm": 150,
    "visibility_angle": 45,
    "foot_traffic": {"weekday_noon": 2500, "weekday_night": 800, "weekend_avg": 1800}
  },
  "impedance": ["step"],
  "competition": [{"name": "竞品A", "distance_m": 50, "scale_sqm": 150}],
  "financials": {
    "rent_monthly": 50000, "deposit_terms": "3押1付", "renovation_cost": 300000,
    "transfer_fee": 0, "avg_check": 45, "cogs_ratio": 0.35, "opex_ratio": 0.25
  },
  "red_flags": []
}
```

`category_recommender.py` 另需商圈特征（`trade_area_type` / `consumption_level` / `commercial_density` / `competition_intensity` / `tqi` / `red_flags`），通常由 `report_generator.py` 从地图数据与分析结果自动推导，亦可由 `map_data.json` 直接提供（schema 见 `references/map_mcp_guide.md`）。

### 4. 注意事项

- **地图数据是代理，不是实时人流**：地图 MCP 提供 POI 密度、业态构成、路网可达性等*空间代理指标*，是客流潜力的强信号；真实客流仍需现场分时段人工计数或第三方移动大数据补充。二者在报告中须明确区分。
- **置信区间非收益承诺**：三情景回本区间为数据推演，不代表确定结果；悲观情景受"竞争分流 50% 半实现"假设影响。
- **Red Flag 一票否决**：命中消防 / 排烟 / 产权 / 排污硬伤，系统直接终止评估，不进入乐观叙事。
- **竞争距离禁编造**：竞品距离须来自地图 MCP 实测或现场测距，不得凭印象虚构。
- **数据来源透明度**：未接入地图 MCP 时，商圈价值相关结论标注"人工估算/待补"，不混入地图结构化数据的置信度。
- **地图数据出境必须 opt-in**：调用地图 MCP 前须向用户明确说明"将把铺位地址/坐标发送至地图服务商"并征得同意；用户拒绝则纯本地降级，绝不静默外发。且仅地址/经纬度出境，财务与合规数据一律本地处理（详见「安全与合规」与 `references/map_mcp_guide.md` 第六节）。
- **发布前替换作者**：`SKILL.md` 的 `author` 字段当前为 `WorkBuddy`，对外发布前请改为你的品牌。
- **环境要求**：脚本仅依赖 Python 标准库；地图 MCP 采集需对应 MCP 已连接。

## 核心工作流（Workflow）

### Stage 0 · 地图 MCP 数据采集（v3.0 新增 · 人流量/商圈价值）

> ⚠️ **出境前必须显式 opt-in（安全红线）**：地图 MCP 是外部服务，调用会把目标
> **位置信息（地址 / 经纬度）** 发送给地图服务商。在首次调用任何地图 MCP 工具前，
> **必须向用户明确说明"将把该铺位地址/坐标发送至地图服务商"并征得同意**；用户拒绝则
> 直接进入纯本地降级模式（见下方"未连接 / 拒绝"分支），**不得静默外发**。
> 详见「安全与合规」章节与 `references/map_mcp_guide.md` 第六节。

若环境已连接地图 MCP（如 `tencent-map`）**且用户已 opt-in**，按
`references/map_mcp_guide.md` 的能力→工具→输出映射执行：

1. **地理编码**：地址 → 经纬度，写入 `location.longitude/latitude`。
2. **人流量测量（代理）**：地图 MCP 不直接计数人头，但提供强代理——
   - 周边 POI 密度与业态构成（商业密度、消费水平推断）；
   - 路网可达性（步行/驾车到地铁、公交、小区）。
   同时**要求用户补充现场分时段人工计数**（午市/晚市/周末），填入 `location.foot_traffic`。
3. **竞品分布**：周边搜索（关键词=竞品品牌/品类，半径 500m）→ 映射为 `competition[]`
   （`name / distance_m / scale_sqm`），并保留 `map_data.competitor_pois` 供报告展示。
4. **消费水平 & 商业密度**：由 POI 分业态计数推断（阈值见 `references/benchmarks.md`
   第十/十一节），写入 `map_data.consumption_level / commercial_density / trade_area_type`。
5. **可达性**：步行路线规划 → `map_data.accessibility`。

> **数据最小化**：仅 `location.address` / 经纬度会被发送至地图服务商；
> `financials`（租金/装修/客单等）、`red_flags`、`category` 等**商业与合规数据一律
> 只在本地参与计算，绝不外发**。

> 未连接地图 MCP **或用户拒绝 opt-in** 时：跳过本阶段，提示用户补充人工数据，并在报告中标注
> `⚠️ 未接入地图 MCP / 未授权外发，以下为人工估算/待补`（降级策略见 map_mcp_guide.md 第五节）。

### Stage 1 · Reilly's Law（雷利零售引力定律）→ 商圈分析
- 断裂点公式：`D_ab = d / (1 + √(S_b / S_a))`
  - `d` = 本店与竞品间距（m）；`S_a` = 本店吸引力（面积）；`S_b` = 竞品吸引力。
  - `D_ab` = 自本店起、顾客偏好从本店转向竞品的**断裂点距离（km）**。
- 核心商圈半径 = 各竞品断裂点的最小值（受最近强竞品约束）；无竞品时默认 1.5 km。
- 有效捕获面积（Catchment Area）= π × 半径²（km²）。

### Stage 2 · TQI（Traffic Quality Index，客流质量指数）
- 原始日客流（Network Analysis 折算）= `((午市+晚市)×5 + 周末×2)/7 × 日曝光放大系数(4)`。
- **可视衰减因子** `visibility_decay(angle)`：<30°→0.70；30–60°线性 0.70→1.00；≥60°→1.00。
- **阻抗因子** `impedance_factor`：台阶×0.85、隔离带×0.70、挑高低×0.90、柱头×0.92、停车难×0.85（乘性叠加）。
- `TQI = 可视衰减 × 阻抗`。**修正后有效日客流 = 原始日客流 × TQI**。
- 捕获率（Capture Rate）：按品类基准（快餐 3–5%、正餐 1–2%、茶饮 5–8% 等），中性用基准值，
  悲观按竞品分流潜力 50% 实现折减。**预计日翻台/客单 = 修正后有效日客流 × 捕获率**。

### Stage 3 · Hotelling 区位模型 → 竞争影响
- 单竞品分流率：距离<100m 且规模相当时 20–40%（本店规模大→下探 20%，竞品规模大→上探 40%）；
  100–300m 线性衰减至 5%；≥300m 视为 0。
- 综合分流率 = `1 − Π(1 − 单竞品分流率)`，上限 85%。

### Stage 4 · 财务建模 + 三情景
- 总投资 = 装修设备 + 首期租金(押+付) + 转让费。
- 贡献毛利率 `CM = 1 − cogs_ratio − opex_ratio`；月固定成本 = 月租（opex 已按营收比例计入变动）。
- 盈亏平衡点（月营收）= 月固定成本 / CM。
- 三情景营收：乐观 = 中性 ×1.2（客流+20%）；中性 = 修正客流×基准捕获×客单×30；
  悲观 = 修正客流×悲观捕获(含竞争分流)×客单×30。
- 月净利润 = 营收×CM − 月固定成本；**回本周期 = 总投资 / 月净利润**。
- **置信区间** = [悲观回本, 乐观回本] 月；风险等级：≤12 Low / ≤18 Medium / ≤24 Elevated / >24 High。

### Stage 5 · 品类选址建议（v3.0 新增 · 数据驱动）
调用 `scripts/category_recommender.py`，基于 `map_data` 中的商圈类型 / 消费水平 / 商业密度 /
竞争强度 + 分析引擎的 TQI + 合规硬伤，输出**餐饮品类评分排序**与回避清单：
- 评分 0–100，绿(推荐)≥70 / 黄(慎选)50–69 / 红(回避)<50。
- 核心逻辑（透明）：商圈适配 + 消费匹配 + 商业密度 − 竞争敏感度×竞争强度 ± 消费溢价 ± TQI − 合规硬伤。
- 冲动型低壁垒品类（茶饮/烘焙）对红海最敏感；高壁垒目的地品类（火锅/正餐）最抗竞争。

### 生成决策报告
调用 `scripts/report_generator.py --json input.json [--map-json map_data.json]`，
自动整合 Stage 1–5 结论，输出**面向餐饮选址决策人的 Markdown 报告**（详见下节）。

## 输出规范：决策人 Markdown 报告

严格输出以下 7 节（由 `report_generator.py` 生成，含 ASCII/表格可视化）：

### 一、决策摘要（一页结论）
- **综合裁定**：🔴红·终止 / 🔴红·高风险 / 🟡黄·条件推进 / 🟢绿·推进 + 一句话理由。
- **KPI 卡**：有效日客流、预计日翻台、总投资、中性回本、回本置信区间、首选品类。
- **核心结论** 3 条（商圈 / 客流 / 财务）。

### 二、地图数据勘察（商圈价值）
- 地理坐标、可达性（最近地铁/步行分钟）、消费水平、商业密度、商圈类型、业态构成（POI 计数）。
- 地图核验链接（卫星/街景）。未接入 MCP 时标注人工估算。

### 三、商圈与客流（Space & Traffic）
- Reilly 断裂点、有效捕获面积、TQI。
- **客流漏斗 ASCII**：原始日客流 → ×TQI → ×捕获率 → 日翻台。

### 四、竞争态势（Competition）
- 逐竞品表（距离/规模/断裂点/分流率）+ 综合分流率。

### 五、财务预测（Financial Projection）
- 三情景表（月营收/月净利润/回本周期）+ 回本区间 ASCII 条形（标注 12 月安全线、24 月警戒线）。

### 六、品类选址建议（Category Fit · 数据驱动）
- 首选品类 + 回避清单 + 评分排序表（含等级/壁垒/投资/依据）。
- 决策象限（消费水平 × 竞争强度 → 适配品类）。

### 七、行动清单（Action Plan）
- 🟢 立即推进 / 🟡 签约前条件（谈判筹码：租金下调%、免租天数）/ 🔴 否决项（Red Flag）。

## 约束（Constraints）

- 输出必须包含 **置信区间**，不得承诺确定性收益；明确"本结果仅为数据推演"。
- 必须使用 **GIS 术语**（Buffer Zone、Network Analysis、Catchment Area、断裂点等）。
- 若 `red_flags` 含消防/排烟/产权/排污硬伤 → 直接判定 **"Red Flag: Project Termination"**，
  输出强硬否决建议，不进入财务测算的乐观叙事。
- **数据来源透明度**：区分"地图 MCP 结构化数据"与"人工估算"，不得混淆置信度。
- 末尾标注：*本测算基于行业平均值、空间经济模型与地图结构化数据，具体经营结果取决于实际运营能力。*

## 安全与合规（Security & Compliance）

本 Skill 通过静态分析（无网络/子进程/eval/exec/文件外泄代码）与最小数据出境原则保障安全。
地图 MCP 是**唯一的外部数据出境通道**，对其使用受以下硬性约束：

1. **出境前显式 opt-in（不可静默外发）**：在首次调用任何地图 MCP 工具前，**必须主动向用户说明**
   "将把该铺位地址/坐标发送至地图服务商"并**显式征得同意**。用户拒绝则立即进入纯本地降级模式，
   不得绕过、不得静默补发、不得用"已读默认同意"等话术默认授权。
2. **数据最小化（Data Minimization）**：仅 `location.address` 与经纬度（地理编码所需）会被发送至
   地图服务商；`financials`（租金/装修/客单等）、`red_flags`（消防/产权等合规硬伤）、`category`
   （拟选品类）等**商业与合规敏感数据一律只在本地参与计算，绝不外发**。地图返回的空间代理数据
   （POI 密度/业态/可达性）亦仅用于本地分析，不回传任何第三方。
3. **纯本地降级模式**：未连接地图 MCP **或用户拒绝 opt-in** 时，跳过所有地图调用，改用人工估算
   推进，并在报告中明确标注 `⚠️ 未接入地图 MCP / 未授权外发，以下为人工估算/待补`，不混入地图
   数据的置信度。
4. **触发透明**：即使命中"选址/人流量/竞品"等宽泛关键词，也**不会**在取得 opt-in 前自动外发位置；
   宽泛触发只用于启动"本地分析 + 询问是否采集地图数据"的对话，而非直接出境。
5. **无隐藏行为**：所有脚本仅用 Python 标准库，无 `urllib/requests/socket/subprocess/eval/exec/
   __import__/open(https...)` 等任何联网或动态执行代码；本 Skill 不会写入、上传或外泄用户文件系统的
   其他数据。

> 完整数据流与最小化细则见 `references/map_mcp_guide.md` 第六节。

## 少样本示例（Few-Shot，引擎实算）

**Input**（Spec 内置示例 JSON）：新店001 / 正餐 / 可视角度 45° / 客流 2500·800·1800 /
竞品A 50m·150㎡ / 月租5万·3押1付·装修30万·客单45·COGS35%·OPEX25%。

**执行链**：
1. `python scripts/roi_calculator.py --demo` → 量化结论（断裂点/捕获面积/TQI/三情景）。
2. `python scripts/category_recommender.py --demo` → 品类排序。
3. `python scripts/report_generator.py --demo --map-json examples/demo_map_data.json`
   → 决策人 Markdown 报告（见 `examples/decision_report_demo.md`）。

**报告节选**：
```
【决策摘要】综合裁定：🔴 红·高风险（中性回本 17.2 月，风险 High）
  有效日客流 9,763 人 | 预计日翻台 146 单 | 总投资 ¥50.0万
  回本置信区间 29.0–11.1 月 | 首选品类：火锅（黄·慎选）

【客流漏斗】原始 11,486 → ×TQI 9,763 → ×捕获率 146 单/日
【回本区间】乐观11.1 ███ 中性17.2 █████ 悲观29.0 ████████(超24月警戒线)
【品类】饱和商圈中目的地品类(火锅/正餐)相对优于冲动红海(茶饮)，需差异化突围
【行动】租金下调10% + 45天免租期；排烟/产权硬伤一票否决
```

> 完整示例报告：`examples/decision_report_demo.md`（已随 Skill 附带，可由你直接审阅格式）。

## 参考资源

| 文档 | 内容 | 何时加载 |
| :--- | :--- | :--- |
| `references/benchmarks.md` | 可视衰减/阻抗映射、品类捕获率、Reilly/Hotelling 模型、消费水平/商业密度分级、商圈类型、品类推荐矩阵、押付解析、GIS 术语表、假设说明 | 每次测算引用基准与公式时 |
| `references/map_mcp_guide.md` | 地图 MCP 能力→工具→输出映射、map_data schema、降级策略、安全与数据流（出境opt-in/数据最小化）、数据质量红线 | 调用地图 MCP 采集数据时 |
| `scripts/roi_calculator.py` | 精确分析引擎（Reilly/TQI/Hotelling/三情景/置信区间/Red Flag） | 用户提交 JSON 后执行 |
| `scripts/category_recommender.py` | 数据驱动品类推荐引擎（评分矩阵/回避清单） | Stage 5 执行 |
| `scripts/report_generator.py` | 决策人级 Markdown 报告生成器（可视化/行动清单） | 最终输出报告 |

## 核心金句

1. 流量不等于生意——TQI 把"通过人流"折算成"进店人流"。
2. 断裂点告诉你：超出 X 米，顾客就归竞品了。
3. 没有置信区间的选址建议，都是伪科学。
4. 饱和商圈里，目的地品类比冲动红海更抗竞争——选品就是选护城河。
5. 消防/排烟/产权硬伤，再便宜也是雷——Red Flag，直接终止。
