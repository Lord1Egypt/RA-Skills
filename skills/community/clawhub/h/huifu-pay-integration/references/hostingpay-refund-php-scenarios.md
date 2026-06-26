# PHP 场景示例

本文件覆盖托管支付退款与退款查询的 PHP 调用方式。

## 目录

- 发起退款
- 退款查询
- 落地建议

默认你已经按 `references/hostingpay-php-adapter.md` 初始化了：

```php
require_once dirname(__DIR__) . '/bootstrap/loader.php'; // 默认业务脚本位于 examples/，loader.php 模板见 hostingpay-php-adapter.md
use BsPaySdk\core\BsPayClient;

$client = new BsPayClient();
```

字段保留规则：外部 DTO / Controller 已接收 `req_date`、`req_seq_id`、`huifu_id`、退款金额、通知地址、原交易或原退款定位键时，必须保留入参，缺失或非法时显式报错。下面示例里的 `date('Ymd')` 和随机流水号只适用于服务端自主管理这些字段的独立 demo，不得覆盖上游传入值。

## 发起退款

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentHtrefundRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentHtrefundRequest;

$request = new V2TradeHostingPaymentHtrefundRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'RF' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'ord_amt' => '10.00',
        'org_req_date' => $order->getReqDate(),
        'org_req_seq_id' => $order->getReqSeqId(),
        'notify_url' => getenv('HUIFU_REFUND_NOTIFY_URL') ?: getenv('HUIFU_NOTIFY_URL'),
        'risk_check_data' => json_encode([
            'ip_addr' => $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1',
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        'terminal_device_data' => json_encode([
            'device_type' => '4',
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        'remark' => '用户取消订单退款',
    ],
]);
```

适合场景：

- 全额退款
- 部分退款
- 售后退款

补充说明：

1. 线上交易退款通常至少要补 `risk_check_data`、`terminal_device_data`；官方 demo 里的 `test` 只说明字段位置，不能直接上线。
2. `notify_url` 建议保留，方便退款异步通知补单。
3. 银行大额转账退款才补 `bank_info_data`，普通线上退款不要伪造这组字段。
4. 分账退款才补 `acct_split_bunch`，普通全额退款不要机械照抄分账对象。

## 退款查询

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentQueryrefundinfoRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentQueryrefundinfoRequest;

$request = new V2TradeHostingPaymentQueryrefundinfoRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'RQ' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'org_req_date' => $refund->getReqDate(),
        'org_req_seq_id' => $refund->getReqSeqId(),
    ],
]);

$response = $result->getRspDatas()['data'] ?? [];
$transStat = $response['trans_stat'] ?? 'P';
```

如果账务系统已经保存退款全局流水号，也可以改成：

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentQueryrefundinfoRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentQueryrefundinfoRequest;

$request = new V2TradeHostingPaymentQueryrefundinfoRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'RQ' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'org_req_date' => $refund->getReqDate(),
        'org_hf_seq_id' => $refund->getHuifuSeqId(),
    ],
]);
```

适合场景：

- 退款处理中轮询
- 售后系统回查退款终态

## 落地建议

1. 退款请求流水和原交易流水要分开存储。
2. 部分退款前先校验累计退款金额，避免超退。
3. 退款成功与否仍以查询 / 异步通知中的 `trans_stat` 为准，不要只看同步受理结果，也不要读取其它退款状态别名。
4. 线上退款优先准备真实的风控与设备信息，再发起请求。
5. 退款查询时 `org_hf_seq_id` 和 `org_req_seq_id` 二选一即可，但不能同时留空。
6. 如果项目是 Composer 安装的 `dg-php-sdk`，request 类仍要通过 `HUIFU_SDK_ROOT` 显式加载，不要省掉这一步。
7. 生成真实业务代码时，先判断外部 DTO / Controller 是否已经接收字段；已经接收就必须保留入参，缺失或非法时显式报错，不要在 SDK Request 组装层重新生成并覆盖。
