# PHP 场景示例

本文件覆盖聚合支付 PHP 的下单、扫码交易查询、关单、关单查询、退款、退款查询、对账。

## 目录

- 聚合支付下单
- 扫码交易查询
- 扫码交易关单
- 扫码交易关单查询
- 扫码交易退款
- 扫码交易退款查询
- 对账单查询
- 生产写法约束

默认你已经按 `references/aggregation-php-adapter.md` 初始化了：

```php
require_once dirname(__DIR__) . '/bootstrap/loader.php'; // 默认业务脚本位于 examples/，loader.php 模板见 aggregation-php-adapter.md
use BsPaySdk\core\Payment;
use BsPaySdk\core\BsPayClient;

$payment = new Payment();
$client = new BsPayClient();
```

聚合支付 PHP 查单、关单、关单查询回答必须显式写明：原交易定位键必须来自落库 / 持久化结果，不能临时猜测 `req_date`、`req_seq_id`、`hf_seq_id`。

字段保留规则：外部 DTO / Controller 已接收 `req_date`、`req_seq_id`、`huifu_id`、金额、通知地址或原交易定位键时，必须保留入参，缺失或非法时显式报错。下面示例里的 `date('Ymd')` 和随机流水号只适用于服务端自主管理这些字段的独立 demo，不得覆盖上游传入值。

## 聚合支付下单

```php
require_once HUIFU_SDK_ROOT . '/request/v4/payment/TradePaymentCreateRequest.php';

use BsPaySdk\request\v4\payment\TradePaymentCreateRequest;

$request = new TradePaymentCreateRequest();
$request->setReqDate(date('Ymd'));
$request->setReqSeqId('AP' . date('YmdHis') . random_int(1000, 9999));
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setTradeType('A_JSAPI');
$request->setTransAmt('0.10');
$request->setGoodsDesc('测试订单');
$request->setNotifyUrl(getenv('HUIFU_NOTIFY_URL'));
$request->setMethodExpand(json_encode([
    'buyer_id' => getenv('HUIFU_ALIPAY_BUYER_ID'),
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));

$result = $payment->create($request);
```

适合场景：

- 二维码、JSAPI、小程序、付款码等聚合支付统一下单入口
- 需要显式体现官方 PHP SDK 的聚合支付主链路

字段拆分：

1. `trade_type`、`method_expand`、`notify_url` 等值必须按真实场景组装。
2. `T_JSAPI`、`T_MINIAPP`、`T_APP`、`T_MICROPAY`、`A_JSAPI`、`A_NATIVE`、`A_MICROPAY`、`U_JSAPI`、`U_NATIVE`、`U_MICROPAY` 这些值不是 `method_expand` 的 key；`method_expand` 的 JSON 内容直接是当前场景对象本身。
3. `tx_metadata` 本身不作为请求字段上送；交易能力扩展按能力名直接传 `acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info`。
4. `req_date`、`req_seq_id`、`huifu_id` 必须持久化，后续查单、关单、退款都会复用。

## 扫码交易查询

```php
require_once HUIFU_SDK_ROOT . '/request/v4/payment/TradePaymentScanpayQueryRequest.php';

use BsPaySdk\request\v4\payment\TradePaymentScanpayQueryRequest;

$request = new TradePaymentScanpayQueryRequest();
$request->setReqDate(date('Ymd'));
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setHfSeqId($order->getHfSeqId());

$result = $payment->query($request);
```

适合场景：

- 前端回调后确认最终支付状态
- 订单处理中，需要轮询直至 `trans_stat` 明确

字段拆分：

1. 这里的 `req_date` 是本次查询请求日期，不是原交易下单日期。
2. `hf_seq_id`、`out_ord_id`、`req_seq_id` 才是原交易定位键；示例按 `hf_seq_id` 查单。

## 扫码交易关单

```php
require_once HUIFU_SDK_ROOT . '/request/v4/payment/TradePaymentScanpayCloseRequest.php';

use BsPaySdk\request\v4\payment\TradePaymentScanpayCloseRequest;

$request = new TradePaymentScanpayCloseRequest();
$request->setReqDate(date('Ymd'));
$request->setReqSeqId('AC' . date('YmdHis') . random_int(1000, 9999));
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setOrgReqDate($order->getReqDate());
$request->setOrgReqSeqId($order->getReqSeqId());

$result = $payment->close($request);
```

适合场景：

- 微信 / 支付宝订单超时未支付，主动释放订单
- 服务端轮询后确认订单仍未支付，需要结束交易

## 扫码交易关单查询

