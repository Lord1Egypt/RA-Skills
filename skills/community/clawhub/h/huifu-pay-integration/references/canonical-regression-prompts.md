# 最小回归 Prompt

这份文件随 Skill 分发，用于安装后快速复测主路径。完整回归仍以仓库级回归 Prompt JSON 为准。

## 使用方式

每个 Prompt 都要求回答中列出 3-5 份本轮实际使用的本地 references。不要把官网 URL 当作依据。

## Prompt 清单

### C01 首次接入

```text
第一次接汇付支付，我们只有一个普通 Java 服务端收款需求，不确定产品线。请用 $huifu-pay-integration 给我接入判断卡。
```

期望：推荐聚合支付，输出用户类型、产品线、阶段、技术栈、端形态、当前目标和还缺配置。

### C02 存量系统

```text
第一次接汇付，但这是现有商城项目，里面已经有 OrderService、PaymentService、NotifyController 和订单状态枚举。请用 $huifu-pay-integration 判断是不是存量项目并给改造建议。
```

期望：识别为存量业务系统首次接汇付，输出新增、保留、人工确认、落库字段、风险点和回归检查；不能因为“第一次接汇付”判成非存量，不直接替换原状态机。

### C03 checkout-js 已完成前置

```text
托管预下单和服务端查单已经跑通，现在只想接 checkout-js 前端按钮。请用 $huifu-pay-integration 给我下一步。
```

期望：直接进入 checkout-js、callback 和异步通知/最终确认链路；不重新列 quickstart、base、preorder、query 作为本轮阅读顺序。

### C04 参数检查

```text
我贴的请求里 time_expire 是昨天，req_seq_id 也跟上一笔一样。请用 $huifu-pay-integration 做参数检查。
```

期望：输出阻断结论，说明过期时间必须是未来时间且 `req_seq_id` 不能重复。

### C05 版本升级

```text
后续你们 Skill 更新了，我怎么更新本地这个 $huifu-pay-integration？它能不能主动提醒我升级？
```

期望：读取版本策略，说明当前本地版本、不能主动联网检查或推送升级，以及 Git 拉取、本地目录整体覆盖或内部发布包替换方式。

### C06 托管新增接口

```text
我要接抖音直连下单，另外还要查微信小程序拆单支付订单。请用 $huifu-pay-integration 给我阅读路径和字段边界。
```

期望：路由到抖音直连下单和拆单支付订单查询 reference；说明 `pre_order_type=4`、`dy_data`、`splitpay/query`，不能混用普通托管查单或 H5/PC `pre_order_type=1` 场景语义。

### C07 聚合字段更新

```text
我要做聚合支付合单交易关单和关单查询，还要拉取合并账单。请用 $huifu-pay-integration 告诉我关键字段边界。
```

期望：路由到聚合关单、关单查询和对账 reference；说明 `merge_flag=Y` 时用主单信息、非合单用子单信息；对账 `bill_type` 可用 `MERGE_BILL`，文件名需兼容 `file_name/file_Name`。

### C08 FAQ 权限与通道

```text
官网 FAQ 里有接口权限认证失败、数据权限认证失败，还有该路由下未配置可用通道。请用 $huifu-pay-integration 给我排查顺序。
```

期望：路由到商户进件/权限 FAQ 摘要和问题解决中心；说明接口权限查 `sys_id` 接口权限，数据权限查 `product_id`、`sys_id`、`huifu_id`、`upper_huifu_id` 和层级；路由问题查通道开通、`pay_channel`、`pay_scene`，不要传空 `channel_no`。
