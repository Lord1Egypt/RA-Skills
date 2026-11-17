# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## INTERNATIONAL_BILL (国际汇票)
- `draftNumber`: 汇票号码
- `draftDate`: 出票日期
- `amount`: 汇票金额
- `amountInWords`: 汇票金额大写
- `payeeName`: 收款人名称
- `draweeName`: 付款行/受票人
- `draftTenor`: 汇票期限
- `lcNumber`: 信用证号码
- `issueDate`: 信用证开证日期
- `issueBank`: 信用证开证行
- `drawer`: 出票人


