# 托管支付预下单快速接入


## 目录

- 这份文档解决什么问题
- 细分文档
- 场景选择
- 官方开发指引确认的接入前置项
- 端到端支付流程
- 快速接入（H5/PC 场景）
- 额外环境变量
- 常见问题

覆盖四种预下单场景：H5/PC 网页支付、支付宝小程序、微信小程序、抖音直连。开发者接入汇付支付最高频的第一个接口。

> **前置依赖**：首次接入请先完成 `references/hostingpay-base.md` 的 SDK 初始化。

> **编码约束**：开始写 Controller / DTO 前，先看 `references/hostingpay-customer-preparation.md` 和 `references/hostingpay-payload-construction.md`。`hosting_data`、`biz_info`、`wx_data` 这类字段在业务层应保持对象形态，做完校验后再序列化给 SDK。

## 这份文档解决什么问题

调用汇付预下单接口创建支付订单，获取支付跳转链接（`jump_url`）或小程序拉起参数，引导用户完成支付。

## 细分文档

- `references/hostingpay-preorder.md`
- `references/hostingpay-preorder-h5-pc.md`
- `references/hostingpay-preorder-h5-pc-request.md`
- `references/hostingpay-preorder-h5-pc-channel.md`
- `references/hostingpay-preorder-h5-pc-response.md`
- `references/hostingpay-preorder-h5-pc-response-channel.md`
- `references/hostingpay-preorder-h5-pc-errors.md`
- `references/hostingpay-preorder-alipay-mini.md`
- `references/hostingpay-preorder-wechat-mini.md`
- `references/hostingpay-preorder-douyin-direct.md`
- `references/hostingpay-preorder-php-scenarios.md`

## 场景选择

| 用户支付方式 | pre_order_type | 参考文档 |
|------------|---------------|---------|
| H5 手机网页 / PC 网页 | `1` | `references/hostingpay-preorder-h5-pc.md` |
| 支付宝小程序 | `2` | `references/hostingpay-preorder-alipay-mini.md` |
| 微信小程序 | `3` | `references/hostingpay-preorder-wechat-mini.md` |
| 抖音直连 | `4` | `references/hostingpay-preorder-douyin-direct.md` |

## 官方开发指引确认的接入前置项

- H5 / PC 场景：先在合作伙伴控台创建托管项目，启用实际要展示的支付方式，并留存 `project_id`。
- H5 / PC 微信支付：先配置微信授权域名 `api.huifu.com/hostingH5/`。
- 微信小程序场景：先完成小程序托管授权、代码发布和 appid 绑定，拿到真实应用 ID `seq_id`。
- 微信小程序拆单支付：不是普通字段开关，需先特批并开通权限。
- 抖音直连场景：确认抖音开放平台应用、`dy_data.sub_appid`、`busi_scene` 和真实客户端 IP；可复用托管预下单 request，但必须固定 `pre_order_type=4`，不要按 H5/PC `pre_order_type=1` 场景处理。
- `notify_url` 需满足官方约束：`http/https`、不重定向、不带参数、自定义端口在 `8000-9005`、收到回调后返回 `200`。

## 端到端支付流程

预下单只是支付链路的第一步，完整流程如下：

```
① 预下单（当前文档链路）
   调用 preorder 接口 → 获得 jump_url → 保存 req_seq_id + req_date
       ↓
② 用户支付
   H5/PC：window.location.href = jump_url
   小程序：scheme_code 或 gh_id + path 拉起支付
       ↓
③ 接收异步通知
   汇付 POST 到 notify_url → 5 秒内返回 RECV_ORD_ID_{req_seq_id}
   幂等键：hf_seq_id → 详见 `references/hostingpay-async-webhook.md`
       ↓
④ 二次查询确认（references/hostingpay-query.md）
   trans_stat=P 时轮询：间隔 5 秒，最多 30 次
       ↓
⑤ 退款（可选，references/hostingpay-refund.md）
   trans_stat=S 后可发起退款
```

## 快速接入（H5/PC 场景）

### 1. 构建请求

