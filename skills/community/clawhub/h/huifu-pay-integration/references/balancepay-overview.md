# 余额支付接入

## 路由与边界

余额支付使用通用斗拱 V2 API；不使用聚合 V4 下单、托管预下单或 checkout-js。开户、余额支付业务开通及用户分级配置交给 `$huifu-merchant-onboarding`；交易执行与付款关系、短信验证由本 Skill 处理。

| 目标 | 原子 reference |
| --- | --- |
| 支付 | `balancepay-pay.md` |
| 查询支付结果 | `balancepay-query.md` |
| 退款 | `balancepay-refund.md` |
| 查询退款结果 | `balancepay-refund-query.md` |
| 手续费试算 | `balancepay-fee-calc.md` |
| 付款关系 ADD/DEL | `balancepay-pay-relation.md` |
| 发送短信验证码 | `balancepay-sms.md` |

字段或代码任务同时读取 `payment-complete-field-catalog.md`、`balancepay-field-contracts.md`；按语言选择 `balancepay-java-adapter.md`、`balancepay-php-adapter.md` 或 `balancepay-python-adapter.md`，SDK 专属类与通用入口见 `balancepay-sdk-matrix.md`。

## 按条件组织调用

1. 核对出款方、入账方、账户类型及余额支付能力；开户不等于业务已开通。需要用户开户或调整配置时交给进件 Skill，再返回交易流程。
2. 只有须预先维护付款关系的商户才调用付款关系提交。提交成功后可能仍等待页面确认；检查每项提交结果。
3. 需要展示费用时调用手续费试算；它不是每笔支付的必经步骤，也不承诺最终实际手续费。
4. 采用 SMS 核验时先发送验证码，再在支付中设置 `verify_type=SMS` 和 `verify_value`。短信发送成功不是支付成功。
5. 提交余额支付并保存调用方原始流水、日期、出款方及全局流水。收到 LV3 用户密码验证 `jump_url` 时引导验证，跳转完成仍需确认交易结果。
6. 根据正式 `trans_stat` 判断结果，处理中或传输结果未知时先查询原交易，不自行生成新流水再次扣款。
7. 退款使用独立退款流水与原支付定位；退款查询定位原退款请求，不使用原支付流水代替。

异步通知仅在支付页声明的场景出现。退款、查询、试算、付款关系及短信页没有声明异步字段，不能自动套用支付通知。余额支付也没有本轮指定的关单接口。

## 终态与复查

同步支付通常为 `P/S/F`；支付查询及支付异步还声明灵活用工 `C=完成`。`C` 必须查看各 `acct_infos[]` 的分账状态，不能整体映射成成功。`resp_code=00000000` 表示接口业务处理完成，具体支付结果仍取交易状态；查询成功也只表示查询处理成功。

对已验证结果核对本地原订单的身份、金额、日期、流水及状态，再幂等更新。前端回跳、密码验证页面、短信结果和手续费试算都不能触发支付成功。

官网未明确的通知包装/验签/ACK、String 子表编码或示例冲突，按字段合同标记 `[需要官方确认]`；继续已明确的 SDK 调用与业务框架，未明确部分保留 TODO，不猜协议。

## 本地沙箱

现有冻结 `r1–r4` 沙箱不覆盖余额支付七接口。可以运行 SDK 请求构造、字段与回归检查；这些检查不证明真实资金交易、短信下发、商户权限或费率结果。

## 来源

七份官方接口原文冻结于 `2026-11-04`，逐页 URL/SHA 见 `official-payment-page-lock.md`；七接口共266个完整字段路径，父节点计入。
