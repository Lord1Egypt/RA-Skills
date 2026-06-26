# PHP 场景示例


## 目录

- 公共前提
- H5 / PC 预下单
- 抖音直连下单
- 支付宝小程序预下单
- 微信小程序预下单
- 生产写法约束

本文件只覆盖托管支付 PHP 场景。

默认你已经按 `references/hostingpay-php-adapter.md` 初始化了：

```php
require_once dirname(__DIR__) . '/bootstrap/loader.php'; // 默认业务脚本位于 examples/，loader.php 模板见 hostingpay-php-adapter.md
use BsPaySdk\core\BsPayClient;

$client = new BsPayClient();
```

## 公共前提

1. 先完成 `references/hostingpay-php-adapter.md`
2. 所有请求头必须符合 `references/shared-request-header-policy.md`
3. `req_seq_id`、`req_date`、`jump_url`、`pre_order_id` 必须落库
4. 外部 DTO / Controller 已接收 `req_date`、`req_seq_id`、`huifu_id`、金额、项目号或回调地址时，必须保留入参，缺失或非法时显式报错；下面示例里的 `date('Ymd')` 和随机流水号只适用于服务端自主管理这些字段的独立 demo

## H5 / PC 预下单

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentPreorderH5Request.php';

use BsPaySdk\request\V2TradeHostingPaymentPreorderH5Request;

$request = new V2TradeHostingPaymentPreorderH5Request();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'HP' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'trans_amt' => '88.00',
        'goods_desc' => '会员充值',
        'pre_order_type' => '1',
        'notify_url' => getenv('HUIFU_NOTIFY_URL'),
        'hosting_data' => json_encode([
            'project_id' => getenv('HUIFU_PROJECT_ID'),
            'project_title' => getenv('HUIFU_PROJECT_TITLE'),
            'callback_url' => getenv('HUIFU_CALLBACK_URL'),
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        'delay_acct_flag' => 'N',
    ],
]);

$response = $result->getRspDatas()['data'] ?? [];
$jumpUrl = $response['jump_url'] ?? '';
```

适合场景：

- 商户自己的 H5 页面跳转托管收银台
- PC 收银台二维码 / 跳转页拉起

补充说明：

1. 最小必填通常是 `req_date`、`req_seq_id`、`huifu_id`、`trans_amt`、`goods_desc`、`pre_order_type`。
2. `hosting_data.project_id`、`hosting_data.project_title`、`hosting_data.callback_url`、`notify_url` 属于生产接入高频推荐字段，不建议照着官网最小 demo 再删减。
3. `acct_split_bunch`、`biz_info` 属于条件字段，只有在分账、付款人校验、实名限制等场景才补。

## 抖音直连下单

PHP SDK 使用托管预下单 `V2TradeHostingPaymentPreorderH5Request` 承载抖音直连场景，关键是固定 `pre_order_type=4` 并传入 `dy_data`；不要生成不存在的抖音专属 request 类。

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentPreorderH5Request.php';

use BsPaySdk\request\V2TradeHostingPaymentPreorderH5Request;

$request = new V2TradeHostingPaymentPreorderH5Request();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'DY' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'trans_amt' => '12.50',
        'goods_desc' => '抖音订单',
        'pre_order_type' => '4',
        'notify_url' => getenv('HUIFU_NOTIFY_URL'),
        'dy_data' => json_encode([
            'sub_appid' => getenv('DOUYIN_SUB_APPID'),
            'busi_scene' => 'H5',
            'h5_info' => [
                'type' => 'Wap',
                'app_name' => getenv('DOUYIN_H5_APP_NAME'),
                'app_url' => getenv('DOUYIN_H5_APP_URL'),
            ],
            'scene_info' => [
                'payer_client_ip' => $clientIp,
            ],
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
    ],
]);
```

字段拆分：

1. `pre_order_type` 固定传 `4`。
2. `dy_data` 是 `String(JSON Object)`，必须 `json_encode` 后交给 SDK 签名。
3. `payer_client_ip` 必须来自真实用户终端 IP，不能写示例值。
4. 同步 `jump_url` 只用于拉起支付，最终状态仍以异步通知验签、幂等和查单闭环为准。

## 支付宝小程序预下单

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentPreorderAliRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentPreorderAliRequest;

