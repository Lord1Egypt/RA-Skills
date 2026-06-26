# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## WITHDRAWAL_VOUCHER (支款凭证)
- `title`: 标题
- `currency`: 账别
- `fillDate`: 填单日期
- `voucherNo`: 凭证编号
- `payerName`: 支款人全称
- `payerAccount`: 支款人账号
- `payerBank`: 支款人开户行
- `payeeName`: 收款人全称
- `payeeAccount`: 收款人账号
- `payeeBank`: 收款人开户行
- `amountUpper`: 大写金额
- `amountLower`: 小写金额
- `usage`: 用途