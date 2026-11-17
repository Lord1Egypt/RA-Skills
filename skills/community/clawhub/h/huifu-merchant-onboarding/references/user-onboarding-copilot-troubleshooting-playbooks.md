# 用户开户故障排查手册

## 路由或 ID 被拒绝

1. 记录实际 URI，确认是 `/v2/user/*` 而非相似 `/v2/merchant/*`。
2. 在领域层确认 `userHuifuId`、`merchantHuifuId/channelHuifuId`、`sys_id` 的角色。
3. 业务入驻核对 `data.huifu_id` 是用户号、`upper_huifu_id` 是上级主体号。
4. 开户接口确认没有为请求头兼容额外加入 `data.huifu_id`。
5. 图片上传若使用用户号，立即停止并改按图片接口直属商户号边界处理。

## 条件字段校验失败

1. 从完整字段目录按父路径定位字段，不按叶名搜索后合并。
2. 核对 Y/N/C 及说明条件：证件有效期、国籍、短信登录名、卡类型、费率、电子回单签约人。
3. 删除目标接口示例中参数表未定义的键：用户业务入驻 `card_info` 的 `bank_code/branch_name`。个人开户当前示例已删除旧版 `operator_id`，正式 DTO 仍不得加入该键；企业开户的 `operator_id` 则是正式字段，不能误删。
4. 不用空字符串满足 SDK required；通过 SDK exact-key 能力和探针验证最终 wire。

## JSON 类型或解析失败

1. 先保存脱敏后的父字段类型与长度，不记录敏感正文。
2. 只对合同标明 String(JSON) 的父字段解/编码一层。
3. 对 `file_list`、`elec_card_list`、审核 `resp_business` 和公共返回 `data` 按 `user-onboarding-platform-contracts.md` 的 wire 矩阵逐层编码/解码；详情 `resp_code` 当前正式长度已统一为8位。
4. 未命中已登记冲突时保留脱敏类型证据，按 `shared-overview.md` 给出对应官方文档及咨询建议；用 TODO/配置隔离有疑义的转换，继续已明确部分，不猜测也不等待答复才开始整体开发。

## 审核或配置状态不一致

分别记录同步业务码、审核状态、配置类型结果、银行状态和申请单号。`S`、`Y` 只解释所在完整路径；不要以一个成功覆盖其他层。申请状态接口只补偿非同名对公卡审核。

## 没收到异步消息

确认是否为支持接口异步的用户业务入驻或用户业务入驻修改、是否实际传入 `async_return_url`，并检查网络入口和脱敏审计。接口通知必须使用配置类 `data`、原始字符串免排序 RSA 验签、HTTP 200 + `RECV_ORD_ID_` + `req_seq_id`；核对5秒处理预算、超时/500-599重试及幂等记录。不要改用控台 Webhook 协议，也不要通过重复提交制造回调。

## SDK 调用路径异常

如果产物没有使用对应语言的官方 Request/Client，立即停止并替换为官方 SDK 调用；不得生成 `HttpClient`、OkHttp、Guzzle、curl 或自实现 HTTP+签名客户端。通用 Java 3.0.41 使用默认 TLS 工厂；PHP 2.0.31 本地源码仍关闭证书校验，此处仅作非阻断提醒，不要求先取得修复证明或官方答复；继续官方 SDK，可建议开发者查文档或咨询汇付官方、汇付开发者交流沟通群。PHP 仍需独立 DEBUG 启动检查，在加载 SDK 前固定 `DEBUG=false`；不把继续开发说成 TLS 风险已修复。
