---
name: migu-attraction-query
display_name: "咪咕旅游资源查询"
description: 咪咕旅游资源查询。查询城市或城市下某区县的景点列表，并进一步查询这些景点周边的酒店与美食。当用户询问“XX市有什么景点”“成都武侯区热门景点”“这些景点附近有什么酒店/好吃的”“景点周边住宿美食”等资源查询需求时使用。仅做景点/酒店/美食的资源检索，不生成行程规划。
metadata:
  openclaw:
    emoji: "🗺️"
    priority: 78
    intents:
      - attraction_query
      - poi_query
      - scenic_spot_list
      - nearby_hotel_food
      - 景点查询
      - 景点列表
      - 周边酒店
      - 周边美食
---

# 咪咕旅游资源查询

调用咪咕旅游资源接口，做两类查询：

1. **景点列表**：按城市（可选区县）查询最热门的景点。
2. **周边资源**：按景点名称列表查询其周边的酒店和美食。

## 接口约定

- 景点 Top：`POST https://gulangyu.migudm.cn/gallery/api/v1/attraction/top`
  - body：`{ "city": "成都市", "area": "武侯区", "top": 10 }`
  - `city` 必填；`area` 选填；`top` 选填，返回最热门的条数，不传默认 10。
- 景点周边：`POST https://gulangyu.migudm.cn/gallery/api/v1/attraction/nearby`
  - body：`{ "city": "成都市", "area": "武侯区", "names": ["成都武侯祠博物馆", "锦里古街"] }`
  - `city`、`area`、`names` 均必填；`names` 为景点名称数组。
- 请求方式为 **POST + JSON body**，并携带头部 `X-APP-From: 10`、`X-App-Version: 0.6.4`、`Origin`、`Referer`。
- 这两个接口**无需 Token 鉴权**，直接调用即可。

⚠️ **城市名要带行政区后缀**（如「成都市」「重庆市」「北京市」）。脚本会在缺少后缀时自动补「市」，但区县名（如「武侯区」「都江堰市」）需按接口数据原样传入。

## 运行

进入目录：

```powershell
cd C:\Users\ll\.openclaw\workspace\skills\migu-attraction-query
```

景点列表：

```powershell
node scripts\migu_attraction_client.mjs --action top --city 成都市 --limit 10 --json
# 限定区县：
node scripts\migu_attraction_client.mjs --action top --city 成都市 --area 武侯区 --limit 5 --json
```

景点周边酒店/美食：

```powershell
node scripts\migu_attraction_client.mjs --action nearby --city 成都市 --area 武侯区 --names "成都武侯祠博物馆,锦里古街" --json
```

参数：

- `--action`：`top` | `nearby`（必填）
- `--city`：城市（可省略“市”后缀，脚本自动补全）
- `--area`：区县（`top` 选填；`nearby` 必填）
- `--limit`：`top` 返回数量，默认 10
- `--names`：`nearby` 的景点名称，英文逗号分隔
- `--json`：输出原始 JSON（含 `data`）；不加时输出表格文本

## 使用流程

1. 用户要“某城市/某区县的景点” → 用 `--action top`（`area` 按需带上，`limit` 默认 10）。
2. 用户要“某景点附近的酒店/美食” → 先用 `--action top` 拿到景点名称与 `area`，再用 `--action nearby` 传入 `city`、`area` 和景点 `names`（都必须来自 top 查询结果，保证名称与区县匹配）。
3. 直接把脚本输出的表格/JSON 结果展示给用户；`--json` 的 `data` 字段是事实来源，不要编造。

## 输出规范

- `top` 返回景点数组，字段：`poiId`、`name`、`lng`/`lat`、`province`/`city`/`area`、`rating`、`tags`、`level`、`open`。
- `nearby` 返回以景点名称为键的对象，每个值含 `hotels[]` 与 `foods[]`；条目字段：`name`、`rating`、`price`、`distance`、`level`、`area` 等。
- 字段为空时展示「待定」或「暂无评分」，不要臆造价格、评分或距离。