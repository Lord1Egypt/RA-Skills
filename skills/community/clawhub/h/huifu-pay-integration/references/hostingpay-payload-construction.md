# 托管支付参数校验与 JSON 构造规范

> 汇付文档里大量字段被标成 `String(JSON Object)` 或 `String(JSON Array)`。这只代表 **SDK 边界类型** 是字符串，不代表业务代码应该直接把对象定义成裸字符串，更不代表可以在代码里手写残缺的 JSON 片段。


## 目录

- 推荐的分层方式
- 必填、非必填、条件必填怎么处理
- 托管支付里最常见的条件必填
- 建模规则
- 推荐代码形态
- 校验建议
- URL 与回调校验建议
- 对象字段完整性的最低要求
- 官方产品文档驱动的额外校验
- 明确禁止的写法

## 推荐的分层方式

```
外部请求 DTO（强类型、嵌套对象）
        ↓
参数校验层（必填 / 条件必填 / 业务规则）
        ↓
SDK Request Builder（只在这里做 JSON 序列化）
        ↓
dg-java-sdk Request
```

## 必填、非必填、条件必填怎么处理

| 类型 | 建议处理方式 | 说明 |
|------|-------------|------|
| 必填 | API 层直接拦截 | 如 `huifu_id`、`trans_amt`、`goods_desc` |
| 非必填 | 仅在有真实来源时才传 | 不要为了“字段完整”乱补默认值 |
| 条件必填 | 先判断场景，再做组合校验 | 不能只做单字段 `@NotBlank` |

## 托管支付里最常见的条件必填

| 条件 | 需要补充校验的字段 |
|------|------------------|
| 指定了 H5/PC 单一 `trans_type` | `hosting_data.request_type` |
| 微信小程序自有渠道场景 | `miniapp_data.seq_id` 必须来自真实应用绑定结果 |
| `split_pay_flag=Y` | `split_pay_data`，且业务侧已确认拆单支付权限开通 |
| 打开支付宝买家校验 `need_check_info=T` | `person_payer.name`、`cert_type`、`cert_no` |
| `promotion_flag=Y` | `detail` 及 `goods_detail[]` |
| 使用报备机具场景 | `terminal_device_data.devs_id` |
| 大额支付三要素校验 | `largeamt_data.certificate_name` |
| 大额支付四要素校验 | `largeamt_data.bank_card_no` |
| 百分比分账 | `acct_split_bunch.acct_infos[].percentage_div` 总和必须为 `100.00` |

## 建模规则

### 规则 1：对外 API DTO 不要把复杂对象直接定义成 `String`

不推荐：

```java
public class PreOrderRequest {
    private String hostingData;
    private String bizInfo;
    private String wxData;
}
```

推荐：

```java
public class PreOrderRequest {
    private HostingData hostingData;
    private BizInfo bizInfo;
    private WxData wxData;
}
```

### 规则 2：只在 SDK 边界做一次序列化

不推荐：

```java
request.setHostingData("{\"project_id\":\"P1\"}");
extendInfoMap.put("biz_info", "{\"payer_check_wx\":{\"real_name_flag\":\"Y\"}}");
```

推荐：

```java
request.setHostingData(objectMapper.writeValueAsString(cmd.getHostingData()));
extendInfoMap.put("biz_info", objectMapper.writeValueAsString(cmd.getBizInfo()));
```

### 规则 3：对象一旦出现，就要保证子字段完整

如果业务代码决定传 `biz_info`、`acct_split_bunch`、`wx_data.detail`、`largeamt_data` 这类对象，就不能只拼一个最小壳子。要么不传，要么传完整的业务有效对象。

## 推荐代码形态

