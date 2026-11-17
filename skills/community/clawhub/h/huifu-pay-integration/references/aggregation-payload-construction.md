# 聚合支付参数校验与 JSON 构造规范

> 聚合支付最容易被大模型写坏的地方有三个：一是 `trade_type` 驱动的条件必填没有校验，二是把 `method_expand` 错写成带支付类型包装 key 的对象，三是把交易能力扩展字段错包进 `tx_metadata`。这里统一约束接入方式。


## 目录

- 推荐的分层方式
- 必填、非必填、条件必填怎么处理
- 聚合支付里最常见的条件必填
- 建模规则
- 顶层字段边界
- 推荐代码形态
- 校验建议
- `method_expand` 构造约束
- `acct_split_bunch` 构造约束
- `terminal_device_data` 构造约束
- 补贴类顶层扩展字段构造约束
- 明确禁止的写法

## 推荐的分层方式

```
外部请求 DTO（按 trade_type 使用强类型嵌套对象）
        ↓
参数校验层（必填 / 条件必填 / 场景组合）
        ↓
Payload Builder（序列化 method_expand / acct_split_bunch / terminal_device_data / combinedpay_data / combinedpay_data_fee_info / trans_fee_allowance_info）
        ↓
dg-lightning-sdk Request
```

## 必填、非必填、条件必填怎么处理

| 类型 | 建议处理方式 |
|------|-------------|
| 必填 | API 层直接校验并拦截 |
| 非必填 | 有真实来源才传，不要为了“更完整”硬补 |
| 条件必填 | 依据 `trade_type` 或业务开关做组合校验 |

## 聚合支付里最常见的条件必填

| 条件 | 需要补充校验的字段 |
|------|------------------|
| `trade_type=T_JSAPI` / `T_MINIAPP` | `method_expand` 中微信对象的 `sub_appid`、`sub_openid`，且两者来源必须匹配 |
| `trade_type=T_MICROPAY` / `A_MICROPAY` / `U_MICROPAY` | `method_expand` 中的 `auth_code` |
| `trade_type=A_JSAPI` | `method_expand` 中 `buyer_id`、`buyer_logon_id` 二选一 |
| `trade_type=U_JSAPI` | `method_expand` 中 `user_id`、`customer_ip`，并按官方说明核对 `qr_code` |
| 传入 `acct_split_bunch` | `acct_infos`、接收方 `huifu_id`、金额 / 比例规则完整 |
| 反扫或设备报备场景 | `terminal_device_data` 中真实设备信息 |
| 使用报备机具 | `terminal_device_data.devs_id` |
| 传入 `trans_fee_allowance_info` | 补贴金额和活动来源完整 |

## 建模规则

### 规则 1：不要把复杂对象在 DTO 层建成 `String`

不推荐：

```java
public class CreateOrderCommand {
    private String methodExpand;
    private String terminalDeviceData;
}
```

推荐：

```java
public class CreateOrderCommand {
    private String tradeType;
    private WechatMethodExpand wechat;
    private AlipayMethodExpand alipay;
    private UnionpayMethodExpand unionpay;
    private AcctSplitBunch acctSplitBunch;
    private TerminalDeviceData terminalDeviceData;
    private List<CombinedpayData> combinedpayData;
    private CombinedpayDataFeeInfo combinedpayDataFeeInfo;
    private TransFeeAllowanceInfo transFeeAllowanceInfo;
}
```

### 规则 2：只在 SDK 边界序列化一次

不推荐：

```java
request.setMethodExpand("{\"<trade_type>\":{\"sub_openid\":\"...\"}}");
request.setTerminalDeviceData("{\"device_ip\":\"10.0.0.1\"}");
// 不要再构造 tx_metadata 包装层承载补贴、分账或设备字段
```

推荐：

```java
request.setMethodExpand(objectMapper.writeValueAsString(methodExpand));
request.setTerminalDeviceData(objectMapper.writeValueAsString(terminalDeviceData));
request.addExtendInfo("combinedpay_data", objectMapper.writeValueAsString(combinedpayData));
request.addExtendInfo("combinedpay_data_fee_info", objectMapper.writeValueAsString(combinedpayDataFeeInfo));
request.addExtendInfo("trans_fee_allowance_info", objectMapper.writeValueAsString(transFeeAllowanceInfo));
```

### 规则 3：对象出现就要保证子字段业务有效

如果业务决定传 `method_expand`、`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info`，就不能只给一个半截对象。要么不传，要么传可执行的完整结构。

## 顶层字段边界

| 字段 | 正确层级 | 说明 |
|------|---------|------|
| `trade_type` | 请求顶层字段 | 只负责选场景 |
| `method_expand` | 请求顶层字段 | JSON 内容就是当前场景自己的对象本身 |
| `acct_split_bunch` | 请求顶层字段 | Java SDK 有独立 setter |
| `terminal_device_data` | 请求顶层字段 | Java SDK 有独立 setter |
| `combinedpay_data` | 顶层扩展字段 | 通过 `request.addExtendInfo(...)` / `client.optional(...)` 注入 |
| `combinedpay_data_fee_info` | 顶层扩展字段 | 通过 `request.addExtendInfo(...)` / `client.optional(...)` 注入 |
| `trans_fee_allowance_info` | 顶层扩展字段 | 通过 `request.addExtendInfo(...)` / `client.optional(...)` 注入 |

