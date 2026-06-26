# 托管支付常见问题汇总

## 收银台页面问题

**Q：收银台页面白屏/无法跳转？**
A：检查以下几点：
1. 确认 `jump_url` 是否正确获取 — 预下单成功后返回，用于跳转收银台
2. H5/PC 场景使用 `window.location.href = jump_url` 或 HTTP 302 重定向
3. 确认浏览器未拦截弹窗（部分浏览器会拦截 `window.open`）
4. 检查网络环境，收银台页面需要访问汇付 CDN 资源

**Q：callback_url 设置了但支付后不生效？**
A：`callback_url`（前端回调地址）仅在 **H5/PC** 场景生效。小程序场景支付完成后由小程序自身控制页面跳转，不会使用 callback_url。确认 callback_url 为完整 URL（含 `https://`）。

## 小程序支付问题

**Q：小程序唤起支付失败？**
A：
- **支付宝小程序**：确认 scheme_code 正确获取并传入支付宝 SDK
- **微信小程序**：确认返回的 gh_id + path 正确，且微信小程序已关联商户号
- 检查小程序环境是否已在汇付后台完成配置（appid 绑定）
- 联调环境需使用联调专用的小程序配置

## 预下单问题

**Q：预下单成功但用户无法支付？**
A：最常见原因是 `time_expire`（交易失效时间）已过期。默认 10 分钟，预下单到用户实际支付间隔过长会导致订单超时。解决方案：
1. 适当延长 `time_expire`（格式 `yyyyMMddHHmmss`）
2. 超时后重新调用预下单接口生成新订单

**Q：预下单返回成功但 jump_url 为空？**
A：检查 `pre_order_type` 是否正确设置（1=H5/PC、2=支付宝小程序、3=微信小程序、4=抖音直连）。不同类型返回的跳转信息字段不同，抖音直连还要确认 `dy_data`、`busi_scene` 和真实客户端 IP。

## SDK 使用问题

**Q：Java 初始化时产品号 setter 应该用哪个？**
A：以最新 `dg-java-sdk 3.0.38` 源码为准，`MerConfig` 使用 `setProductId(...)`。不要再生成旧文档中的 `setProcutId(...)`。

```java
// ✓ dg-java-sdk 3.0.38
config.setProductId("YYZY");
```

**Q：Spring Boot 3.x 启动报错 javax 相关异常？**
A：先核对项目实际安装的 `dg-java-sdk` 版本和依赖树。当前 `3.0.38` 源码未检出 `javax.validation` 注解；如果项目仍因历史版本或传递依赖报 `javax.validation` 缺失，再补兼容依赖：

```xml
<dependency>
    <groupId>javax.validation</groupId>
    <artifactId>validation-api</artifactId>
    <version>2.0.1.Final</version>
</dependency>
```

或在 Spring Boot 3.x 中排除 SDK 的 validation 依赖，手动处理参数校验。

**Q：退款调用 `setOrgReqSeqId()` 编译报错？**
A：退款接口的 `org_req_seq_id` 字段**没有独立的 setter**，必须通过 `extendInfoMap` 传入。详见 `references/hostingpay-refund.md`。

```java
// ✗ 编译错误
request.setOrgReqSeqId("20240514...");

// ✓ 正确
Map<String, Object> extendInfoMap = new HashMap<>();
extendInfoMap.put("org_req_seq_id", "20240514...");
request.setExtendInfo(extendInfoMap);
```

## 异步通知问题

**Q：异步通知收不到？**
A：排查步骤：
1. **公网可达性** — `notify_url` 需是公网可访问的 `http/https` 地址；生产环境建议使用 HTTPS，本地联调可使用 ngrok/frp 等内网穿透工具
2. **IP 白名单** — 确认服务器防火墙/安全组已放行汇付通知 IP 段（见 `references/hostingpay-java-tech-spec.md` 异步通知 IP 白名单章节）
3. **5 秒内响应** — 接收通知后必须在 5 秒内返回 `RECV_ORD_ID_` + req_seq_id，否则汇付会重试（最多 3 次）
4. **HTTPS 证书** — 如果使用 HTTPS，确认 SSL 证书有效且未过期
5. **POST 请求** — 汇付以 POST 方式发送通知，确认接口支持 POST

**Q：异步通知重复收到？**
A：汇付会在未收到正确响应时重试。以 `hf_seq_id` 为幂等键，收到重复通知时跳过已处理的交易。确保返回格式正确：`RECV_ORD_ID_` + req_seq_id（注意下划线）。

## 对账单问题

**Q：对账单查询接口返回的文件格式？**
A：常规账单一个链接通常对应一个压缩文件，压缩包内多为 csv。`SETTLE_FUND_BILL` 模板为 `.xlsx`，不要把所有账单都按 csv 解析。单个文件超过 400,000 条时会拆分为多个 csv。

**Q：对账单什么时候适合下载？**
A：最新产品介绍口径建议按跑批节奏取数：交易/分账文件 03:00 跑批后建议 12:00 再取，出金对账单 10:30 跑批后一小时，结算对账单 17:00 跑批后一小时。

**Q：对账单能查多久以前的数据？**
A：接口当前支持 1 年内账单下载；控台下载暂未见时间限制说明。
