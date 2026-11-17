# 地图 MCP 调用与数据映射指南（map_mcp_guide.md）

本文件指导 Skill 在**已连接地图 MCP**（如腾讯地图 MCP / `tencent-map`）时，如何采集
「人流量测量、商圈价值、竞品分布、消费水平、商业密度」数据，并将其映射进分析引擎
（`roi_calculator.py`）与报告生成器（`report_generator.py`）的输入 schema。

> ⚠️ 地图 MCP 不直接提供"实时人头计数"。它提供 **结构化空间代理指标**
> （POI 密度、业态构成、路网可达性、空间关系），是客流潜力的强代理；
> 真实客流还需结合**现场人工计数**或第三方移动大数据补充。Skill 必须如实区分二者。

---

## 一、前置条件：确认 MCP 已连接

- 在连接器面板确认 `tencent-map`（或等效地图 MCP）状态为 **connected**。
- 若未连接：跳过本章，按 SKILL.md「降级策略」用人工估算/待补，并在报告中标注
  `⚠️ 未接入地图 MCP`。

> 不同地图 MCP 暴露的工具名不同（如 `mcp__tencent-map__around_search`、
> `mcp__tencent-map__place_search`、`mcp__tencent-map__geocoder` 等）。
> 请以你环境中**实际可用的工具名**为准；下表为能力映射，非强制命名。

---

## 二、能力 → 工具 → 输出映射

| 采集目标 | 推荐 MCP 能力 | 关键输出 | 映射到 |
| :--- | :--- | :--- | :--- |
| 地址→坐标 | 地理编码 geocoder | `lng, lat` | `location.longitude / latitude` |
| 竞品分布 | 周边搜索 around_search（关键词=竞品品牌/品类） | POI 列表（名/距/规模） | `competition[]` + `map_data.competitor_pois` |
| 业态构成 | 周边搜索（全品类计数） | POI 分业态计数 | `map_data.poi_counts` → 商业密度/消费水平 |
| 可达性 | 步行/驾车路线规划 | 最近地铁/公交距离、步行分钟 | `map_data.accessibility` |
| 商圈边界 | 行政区划 district / Buffer | 商圈类型判定 | `map_data.trade_area_type` |
| 坐标→地址 | 逆地理编码 reverse_geocoder | 周边描述（辅助核验） | 报告备注 |

---

## 三、采集流程（伪代码）

```
1) 地理编码：geocoder(address) → {lng, lat}
   写入 location.longitude / latitude

2) 竞品周边搜索：around_search(center={lng,lat}, radius=500, keyword="餐饮"/竞品品牌)
   → 取 Top-N 竞品，映射为 competition[]:
       {name, distance_m, scale_sqm}
   （scale_sqm 可由 POI 类型/面积字段估算，缺省按本店面积）
   → 同时写入 map_data.competitor_pois 供报告展示

3) 全业态计数：around_search(center, radius=500) 全品类
   → 统计 poi_counts（餐饮/茶饮/零售/写字楼/商场…）
   → 据此判定 commercial_density（见 benchmarks.md 十一）
     与 consumption_level（见 benchmarks.md 十）

4) 可达性：walking_route(center → 最近地铁站/公交站)
   → accessibility.{nearest_metro_m, walk_min}

5) 商圈类型：结合 district + poi_counts 主导业态
   → trade_area_type ∈ {商圈型/办公型/社区型/校园型/交通枢纽型/旅游型}

6) 地图链接（可选）：构造卫星/街景核验链接写入 map_links
```

---

## 四、map_data schema（传入 report_generator --map-json）

```json
{
  "geocoded": {"lng": 121.4737, "lat": 31.2304},
  "accessibility": {"nearest_metro_m": 180, "walk_min": 3},
  "consumption_level": "Medium",
  "commercial_density": "High",
  "competition_intensity": "High",
  "trade_area_type": "商圈型",
  "poi_counts": {"餐饮": 142, "茶饮咖啡": 38, "零售": 96, "写字楼": 22, "商场": 5},
  "competitor_pois": [
    {"name": "竞品A·奶茶", "distance_m": 50, "scale_sqm": 150}
  ],
  "map_links": {"satellite": "https://...", "street": "https://..."}
}
```

> `competition_intensity` 若未显式给出，report_generator 会由分析引擎的
> `total_diversion_rate` 反推（<0.15 Low / <0.4 Medium / 否则 High）。

---

## 五、降级策略（MCP 未连接）

1. 提示用户：本点位需补充（a）现场分时段人流计数；（b）周边竞品清单与距离；
   （c）商圈类型与消费能级判断。
2. 由用户提供自然语言，抽取为 JSON 后照常调用 `roi_calculator.py`。
3. `map_data` 留空，报告第二节自动标注 `⚠️ 未接入地图 MCP，以下为人工估算/待补`。
4. 必须在报告中区分"地图结构化数据"与"人工估算"，不得混淆置信度。

---

## 六、安全与数据流（出境前 opt-in / 数据最小化）

地图 MCP 是**本 Skill 唯一的外部数据出境通道**。采集前必须遵循以下安全红线：

1. **出境前显式 opt-in**：首次调用任何地图 MCP 工具前，必须向用户说明
   "将把该铺位地址/坐标发送至地图服务商"并显式征得同意。用户拒绝则按第五节降级，
   **绝不静默外发**，不得用"已读默认同意"等话术绕过。
2. **数据最小化（仅位置出境）**：

   | 数据 | 是否发送至地图服务商 | 说明 |
   | :--- | :--- | :--- |
   | `location.address` | ✅ 是 | 地理编码所需 |
   | `location.longitude/latitude` | ✅ 是 | 周边搜索/可达性所需 |
   | `financials`（租金/装修/客单…） | ❌ 否 | 仅本地财务测算 |
   | `red_flags`（消防/产权…） | ❌ 否 | 仅本地合规判定 |
   | `category`（拟选品类） | ❌ 否 | 仅本地品类推荐 |
   | 地图返回的 POI/可达性数据 | ❌ 否（不出境） | 仅本地分析与报告 |

   即：地图 MCP 收到的请求参数**仅限地址/坐标**；任何商业、财务、合规上下文都不进入
   请求体。地图返回的数据也只用于本地分析，不回传任何第三方。
3. **宽泛触发不自动出境**：命中"选址/人流量/竞品"等宽泛关键词仅用于启动对话与本地分析，
   不会在取得 opt-in 前自动外发位置。
4. **无隐藏外泄**：调用地图 MCP 之外，本 Skill 不通过任何方式联网或上传用户文件；脚本仅
   用 Python 标准库，无 `urllib/requests/socket/subprocess/eval/exec` 等代码。

> 与 SKILL.md「安全与合规」章节保持一致：最小化出境 + 显式 opt-in + 纯本地降级。

---

## 七、数据质量红线

- 竞品距离必须来自 MCP 实测或现场测距，**禁止凭印象编造**。
- 消费水平判定需有业态/租金 proxy 支撑，单点样本不代表性。
- 任何来自 MCP 的数值，在报告中保留原始口径（如"500m Buffer 内 POI 计数"）。
