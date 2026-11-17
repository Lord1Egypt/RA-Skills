# 资金代发

官方来源：<https://paas.huifu.com/partners/api/doc/daifa/api_daifa_yhkdf.md>。来源快照：2026-11-04；SHA-256：`bc249fe82be276210bad46b40deee9842d8e91989c4a7924e653047acd52bae0`。

接口：`/v2/trade/settlement/surrogate`。方法：POST。

## 使用条件与请求

官方标题为银行卡代发，本页按用户名称资金代发索引。付款商户须已开通代发权限，代发向指定收款银行卡出金，不使用主动取现的token_no DTO。文档说明先通过控台充值或网银充值接口向商户基本账户入金；可指定基本户、现金户的acct_id，不填默认基本户。`huifu_id` 为付款商户；收款人资料、商户身份及业务权限不混同。

金额cash_amt以元计两位小数。`card_acct_type` 为E对公/P对私；对公的省份province+地区area与联行号correspondent_code二选一；bank_code在E时必填；certificate_type在P时必填。正式 `certificate_no_crypt` 仍Y，不能因certificate_type条件性自行改成N。到账 `into_acct_date_type` 为T0/T1/D1，不复制取现的D0/DM。

`bank_card_no_crypt`、`certificate_no_crypt` 使用汇付系统公钥RSA加密后传入；生成Request只透传，不自动加密。调用官方Java RsaUtils.encrypt、PHP BsPayTools::encrypt_with_rsa_pubkey 或Python rsa_long_encrypt，先检查返回状态、合法base64和密文长度等；Python异常可能返回非空错误字符串，不能只用truthy判断成功。不得记录明文或完整密文，不把签名当作敏感字段加密。

## 状态与通知

同步trans_stat为S/F/P；异步trans_status、acct_status（S/F/P/B）、channel_status（S/F/P）、msg_type（01通道/02账务）、re_exchange（Y已退汇）独立保存。B仅表示回账成功。先01后02、成功后退汇必须继续更新，不以一次S永久终结记录；外层成功或同步P不等于到账。未知状态优先级留TODO，通过出金查询核对，不重新代发。

正式异步表已公布外层 `sign:String(255) Y`，说明为“对报文整体签名”；`resp_data:String N` 说明为json格式，长度未公布。保留原始报文，先验证签名和交易归属再解码更新；待验签字符串构造、HTTP承载、ACK和重试协议未给出，[需要官方确认]，不可复制其他支付通知实现。通知与查单的状态字段名按方向保留。

## 示例与正式表

`bank_acct_three_in_one`、`mobile_no_crypt`、`risk_check_data` 仅出现于示例，未在正式请求表定义，不进入完整正式DTO，不猜类型和必填。若用户明确传入这些字段，标记TODO并确认合同后再发送，不静默丢弃。

## 完整字段与SDK

单字段类型/必填、完整DTO、响应或通知字段均按接口与方向读取 `payment-extension-complete-field-catalog.md` 中的“资金代发”，覆盖46条正式字段路径。代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`；专属类 `V2TradeSettlementSurrogateRequest`，Python模块 `v2_trade_settlement_surrogate`。扩展字段先拒绝覆盖SDK已声明字段，再经官方SDK发送；SDK合并本身不提供此保护。日期、流水、金额、账户和角色ID保持调用方值，来源头按实际参与的Skill确定。
