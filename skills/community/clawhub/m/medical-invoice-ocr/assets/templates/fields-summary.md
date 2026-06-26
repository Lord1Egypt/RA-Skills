# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## MEDICAL_INVOICE (医疗发票)
- `title`: 标题
- `invoiceCode`: 发票代码
- `invoiceNo`: 发票号码
- `invoiceDate`: 开票日期
- `checkCode`: 校验码
- `payerName`: 交款人
- `payerAccount`: 交款人统一社会信用代码
- `payeeName`: 收款单位
- `totalAmountUpper`: 合计金额(大写)
- `totalAmountLower`: 合计金额(小写)
