---
name: jz-parts-price4s
description: 使用积智数据 4S价 API，通过 配件编码 列表 查询 配件的 4S价 信息。
metadata: { "openclaw": {  "requires": { "bins": ["python3"], "env": ["JZ_API_KEY"] }, "primaryEnv": "JZ_API_KEY" } }
---

# 积智数据 4S价查询（ parts）

基于 [配件4S价查询 API] 的 OpenClaw 技能，支持：

- **配件 4S价 查询**：通过 配件编码 列表 查询 配件的 4S价 信息；


使用技能前需要申请数据，请联系【积智数据】  MOBILE (+86 13916450206/15821282326) ; EMAIL( juyuan@jikugroup.com/jiangzhihui@jikugroup.com)  获取。

## 后端服务
本技能依赖积智数据 4S价查询服务，接口地址：https://erp.qipeidao.com/jzOpenClaw/getPrice4s

## 环境变量配置

```bash
# Linux / macOS
export JZ_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JZ_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/prices/get_parts_price4s.py`

## 使用方式

### 1. 按 配件编码 列表 查询 4S价 信息

```bash
python3 skills/prices/get_parts_price4r.py LSVAL41Z882104202 '["1ZD807221GRU", "5LD807835BU34"]'
```

```
## 查询 4S价 信息请求参数

| 字段名  | 类型   | 必填 | 说明                                           |
|--------|--------|------|------------------------------------------------|
| vin    | string | 是   | 17 位 VIN 车架号                               |
| partsCodes | list | 是   | 配件编码 列表，每个编码为 字母数字组合 |

示例：
 LSVAL41Z882104202 ["1ZD807221GRU", "5LD807835BU34"]
```

## 查询 4S价 信息返回结果示例

脚本直接输出接口 `model` 字段，结构与示例一致（示例简化）：

``` json
 [
    {
      "partsCode": "1ZD807221GRU",
      "brandName": null,
      "subBrandName": null,
      "price": null,
      "salePriceNoTax": 1248.67,
      "salePriceWithTax": 1411.0,
      "netPriceNoTax": 891.55,
      "netPriceWithTax": 1007.45,
      "publishTime": null
    },
    {
      "partsCode": "5LD807835BU34",
      "brandName": null,
      "subBrandName": null,
      "price": null,
      "salePriceNoTax": 253.1,
      "salePriceWithTax": 286.0,
      "netPriceNoTax": 186.94,
      "netPriceWithTax": 211.24,
      "publishTime": null
    }
  ]
```

当出现错误（如 VIN 不正确或无数据），脚本会输出：

```json
{
  "error": "api_error",
  "state": 202,
  "msg": "VIN不正确"
}
```


## 常见错误码


| 代号   | 说明      |
|------|---------|
| 10001 | 参数错误    |
| 10004 | VIN 不正确或无数据 |


## 在 OpenClaw 中的推荐用法

1. 用户给出车架号：「帮我查一下 VIN  `LSVAL41Z882104202` 询价配件编码： 1ZD807221GRU,5LD807835BU34 的4S价 」。  
2. 调用1-有车架号+配件编码列表查询：  
   `python3 skills/price4s/get_parts_price4s.py LSVAL41Z882104202 '["1ZD807221GRU", "5LD807835BU34"]`
3. 调用2-无车架号,纯配件编码列表查询:
   `python3 skills/price4s/get_parts_price4s.py '' '["1ZD807221GRU", "5LD807835BU34"]'`
3. 从返回中选取 `partsCode/brandName/subBrandName/salePriceNoTax/salePriceWithTax/netPriceNoTax/netPriceWithTax` 等字段，给出自然语言总结；

