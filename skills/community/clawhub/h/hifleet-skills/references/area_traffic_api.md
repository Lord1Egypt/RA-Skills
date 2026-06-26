# 区域船舶 API / Area Traffic API

查询指定区域内的当前船舶列表。**需配置 `api_key`。**

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 `HIFLEET_API_BASE`（无末尾 `/`）。见 [api_base.md](api_base.md)。

## 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/position/gettraffic/token` |
| 请求方式 | `GET` |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| api_key | (从配置读取) | 是 | string | 接口授权 `api_key` |
| bbox | 120,15,121,17 | 否 | string | 矩形区域：左下角经度、左下角纬度、右上角经度、右上角纬度（逗号分隔） |
| areaId | 52 | 否 | number | 区域 id，来自 [区域清单接口](areas_api.md) 返回的 list[].id |
| polygon | POLYGON((...)) | 否 | string | WKT 格式多边形，如 POLYGON((lon1 lat1,lon2 lat2,...)) |

**区域指定方式**：**bbox**、**areaId**、**polygon** 三选一。用户仅文字描述区域时，先调区域清单接口取 id 再传 areaId；用户提供任意多边形时传 polygon（WKT）。

## 成功响应

- `result`: "ok"
- `num`: 数量
- `list`: 船舶列表，每项字段见下

### list 单项字段说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| name | string | 船名 |
| lon | number | 经度（度） |
| lat | number | 纬度（度） |
| mmsi | string | MMSI |
| heading | string | 航艏向（度） |
| speed | string | 航速（节） |
| updatetime | string | 最后更新时间（UTC+8） |
| an | string | 船籍简称 |
| dn | string | 船籍中文 |
| eta | string | 预计抵港时间（UTC） |
| draught | string | 吃水（米） |
| destination | string | 目的港 |
| width | string | 船宽（米） |
| length | string | 船长（米） |
| type | string | 船舶类型 |
| minotype | string | 档案船舶类型 |
| callsign | string | 呼号 |
| imonumber | string | IMO |
| course | string | 航向 |
| turnrate | string | 转向率 |
| status | string | 状态 |
| fn | string | 船籍国 |
| dwt | string | 载重吨 |

## 调用流程

1. 检查 `api_key`；无则提示并终止。
2. 确定区域：
   - **用户提供矩形坐标**：西/南/东/北 或 左下经度、左下纬度、右上经度、右上纬度 → 请求带 `bbox=...`。
   - **用户仅文字描述区域**（如「红海」「北太平洋」「马六甲海峡」）：先调用 [区域清单接口](areas_api.md)（`position/areas/token`），用返回的 `name`/`cnName` 匹配用户描述，取匹配项的 `id`，请求带 `areaId={id}`。
   - **用户提供 WKT 多边形**：请求带 `polygon=...`（如 `POLYGON((lon1 lat1,lon2 lat2,...))`）。
3. 请求：`GET .../position/gettraffic/token?api_key={api_key}&bbox=...` 或 `&areaId=...` 或 `&polygon=...`（三选一）。
4. 若 `result === "ok"` 解析 list，按需展示船名、MMSI、经纬度、航速、状态、目的港等。
