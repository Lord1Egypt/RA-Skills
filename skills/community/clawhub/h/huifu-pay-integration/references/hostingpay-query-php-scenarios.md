# PHP 场景示例

本文件覆盖托管支付查询、关单与对账的 PHP 调用方式。

## 目录

- 交易查询
- 拆单支付订单查询
- 交易关单
- 对账单查询
- 落地建议

默认你已经按 `references/hostingpay-php-adapter.md` 初始化了：

```php
require_once dirname(__DIR__) . '/bootstrap/loader.php'; // 默认业务脚本位于 examples/，loader.php 模板见 hostingpay-php-adapter.md
use BsPaySdk\core\BsPayClient;

$client = new BsPayClient();
```

字段保留规则：外部 DTO / Controller 已接收 `req_date`、`req_seq_id`、`huifu_id`、原交易定位键或对账日期时，必须保留入参，缺失或非法时显式报错。下面示例里的 `date('Ymd')` 和随机流水号只适用于服务端自主管理这些字段的独立 demo，不得覆盖上游传入值。

## 交易查询

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentQueryorderinfoRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentQueryorderinfoRequest;

$request = new V2TradeHostingPaymentQueryorderinfoRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'Q' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'org_req_date' => $order->getReqDate(),
        'org_req_seq_id' => $order->getReqSeqId(),
    ],
]);

$response = $result->getRspDatas()['data'] ?? [];
$transStat = $response['trans_stat'] ?? 'P';
```

按字段组合时遵守以下规则：

1. 常规回查走 `huifu_id + org_req_date + org_req_seq_id`。
2. 如果账单侧已经保存 `party_order_id`，可以改用 `party_order_id` 单独查询。
3. `party_order_id` 与原交易三元组至少要有一套，不要两套都留空。

用途：

- 前端回跳后做终态确认
- 异步通知后做二次确认
- 处理中订单轮询

## 拆单支付订单查询

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentSplitpayQueryRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentSplitpayQueryRequest;

$request = new V2TradeHostingPaymentSplitpayQueryRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'SQ' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'org_req_date' => $splitOrder->getReqDate(),
        'org_req_seq_id' => $splitOrder->getReqSeqId(),
    ],
]);

$response = $result->getRspDatas()['data'] ?? [];
$transList = $response['trans_list'] ?? [];
```

用途：

- 微信小程序拆单支付后查询拆单明细
- 逐条读取 `trans_list[].trans_stat`

注意事项：

1. 这是拆单支付订单查询，不是普通托管 `queryorderinfo`。
2. `org_req_date` 和 `org_req_seq_id` 必须来自原拆单支付请求落库字段。
3. `order_stat` 是订单级状态，不能替代子交易 `trans_list[].trans_stat`。

## 交易关单

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentCloseRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentCloseRequest;

$request = new V2TradeHostingPaymentCloseRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'C' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'org_req_date' => $order->getReqDate(),
        'org_req_seq_id' => $order->getReqSeqId(),
    ],
]);
```

用途：

- 用户超时未支付
- 业务主动取消订单

## 对账单查询

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeCheckFilequeryRequest.php';

use BsPaySdk\request\V2TradeCheckFilequeryRequest;

$request = new V2TradeCheckFilequeryRequest();
$tradeDate = new DateTimeImmutable('-1 day');
$fileDate = $tradeDate->modify('+1 day')->format('Ymd');
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'R' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'file_date' => $fileDate,
        'bill_type' => 'TRADE_BILL',
    ],
]);

$response = $result->getRspDatas()['data'] ?? [];
$fileDetails = $response['file_details'] ?? [];
$downloadUrl = $fileDetails[0]['download_url'] ?? '';
```

用途：

- 每日交易对账
- 结算账单补拉

## 落地建议

1. `trans_stat=P` 时按照业务 skill 里的 5 秒、最多 30 次轮询策略处理。
2. 关单只适用于未支付订单，不要把已成功订单拿去关单。
3. 对账单字段固定使用 `file_date`、`bill_type`，其中交易对账单常用值是 `TRADE_BILL`；`file_date` 是文件生成日期，补生成时按交易日期 `+1` 天计算。
4. 交易查询也支持账单商户单号回查；如果业务链路里有 `party_order_id`，不要强行依赖原交易三元组。
5. `loader.php` 只负责 SDK 初始化和定义 `HUIFU_SDK_ROOT`；每个业务文件仍要显式加载自己用到的 request 类。
6. 生成真实业务代码时，先判断外部 DTO / Controller 是否已经接收字段；已经接收就必须保留入参，缺失或非法时显式报错，不要在 SDK Request 组装层重新生成并覆盖。
