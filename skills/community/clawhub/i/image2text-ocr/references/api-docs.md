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
      "traceId": "202604010000001",
      "originalFilename": "通用文字示例.png",
      "cosPath": "/ocr/202604/01/通用文字示例.png",
      "result": [
        {
          "imageBase64": "",
          "offset": 0,
          "confidence": 0.9668,
          "width": 989,
          "height": 1200,
          "angle": 0,
          "text": [
            {
              "pos": [
                [
                  117,
                  14
                ],
                [
                  931,
                  18
                ],
                [
                  931,
                  63
                ],
                [
                  117,
                  58
                ]
              ],
              "width": 814,
              "height": 44,
              "text_class": "2",
              "x": 117,
              "y": 14,
              "anglenet_class": "0",
              "text": "喜欢欣赏",
              "chars": [
                {
                  "pos": [
                    [
                      468.01,
                      16.08
                    ],
                    [
                      514.78,
                      16.35
                    ],
                    [
                      514.78,
                      60.88
                    ],
                    [
                      468.01,
                      60.61
                    ]
                  ],
                  "text": "喜"
                },
                {
                  "pos": [
                    [
                      514.78,
                      16.35
                    ],
                    [
                      554.68,
                      16.58
                    ],
                    [
                      554.68,
                      61.11
                    ],
                    [
                      514.78,
                      60.88
                    ]
                  ],
                  "text": "欢"
                },
                {
                  "pos": [
                    [
                      554.68,
                      16.58
                    ],
                    [
                      602.83,
                      16.86
                    ],
                    [
                      602.83,
                      61.39
                    ],
                    [
                      554.68,
                      61.11
                    ]
                  ],
                  "text": "欣"
                },
                {
                  "pos": [
                    [
                      602.83,
                      16.86
                    ],
                    [
                      635.85,
                      17.05
                    ],
                    [
                      635.85,
                      61.58
                    ],
                    [
                      602.83,
                      61.39
                    ]
                  ],
                  "text": "赏"
                }
              ]
            }
          ]
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
