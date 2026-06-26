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
    "code": "0",
    "msg": "success",
    "data": [
        {
            "traceId": "202604010000002",
            "originalFilename": "身份证示例.jpg",
            "cosPath": "/ocr/202604/01/身份证示例.jpg",
            "result": [
                {
                    "status": 200,
                    "originFilename": "身份证示例.jpg",
                    "cosPath": "/ocr/202604/01/身份证示例.jpg",
                    "fileIndex": 1,
                    "cutIndex": 0,
                    "coordinate": [],
                    "classifyCode": "ID_CARD",
                    "confidence": 0.998,
                    "elements": {
                        "name": "张示例",
                        "gender": "男",
                        "nation": "汉",
                        "bornDate": "1990年9月4日",
                        "address": "湖南省衡东县霞流镇白村村1组11号",
                        "IDNumber": "430024199009042311",
                        "issueInstitution": "沂源县公安局",
                        "validityPeriod": "2013.11.16-2023.11.16"
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