```java
public class H5PreOrderCommand {
    private String reqDate;
    private String reqSeqId;
    private String huifuId;
    private String transAmt;
    private String goodsDesc;
    private HostingData hostingData;
    private BizInfo bizInfo;
    private TerminalDeviceData terminalDeviceData;
}

public V2TradeHostingPaymentPreorderH5Request buildRequest(
        H5PreOrderCommand cmd,
        ObjectMapper objectMapper) throws JsonProcessingException {
    validate(cmd);

    V2TradeHostingPaymentPreorderH5Request request =
            new V2TradeHostingPaymentPreorderH5Request();
    request.setReqDate(cmd.getReqDate());
    request.setReqSeqId(cmd.getReqSeqId());
    request.setHuifuId(cmd.getHuifuId());
    request.setTransAmt(cmd.getTransAmt());
    request.setGoodsDesc(cmd.getGoodsDesc());
    request.setPreOrderType("1");
    request.setHostingData(objectMapper.writeValueAsString(cmd.getHostingData()));

    Map<String, Object> extendInfo = new HashMap<>();
    if (cmd.getBizInfo() != null) {
        extendInfo.put("biz_info", objectMapper.writeValueAsString(cmd.getBizInfo()));
    }
    if (cmd.getTerminalDeviceData() != null) {
        extendInfo.put(
                "terminal_device_data",
                objectMapper.writeValueAsString(cmd.getTerminalDeviceData()));
    }
    request.setExtendInfo(extendInfo);
    return request;
}
```

如果外部 DTO / Controller 已经接收 `req_date`、`req_seq_id`、`notify_url`、`project_id`、金额或商户号，Builder 只能校验和映射，不要在 Builder 里重新生成并覆盖。只有当前服务端明确拥有字段生成权，且生成值会落库供后续查询、关单、退款复用时，才允许在进入 Builder 之前生成。

## 校验建议

### 第一层：DTO 基础校验

- `req_date`、`req_seq_id`、金额、日期、URL、ID 长度、枚举值
- 字段是否为空

### 第二层：场景组合校验

- `pre_order_type=1` 时是否提供了 `hosting_data`
- 指定 `trans_type` 时是否同步提供了 `request_type`
- 微信 / 支付宝买家校验对象是否完整
- 对象字段出现时，子结构是否完整到可以真正发起交易

### 第三层：业务来源校验

- `project_id` 是否来自客户已在控台创建并留存的托管项目，而不是示例值
- `sub_openid`、`seller_id`、`devs_id` 是否来自真实渠道授权 / 报备结果
- `miniapp_data.seq_id` 是否来自小程序托管授权、代码发布、绑定 appid 后生成的应用 ID
- `req_date`、`req_seq_id`、`hf_seq_id` 是否已在上游沉淀，供查询 / 退款复用

## URL 与回调校验建议

### `notify_url`

- 只允许 `http` / `https`
- 不允许重定向地址
- URL 不带查询参数
- 使用自定义端口时限制在 `8000-9005`
- 回调处理成功后必须返回 `200`

### `callback_url`

- 仅用于支付完成后页面跳转
- 不能作为支付成功判定依据
- 前端回跳后，后端仍需走查询接口确认订单状态

## 对象字段完整性的最低要求

| 对象 | 最低要求 |
|------|---------|
| `hosting_data` | 至少能落地 `project_id`、`project_title`，需要跳转时再带 `callback_url` |
| `biz_info.person_payer` | 一旦做实名校验，就不要只传姓名不传证件信息 |
| `acct_split_bunch` | 至少保证接收方标识存在，且金额或比例规则完整 |
| `terminal_device_data` | 报备机具场景至少保证 `devs_id` 来源真实 |
| `largeamt_data` | 进入大额支付校验就要保证三要素 / 四要素完整，不要只传一半 |

## 官方产品文档驱动的额外校验

- H5 / PC 场景下，若指定了某个 `trans_type`，要先确认托管项目里已启用该支付方式。
- 微信支付接入 H5 / PC 收银台前，要先确认微信授权域名配置已完成。
- 小程序拆单支付不是普通字段开关，业务侧未确认权限开通时不要生成 `split_pay_flag=Y`。
- 对账单相关请求前，要先确认商户已在控台配置对账文件生成，而不是只看接口字段是否齐全。

## 明确禁止的写法

- 在 Java 代码里直接拼一长串硬编码 JSON 字符串再塞给 SDK。
- 只因为文档说“字段类型是 String”，就把复杂对象在 DTO 层设计成字符串。
- 明知道字段是条件必填，却只做平铺字段校验，不做场景组合校验。
- 对没有来源的值使用示例值、占位值、空对象、半截对象凑请求。
- 把 `callback_url` 当成支付成功通知地址使用，或把前端回跳直接当成成功终态。
