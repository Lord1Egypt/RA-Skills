# Sugon-Scnet 移动支付账单 OCR API 文档摘要

> 本文档仅针对 `mobile_pay_bill_ocr` 技能使用的 **移动支付账单识别** 场景。本技能仅支持 `MOBILE_PAYMENT_BILL` 一种识别类型，不接受身份证、合同、印章、发票、卡证等非支付类文档。

## 接口地址
`POST https://api.scnet.cn/api/llm/v1/ocr/recognize`

## 请求头
- `Content-Type: multipart/form-data`
- `Authorization: Bearer <你的 API Key>`

## 请求参数（表单）
| 参数名  | 类型 | 必填 | 描述                                   |
| ------- | ---- | ---- | -------------------------------------- |
| file    | File | 是   | 需要识别的移动支付账单图片（jpg/png 等常见图片格式） |
| ocrType | str  | 是   | 识别类型枚举，本技能固定为 `MOBILE_PAYMENT_BILL` |

## 响应结构
```json
{
  "code": "0",
  "msg": "success",
  "data": {
    "traceId": "12345678909",
    "originalFilename": "移动支付账单示例.PNG",
    "cosPath": "scnetAPIService/20260101/3990c1e6b3944947bcb75d548313bbff.PNG",
    "result": [
      {
        "status": 200,
        "originFilename": "移动支付账单示例.PNG",
        "cosPath": "scnetAPIService/20260101/3990c1e6b3944947bcb75d548313bbff_cut_1.PNG",
        "fileIndex": 1,
        "cutIndex": 1,
        "coordinate": [21, 1754, 21, 0, 801, 0, 801, 1754],
        "classifyCode": "",
        "confidence": 0.951,
        "elements": {
          "title": "耶里夏丽东方店",
          "transAmount": "-179.00",
          "transStatus": "支付成功",
          "transDate": "2025年10月20日 18:00:53",
          "goods": "耶里夏丽东方店",
          "merchantName": "上海西夜餐饮有限公司",
          "acquiringInstitution": "财付通支付科技有限公司",
          "transType": "招商银行储蓄卡(2005)",
          "transNo": "4200002955202510205438716000",
          "merchantNo": "003518872Y3NtApckr98IHaySg2PeM",
          "remarks": "",
          "refundNo": ""
        },
        "stamps": []
      }
    ]
  }
}
```
## 错误码
- `401 / 403: Token 无效或过期`
- `其他 4xx/5xx: 请检查请求参数或联系服务商`
- `业务错误码（如 code 非 0）：见返回的 msg 字段`

## 注意事项
- 本技能仅识别单张移动支付账单图片。
- 识别结果位于 `data[0].result[0].elements` 中。
- 返回字段以 `assets/templates/fields-summary.md` 为准。