`tx_metadata` 本身不作为请求字段上送。API 文档把它写成“交易能力扩展”时，按实际扩展能力直接传它下面的字段：`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info`。

## 推荐代码形态

```java
public TradePaymentCreateRequest buildRequest(
        CreateOrderCommand cmd,
        ObjectMapper objectMapper) throws JsonProcessingException {
    validate(cmd);

    TradePaymentCreateRequest request = new TradePaymentCreateRequest();
    request.setReqDate(cmd.getReqDate());
    request.setReqSeqId(cmd.getReqSeqId());
    request.setHuifuId(cmd.getHuifuId());
    request.setTradeType(cmd.getTradeType());
    request.setTransAmt(cmd.getTransAmt());
    request.setGoodsDesc(cmd.getGoodsDesc());

    Object methodExpand = buildMethodExpand(cmd);
    request.setMethodExpand(objectMapper.writeValueAsString(methodExpand));

    if (cmd.getAcctSplitBunch() != null) {
        request.setAcctSplitBunch(objectMapper.writeValueAsString(cmd.getAcctSplitBunch()));
    }
    if (cmd.getTerminalDeviceData() != null) {
        request.setTerminalDeviceData(objectMapper.writeValueAsString(cmd.getTerminalDeviceData()));
    }
    if (cmd.getCombinedpayData() != null) {
        request.addExtendInfo("combinedpay_data", objectMapper.writeValueAsString(cmd.getCombinedpayData()));
    }
    if (cmd.getCombinedpayDataFeeInfo() != null) {
        request.addExtendInfo("combinedpay_data_fee_info", objectMapper.writeValueAsString(cmd.getCombinedpayDataFeeInfo()));
    }
    if (cmd.getTransFeeAllowanceInfo() != null) {
        request.addExtendInfo("trans_fee_allowance_info", objectMapper.writeValueAsString(cmd.getTransFeeAllowanceInfo()));
    }
    return request;
}
```

## 校验建议

### 第一层：基础字段校验

- 金额、日期、IP、URL、枚举值
- `req_seq_id` 是否唯一
- `goods_desc` 是否为真实业务描述

### 第二层：trade_type 驱动的组合校验

- 微信公众号 / 小程序：`sub_appid`、`sub_openid`
- 支付宝 JS：`buyer_id` / `buyer_logon_id`
- 付款码：`auth_code`
- 银联 JS：`customer_ip`

### 第三层：扩展能力校验

- 分账对象是否完整、比例是否闭合
- 设备对象是否来自真实终端采集
- `devs_id` 是否来自报备结果
- 补贴 / 手续费对象是否有真实承担方信息

### 第四层：官方来源校验

- `sub_openid` 是否真的来自当前 `sub_appid` 对应的公众号 / 小程序授权流程
- `buyer_id` 是否真的来自支付宝 `user_id`
- `user_id` 是否真的来自银联 `auth_code -> user_id` 交换流程
- `auth_code` 是否来自本次扫码设备实时采集，而不是配置文件、测试常量或历史缓存

## `method_expand` 构造约束

| 规则 | 说明 |
|------|------|
| `trade_type` 只做场景选择 | `T_JSAPI`、`T_MINIAPP`、`T_APP`、`T_MICROPAY`、`A_JSAPI`、`A_NATIVE`、`A_MICROPAY`、`U_JSAPI`、`U_NATIVE`、`U_MICROPAY` 这些值不是 `method_expand` 的 key |
| JSON 内容只放当前场景对象 | 不要把多个渠道对象一起塞进一个 `method_expand` |
| 对象字段必须完整 | 有 `detail` 就把 `goods_detail[]` 补完整；有 `pid_info` 就把子字段补完整 |
| 关键身份字段必须真实 | `sub_openid`、`buyer_id`、`user_id`、`auth_code` 只能来自官方指引对应的真实获取链路 |

## `acct_split_bunch` 构造约束

| 对象 | 约束 |
|------|------|
| `acct_infos` | 金额分账和百分比分账不要混乱拼接；比例之和要闭合 |
| `percentage_flag` | 走百分比分账时再传 |
| `is_clean_split` | 只有“手续费内扣 + 百分比分账”场景才有意义 |

## `terminal_device_data` 构造约束

| 对象 | 约束 |
|------|------|
| `device_ip` | 优先使用真实采集值，反扫场景尤其重要 |
| `devs_id` | 走报备机具时传，来源应是汇付报备 / 查询结果 |
| `mer_device_type` / `location` 等 | 按真实终端能力补，不要造示例值 |

## 补贴类顶层扩展字段构造约束

| 对象 | 约束 |
|------|------|
| `combinedpay_data` | 没有真实补贴账户就不要传 |
| `combinedpay_data_fee_info` | 没有明确承担方就不要传空壳 |
| `trans_fee_allowance_info` | 没有活动或补贴金额来源时不要硬造 |

## 明确禁止的写法

- 在代码里直接手写长 JSON 字符串，然后把变量名叫 `methodExpand` / `txMetadata`。
- 不做场景组合校验，只按平铺字段做 `@NotBlank`。
- 用示例值、空对象、半截对象去“补齐”复杂参数。
- 把多个 `trade_type` 的对象同时塞进一个请求里，指望汇付侧自己兜底。
- 把 `method_expand` 写成带支付类型包装 key 的结构。
- 把 `tx_metadata` 当请求字段传。
- 把 `acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 塞进 `tx_metadata`。
- 把前端 success 回调直接当作支付成功，不再走后端查单确认。
