# 用户开户 V2 签名与验签

## 已确认范围

九份接口页确认请求与公共响应 `sign:String(512) Y`，业务入驻及其修改的异步外层另声明 `sign`。接入方补充并已核验伙伴平台公共原文：[加签验签](https://paas.huifu.com/partners/start/api_v2jqyq.md)、[获取密钥](https://paas.huifu.com/partners/start/guide_gsycshq.md)、[异步消息简介](https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md)。

## 实现规则

- 请求只签 `body.data`：第一层实际传递字段按字段名 ASCII 升序排序，字段名区分大小写；嵌套 String(JSON) 的字符串内部不排序。排序后的 UTF-8 字符串使用商户私钥执行 `SHA256WithRSA`，签名后不得修改任何业务值或嵌套字符串。
- 同步响应只验 `response.data`：第一层按同样规则排序后，使用汇付公钥执行 `SHA256WithRSA` 验签；先验签，再读取或解码敏感业务数据，验签失败不得降级为业务失败码。
- 异步通知保存收到的原始 `data` 字符串，使用汇付公钥直接验签，不排序，也不得先反序列化再重新序列化；验签通过后才解码 String(JSON)。
- 出站请求使用锁定官方 SDK 实现上述规则；自行实现的入站通知验签代码须用公共指南测试向量验证序列化、中文、斜杠、空值和大小写行为，不借此生成手写出站 HTTP 客户端。
- 仅字段合同明确为 `String(JSON Object)` / `String(JSON Array)` 时序列化为字符串；原生 `Object` / `Array` 保持原生类型，不因嵌套或旧版类型而统一字符串化。
- 本轮保持 RSA。已核验 SDK 提供 SM2 不等于开户 API 已取得对应算法授权；Python `2.0.28` 初始化使用 `sign_type="RSA", jpt_x_skill_source=skill_source`，不得用第五位置参数传来源。实际项目版本的构造器与算法差异按 `user-onboarding-shared-server-sdk-matrix.md` 提醒核对，不阻断已明确部分。
- 私钥只从服务端密钥管理系统或受控密钥挂载读取，不进入源码、环境展示、前端、日志、异常文本或回答示例。

## 加密与密钥角色

- 汇付公钥：验证同步响应/异步通知，并加密接口明确要求加密的请求敏感字段。
- 商户私钥：请求加签，并解密接口明确返回的密文敏感字段。
- 仅在具体字段说明要求时执行 RSA 加解密；不能仅凭“手机号/卡号/证件号”名称对九接口全部字段盲目加密。

接口通知的 POST、UTF-8、ACK、超时、重试和幂等合同读取 `user-onboarding-platform-contracts.md`；控台 Webhook 是独立协议，不使用本页 RSA 通知合同。
