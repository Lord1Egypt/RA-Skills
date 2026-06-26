# 区域清单 API / Areas API

获取可直接使用的区域清单（海区、贸易区），用于按名称选择区域后以 **areaId** 调用区域船舶接口。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 `HIFLEET_API_BASE`（无末尾 `/`）。见 [api_base.md](api_base.md)。

## 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/position/areas/token` |
| 请求方式 | `GET` |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| api_key | (从配置读取) | 否 | string | 接口授权 `api_key`；传了之后 `includeBound` 才生效 |
| includeBound | false | 否 | string | 是否返回边界 WKT，仅 `api_key` 有效时生效，默认 false |

## 成功响应

- `result`: "ok"
- `num`: 数量
- `list`: 区域列表，每项字段见下

### list 单项字段说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | number | 区域 id，**用于 gettraffic 接口的 areaId 参数** |
| number | number | 编号 |
| name | string | 区域英文名称 |
| cnName | string | 区域中文名称 |
| type | string | 类型：seaArea（海区）、tradeArea（贸易区） |
| createTime | string | 创建时间 |

## 调用流程

1. 用户文字描述区域（如 [波斯湾]「红海」「北太平洋」「马六甲海峡」）时，先调用本接口获取区域清单。
2. 用 `name` 或 `cnName` 模糊/精确匹配用户描述，取匹配项的 `id`。
3. 使用该 `id` 作为 **areaId** 调用 `position/gettraffic/token` 查询该区域内船舶。参见 [area_traffic_api.md](area_traffic_api.md)。

## 脚本

`scripts/get_areas.py`：无参数时返回区域列表；`--include-bound` 时返回边界 WKT（需配置 `api_key`）。
