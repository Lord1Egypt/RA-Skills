---
name: "3.3-市场主体统计接口"
description: "用于L1小程序首页查看市场主体统计情况，包含在营企业数量、本月新增、企业区域分布等统计数据。Invoke when user needs market entity statistics or business data."
---

# 3.3 市场主体统计接口

## 接口说明
用于L1小程序首页查看市场主体统计情况。包含：在营企业数量，本月新增，较年初新增数量，指定时间范围内在营、新增、注销/吊销企业数量及增长率，企业区域分布统计，企业规模分布，企业金字塔分布，融资分布统计。

## 调用信息
- **请求方式**：POST
- **统一入口地址**：`https://rcd-test.dfwycredit.com/s1/skill/unified-invoke`
- **Category标识**：`3.3`

## 请求参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| category | String | 是 | 接口标识，固定值：`3.3` |
| API_KEY | String | 是 | 用户身份认证密钥 |
| provinceCode | String | 否 | 省级代码（三选一必填） |
| cityCode | String | 否 | 市级代码（三选一必填），如果省级代码为直辖市，该字段必传且为XX0100 |
| districtCode | String | 否 | 区县代码（三选一必填） |
| dateValue | String | 是 | 查询年份 |
| entnature | String | 否 | 企业性质 |
| entindustry | String | 否 | 所属行业 |

## 返回数据说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | String | 接口返回代码，200：接口正常，500：接口异常 |
| msg | String | 状态码说明，成功：查询成功，失败：查询失败 |
| total | int | 条数 |
| rows | JsonArray | 返回记录集 |

## 调用示例

统一入口调用方式：

```bash
curl --location 'https://rcd-test.dfwycredit.com/s1/skill/unified-invoke' \
--header 'Content-Type: application/json' \
--data '{
    "category": "3.3",
    "API_KEY": "用户的API_KEY",
    "provinceCode": "650000",
    "dateValue": "2024"
}'
```

## 使用场景

当用户需要查询以下数据时调用此接口：
- 查看在营企业数量
- 查询本月新增企业数量
- 较年初新增数量统计
- 指定时间范围内的企业变化情况
- 企业区域分布统计
- 企业规模分布统计
- 企业金字塔分布
- 融资分布统计

## 注意事项

1. 地区代码（provinceCode、cityCode、districtCode）三选一必填
2. dateValue为必填参数，表示查询年份
3. 返回数据直接透传接口原始结果，不做额外处理
