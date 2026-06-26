# Sugon-Scnet OCR API 文档摘要

## 接口地址
`POST https://api.scnet.cn/api/llm/v1/ocr/recognize`

## 请求头
- `Content-Type: multipart/form-data`
- `Authorization: Bearer <你的 API Key>`

## 请求参数（表单）
| 参数名  | 类型 | 必填 | 描述                                   |
| ------- | ---- | ---- | -------------------------------------- |
| file    | File | 是   | 需要识别的图片文件                     |
| ocrType | str  | 是   | 识别类型枚举，详见 SKILL.md 参数说明   |

## 响应结构
```json
{
  "code": "0",          // 应答码，0 表示成功
  "msg": "success",     // 应答信息
  "data": [             // 应答数据体
    {
        "traceId": "1234567890",
        "originalFilename": "id-card.jpg",
        "cosPath": "scnetAPIService/20260323/2e204eb284bb438ba7863f5e65470c40.jpg",
        "result": [
          {
            "status": 200,
            "originFilename": "id-card.jpg",
            "cosPath": "scnetAPIService/20260323/2e204eb284bb438ba7863f5e65470c40_cut_1.jpg",
            "fileIndex": 1,
            "cutIndex": 1,
            "coordinate": [ 88, 734, 88, 61, 1115, 61, 1115, 734 ],
            "classifyCode": "",
            "confidence": 1.0,
            "elements": {
              "address": "湖南省衡东县**镇**村1组11号",
              "gender": "男",
              "nation": "汉",
              "confidence": "1.0",
              "name": "张示例",
              "bornDate": "1990年9月4日",
              "IDNumber": "2300***********311"
            },
            "stamps": []
          }
        ]
    }
  ]
}
```
## 错误码
- `401 / 403: Token 无效或过期`
- `其他 4xx/5xx: 请检查请求参数或联系服务商`
- `业务错误码（如 code 非 0）：见返回的 msg 字段`

## 注意事项
- `支持单张图片、PDF 或多页压缩包（自动解压识别）`
- `识别结果位于 data[0].result[0].elements 中`
- `不同 ocrType 返回的 elements 字段不同，详见 assets/templates/fields-summary.md`