```php
require_once HUIFU_SDK_ROOT . '/request/v4/payment/TradePaymentScanpayCloseQueryRequest.php';

use BsPaySdk\request\v4\payment\TradePaymentScanpayCloseQueryRequest;

$request = new TradePaymentScanpayCloseQueryRequest();
$request->setReqDate(date('Ymd'));
$request->setReqSeqId('AQ' . date('YmdHis') . random_int(1000, 9999));
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setOrgReqDate($order->getReqDate());
$request->setOrgReqSeqId($order->getReqSeqId());

$result = $payment->closeQuery($request);

$response = $result->getRspDatas()['data'] ?? [];
$transStat = $response['trans_stat'] ?? 'P';
```

适合场景：

- 关单请求返回处理中，需要继续确认最终状态
- 业务系统重试前，先确认关单是否已经生效

## 扫码交易退款

```php
require_once HUIFU_SDK_ROOT . '/request/v4/payment/TradePaymentScanpayRefundRequest.php';

use BsPaySdk\request\v4\payment\TradePaymentScanpayRefundRequest;

$request = new TradePaymentScanpayRefundRequest();
$request->setReqDate(date('Ymd'));
$request->setReqSeqId('AR' . date('YmdHis') . random_int(1000, 9999));
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setOrgReqDate($order->getReqDate());
$request->setOrgReqSeqId($order->getReqSeqId());
$request->setOrdAmt('0.10');
$request->setNotifyUrl(getenv('HUIFU_NOTIFY_URL'));

$result = $payment->refund($request);
```

适合场景：

- 原交易确认成功后发起部分或全额退款
- 需要体现官方 PHP SDK 的退款主链路

## 扫码交易退款查询

```php
require_once HUIFU_SDK_ROOT . '/request/v4/payment/TradePaymentScanpayRefundQueryRequest.php';

use BsPaySdk\request\v4\payment\TradePaymentScanpayRefundQueryRequest;

$request = new TradePaymentScanpayRefundQueryRequest();
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setOrgReqDate($refundOrder->getReqDate());
$request->setOrgReqSeqId($refundOrder->getReqSeqId());

$result = $payment->refundQuery($request);
```

适合场景：

- 退款申请返回受理中，需要继续确认最终结果
- 异步通知存在延迟，需要主动补查

## 对账单查询

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeCheckFilequeryRequest.php';

use BsPaySdk\request\V2TradeCheckFilequeryRequest;

$request = new V2TradeCheckFilequeryRequest();
$tradeDate = new DateTimeImmutable('-1 day');
$fileDate = $tradeDate->modify('+1 day')->format('Ymd');
$request->setReqDate(date('Ymd'));
$request->setReqSeqId('AF' . date('YmdHis') . random_int(1000, 9999));
$request->setHuifuId(getenv('HUIFU_MERCHANT_ID'));
$request->setFileDate($fileDate);
$request->setExtendInfo([
    'bill_type' => 'TRADE_BILL',
]);

$result = $client->postRequest($request);
```

适合场景：

- 下载交易账单或结算账单
- 抽平业务对账和财务核对数据

## 生产写法约束

1. 官网 demo 里的 `test` 只可作为字段占位，不可进入实际 skill 示例；所有交易定位键都必须来自原订单落库值。
2. 聚合支付核心主链路优先 `BsPaySdk\core\Payment`；对账才使用 `BsPayClient::postRequest()`。
3. 扫码关单、关单查询、退款、退款查询都依赖原交易或原退款定位键，不能只靠本次请求自身判断。
4. 银联二维码、数字人民币和已成功订单不适合继续关单，遇到这类订单应改走查询或退款链路。
5. 如果项目是 Composer 安装的 `dg-php-sdk`，request 类仍要通过 `HUIFU_SDK_ROOT` 显式加载，不要假设 `vendor/autoload.php` 会自动装载。
6. 对账 `file_date` 是文件生成日期，补生成时按交易日期 `+1` 天计算，不要简单写成“昨天”。
7. 生成真实业务代码时，先判断外部 DTO / Controller 是否已经接收字段；已经接收就必须保留入参，缺失或非法时显式报错，不要在 SDK Request 组装层重新生成并覆盖。
8. 输出 PHP 业务调用模板时，即使业务脚本只 `require_once bootstrap/loader.php`，最终回答也必须显式写明 `loader.php` 中要配置 `skill_source` / `MerConfig.skill_source`；官方 SDK 在配置后自动补 HTTP 请求头 `jpt-x-skill-source`，并在本次请求 `huifu_id` 非空时自动补 `jpt-x-skill-huifu_id`。
