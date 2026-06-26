# Document Type Identification Reference

## Supported Document Types

| Type | Aliases | Key Patterns |
|------|---------|---------------|
| invoice | 发票, 增值税发票, 普通发票, 电子发票 | 发票号, 价税合计, 销方, 购方, 开票日期 |
| contract | 合同, 协议书, agreement | 甲方, 乙方, 签订日期, 违约条款 |
| receipt | 收据, 小票, 凭据 | 收款方, 消费, 流水号 |
| bank_statement | 银行对账单, 银行流水 | 借方, 贷方, 余额, 对方账户 |
| license | 营业执照, 经营许可证 | 统一社会信用代码, 法定代表人, 注册资本 |
| id_card | 身份证, 护照, 证件 | 姓名, 性别, 公民身份号码 |
| express | 快递单, 运单, 物流单 | 运单号, 发件人, 收件人 |
| generic | 通用, 其他, 文档 | No specific patterns |

## Identification Algorithm

1. **User hint priority**: If user provides a hint (e.g., "发票"), use it directly
2. **Keyword scoring**: Count keyword matches for each type
3. **Confidence threshold**: Require at least 2 keyword matches to confirm a type
4. **Fallback**: Default to "generic" if no type meets confidence threshold

## Field Extraction by Type

### Invoice (发票)
- 发票号, 日期, 金额, 买方, 卖方, 商品明细, 税率, 发票代码, 备注

### Contract (合同)
- 合同号, 签订日期, 到期日期, 金额, 甲方, 乙方, 地址, 联系人, 违约条款, 解除条款, 付款条件

### Receipt (收据)
- 日期, 金额, 收款方, 消费内容, 明细项目, 小费

### Bank Statement (银行对账单)
- 日期, 交易金额, 对方账户, 余额, 交易类型, 摘要

### License (营业执照)
- 统一社会信用代码, 公司名称, 法人, 注册资本, 注册地址, 经营范围

### ID Card (身份证/护照)
- 姓名, 性别, 出生日期, 国籍, 证件号码, 有效期

### Express (快递单)
- 运单号, 发件人, 收件人, 地址, 重量, 运费
