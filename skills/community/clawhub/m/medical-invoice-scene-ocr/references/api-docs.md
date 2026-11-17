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
      "traceId": "202604010000020",
      "originalFilename": "医疗住院发票示例.jpg",
      "cosPath": "scnetAPIService/20260101/afcbc98accf74222a30ca448a697fb49.jpg",
      "result": [
        {
          "status": 200,
          "originFilename": "医疗住院发票示例.jpg",
          "cosPath": "scnetAPIService/20260101/afcbc98accf74222a30ca448a697fb49.jpg",
          "fileIndex": 1,
          "cutIndex": 0,
          "coordinate": [],
          "classifyCode": "",
          "confidence": 0.9473,
          "elements": {
            "title": "山东省医疗住院收费票据(电子)",
            "invoiceCode": "37370137010",
            "invoiceNo": "0002000565",
            "payerName": "金历科",
            "payerAccount": "370103701037010",
            "checkCode": "f379af",
            "invoiceDate": "2021-10-22",
            "totalAmountUpper": "柒仟肆佰捌拾肆元壹角",
            "totalAmountLower": "7,484.10",
            "payeeName": "山东大学齐鲁医院",
            "checker": "20211",
            "payee": "20211",
            "businessSerialNo": "202110152110101",
            "medicalRecordNo": "20211015211",
            "inpatientNo": "202110152110000",
            "inpatientDept": "化疗五(中心五)",
            "admissionTime": "20211015-20211015",
            "medicalOrgType": "综合医院",
            "insuranceType": "职工医保",
            "insuranceNo": "370103701037037010",
            "gender": "女",
            "poolFundPay": "7119.26",
            "personalAccountPay": "151.26",
            "personalCashPay": "213.10",
            "personalSelfPay": "364.36",
            "personalSelfExpense": "0.00",
            "itemDetails": [
              {
                "itemName": "化验费",
                "itemAmt": "829.80"
              },
              {
                "itemName": "西药费",
                "itemAmt": "6,402.72"
              },
              {
                "itemName": "护理费",
                "itemAmt": "30.00"
              },
              {
                "itemName": "治疗费",
                "itemAmt": "50.00"
              },
              {
                "itemName": "一般诊疗费",
                "itemAmt": "48.00"
              },
              {
                "itemName": "卫生材料费",
                "itemAmt": "73.58"
              },
              {
                "itemName": "床位费",
                "itemAmt": "50.00"
              }
            ]
          },
          "stamps": []
        }
      ]
    }
  ]
}
```

```json
{
  "code": "0",
  "msg": "success",
  "data": [
    {
      "traceId": "202604010000020",
      "originalFilename": "医疗费用结算单示例.jpg",
      "cosPath": "scnetAPIService/20260101/d122e94922a84d0f9b1253dccf1a2265.jpg",
      "result": [
        {
          "status": 200,
          "originFilename": "医疗费用结算单示例.jpg",
          "cosPath": "scnetAPIService/20260101/d122e94922a84d0f9b1253dccf1a2265.jpg",
          "fileIndex": 1,
          "cutIndex": 0,
          "coordinate": [],
          "classifyCode": "",
          "confidence": 0.9473,
          "elements": {
            "title": "北京大学附属北京极地医院北京市医疗保险住院结算单",
            "institutionCode": "H9814131",
            "institutionName": "北京大学附属北京极地医院",
            "hospitalLevel": "三甲医院",
            "patientName": "赵德柱",
            "gender": "男",
            "idNumber": "510687199206253019",
            "personnelCategory": "居民 (成年)",
            "socialSecurityCardNumber": "89890913731",
            "settlementTime": "2024-06-25",
            "printTime": "2026年06月25日",
            "insuranceType": "城乡居民医疗保险",
            "insuredRegion": "北京市",
            "medicalRegion": "西城区",
            "settlementId": "6120779013",
            "admissionNumber": "13987410937",
            "admissionMethod": "新入院",
            "dischargeDepartment": "普外科",
            "primaryDiagnosis": "囊结石半慢性胆囊炎",
            "secondaryDiagnosis": "脂肪肝中度, 前列腺钙化灶",
            "admissionDate": "2024-06-13",
            "dischargeDate": "2024-06-18",
            "hospitalizationDays": "5",
            "totalAmountUpper": "叁萬肆仟伍佰陆拾柒元陆角伍分",
            "totalAmountLower": "34567.65",
            "medicalCoveredAmount": "37983.08",
            "personalSelfExpense": "2338.98",
            "aboveLimitSelfPayAmount": "89.07",
            "deductible": "2000",
            "totalFundPay": "32180.23",
            "pooledFundPay": "32180.23",
            "largeMutualAidFundPay": "0.00",
            "retireeSupplFundPay": "0.00",
            "employerSupplFundPay": "0.00",
            "disabledVeteranSubsidyPay": "0.00",
            "criticalIllnessPay": "0.00",
            "medicalAssistancePay": "0.00",
            "civilServantSubsidyPay": "0.00",
            "otherFundPay": "0.00",
            "selfPayCategoryOne": "3210.89",
            "selfPayCategoryTwo": "8799.87",
            "personalCashPay": "15799.87",
            "personalAccountPay": "0.00"
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
- `识别结果位于 data[0].result[0].stamps 中`
- `不同 ocrType 返回的 stamps 字段不同，详见 assets/templates/fields-summary.md`
