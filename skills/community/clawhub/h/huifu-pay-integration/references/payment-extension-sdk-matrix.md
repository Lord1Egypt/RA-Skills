# 新增支付接口SDK矩阵

## 目录

- 精确入口
- 字段与传输
- 初始化与响应

## 精确入口

2026-11-04核对当前锁定的通用Java3.0.41、PHP2.0.31和Python2.0.28源码；未声称升级或完成生产联调。类名和路由不能只按中文标题选择。

| 接口 | Java/PHP类 | Python模块 | 路由 | SDK声明字段 |
| --- | --- | --- | --- | --- |
| 交易确认 | `V2TradePaymentDelaytransConfirmRequest` | `v2_trade_payment_delaytrans_confirm` | `/v2/trade/payment/delaytrans/confirm` | `req_date`, `req_seq_id`, `huifu_id`, `pay_type` |
| 交易确认查询 | `V3TradePaymentDelaytransConfirmqueryRequest` | `v3_trade_payment_delaytrans_confirmquery` | `/v3/trade/payment/delaytrans/confirmquery` | `org_req_date`, `org_req_seq_id`, `huifu_id` |
| 交易确认退款 | `V2TradePaymentDelaytransConfirmrefundRequest` | `v2_trade_payment_delaytrans_confirmrefund` | `/v2/trade/payment/delaytrans/confirmrefund` | `req_date`, `req_seq_id`, `huifu_id`, `org_req_date`, `org_req_seq_id` |
| 交易确认退款查询 | `V2TradePaymentDelaytransConfirmrefundqueryRequest` | `v2_trade_payment_delaytrans_confirmrefundquery` | `/v2/trade/payment/delaytrans/confirmrefundquery` | `huifu_id`, `org_req_date`, `org_req_seq_id`, `org_hf_seq_id` |
| 账户余额信息查询 | `V2TradeAcctpaymentBalanceQueryRequest` | `v2_trade_acctpayment_balance_query` | `/v2/trade/acctpayment/balance/query` | `req_date`, `huifu_id` |
| 账务流水查询 | `V2TradeAcctpaymentAcctlogQueryRequest` | `v2_trade_acctpayment_acctlog_query` | `/v2/trade/acctpayment/acctlog/query` | `req_seq_id`, `huifu_id`, `acct_date` |
| 账务流水汇总结果查询 | `无专属类，使用官方通用入口` | `官方通用入口` | `/v2/trade/acctpayment/acctlog/summary` |  |
| 主动取现 | `V2TradeSettlementEncashmentRequest` | `v2_trade_settlement_encashment` | `/v2/trade/settlement/encashment` | `req_date`, `req_seq_id`, `cash_amt`, `huifu_id`, `into_acct_date_type`, `token_no` |
| 资金代发 | `V2TradeSettlementSurrogateRequest` | `v2_trade_settlement_surrogate` | `/v2/trade/settlement/surrogate` | `req_seq_id`, `req_date`, `huifu_id`, `cash_amt`, `purpose_desc`, `province`, `area`, `bank_code`, `correspondent_code`, `bank_account_name`, `card_acct_type`, `bank_card_no_crypt`, `certificate_no_crypt`, `certificate_type`, `into_acct_date_type` |
| 出金交易查询 | `V2TradeSettlementQueryRequest` | `v2_trade_settlement_query` | `/v2/trade/settlement/query` | `huifu_id`, `org_req_date`, `org_hf_seq_id`, `org_req_seq_id` |
| 批量出金交易查询 | `V2TradeBatchtranslogQueryRequest` | `v2_trade_batchtranslog_query` | `/v2/trade/batchtranslog/query` | `huifu_id`, `begin_date`, `end_date` |
| 结算记录查询 | `V2MerchantBasicdataSettlementQueryRequest` | `v2_merchant_basicdata_settlement_query` | `/v2/merchant/basicdata/settlement/query` | `req_seq_id`, `req_date`, `huifu_id`, `begin_date`, `end_date`, `page_size` |
| DM取现额度查询 | `V2TradeSettlementEnchashmentDmamtQueryRequest` | `v2_trade_settlement_enchashment_dmamt_query` | `/v2/trade/settlement/enchashment/dmamt/query` | `huifu_id` |

## 字段与传输

专属类的Java完整包为 `com.huifu.bspay.sdk.opps.core.request`，PHP命名空间为 `BsPaySdk\request`，Python公开模块为 `dg_sdk.request`。Java使用对应setter和setExtendInfo，PHP使用setter和setExtendInfo，Python向生成Request属性赋值后调用post(extend_infos)。SDK声明集合只是生成类结构，不决定官网Y/N/C；其余正式字段走exact-key扩展，先拒绝覆盖已声明字段。

String(JSON Object/Array)按父路径编码；交易确认acct_split_bunch不能扁平放到顶层。是否必填、空字段是否应省略由原子接口的场景决定。Python专属Request先组装空字段，最终ApiRequest._build_request_info会删除空字符串、None、空列表和空字典；以最终签名/HTTP请求体核对，不能把post参数截图当成wire。request_tools的注释称补日期流水，但实现未补，调用方须显式提供。

账务流水汇总没有专属Request：Java使用 `BasePayClient.request(params, "v2.trade.acctpayment.acctlog.summary", false)`；PHP使用 `BsPayClient::postRequest` 数组入口，funcCode为 `v2/trade/acctpayment/acctlog/summary`、params为字段映射、tag=false；Python使用 `dg_sdk.DGTools.request_post("/v2/trade/acctpayment/acctlog/summary", payload)`。后者封装不接收need_sign等关键字，保留SDK默认签验；这些是官方通用入口，不是手写HTTP。

交易确认查询固定使用V3类和V3路由，不误用V2类。交易确认退款查询的JSON未定义响应，SDK返回类型不补充官网业务响应合同；汇总查询的同步/异步矛盾按原子页保留。

## 初始化与响应

代码任务必须补读 `shared-server-sdk-matrix.md` 的安全初始化与实际返回形状：Java在任何调用前全局关闭BasePay.debug；PHP在加载任何SDK文件前固定DEBUG=false，不使用会启用调试的Demo/Composer入口；Python MerConfig使用明确关键字，并绑定生产配置到DGClient。密钥仅从服务端安全配置读取。

通用Java已返回验签后的业务Map，不再get("data")；PHP先拒绝null/isError，再验证getRspDatas信封和data类型；Python业务数据仅在SDK验签成功后消费。未知响应保持适配点，不能以空对象冒充成功。

完整字段见 `payment-extension-complete-field-catalog.md`；分别按原子参考选择目标方向，不默认加载整份目录。

## 出金专属约束

六个出金接口均有上述三语言专属类。Java/PHP是源码路由和字段核验；Python另执行真实Request.post到最终_build_request_info的离线签名、来源头、空值清理和扩展覆盖探针，不声称已完成三语言出金网关联调。主动取现和出金查询虽信封表将data写为String(JSON)，SDK最终body.data是对象，不二次JSON编码。

银行卡代发的bank_card_no_crypt和certificate_no_crypt在Request外先用汇付系统公钥RSA加密：Java RsaUtils.encrypt、PHP BsPayTools::encrypt_with_rsa_pubkey、Python rsa_long_encrypt。Python错误可能以字符串返回，检查合法base64与RSA块长度，拒绝错误字符串，不记录敏感数据。SDK不会自动加密。

Java读取验签后业务Map；PHP拒绝null/isError后再读信封data；Python仅消费已验签的业务结果，未验签分支的原始信封不能当成成功。所有语言的扩展合并都可能覆盖已声明键，调用方必须先拒绝冲突。
