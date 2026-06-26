# MCP Server 接口设计准则

> 基于麦当劳中国 MCP Server 和高德地图 MCP Server 的实践分析，总结 MCP 接口设计与传统微服务 API 的核心差异和设计要点。

## 参考案例

| 案例 | 说明 | 链接 |
|------|------|------|
| 麦当劳中国 MCP | 18 个工具，覆盖外卖点单、优惠券、积分商城 | [open.mcd.cn/mcp/doc](https://open.mcd.cn/mcp/doc)　·　[GitHub](https://github.com/M-China/mcd-mcp-server) |
| 高德地图 MCP（官方） | 12+ 能力，地理编码、路线规划、POI 搜索 | [lbs.amap.com/api/mcp-server/summary](https://lbs.amap.com/api/mcp-server/summary) |
| 高德地图 MCP（社区） | 15 个工具，支持 stdio/sse/streamable-http | [GitHub - sugarforever/amap-mcp-server](https://github.com/sugarforever/amap-mcp-server) |

---

## 一、核心认知：MCP Tool ≠ REST API

MCP Server 的消费者是 LLM，不是前端代码。这一根本差异决定了接口设计的所有取舍。

| 维度 | 微服务 REST API | MCP Server Tool |
|------|----------------|-----------------|
| **消费者** | 前端 / 其他服务（确定性代码） | LLM（概率性推理） |
| **路由** | URL path + HTTP method | LLM 根据 tool name + description **自主选择** |
| **参数来源** | 前端表单 / 代码硬编码 | LLM 从**对话上下文**中提取 |
| **响应消费** | 代码解析 JSON 取字段 | LLM 需要**理解并转述**给用户 |
| **调用编排** | 业务代码显式调用链 | LLM **自主决定**调用顺序和组合 |
| **鉴权** | 每个 API 各自处理签名 | Token / Key 在传输层统一解决，tool 层不涉及 |
| **文档受众** | 给人看 | 给 LLM 看——description **就是路由规则** |

---

## 二、Tool 命名

### 2.1 加命名空间前缀

MCP 客户端可同时连接多个 Server，tool name 全局共享。不加前缀极易冲突。

| 案例 | 做法 |
|------|------|
| 高德 | 所有工具加 `maps_` 前缀：`maps_geo`, `maps_text_search` |
| 麦当劳 | 业务域前缀：`delivery-*`, `mall-*`, `query-*` |

### 2.2 动词优先，表达意图

`create-order` > `order-creation`；`calculate-price` > `price-calculator`

### 2.3 保持风格一致

- 高德统一 snake_case：`maps_direction_walking_by_address`
- 麦当劳统一 kebab-case：`delivery-query-addresses`

**不要混用。**

---

## 三、Tool Description——最关键的设计差异

Description 是 LLM 选择工具的唯一依据。写得好不好，直接决定工具能不能被正确调用。

### 3.1 结构公式

```
第一句：这个工具做什么（事实描述）
第二句：什么场景下应该用它（LLM 路由提示）
第三句（可选）：用户可能怎么说（自然语言触发短语）
```

**麦当劳实例：**

```python
# list-nutrition-foods
"获取麦当劳常见餐品的营养成分数据，包括能量、蛋白质、脂肪、碳水化合物、钠、钙等信息。"
"当用户咨询麦当劳餐品的热量、营养，或需要帮助用户搭配指定热量套餐时使用此工具。"

# auto-bind-coupons
"自动领取麦麦省所有当前可用的麦当劳优惠券。"
"无需指定具体的优惠券和couponId，系统会自动领取用户可领的所有券。"
"当用户说'帮我领券'、'自动领取优惠券'、'一键领券'时使用此工具。"
```

### 3.2 关键技巧

| 技巧 | 说明 | 示例 |
|------|------|------|
| **嵌入触发短语** | 把用户可能说的话写进 description | `当用户说"帮我领券"时使用此工具` |
| **声明"不需要什么"** | 减少 LLM 在参数上的犹豫 | `无需指定couponId，系统自动领取` |
| **标注数据来源** | 在参数描述中注明值从哪个 tool 获取 | `storeCode: 从 delivery-query-addresses 获取` |
| **引导优先级** | 多个变体时引导 LLM 选更合适的 | 高德：`推荐使用此工具而非坐标版本` |
| **说明不做什么** | 避免 LLM 对工具能力过度假设 | `不包含积分兑换的实物或第三方码` |

---

## 四、参数设计

### 4.1 极简参数——能推断的不要让 LLM 传

麦当劳 18 个工具中 **10 个零参数**，用户身份从 Bearer token 推断。高德大部分工具只需 1-4 个 string 参数。

```
微服务思维：member_query(member_id, fields[], include_history, page, page_size)
MCP 思维：  member_query()  ← 从 token 知道是谁，返回常用字段即可
```

**原则：每多一个参数，LLM 填错的概率就增加一分。**

### 4.2 扁平结构，避免嵌套

LLM 构造嵌套 JSON 容易出错。尽量用 string 类型的扁平参数。

```python
# 高德：坐标用一个 string，不拆成 lat/lng 两个 float
def maps_regeocode(location: str):  # "116.481028,39.989643"

# 反例：
def maps_regeocode(longitude: float, latitude: float):  # LLM 容易搞反
```

必须嵌套时（如购物车 items），保持结构尽量简单，字段不超过 4-5 个。

### 4.3 参数描述里写"从哪来"

```python
storeCode: str  # 门店编码，从 delivery-query-addresses 返回结果中获取
beCode: str     # BE编码，从 delivery-query-addresses 返回结果中获取
```

这相当于给 LLM 画了一条调用链路线图，不需要额外文档。

### 4.4 提供高低层级变体

高德的做法：

```python
# 高层级——接受地址文本，内部自动 geocode（推荐）
maps_direction_walking_by_address(origin_address, destination_address)

# 低层级——接受坐标，精确控制
maps_direction_walking_by_coordinates(origin, destination)
```

高层级工具内部组合低层级工具，减少 LLM 需要串联的步骤数。Description 中引导 LLM 优先用高层级版本。

---

## 五、响应格式

### 5.1 两种流派

| 流派 | 代表 | 做法 | 适用场景 |
|------|------|------|---------|
| **结构化 JSON** | 高德 | 返回 dict，LLM 自己组织展示 | 数据型工具、需二次计算 |
| **格式化 Markdown** | 麦当劳（部分工具） | 返回排版好的 markdown | 展示型工具、券列表、活动日历 |

两种都可以，也可以混用。关键原则见下。

### 5.2 裁剪字段，不透传后端全量响应

高德 POI 搜索后端返回 20+ 字段，MCP 工具只返回 `id`, `name`, `address`, `typecode` 四个。

**每多返回一个无用字段，就多消耗 LLM 的 token 和注意力。**

### 5.3 大数据量用紧凑格式

麦当劳营养数据用类 TSV 格式而非 JSON，节省 token：

```
[1]{productName,energyKj,energyKcal,protein,fat,carbohydrate,sodium,calcium}:
  猪柳麦满分,1288,308,16,16,24,781,213
  麦辣鸡腿堡,2344,560,24,30,46,1125,null
```

### 5.4 错误响应统一格式

```json
{"error": "Geocoding failed: INVALID_USER_KEY"}
```

不要让 LLM 猜错误结构。统一用同一个 key（如 `error`）返回错误信息。

### 5.5 单位和格式一致

麦当劳部分工具返回"分"，部分返回"元"——这是**反面教材**。应在所有工具中统一单位，或在返回值中显式标注。

### 5.6 敏感信息脱敏

手机号返回 `152****6666`，不暴露全量。MCP 响应可能直接展示给用户或经过 LLM 转述，脱敏是必须的。

---

## 六、调用链与编排

### 6.1 微服务 vs MCP 的编排差异

```
微服务：前端代码 → getAddress() → getMenu(storeCode) → calculatePrice(items) → createOrder(...)
         ↑ 代码控制每一步

MCP：   LLM 读 description → 自己决定先调 query-addresses → 再调 query-meals → ...
         ↑ LLM 自主推理调用顺序
```

### 6.2 List → Detail 渐进式披露

先返回列表（少量字段 + ID），LLM 按需再用 ID 查详情：

| List 工具 | Detail 工具 |
|-----------|-------------|
| `query-meals` → 返回 code + name + price | `query-meal-detail` → 返回套餐组成、默认选择 |
| `mall-points-products` → 返回 spuId + name + 积分 | `mall-product-detail` → 返回图片、有效期、说明 |

### 6.3 写操作前置确认步骤

麦当劳的 `calculate-price` 和 `create-order` 接受相同的参数结构。流程是：

```
calculate-price(items) → 展示价格给用户确认 → create-order(items) → 完成下单
```

**不要让一个 tool 同时算价和下单。** 给用户确认的机会。

### 6.4 工具内部可以组合

高德的 `maps_bicycling_by_address` 内部调用 `maps_geo()` 做地理编码，再调用坐标版路线规划。LLM 只需调一次，不用手动串两步。

**原则：能在 Server 内部编排的，就不要让 LLM 来编排。LLM 串的步骤越多，出错概率越高。**

---

## 七、安全与运维

| 准则 | 说明 |
|------|------|
| **鉴权在传输层** | Bearer token / API key 在 MCP 连接层处理，tool 不暴露 auth 参数 |
| **工具分级** | L0（公开只读）→ L3（高危写入），写操作加频率限制 |
| **频率限制** | 麦当劳 600 次/分钟/token；超限返回 429 |
| **幂等性** | 领券、下单等写操作要幂等——LLM 可能因超时重试 |
| **时间感知** | LLM 不知道当前时间，麦当劳专门提供 `now-time-info` 工具 |
| **错误码精简** | 不需要微服务那么多错误码，401 / 429 + 业务错误文案够用 |
| **响应脱敏** | 手机号、地址等 PII 数据在 tool 响应中脱敏 |

---

## 八、设计 Checklist

设计一个新的 MCP Tool 之前，逐条检查：

- [ ] **Description** 写了"做什么" + "什么时候用" + "用户怎么说"？
- [ ] **参数**能从 token / 上下文推断的都去掉了？
- [ ] **参数描述**标注了"值从哪个 tool 获取"？
- [ ] **响应**裁剪到只剩 LLM 需要的字段？
- [ ] 有没有提供**高层级便捷变体**（减少 LLM 编排步骤）？
- [ ] **写操作**前有确认 / 预览步骤？
- [ ] Tool name 加了**命名空间前缀**？
- [ ] 大数据量返回用了**紧凑格式**？
- [ ] **错误格式**和其他工具一致？
- [ ] 敏感信息做了**脱敏**？

---

## 参考链接

- [麦当劳中国 MCP 平台](https://open.mcd.cn/mcp) — 官方文档与接入指南
- [麦当劳中国 MCP Server GitHub](https://github.com/M-China/mcd-mcp-server) — 接入文档、工具列表、参数说明
- [高德地图 MCP Server 概述](https://lbs.amap.com/api/mcp-server/summary) — 官方能力说明
- [高德地图 MCP Server GitHub（社区版）](https://github.com/sugarforever/amap-mcp-server) — 完整源码，15 个工具实现
- [MCP 协议规范](https://spec.modelcontextprotocol.io/) — Model Context Protocol 官方规范
