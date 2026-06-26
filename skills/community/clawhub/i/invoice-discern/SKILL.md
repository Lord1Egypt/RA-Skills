---
name: huisuiyun-invoicediscern-hsy
description: 使用慧穗云发票识别 API，通过上传发票影像文件（图片、PDF、OFD、ZIP）自动识别发票信息。
metadata: { "openclaw": { "emoji": "📄", "requires": { "bins": ["python3"], "env": ["HSY_AK", "HSY_SK"] }, "primaryEnv": "HSY_AK" } }
---

## 发票识别-慧穗云（Invoice Discern）

基于慧穗云官方 API 的发票识别技能，支持通过上传发票影像文件自动识别发票信息，包括增值税发票、机动车发票、火车票、飞机票等多种票据类型。

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

脚本文件：`skills/invoice-discern/invoice-discern.py`

## 使用方式

### 1. 识别发票信息

通过 `/api/v2/agent/cdk/invoice/discern` 接口识别发票影像文件

```bash
python3 skills/invoice-discern/invoice-discern.py discern /path/to/invoice.jpg
```

### 支持的文件格式

- 图片格式：.jpg, .jpeg, .png（一张图片最多包含9张发票）
- PDF格式：.pdf（每页只能有一张发票，最多30页）
- OFD格式：.ofd
- 压缩包：.zip（多张发票存放在一个文件夹内压缩，不允许二级目录）
- 文件大小：不超过 6M

### 支持的票种类型

| 票种名称 | 票种代码 |
| :------- | :------- |
| 增值税专用发票 | 01 |
| 机动车销售统一发票 | 03 |
| 增值税普通发票 | 04 |
| 增值税专用电子发票 | 08 |
| 增值税电子普通发票 | 10 |
| 增值税普通发票(卷票) | 11 |
| 通行费增值税电子普通发票 | 14 |
| 二手车销售统一发票 | 15 |
| 全电发票(普通发票) | 90 |
| 全电发票(增值税专用发票) | 09 |
| 全电纸质发票(增值税专用发票) | 85 |
| 全电纸票发票(普通发票) | 86 |
| 全电发票(铁路电子客票) | 51 |
| 全电发票(航空运输电子客票行程单) | 61 |
| 机打发票 | 199 |
| 定额发票 | 200 |
| 火车票 | 201 |
| 航空运输电子客票行程单 | 202 |
| 客运汽车 | 203 |
| 过路费 | 205 |
| 船票 | 204 |
| 出租车发票 | 207 |
| 电子医疗票据 | 209 |
| 滴滴出行行程单 | 210 |
| 非税收入类票据 | 211 |

### 返回结果示例

```json
{
  "code": "200",
  "message": "OK",
  "serialNo": "635436126077288448",
  "data": {
    "invoiceList": [
      {
        "invoiceType": "01",
        "invoiceCode": "3100212130",
        "invoiceNo": "37243570",
        "drewDate": "2021-10-27",
        "amount": 2990.25,
        "amountWithTax": 3378.98,
        "taxAmount": 388.73,
        "purchaserName": "慧穗数字科技****",
        "purchaserTaxNo": "9131011****",
        "sellerName": "上海京东鸿为****",
        "sellerTaxNo": "91310107M****",
        "filePath": "http://...",
        "items": [
          {
            "goodsName": "*电子计算机*笔记本电脑",
            "amount": "3538.94",
            "taxRate": "13%",
            "taxAmount": "460.06"
          }
        ]
      }
    ],
    "nonVatInvoiceList": [
      {
        "invoiceType": "201",
        "invoiceNo": "Z106J018400",
        "drewDate": "2019-11-18",
        "amountWithTax": "73.00",
        "stationGetOn": "杭州东",
        "stationGetOff": "上海虹桥",
        "passengerName": "张三",
        "trainNumber": "G7510"
      }
    ]
  }
}
```

### 返回参数说明

| 参数名 | 类型 | 说明 |
| :----- | :--- | :--- |
| code | String | 返回状态码：200-成功 |
| serialNo | String | 返回流水号 |
| message | String | 返回信息 |
| data | Object | 识别的发票信息集合 |
| data.invoiceList | Array | 增值税发票信息列表 |
| data.nonVatInvoiceList | Array | 非增值税发票信息列表 |

#### 增值税发票字段（invoiceList）

| 字段名 | 类型 | 说明 |
| :----- | :--- | :--- |
| invoiceType | String | 发票类型（见票种码值表） |
| invoiceCode | String | 发票代码（全电发票为空） |
| invoiceNo | String | 发票号码 |
| drewDate | String | 开票日期 |
| amount | BigDecimal | 不含税金额 |
| amountWithTax | BigDecimal | 含税金额 |
| taxAmount | BigDecimal | 税额 |
| purchaserName | String | 购方名称 |
| purchaserTaxNo | String | 购方税号 |
| sellerName | String | 销方名称 |
| sellerTaxNo | String | 销方税号 |
| filePath | String | 文件下载地址 |
| items | Array | 商品明细列表 |

### 常见错误码

| 错误码 | 说明 |
| :----- | :--- |
| 200 | 识别成功 |
| 501 | 连接超时，请稍后重试 |
| 其他 | 详见接口返回的 message |

## 注意事项

1. 支持的文件格式：.jpg, .jpeg, .png, .pdf, .ofd, .zip
2. 文件大小不超过 6M
3. 图片格式一张图片最多包含 9 张发票
4. PDF 文件每页只能有一张发票，最多 30 页
5. ZIP 文件不允许存在二级目录
6. 全电多明细 PDF 会分别返回每页发票信息
7. Token 有效期为 30 天，超出有效期后需重新获取

## 在 OpenClaw 中的推荐用法

1. 用户提供发票影像文件路径
2. 代理调用：`python3 skills/invoice-discern/invoice-discern.py discern <file_path>`
3. 从返回结果中读取识别的发票信息
4. 向用户总结发票的关键信息（发票类型、金额、购销方等）

## 如需了解更多欢迎扫码联系
![image](https://www.smarttax.net/images/footer-ercode-01.png)
