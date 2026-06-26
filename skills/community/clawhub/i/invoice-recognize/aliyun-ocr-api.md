# 阿里云发票 OCR API 参考

## API 概述

阿里云 OCR 票据凭证识别支持 **17+ 种发票类型**：

### 支持的发票类型

| 类型 | API | 说明 |
|------|-----|------|
| 混贴发票 | `RecognizeMixedInvoices` | 自动识别多种发票，推荐使用 |
| 增值税发票 | `RecognizeInvoice` | 专用发票、普通发票、电子发票 |
| 火车票 | `RecognizeTrainInvoice` | 火车票识别 |
| 出租车发票 | `RecognizeTaxiInvoice` | 出租车机打发票 |
| 定额发票 | `RecognizeQuotaInvoice` | 定额发票识别 |
| 航空行程单 | `RecognizeAirItinerary` | 机票行程单 |
| 机动车销售发票 | `RecognizeCarInvoice` | 购车发票 |
| 过路过桥费 | `RecognizeTollInvoice` | 过路费发票 |

### 推荐：使用混贴发票识别

`RecognizeMixedInvoices` 可以自动识别发票类型，无需预先知道发票类型。

## 认证方式

使用 AccessKey 认证 + 签名。

## API 端点

```
https://ocr-api.cn-hangzhou.aliyuncs.com
```

## 请求方式

**重要：图片数据直接放到 HTTP body 中，不是 JSON 参数！**

```
POST /?Action=RecognizeMixedInvoices&AccessKeyId=xxx&... HTTP/1.1
Host: ocr-api.cn-hangzhou.aliyuncs.com
Content-Type: application/octet-stream

<图片二进制数据>
```

### 请求参数（URL Query）

| 参数 | 必填 | 说明 |
|------|------|------|
| Action | 是 | API 名称 |
| AccessKeyId | 是 | AccessKey ID |
| Signature | 是 | 签名 |
| SignatureMethod | 是 | HMAC-SHA1 |
| SignatureVersion | 是 | 1.0 |
| Timestamp | 是 | UTC 时间 |
| SignatureNonce | 是 | 唯一随机数 |
| Version | 是 | 2021-07-07 |
| Format | 否 | JSON |

### HTTP Body

直接放图片二进制数据（不是 base64）

## 响应格式

```json
{
  "RequestId": "xxx",
  "Data": "{\"subMsgs\":[{\"op\":\"invoice\",\"result\":{\"data\":{...}}}]}"
}
```

**注意：`Data` 是 JSON 字符串，需要解析！**

### 混贴发票响应结构

```json
{
  "subMsgs": [
    {
      "index": 1,
      "op": "invoice",  // 发票类型
      "result": {
        "data": {
          "invoiceCode": "发票代码",
          "invoiceNumber": "发票号码",
          "invoiceDate": "开票日期",
          "purchaserName": "购买方名称",
          "purchaserTaxNumber": "购买方税号",
          "sellerName": "销售方名称",
          "sellerTaxNumber": "销售方税号",
          "totalAmount": "价税合计",
          "invoiceAmountPreTax": "不含税金额",
          "invoiceTax": "税额",
          "invoiceDetails": [
            {
              "itemName": "项目名称",
              "specification": "规格型号",
              "unit": "单位",
              "quantity": "数量",
              "unitPrice": "单价",
              "amount": "金额",
              "taxRate": "税率",
              "tax": "税额"
            }
          ]
        }
      }
    }
  ]
}
```

## 签名算法

```python
def create_signature(params: dict, secret: str) -> str:
    # 1. 排序参数
    sorted_params = sorted(params.items())
    
    # 2. 构造规范化请求字符串
    query = '&'.join([f"{percent_encode(k)}={percent_encode(v)}" for k, v in sorted_params])
    
    # 3. 构造待签名字符串
    string_to_sign = 'GET&%2F&' + percent_encode(query)
    
    # 4. HMAC-SHA1 签名
    signature = hmac.new(
        (secret + '&').encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha1
    ).digest()
    
    # 5. Base64 编码
    return base64.b64encode(signature).decode('utf-8')
```

## 文件格式支持

| 格式 | 扩展名 |
|------|--------|
| PDF | .pdf |
| OFD | .ofd |
| 图片 | .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp |

## 文件限制

- **大小**：最大 10MB
- **尺寸**：15px ~ 8192px
- **建议**：小于 1.5MB，长宽 > 500px

## 获取 AccessKey

1. 登录阿里云控制台
2. 开通「票据凭证识别」服务
3. 创建 AccessKey（建议使用 RAM 子账号）
4. 授予 `AliyunOCRFullAccess` 权限

## 费用

- 有免费额度（可测试）
- 按次计费
- 建议设置费用预警

## 常见错误

| 错误码 | 说明 |
|--------|------|
| noPermission | 未授权，检查 RAM 权限 |
| InvalidParameter | 参数错误 |
| ImageDecodeError | 图片格式不支持或损坏 |
| QuotaExhausted | 额度用完 |