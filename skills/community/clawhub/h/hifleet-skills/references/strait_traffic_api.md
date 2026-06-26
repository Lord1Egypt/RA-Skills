# 海峡通航 API / Strait Traffic API（咽喉航道通航船舶统计）

红海与波斯湾相关咽喉航道的通航船舶统计。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 `HIFLEET_API_BASE`（无末尾 `/`）。见 [api_base.md](api_base.md)。

方向定义
霍尔木兹海峡：
| 方向 | 含义 | 说明 |
|------|------|------|
| 东 | 出湾 | 波斯湾 → 阿曼湾 |
| 西 | 入湾 | 阿曼湾 → 波斯湾 |

## 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/position/statisticzonetraffic` |
| 请求方式 | **POST** |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| oid | 132808 | 是 | string | 区域 oid，见下表 |
| startdate | 2024-01-17 | 是 | string | 开始日期，格式 yyyy-MM-dd |
| enddate | 2024-01-17 | 是 | string | 结束日期，格式 yyyy-MM-dd |
| i18n | en | 否 | string | 输出语言，zh 或 en，默认 zh |
| api_key | (从配置读取) | 否 | string | 接口授权 `api_key`；**无 `api_key` 仅可查最近 1 周**，有 `api_key` 时间区间不限 |

## 支持的海峡（oid）

| 海峡名称     | oid     | 英文/备注        |
|--------------|---------|------------------|
| 曼德海峡     | 24480   | Bab el-Mandeb    |
| 苏伊士运河   | 132808  | Suez Canal       |
| 好望角       | 1062830 | Cape of Good Hope |
| 霍尔木兹海峡 | 24471   | Strait of Hormuz |

## 成功响应结构

- **oid**：区域 oid
- **zonename**：区域名称
- **startdate** / **enddate**：查询参数回显
- **passdata**：数组，按日与方向统计
  - **passdate**：通过日期
  - **passdirection**：数组
    - **direction**：通过方向（如 S、N）
    - **shiptypecount**：船型及艘次 `[{ "shiptype": "...", "count": n }]`
    - **total**：该日该方向总艘次
    - **ships**：船舶明细 `[{ "mmsi", "imonumber", "shipname", "type", "minotype", "dwt", "length", "width" }]`

## 鉴权与时间范围

- **无 `api_key`**：仅可查询**最近 1 周**内的时间区间；超出则接口可能报错或需鉴权。
- **有 `api_key`**：时间区间不限，可查任意起止时间。

## 调用流程

1. 确定海峡：用户指定海峡名称或 oid，映射到上表 oid。
2. 确定时间区间：startdate、enddate，格式 yyyy-MM-dd。**无 `api_key` 时**校验区间 ≤ 7 天。
3. **POST** 请求：`.../position/statisticzonetraffic?oid={oid}&startdate={startdate}&enddate={enddate}&i18n={zh|en}[&api_key=...]`，有 `api_key` 时传入 `api_key`。
4. 解析响应：zonename、passdata 下按 passdate / passdirection 展示通航方向、船型统计、总艘次及船舶列表。
