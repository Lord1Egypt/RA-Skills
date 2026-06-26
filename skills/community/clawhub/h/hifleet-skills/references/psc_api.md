# 船舶 PSC 检查 API / PSC Inspection API

根据 **IMO** 查询船舶 **港口国监督检查（PSC）** 相关数据。需配置 `api_key`。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 `HIFLEET_API_BASE`（无末尾 `/`）。见 [api_base.md](api_base.md)。

**船名不支持直接查询**：若用户只提供船名或关键字，需先调用 `position/shipSearch` 得到船舶列表，从命中条目的 `imonumber` 取得 IMO，再调本接口。无 IMO 的内贸船无法按 IMO 查 PSC。

## 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/pscapi/get` |
| 请求方式 | `GET` |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| api_key | (从配置读取) | 是 | string | 接口授权 `api_key`；缺省时接口返回 `code` 4005（token is empty） |
| imo | 9123456 | 是 | string | IMO 号（通常 7 位数字） |

参数名以 HiFleet 服务端为准；若与官方 ShowDoc 不一致，以官方文档为准。

## 错误响应（示例）

未带 `api_key`：

```json
{"code":4005,"message":"token is empty.","url":"/pscapi/get"}
```

`api_key` 不存在或无效：

```json
{"code":4004,"message":"this token is not exist.","url":"/pscapi/get"}
```

**`api_key` 有效但无本接口权限**（账号未开通 PSC API 或订阅不含该路径时常见）：

```json
{"code":4001,"message":"this token is unauthoried to access the url.","url":"/pscapi/get"}
```

说明：`message` 中的拼写以服务端返回为准（如 `unauthoried`）。此时其它接口（如档案 `shiparchive/...`、船位 `position/...`）仍可能正常，需在 HiFleet 侧为当前 `api_key` 开通 **PSC 数据 / pscapi** 相关权限，或更换授权范围正确的 `api_key`。

## 成功响应

实测依赖账号权限：若返回 **4001**，则无法在未开通权限前记录「正式」成功样例。

常见可能形态（与 HiFleet 其它 JSON 接口类似，**以实际返回为准**）：

1. **`status` 为 `"1"`**，业务数据在 **`data` 数组**中，每条为一次检查或一条缺陷等键值对象。
2. **顶层 `list`** 为对象数组（与 `shipSearch` 类似命名）。
3. **`code` 为 `0` 或 `200`**，载荷在 **`data`** 中。

脚本 `get_psc.py` 会对上述形态做分条打印；无法识别时输出完整 JSON，便于对照 ShowDoc 或抓包再改展示逻辑。

## 调用流程

1. 检查 `api_key`；无则提示并终止。
2. **用户已提供 IMO**（7 位数字，可带 `IMO` 前缀）：请求 `...?imo={imo}&api_key={api_key}`。
3. **用户仅提供船名或关键字**：`GET position/shipSearch` → 0 条提示未找到；1 条取 `imonumber`；多条请用户指定 MMSI 或从列表选择 → 若有 IMO 再调本接口；**imonumber 为空**则提示无 IMO、无法查 PSC。
4. **用户提供 9 位 MMSI**：可用该 MMSI 作为 `shipname` 调用 `shipSearch` 定位船舶，再取 `imonumber` 调本接口（与船位技能中搜船方式一致）。

## 相关接口

- 搜船：`{base}/position/shipSearch`（见 [position_api.md](position_api.md)）