$request = new V2TradeHostingPaymentPreorderAliRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'AP' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'trans_amt' => '18.80',
        'goods_desc' => '小程序会员',
        'pre_order_type' => '2',
        'notify_url' => getenv('HUIFU_NOTIFY_URL'),
        'app_data' => json_encode([
            'app_schema' => getenv('HUIFU_ALIPAY_APP_SCHEMA'),
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        'delay_acct_flag' => 'N',
        'acct_split_bunch' => json_encode([
            'acct_infos' => [[
                'div_amt' => '0.08',
                'huifu_id' => getenv('HUIFU_SPLIT_HUIFU_ID'),
            ]],
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
    ],
]);
```

可选增强字段：

```php
$optionalPayload = [
    'hosting_data' => json_encode([
        'project_id' => getenv('HUIFU_PROJECT_ID'),
        'project_title' => getenv('HUIFU_PROJECT_TITLE'),
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
    'alipay_data' => json_encode([
        'buyer_id' => getenv('HUIFU_ALIPAY_BUYER_ID'),
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
    'biz_info' => json_encode([
        'payer_check_ali' => [
            'need_check_info' => 'T',
        ],
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
];
```

适合场景：

- 支付宝小程序内拉起托管支付
- 业务侧已经具备 app schema、通知地址和分账信息

字段拆分：

1. 最小必填通常是 `req_date`、`req_seq_id`、`huifu_id`、`trans_amt`、`goods_desc`。
2. 场景必填是 `app_data.app_schema`，否则无法回跳到支付宝小程序链路。
3. `hosting_data`、`acct_split_bunch`、`biz_info`、`alipay_data` 都属于推荐或条件字段，需要根据收银台展示、分账、买家绑定等实际诉求补齐。

## 微信小程序预下单

```php
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentPreorderWxRequest.php';

use BsPaySdk\request\V2TradeHostingPaymentPreorderWxRequest;

$request = new V2TradeHostingPaymentPreorderWxRequest();
$result = $client->postRequest([
    'funcCode' => $request->getFunctionCode(),
    'params' => [
        'req_date' => date('Ymd'),
        'req_seq_id' => 'WX' . date('YmdHis') . random_int(1000, 9999),
        'huifu_id' => getenv('HUIFU_MERCHANT_ID'),
        'trans_amt' => '12.50',
        'goods_desc' => '微信小程序订单',
        'pre_order_type' => '3',
        'notify_url' => getenv('HUIFU_NOTIFY_URL'),
        'miniapp_data' => json_encode([
            'seq_id' => getenv('HUIFU_MINIAPP_SEQ_ID'),
            'private_info' => 'oppsHosting://',
            'need_scheme' => 'Y',
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        'delay_acct_flag' => 'Y',
        'acct_split_bunch' => json_encode([
            'acct_infos' => [[
                'div_amt' => '0.01',
                'huifu_id' => getenv('HUIFU_SPLIT_HUIFU_ID'),
            ]],
        ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
    ],
]);
```

可选增强字段：

```php
$optionalPayload = [
    'wx_data' => json_encode([
        'sub_appid' => getenv('WECHAT_APP_ID'),
        'sub_openid' => $openidFromWechat,
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
    'biz_info' => json_encode([
        'payer_check_wx' => [
            'limit_payer' => 'ADULT',
            'real_name_flag' => 'Y',
        ],
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
];
```

适合场景：

- 微信小程序支付
- 业务侧已经完成 `seq_id` 获取、小程序授权和分账配置

字段拆分：

1. 最小必填通常是 `req_date`、`req_seq_id`、`huifu_id`、`trans_amt`、`goods_desc`。
2. 场景必填是 `miniapp_data.seq_id`；如果要走 scheme 回跳，再补 `need_scheme=Y`。
3. `acct_split_bunch`、`biz_info`、`wx_data.sub_openid` 都属于条件字段，必须来自真实授权或订单上下文，不能照抄 demo 占位值。

## 生产写法约束

1. 官网 demo 里的 JSON 字段看起来像普通字符串，实际都应由 `json_encode(..., JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)` 编码而来，不要手写拼接 JSON。
2. `delay_acct_flag`、`acct_split_bunch`、`biz_info` 在官方 demo 里经常出现，但都属于条件字段，只有业务场景需要时才上送。
3. 官方 PHP SDK 这条写法里，`pre_order_type` 需要在 `params` 中显式给出，不要漏传。
4. 如果项目是 Composer 安装的 `dg-php-sdk`，request 类仍要通过 `HUIFU_SDK_ROOT` 显式加载，不要假设 `vendor/autoload.php` 会自动装载这些类。
5. 生成真实业务代码时，先判断外部 DTO / Controller 是否已经接收字段；已经接收就必须保留入参，缺失或非法时显式报错，不要在 SDK Request 组装层重新生成并覆盖。