```java
ObjectMapper objectMapper = new ObjectMapper();

V2TradeHostingPaymentPreorderH5Request request = new V2TradeHostingPaymentPreorderH5Request();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setTransAmt("1.00");
request.setGoodsDesc("商品描述");
request.setPreOrderType("1");
```

### 2. 设置托管参数和扩展参数

```java
// hosting_data：先构造成完整对象，再统一序列化
ObjectNode hostingData = objectMapper.createObjectNode();
hostingData.put("project_title", "项目名称");
hostingData.put("project_id", "项目ID");
hostingData.put("callback_url", "https://your-domain.com/callback");
request.setHostingData(hostingData.toString());

// biz_info：不要直接手写裸字符串，先把对象树补完整
ObjectNode payerCheckWx = objectMapper.createObjectNode();
payerCheckWx.put("real_name_flag", "Y");
payerCheckWx.put("limit_payer", "ADULT");

ObjectNode personPayer = objectMapper.createObjectNode();
personPayer.put("name", "张三");
personPayer.put("cert_type", "IDENTITY_CARD");
personPayer.put("cert_no", "加密后的证件号");

ObjectNode bizInfo = objectMapper.createObjectNode();
bizInfo.set("payer_check_wx", payerCheckWx);
bizInfo.set("person_payer", personPayer);

// 扩展参数：统一放到 extendInfoMap，复杂对象先序列化
Map<String, Object> extendInfoMap = new HashMap<>();
extendInfoMap.put("notify_url", "https://your-domain.com/notify");
extendInfoMap.put("delay_acct_flag", "N");
extendInfoMap.put("biz_info", objectMapper.writeValueAsString(bizInfo));
request.setExtendInfo(extendInfoMap);
```

### 2.1 本地参数校验建议

在客户自己的接口层先做校验和拦截：

- 必填字段：`huifu_id`、`trans_amt`、`goods_desc`、`pre_order_type`
- 条件必填：指定 `trans_type` 时校验 `hosting_data.request_type`
- 对象完整性：只要决定传 `biz_info`、`acct_split_bunch`、`terminal_device_data`、`largeamt_data`，就把其业务必需子字段补齐
- 来源校验：`project_id`、`notify_url`、`callback_url`、`fee_sign`、`devs_id`、`seq_id` 没有真实来源时不要生成请求
- URL 校验：`notify_url` 需符合官方回调地址规则，`callback_url` 仅作前端回跳，不作为支付成功判定

### 3. 发起请求并处理响应

```java
Map<String, Object> response = BasePayClient.request(request, false);
String respCode = (String) response.get("resp_code");
if ("00000000".equals(respCode)) {
    String jumpUrl = (String) response.get("jump_url");   // 支付跳转链接
    String reqSeqId = (String) response.get("req_seq_id"); // 务必保存！
    String reqDate = (String) response.get("req_date");    // 务必保存！
}
```

### 4. 前端跳转

```javascript
// H5/PC 直接跳转到汇付收银台
window.location.href = jumpUrl;
```

完整参数说明和 JSON 示例见 `references/hostingpay-preorder-h5-pc.md`。

## 额外环境变量

除 `references/hostingpay-base.md` 中列出的 4 个基础变量外，预下单还需要：

| 变量 | 说明 |
|------|------|
| `HUIFU_NOTIFY_URL` | 支付结果异步通知地址 |
| `HUIFU_PROJECT_ID` | 托管项目 ID |
| `HUIFU_PROJECT_TITLE` | 托管项目名称 |
| `HUIFU_CALLBACK_URL` | 支付完成后前端回调地址 |

这些环境变量只覆盖全局固定配置。像 `sub_openid`、`seller_id`、`devs_id`、`person_payer.cert_no`、`payer_client_ip` 这类运行时或场景专属值，仍然需要客户业务侧单独准备。

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `jump_url` 为空 | `resp_code` 非 00000000，预下单失败 | 检查必填参数和商户配置 |
| 流水号重复 (99010002) | `req_seq_id` 当天不唯一 | 使用 `SequenceTools.getReqSeqId32()` |
| 收不到异步通知 | notify_url 不可公网访问 | 检查 URL 可达性、端口范围 8000-9005 |
| 支付宝/微信拉起失败 | 小程序配置不正确 | 检查对应场景文档中的专属参数 |
