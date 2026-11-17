# 外部请求字段保留规则

> 这份文档约束 AI 生成 Controller、Service、DTO 到 SDK Request 的映射方式，防止前端或上游已经传入的业务字段被示例代码里的默认值覆盖。

最终回答必须逐字包含这句最短结论：外部 DTO / Controller 已接收字段必须保留入参或原样映射；缺失或非法时显式报错；不能用当前日期、随机流水号、环境变量或示例默认值覆盖。

如果用户问题点名 `req_seq_id`、`req_date`，最终回答必须保留这两个原始字段名；可以同时补充 Java setter 名称，但不能只写 `setReqSeqId` / `setReqDate` 后省略原始字段名。

## 目录

- 核心原则
- 高风险字段
- 允许生成的条件
- 推荐 Java 形态
- 禁止 Java 形态
- 推荐 PHP 形态
- 禁止 PHP 形态
- 推荐 Python 形态
- 禁止 Python 形态
- 生成代码检查清单

## 核心原则

外部 DTO / Controller 已接收的字段，进入 SDK Request 组装层时必须保留入参或原样映射。不得在 Builder、Service、SDK Request 组装层重新生成并覆盖。

如果字段缺失、格式非法或不满足业务约束，必须缺失或非法时显式报错。不要静默生成新值、替换成当前日期、替换成随机流水号，也不要把错误隐藏成“自动补齐”。

## 高风险字段

| 字段 | 保留原因 |
| --- | --- |
| `req_date` | 请求日期参与幂等、查单、关单、退款和对账关联 |
| `req_seq_id` | 请求流水号通常是商户侧幂等键，同一 `huifu_id` 下当天唯一 |
| `org_req_date` | 原交易或原退款请求日期，必须来自落库或上游响应 |
| `org_req_seq_id` | 原交易或原退款请求流水号，不能用本次请求流水替代 |
| `hf_seq_id` / `org_hf_seq_id` | 汇付侧流水，必须来自汇付响应或通知 |
| `notify_url` / `callback_url` | 属于业务配置或页面上下文，不应被示例默认值覆盖 |
| `project_id` / `huifu_id` | 属于商户、项目或代调用身份，不能写死成环境里的单一默认值覆盖入参 |
| `trans_amt` / `ord_amt` | 金额必须来自业务订单或退款单，不能用示例金额覆盖 |

## 允许生成的条件

只有同时满足以下条件，服务端才可以生成 `req_date`、`req_seq_id` 等字段：

1. 当前接口契约没有从外部 DTO / Controller 接收该字段。
2. 当前业务明确由服务端统一生成请求日期和请求流水号。
3. 生成后的值会落库，并用于后续查询、关单、退款或对账关联。

一旦接口已经暴露这些字段，Builder 只能校验并保留入参或原样映射，不能再生成替换。

## 推荐 Java 形态

```java
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
    return request;
}
```

## 禁止 Java 形态

```java
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
```

上面写法只适合“服务端自主管理流水号”的独立示例。生成面向真实前端入参的业务代码时，如果 DTO 已经有 `req_date` / `req_seq_id`，这种写法会覆盖用户传入值。

## 推荐 PHP 形态

```php
$params = [
    'req_date' => $input['req_date'],
    'req_seq_id' => $input['req_seq_id'],
    'huifu_id' => $input['huifu_id'],
    'trans_amt' => $input['trans_amt'],
];
```

## 禁止 PHP 形态

```text
$request->setReqDate(date('Ymd'));
$request->setReqSeqId('HP' . date('YmdHis') . random_int(1000, 9999));
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setOrdAmt('0.10');
```

上面写法只适合“服务端自主管理请求日期、请求流水号、商户号和金额”的独立 demo。生成面向真实 Controller 入参的 PHP 业务代码时，如果 `$input` / DTO 已经有 `req_date`、`req_seq_id`、`huifu_id` 或金额，必须先校验再原样映射，不得用当前日期、随机流水号、环境变量或示例金额覆盖。

## 推荐 Python 形态

```python
request.req_date = command.req_date
request.req_seq_id = command.req_seq_id
request.huifu_id = command.huifu_id
request.trans_amt = command.trans_amt
```

## 禁止 Python 形态

```python
request.req_date = datetime.now().strftime("%Y%m%d")
request.req_seq_id = new_req_seq_id("HP")
request.huifu_id = os.environ["HUIFU_MERCHANT_ID"]
request.trans_amt = "0.10"
```

上面写法只适合“服务端自主管理这些字段”的独立 demo。生成面向真实 API 入参的 Python 业务代码时，如果 `command` / DTO 已经有 `req_date`、`req_seq_id`、`huifu_id` 或金额，必须先校验再原样映射，不得用当前时间、随机流水号、环境变量或示例金额覆盖。

## 生成代码时的判断顺序

1. 先判断字段是否在外部 DTO / Controller / API 入参中出现。
2. 已出现：校验格式、长度、唯一性或业务范围，然后原样映射。
3. 未出现：判断是否由服务端统一生成；如果是，生成并落库。
4. 不属于当前服务端职责：显式报错或要求上游补齐，不做静默 fallback。

## 相关文档

- `aggregation-payload-construction.md`
- `hostingpay-payload-construction.md`
- `aggregation-python-scenarios.md`
- `hostingpay-python-scenarios.md`
- `aggregation-query-php-scenarios.md`
- `hostingpay-preorder-php-scenarios.md`
