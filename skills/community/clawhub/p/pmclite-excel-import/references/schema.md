# 导入契约字段表（以 get_import_schema 为准）

本文件是**离线参考**，字段名与必填要求和 `get_import_schema` 的返回一致；两者冲突时以工具返回为准，那才是当前安装版本的契约。

## 处理顺序

`materials` → `products` → `bomItems` → `workOrders` → `inventory`

后处理的表可以引用前面刚生成的编码；引用不存在且本批未提供的，整批拒绝，不跳过。

## materials（物料主数据）

同 `code` 视为同一物料；不提供 code 时按 `name` + `spec` 匹配现有，匹配不到生成 `AUTO-MAT-XXXXX`。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| code | string | 否 | 物料编码，不填自动生成 |
| name | string | **是** | 物料名称 |
| spec | string | 否 | 规格型号，与 name 共同决定是否匹配现有物料 |
| unit | string | 否 | 单位，不填默认「个」并在回执提醒 |
| category | string | 否 | 类别 |
| supplier | string | 否 | 供应商 |
| unitPrice | number | 否 | 单价 |

## products（产品）

同 `code` 视为同一产品；不提供时按 `name` 匹配或生成 `AUTO-PRD-XXXXX`。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| code | string | 否 | 产品编码 |
| name | string | **是** | 产品名称 |
| type | string | 否 | 枚举 `finished` / `semi`，默认 finished |
| description | string | 否 | 描述 |

## bomItems（BOM 明细）

同父产品 + 同子项视为同一行，重复导入更新用量。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| productCode | string | **是** | 父产品编码，可用本批刚生成的编码 |
| type | string | **是** | 枚举 `material` / `subproduct` |
| materialCode | string | type=material 时**是** | 子件物料编码 |
| subProductCode | string | type=subproduct 时**是** | 子件半成品编码 |
| quantity | number | **是** | 用量 |

## workOrders（工单）

同 `orderNumber` 视为同一工单。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| orderNumber | string | **是** | 工单号 |
| productCode | string | **是** | 产品编码，工具内部转 productId |
| quantity | number | **是** | 计划数量 |
| priority | string | 否 | 枚举 `高` / `中` / `低`，默认「中」 |
| assignedLine | string | 否 | 指定产线 |
| scheduledStart | string | 否 | `YYYY-MM-DD` |
| scheduledEnd | string | 否 | `YYYY-MM-DD` |
| salesOrderNumber | string | 否 | 销售订单号 |

## inventory（库存）

同 `materialCode` 视为同一行。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| materialCode | string | **是** | 物料编码 |
| quantity | number | **是** | 库存数量 |
| location | string | 否 | 库位 |

## import_data 的参数

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| mode | `preview` / `apply` | preview 只校验不写库；apply 才写入 |
| data | object | key 为表名，值为该表的行数组 |
| idempotency_key | string | `apply` 必填，UUID；同一批重试复用同一个值 |

## 预览回执怎么读

- **新增 N**：这批里新出现的记录数；**更新 M**：按编码/名称匹配到现有记录并覆盖字段的行数。
- **AUTO 编码**：逐条说明哪个对象没给编码、系统生成了什么，让用户知道以后要去物料列表认这个编号。
- **warning**：不是错误，但要让用户知道。典型是“有 N 条未提供单位，已默认为个”和“单价从 1.2 更新为 1.3”这类字段级变化。
- **错误 K**：整批不写入，按 `table` + `row` + `error` 逐条给出，让用户改表后重来。

## 不变的行为保证

- 叠加式 upsert：存在则更新、不存在则新增，**不删除任何现有数据**。
- 字段级 merge：只覆盖请求里出现的字段，没传的保持原值。
- 有错误行时整批回滚，不做“部分成功”。
- 触发免费版额度上限会被拒绝并提示升级，这是业务限制，不是故障，不要当错误重试。