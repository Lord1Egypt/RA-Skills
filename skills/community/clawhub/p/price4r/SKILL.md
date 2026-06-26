---
name: jz-parts-price4r
description: 使用积智数据 参考价格查询 API，通过 配件编码 列表 查询 配件的 参考价格信息。
metadata: { "openclaw": {  "requires": { "bins": ["python3"], "env": ["JZ_API_KEY"] }, "primaryEnv": "JZ_API_KEY" } }
---

# 积智数据 配件编码参考价格查询（ parts）

基于 [配件参考价格查询 API] 的 OpenClaw 技能，支持：

- **配件参考价格 查询**：通过 配件编码 列表 查询 配件的 参考价格信息；


使用技能前需要申请数据，请联系【积智数据】  MOBILE (+86 13916450206/15821282326) ; EMAIL( juyuan@jikugroup.com/jiangzhihui@jikugroup.com)  获取。

## 后端服务
本技能依赖积智数据 参考价格查询服务，接口地址：https://erp.qipeidao.com/jzOpenClaw/getPriceRefer

## 环境变量配置

```bash
# Linux / macOS
export JZ_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JZ_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/prices/get_parts_price4r.py`

## 使用方式

### 1. 按 配件编码 列表 查询 参考价格信息

```bash
python3 skills/prices/get_parts_price4r.py '["1ZD807221GRU", "5LD807835BU34"]' 原厂
```

```
## 查询 4S价 信息请求参数

| 字段名  | 类型   | 必填 | 说明                                           |
|--------|--------|------|------------------------------------------------|
| partsCodes | list | 是   | 配件编码 列表，每个编码为 字母数字组合 |
| quality | string | 可选   | 参考价格类型，可选值：原厂、国内品牌 |

示例：

```
 ["1ZD807221GRU", "5LD807835BU34"]  国内品牌
```

## 查询 参考价格信息返回结果示例

脚本直接输出接口 `model` 字段，结构与示例一致（示例简化）：

```json
 {
    "priceBizArea": [
      {
        "partsCode": 1ZD807221GRU,
        "quality": "FC",
        "price": "80"
      }
    ],
    "priceErpSales": [
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:正厂:",
        "price": "600.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:RX:",
        "price": "120.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:配套:",
        "price": "260.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂::纯正",
        "price": "520.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:正厂:",
        "price": "245.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "150.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:原厂:",
        "price": "680.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:A:",
        "price": "400.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "国内品牌:中国:",
        "price": "200.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "120.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:上海:",
        "price": "180.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:正厂:",
        "price": "700.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "180.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:精品:",
        "price": "165.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "国内品牌:品牌:",
        "price": "145.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:正厂:",
        "price": "700.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "180.0"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "其他:4:",
        "price": "121.51"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "240.0"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "其他:4:",
        "price": "121.51"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂:原厂:",
        "price": "260.0"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "180.0"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      }
    ],
    "priceErpPurchase": [
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:RX:",
        "price": "100.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:配套:",
        "price": "85.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂::纯正",
        "price": "230.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "80.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:原厂:",
        "price": "210.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:A:",
        "price": "85.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "80.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:上海:",
        "price": "120.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "80.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "其他:精品:",
        "price": "85.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "国内品牌:品牌:",
        "price": "100.0"
      },
      {
        "partsCode": "1ZD807221GRU",
        "quality": "原厂:品牌:",
        "price": "100.0"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "其他:4:",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "配套件:延锋:",
        "price": "195.0"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "其他:4:",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.94"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      },
      {
        "partsCode": "5LD807835BU34",
        "quality": "原厂::",
        "price": "186.95"
      }
    ],
    "priceCpcw": null,
    "priceHisQuote": null
  }
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

1. 用户给出车架号：「帮我查一下配件编码： 1ZD807221GRU,5LD807835BU34 的 品质: 原厂/国内品牌 的参考价格信息 」。  
2. 调用1-配件编码列表+配件品质 查询：  
   `python3 skills/prices/get_parts_price4r.py  '["1ZD807221GRU", "5LD807835BU34"]' 原厂`
   `python3 skills/prices/get_parts_price4r.py  '["1ZD807221GRU", "5LD807835BU34"]' 国内品牌`      
3. 调用2-纯配件编码列表 查询 返回所有品质:
   `python3 skills/prices/get_parts_price4r.py  '["1ZD807221GRU", "5LD807835BU34"]  ''`
3. 从返回中选取 `partsCode/quality/price` 等字段，给出自然语言总结；

