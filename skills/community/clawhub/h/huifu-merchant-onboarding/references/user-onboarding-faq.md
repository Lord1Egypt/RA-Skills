# 用户开户 FAQ

## 已有 `huifu_id`，该用本 Skill 还是商户进件？

字段名不足以判断。多方分账/结算用户使用 `userHuifuId` 和 `/v2/user/*`；支付收单商户使用 `merchantHuifuId` 和 `/v2/merchant/*`。上下文不清楚时硬停确认实体。

## 企业/个人开户为什么不能传 `huifu_id`？

这两个接口用于创建新用户，正式请求参数没有 `data.huifu_id`。不能为 SDK 来源头兼容添加空值、调用主体号或其他用户号。

## 用户材料如何上传？

用户开户子域只消费图片接口返回的 `file_id`。图片上传 `data.huifu_id` 只支持直属商户号，不支持用户号；不要把开户返回的 `userHuifuId` 传入上传接口。需要上传时切换到本 Skill 的商户图片路由并遵守其图片边界。

## 用户申请状态查询能查开户或全部业务入驻吗？

不能。`/v2/user/apply/query` 官方范围仅是非同名对公结算卡审核，需要业务入驻返回的 `apply_no`。其他申请状态与补偿方式标记 `[需要官方确认]`。

## `file_list` 应发送数组还是 JSON 字符串？

当前企业/个人开户的类型列均为 String，说明为 jsonArray格式，按一层 String(JSON Array) 发送。不得因官网示例使用原生数组而改写正式字段合同。

## 同步成功是否表示业务入驻全部完成？

不表示。同步业务码、配置 `S/F`、审核 `Y/P/N` 和银行 `S/F` 是不同层。只有所需层次均达到对应成功条件，才能进入后续业务判断。

## 可以直接实现异步回调吗？

可以按伙伴平台公共异步规范实现：配置类接口使用 `data`，对原始字符串免排序执行 RSA 验签，处理成功返回 HTTP 200 与 `RECV_ORD_ID_` + `req_seq_id`，默认5秒超时，超时及500-599默认重试3次，并做状态感知幂等。必须联读 `user-onboarding-platform-contracts.md`，不能混用控台 Webhook；异步 `huifu_id` 的用户号/商户号角色仍不得猜测。

## Java/PHP 会因为 TLS 被硬停吗？

不会仅因本轮指定的既有 TLS 风险停止开发或联调代码生成。通用 Java 3.0.41 使用默认 TLS 工厂；PHP 2.0.31 的 `BsPayRequestV2.php` 仍设置 `CURLOPT_SSL_VERIFYPEER=false`，该事实作为非阻断提醒保留，不声称已修复，也不要求先取得修复证明。继续官方 SDK；疑问可查对应 SDK/官方文档，或咨询汇付官方、汇付开发者交流沟通群。字段疑义按 `shared-overview.md` 处理。PHP Demo/Composer loader 的 `DEBUG=true` 会记录私钥和完整报文，仍须在加载 SDK 前固定 `DEBUG=false`；不能用本轮 TLS 策略放宽日志/签验保护。
