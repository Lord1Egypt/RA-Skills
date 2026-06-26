# Routing Spec

## 1. Intent Routing
当前 market 模块的主要意图路由规则如下：

| User Intent | Route Intent |
|---|---|
| 价格 / 行情 / 最新价 / quote | `snapshot` |
| K线 / 日K / 周K / 月K / 分钟K / kline | `kline` |
| 分时 / 走势（非 K 线语境） | `intraday` |
| 盘口 / 摆盘 / 买卖盘 / orderbook | `orderbook` |
| 资金流向 / 主力资金 / flow | `capital_flow` |
| 市场状态 / 开盘 / 收盘 / state | `market_state` |
| 基础信息 / 上市日期 / 每手 / 退市 / basic | `basicinfo` |

## 2. Symbol Resolution Priority
标的识别优先级如下：

1. **标准代码优先**
   - 例如：`HK-00700`、`US-AAPL`
2. **裸代码**
   - 例如：`00700` → `HK-00700`
   - 例如：`AAPL` → `US-AAPL`
3. **本地名称映射**
   - 例如：`腾讯` → `HK-00700`
   - 例如：`苹果` → `US-AAPL`
4. **中文整句清洗后再尝试归一化**
   - 去掉“看 / 查询 / 最近 / K线 / 资金流向 / 走势”等修饰词后，再尝试识别

## 3. Current Local Name Hints
当前已内置的常见名称映射包括：
- 腾讯 / 腾讯控股 → `HK-00700`
- 苹果 / APPLE → `US-AAPL`
- 英伟达 / NVIDIA → `US-NVDA`
- 特斯拉 / TESLA → `US-TSLA`

说明：
- 当前仍以本地 hint 为主
- 尚未接入正式证券搜索 / 匹配接口

## 4. HK / US Ambiguity Clarification
当前已支持的高频双市场中文名称包括：
- 阿里 / 阿里巴巴
- 百度
- 京东
- 哔哩哔哩
- 蔚来
- 小鹏
- 理想

处理规则：
- 若用户已明确说“港股” / “美股”，直接路由到对应标的
- 若用户已输入 `HK-` / `US-` 标准代码，也直接路由
- 若名称存在双市场歧义且用户未明确市场，则先进入澄清态

## 5. Clarification Output Rule
进入澄清态时，返回的用户态提示应满足：
- 说明该名称同时存在港股和美股
- 列出可选项
- 支持用户直接回复“港股”或“美股”

示例：
- “百度”同时存在港股和美股，请先确认你要查哪个市场：
  1. 港股 百度（HK-09888）
  2. 美股 百度（US-BIDU）
  你直接回复“港股”或“美股”就行。

## 6. Detail Mode Trigger
当用户明确表达以下意图时，进入 detail mode：
- 最近几条
- 明细
- 逐条
- 列出来

当前 detail mode 已支持：
- K线
- 分时
- 资金流向

## 7. Kline Period Mapping
K线周期映射规则如下：

| User Expression | ktype |
|---|---|
| 日K | `K_DAY` |
| 周K | `K_WEEK` |
| 月K | `K_MON` |
| 5分钟K | `K_5_M` |
| 15分钟K | `K_15_M` |
| 30分钟K | `K_30_M` |
| 60分钟K | `K_60_M` |

## 8. Count Extraction
当前会尝试从自然语言中提取数量，例如：
- `最近10根日K` → `num=10`
- `最近5条资金流向` → `num=5`

说明：
- 路由层可识别请求数量
- 但后端实际返回条数不一定严格等于请求值

## 9. Known Routing Limits
当前已知限制包括：
- 名称解析仍以本地映射为主，不是真正的搜索接口
- 某些中文名称尚未加入映射表
- 路由正确不代表后端一定有数据返回
- 某些市场 / 标的 / 周期组合在当前环境可能直接返回 404

## 10. Relationship with Output Policy
路由层负责：
- 识别意图
- 解析标的
- 判断是否需要澄清
- 判断是否进入 detail mode

输出层负责：
- 摘要还是明细展示
- 话术风格
- 错误提示产品化
- detail mode 的展示条数限制
