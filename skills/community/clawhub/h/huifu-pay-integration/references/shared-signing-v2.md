# V2 签名规则

这份文档只保留当前 Skill 包真正共用的签名规则，不绑定某一种语言。

## 适用方式

- 托管支付默认由 `dg-java-sdk` 或官方 PHP SDK `huifurepo/dg-php-sdk` 落地
- 聚合支付默认由 `dg-lightning-sdk` 或官方 PHP SDK `huifurepo/dg-php-sdk` 落地
- 如果接入方自行封装 HTTP 请求，签名逻辑仍要遵守本文件

## 请求外层结构

```json
{
  "sys_id": "调用方 huifu_id",
  "product_id": "汇付分配的产品号",
  "sign": "签名结果",
  "data": {
    "业务字段": "值"
  }
}
```

关键点只有一条：

- 只对 `data` 做签名

## 请求签名规则

1. `data` 必须是 JSON 对象，不是 JSON 字符串。
2. 只对 `data` 第一层字段参与签名。
3. 字段名按 ASCII 字典序排序。
4. 多层对象如果存在，按 JSON 字符串传入，不参与内层排序。
5. 使用商户 RSA 私钥按 `SHA256WithRSA` 签名。
6. 签名结果 Base64 编码后放入 `sign` 字段。

## 同步返回验签

1. 取返回里的 `data`
2. 按 ASCII 字典序排序第一层字段
3. 用汇付 RSA 公钥验签

## 异步回调验签

- 不需要重新排序
- 直接对回调里的原始业务数据体验签
- 业务数据体常见字段为 `resp_data`，少数配置类回调使用 `data`

## 与控台 Webhook 的边界

本文件只适用于 API 请求、同步响应和接口 `notify_url` 回调。

控台 Webhook 不使用 API RSA 密钥体系。Webhook 配置终端密钥后，接收端应按 `shared-webhook-signing.md` 使用原始事件体拼接终端密钥做 MD5 校验。

不要把 Webhook 终端密钥当作 API 加签私钥，也不要用汇付 RSA 公钥校验 Webhook。

## 建模规则

文档里出现 `String(JSON Object)` 或 `String(JSON Array)` 时，含义是：

- SDK 边界是字符串
- 业务层不应直接手拼裸 JSON 字符串

更稳妥的做法是：

1. 业务层先建对象
2. 先做字段校验
3. 再统一序列化
4. 最后把序列化结果塞进 SDK 或 HTTP 请求

## 在当前 Skill 包里的落地位置

- PHP 业务默认入口以官方 `huifurepo/dg-php-sdk` 为准
- 当前 Skill 包不再内置 PHP 签名模板资产
- 绕开官方 SDK 时，应按本节规则实现 JSON 规范化与 RSA 签名，并通过真实验签或官方联调结果验证
- 需要和请求头一起核对时，再读 `references/shared-request-header-policy.md`

## 不应该混进来的内容

- Java 的 setter 细节
- Spring Boot 或 Laravel 的配置写法
- 某个语言的 SDK 类名和包路径

这些都应放到对应产品线或语言落地说明里。
