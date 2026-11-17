# 公开交换合同

只使用一个对应版本：

- DRG：`mfz.drg-single.exchange.v1`
- DIP：`mfz.dip-single.exchange.v1`

NDJSON 每行提交一个对象；也可以把相同对象分批提交给 MCP。NDJSON 外层不得再包数组。

## 通用来源字段

每行必须包含：

```json
{
  "source_row_id": "本文件内稳定的行标识",
  "source_ref": {
    "file": "原始文件名",
    "sheet": "可选 Sheet 名",
    "page": 1,
    "row": 2
  },
  "field_confidence": {
    "关键字段名": 0.98
  }
}
```

只保留适用的来源位置字段。置信度范围为 0 到 1；OCR 得到的编码、数值、分隔符和任何经过解释的字段都应提供置信度。

## DRG 行

必填：`source_row_id`、`group_code`、`group_name`、`source_ref`。

可选公开字段：

- `mdc_code`、`adrg_code`
- 数值型 `weight`、`base_points`、`payment_standard`
- `grassroots_flag`：`true`、`false` 或 `"unknown"`
- `grassroots_kind`：`basic`、`inclined`、`unspecified` 或 `unknown`
- `field_confidence`

多维费率不要写进目录行。在创建任务时通过 `rate_profiles` 提交，包含 `profile_name`、数值型 `rate` 及适用的险种、医院等级、地区、病组范围、生效日期和来源。

```json
{"source_row_id":"weights:18","group_code":"BB19","group_name":"其他神经系统疾病","mdc_code":"MDCB","adrg_code":"BB1","weight":1.245,"grassroots_flag":false,"grassroots_kind":"unknown","source_ref":{"file":"权重表.xlsx","sheet":"病组权重","row":18},"field_confidence":{"group_code":1,"weight":1}}
```

## DIP 行

必填：`source_row_id`、`diagnosis_code`、`diagnosis_name`、`source_ref`。

可选公开字段：

- `catalogue_code`、`catalogue_name`
- `procedure_expression_raw`、`procedure_expression`、`procedure_name`
- 数值型 `score`
- `catalogue_class`：`core`、`comprehensive`、`tcm`、`auxiliary`、`day_surgery`、`bed_day`、`other` 或 `unknown`
- `source_type_raw`
- `grassroots_flag`：`true`、`false` 或 `"unknown"`
- `field_confidence`

规范操作表达只做以下转换：把 `/`、`／` 转成 `|`；保留 `+`；保留 `BSZL`；不得补齐、缩短、改变长度或重排操作编码。

`catalogue_class` 与 `grassroots_flag` 必须独立。核心病种存在基层覆盖时仍是 `catalogue_class: "core"` 和 `grassroots_flag: true`。

```json
{"source_row_id":"p12:r8","catalogue_code":"A15.0-BSZL","diagnosis_code":"A15.0","diagnosis_name":"肺结核","procedure_expression_raw":"BSZL","procedure_expression":"BSZL","score":860,"catalogue_class":"core","grassroots_flag":true,"source_ref":{"file":"DIP目录.pdf","page":12,"row":8},"field_confidence":{"diagnosis_code":0.99,"score":0.97}}
```

## 校验前对账

记录非空源数据行数、提交行数、被排除的标题/合计/注释/重复行及每项排除原因。不得静默丢弃源数据行；等价重复由服务端校验识别。
