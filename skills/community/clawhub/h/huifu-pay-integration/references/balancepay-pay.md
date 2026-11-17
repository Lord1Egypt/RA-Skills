# 余额支付

官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpayzf.md>；本地快照 `2026-11-04`，官网更新时间 `2026-09-23`。

接口：`POST /v2/trade/acctpayment/pay`。适用于已开通余额支付功能的商户使用预存金额交易。完整90个字段路径及请求/响应/通知方向见 `payment-complete-field-catalog.md` 的“余额支付”。代码联读 `balancepay-field-contracts.md` 和对应语言 adapter。

## 请求

- 正式必填：`req_seq_id:String(128)`、`req_date:String(8)`、`out_huifu_id:String(32)`、`ord_amt:String(14)`、`acct_split_bunch:String(JSON Object)`、`risk_check_data:String(JSON Object)`。两个 JSON 字符串长度未给出，不得补猜上限。
- `huifu_id:String(32) N` 已废弃，新接入不建议使用；历史商户已经使用的，该值仍决定后续支付、查询、退款和交易确认接口的发起方定位。不得把它与出款方或入账方合并。
- `ord_amt` 为元、两位小数；`acct_split_bunch.acct_infos[].huifu_id` 为入账方，`acct_id` 可指定基本户/现金户，不填默认基本户。支付请求子项 `div_amt` 与 `percentage_div` 都是 N，按金额/百分比场景处理，不从响应 Y 标记反推请求必填。
- `percentage_flag=Y` 时分账百分比总和必须为100.00%。`is_clean_split=Y` 仅在百分比分账且手续费由出款方承担时起作用。不得把目录中的解码路径 `[]` 写进 wire key。
- `risk_check_data.transfer_type:String(2) Y`：01卡券推广、02卡券核销、03消费、04工资代发、05分润、06灵活用工。经纬度、基站地址、IP 三组至少填写一组；两项经纬度按同一组校验，分别遵守本页格式限制。
- `acct_channel` 默认 `HUIFU`，另支持 `ZXE`；中信E管家时 `fund_type` 条件必填。扣收规则为接口指定承担方时 `trans_fee_take_flag` 必填，枚举 `OUT/IN`。
- `verify_type` 仅声明 `SMS`；非空时 `verify_value` 必填。`delay_acct_flag` 默认 N；`imaxn_pay=SURETY_PAY` 表示延迟交易，字段拼写保持原文。
- LV3 用户参与交易时，`imax_pay_callback_url`、`notify_url` 按本页条件生效；不把密码验证跳转当成已扣款结果。

## 同步响应

`data` 外层为 JSON、N，`sign` 为必填。`trans_stat` 为 `P/S/F`；`jump_url` 在有 LV3 用户参与时返回，支付密码验证链接有效期5分钟。`acct_split_bunch` 为 String(JSON Object)，其中 `acct_infos` 为原生 Array；先解码父字符串，再解析子数组。

`00000000` 要结合 `trans_stat`，`00000100` 通过余额支付查询确认。已知传输失败不直接判交易失败，不重复发起扣款。

## 异步

只有灵活用工平台为汇优财的场景，或交易参与方有 LV3 用户且传入异步地址的场景，才有本页声明的通知。公共字段为 `resp_code/resp_desc/resp_data`；`resp_data` 正式为 String、长度空，正文另给其字段表，但没有声明 JSON 编码、签名位置或 ACK 合同。不能直接套用聚合/托管的通知包装；这些传输适配点留 TODO 并提示核对官方规范。

业务 `acct_split_bunch` 在异步方向为 Object，同步方向为 String。异步 `trans_stat=C` 仅表示完成，需检查每笔 `acct_infos[].trans_stat`；禁止把 C 等同 S。灵活用工分账金额、状态以本页规定的异步结果为准。

## 外部资料与冲突

中信资金类型触发 <https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx>；签验参考 <https://paas.huifu.com/open/doc/guide/#/api_v2jqyq>。未读取正文时说明需人工核验。

响应 `huifu_id` 发起方仍为 Y，而新接入请求该字段已废弃；后续查询必填发起方 ID，不能无依据推定等于 `out_huifu_id`。通知正文的灵活用工条件与请求 `notify_url` 的 LV3 专属说明也需保留为待确认差异。
