# 各识别类型的字段说明（elements 内容）

根据 ocrType 不同，返回的 `elements` 对象包含以下字段：

## MOBILE_PAYMENT_BILL (移动支付账单)
- `title`: 标题
- `transAmount`: 交易金额
- `transStatus`: 交易状态
- `transDate`: 交易时间
- `goods`: 商品
- `merchantName`: 商户全称
- `acquiringInstitution`: 收单机构
- `transType`: 交易方式
- `transNo`: 交易单号
- `merchantNo`: 商户单号
- `remarks`: 备注
- `refundNo`: 退款单号
