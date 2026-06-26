---
name: huisuiyun-invoiceverify-hsy
description: 使用慧穗云发票查验 API，根据发票代码、号码、日期和金额等信息查询发票详情。
metadata: { "openclaw": { "emoji": "🧾", "requires": { "bins": ["python3"], "env": ["HSY_AK", "HSY_SK"] }, "primaryEnv": "HSY_AK" } }
---

## 发票查验-慧穗云（Invoice Verify）

基于慧穗云官方 API 的发票查验技能，支持通过发票代码、号码、开票日期、金额等信息查验发票真伪。

## 环境变量配置

```bash
# Linux / macOS
export HSY_API_URL="https://huisuiyun.com"
export HSY_AK="your_ak_here"
export HSY_SK="your_sk_here"
export HSY_TYPE="2"  # 1: ISV等级AKSK, 2: 慧穗云等级AKSK

# Windows PowerShell
$env:HSY_API_URL="https://huisuiyun.com"
$env:HSY_AK="your_ak_here"
$env:HSY_SK="your_sk_here"
$env:HSY_TYPE="2"
```

**获取 AK/SK：**
- 慧穗云秘钥管理：https://huisuiyun.com/account/conf/secretkey

**注意：** 如果未配置环境变量，脚本会返回包含配置链接的错误信息，方便用户快速获取秘钥。

## 脚本路径

脚本文件：`skills/invoice-verify-hsy/invoice-verify-hsy.py`

## 使用方式

### 1. 查验发票信息

通过 `/api/v2/agent/cdk/invoice/check` 接口查验增值税发票[接口文档](https://cdk.huisuiyun.com/docs/%E8%BE%85%E5%8A%A9%E5%8A%9F%E8%83%BD%E6%8E%A5%E5%8F%A3/invoice-check)

```bash
python3 skills/invoice-verify-hsy/invoice-verify-hsy.py verify '{"storeFlag":0,"invoiceList":[{"invoiceCode":"3300201130","invoiceNo":"00517731","amount":7559.41,"drewDate":"2021-06-22","invoiceType":"01"}]}'
```

请求 JSON 示例：

```json
{
  "storeFlag": 0,
  "invoiceList": [
    {
      "invoiceCode": "3300201130",
      "invoiceNo": "00517731",
      "amount": 7559.41,
      "drewDate": "2021-06-22",
      "invoiceType": "01"
    }
  ]
}
```

### 请求参数（verify）

| 字段名      | 类型    | 必填 | 说明                                            |
|-------------|---------|------|-------------------------------------------------|
| storeFlag   | Integer | 否   | 入库标识：0-入库，1-不入库，默认不入库          |
| invoiceList | array   | 是   | 发票信息集合（一次查验不超过20张）              |

invoiceList 数组中每个对象的字段：

| 字段名          | 类型       | 必填 | 说明                                                                                                  |
|-----------------|------------|------|-------------------------------------------------------------------------------------------------------|
| invoiceNo       | String     | 是   | 发票号码，如：00517731                                                                                |
| drewDate        | String     | 是   | 开票日期，格式：YYYY-MM-DD，如：2021-06-22                                                            |
| invoiceCode     | String     | 否   | 发票代码，如：3300201130（全电发票无需传入）                                                          |
| invoiceType     | String     | 否   | 发票类型：01-增值税专用发票，08-增值税专用发票（电子），04-增值税普通发票，10-增值税普通发票（电子），09-数电发票(增值税专用发票)，90-数电发票(普通发票)等 |
| amount          | BigDecimal | 否   | 金额：专票（01、08、85）传入不含税金额，数电发票（09、90、51、61）传入价税合计                        |
| checkCode       | String     | 否   | 校验码后六位，普票（04、10、11、14、86）必传                                                          |
| originFileFlag  | Integer    | 否   | 是否获取版式文件：1-是，0-否                                                                          |
| exten1-10       | String     | 否   | 扩展字段1-10                                                                                          |

### 返回结果示例（verify）

```json
{
  "code": "200",
  "message": "OK",
  "serialNo": "637680840671330304",
  "data": [
    {
      "checkFlag": true,
      "invoiceCodeNo": "3300201130-00517731",
      "exceptionInfo": null,
      "invoiceVO": {
        "invoiceType": "01",
        "invoiceCode": "3300201130",
        "invoiceNo": "00517731",
        "drewDate": "2021-06-22",
        "checkCode": "56660956691714098653",
        "amount": 7559.41,
        "amountWithTax": 7635,
        "taxAmount": 75.59,
        "sellerName": "杭州江湖有旅人********公司",
        "sellerTaxNo": "91330100MA2H3LL62A",
        "purchaserName": "慧穗数字科技（上海）********司",
        "purchaserTaxNo": "91330108********U",
        "invoiceStatus": 0,
        "detailList": [
          {
            "goodsName": "*设计服务*活动策划",
            "amount": 7559.41,
            "taxRate": 1,
            "taxAmount": 75.59
          }
        ]
      }
    }
  ]
}
```

### 返回参数说明

| 参数名                      | 类型    | 说明                                                     |
|-----------------------------|---------|----------------------------------------------------------|
| code                        | String  | 返回状态码：200-成功                                     |
| serialNo                    | String  | 返回流水号                                               |
| message                     | String  | 返回信息                                                 |
| data                        | Array   | 查验返回的信息数组                                       |
| data[i].checkFlag           | Boolean | 查验是否成功：true-成功，false-失败                      |
| data[i].invoiceCodeNo       | String  | 查验的发票代码+号码                                      |
| data[i].exceptionInfo       | String  | 查验失败的异常信息                                       |
| data[i].invoiceVO           | Object  | 票面信息（查验成功时返回）                               |
| invoiceVO.invoiceStatus     | Integer | 发票状态：0-正常，1-作废，2-红冲，3-失控，4-异常,7-部分红冲,8-全额红冲,80-红冲发票待确认         |
| invoiceVO.amount            | Decimal | 不含税金额                                               |
| invoiceVO.amountWithTax     | Decimal | 含税金额                                                 |
| invoiceVO.taxAmount         | Decimal | 税额                                                     |
| invoiceVO.sellerName        | String  | 销方名称                                                 |
| invoiceVO.sellerTaxNo       | String  | 销方税号                                                 |
| invoiceVO.purchaserName     | String  | 购方名称                                                 |
| invoiceVO.purchaserTaxNo    | String  | 购方税号                                                 |
| invoiceVO.detailList        | Array   | 发票明细                                                 |

### 常见错误码

| 错误码 | 说明                   |
|--------|------------------------|
| 200    | 查验成功               |
| 501    | 连接超时，请稍后重试   |
| 其他   | 详见接口返回的 message |

## 注意事项

1. 本接口支持多发票查验，一次查验张数应不大于20张
2. 同一张票每天最多可以查验5次
3. Token 有效期为30天，超出有效期后需重新获取
4. 全电发票查验时发票类型必填
5. 专票传入不含税金额，数电发票传入价税合计
6. 普票必须传入校验码后六位

## 在 OpenClaw 中的推荐用法

1. 用户提供发票信息（发票代码、号码、开票日期、金额等）
2. 代理构造 JSON 请求体，根据发票类型填写相应的必填字段
3. 调用：`python3 skills/invoice-verify-hsy/invoice-verify-hsy.py verify '<JSON_BODY>'`
4. 从返回结果中读取查验状态和发票详细信息，并向用户总结发票是否有效及关键信息

## 如需了解更多欢迎扫码联系
![image](https://www.smarttax.net/images/footer-ercode-01.png)