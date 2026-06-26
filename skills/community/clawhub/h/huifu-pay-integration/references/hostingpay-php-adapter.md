# PHP 适配说明

本文件对应托管支付 PHP 接入。

## 目录

- 适用范围
- 官方 SDK 入口
- 推荐调用方式
- 强制请求头
- 与官方 PHP SDK 的对齐要点
- 新增接口兼容性
- 启动示例
- 设计约束
- 场景入口

## 适用范围

- 托管支付预下单
- 托管支付查单 / 关单 / 对账
- 托管支付退款 / 退款查询

本文件只负责托管支付 PHP。聚合支付 PHP 另见 `references/aggregation-php-adapter.md`，当前已覆盖下单、扫码交易查询、关单、关单查询、退款、退款查询、对账。

## 官方 SDK 入口

托管支付 PHP 默认使用官方 Composer 包：

- `huifurepo/dg-php-sdk`
- 当前 Skill 包基线：`2.0.27`

业务入口统一走：

- `BsPayClient::postRequest()`

推荐在项目中建立 `loader.php`，只负责：

- 加载官方 SDK `init.php`
- 定义后续 request 类复用的 `HUIFU_SDK_ROOT`
- 调用 `BsPay::init(...)` 导入商户配置

不要只写 `require 'vendor/autoload.php';` 就结束。当前官方 `huifurepo/dg-php-sdk` 包没有声明 Composer autoload 规则，`init.php` 和 request 类都要显式加载。

当前 Skill 包不再内置 PHP 模板资产或非官方自维护 client。排查签名、报文和来源头差异时，先读共享协议文档，再检查项目实际安装的官方 SDK 源码。

`loader.php` 初始化 `MerConfig` 时，必须显式配置 `skill_source`。只有这个值非空时，官方 SDK 才会自动带出 `jpt-x-skill-source`，并在本次请求 `huifu_id` 存在且非空时自动带出 `jpt-x-skill-huifu_id`。

## 安装与环境变量前置检查

输出 PHP 可运行代码时，必须先给出 SDK 安装和环境变量准备；不要只给 `require_once` 业务代码。

当前 PHP SDK 包版本口径：

| 项 | 值 |
| --- | --- |
| Composer 包 | `huifurepo/dg-php-sdk` |
| 当前 Skill 包基线 | `2.0.27` |
| 官方 SDK 文档 | `https://paas.huifu.com/partners/prod/devtools/doc/sdk_php.md` |
| Packagist 包路径 | `https://packagist.org/packages/huifurepo/dg-php-sdk` |
| GitHub 项目主页 | `https://github.com/huifurepo/bspay-php-sdk` |
| 备用下载包 | `https://api.github.com/repos/huifurepo/bspay-php-sdk/zipball/refs/tags/2.0.27` |

新项目安装当前 Skill 基线：

```bash
composer require "huifurepo/dg-php-sdk:^2.0.27"
composer show huifurepo/dg-php-sdk
test -f vendor/huifurepo/dg-php-sdk/BsPaySdk/init.php
```

已有项目升级到当前 Skill 基线：

```bash
composer require "huifurepo/dg-php-sdk:^2.0.27" --with-all-dependencies
composer update huifurepo/dg-php-sdk --with-all-dependencies
composer show huifurepo/dg-php-sdk
test -f vendor/huifurepo/dg-php-sdk/BsPaySdk/init.php
```

如果用户项目已经安装了低于 `2.0.27` 的 SDK，约定是先把 `composer.json` 中 `huifurepo/dg-php-sdk` 的版本约束调整到 `^2.0.27` 或更精确的 `2.0.27`，再执行上面的升级命令；不要在旧 SDK 上继续生成新字段或新接口代码。

Composer 不可用或内网不能访问 Packagist 时，可使用当前基线对应的官方包分发地址手动落地：

```bash
curl -L "https://api.github.com/repos/huifurepo/bspay-php-sdk/zipball/refs/tags/2.0.27" -o dg-php-sdk-2.0.27.zip
unzip dg-php-sdk-2.0.27.zip
export HUIFU_SDK_ROOT="/absolute/path/to/extracted/BsPaySdk"
test -f "$HUIFU_SDK_ROOT/init.php"
```

手动下载方式只解决安装来源问题，不改变运行约束：只能保留一个实际使用的 SDK 路径，`HUIFU_SDK_ROOT` 必须指向本次确认过的 `BsPaySdk` 目录。官方 SDK 文档版本表在 2026-04-24 直接校验时仍只列到 `v2.0.25`，且该行 OSS 下载地址返回 404；不要把可访问的旧包地址当作 `2.0.27` 替代品。

运行前至少准备以下环境变量：

```bash
export HUIFU_SYS_ID="渠道商或商户系统号"
export HUIFU_PRODUCT_ID="汇付产品号"
export HUIFU_RSA_PRIVATE_KEY="商户 RSA 私钥"
export HUIFU_RSA_PUBLIC_KEY="汇付 RSA 公钥"
export HUIFU_SKILL_SOURCE="hfps/1.3.0"
export HUIFU_MERCHANT_ID="本次请求的 huifu_id"
export HUIFU_NOTIFY_URL="https://your-domain.example/huifu/notify"
export HUIFU_PROJECT_ID="托管项目 project_id"
export HUIFU_PROJECT_TITLE="托管收银台展示标题"
export HUIFU_CALLBACK_URL="支付完成后的前端回跳地址"
export HUIFU_ALIPAY_APP_SCHEMA="支付宝小程序 app_schema；非支付宝小程序可不配置"
export HUIFU_ALIPAY_BUYER_ID="支付宝 buyer_id；按场景配置"
export HUIFU_MINIAPP_SEQ_ID="微信小程序 seq_id；按场景配置"
export HUIFU_SPLIT_HUIFU_ID="分账接收方 huifu_id；按场景配置"
```

如项目没有使用默认 Composer 目录，额外设置：

```bash
export HUIFU_SDK_ROOT="/absolute/path/to/BsPaySdk"
```

## 可直接运行的 `loader.php` 模板

下面给的是当前 skill 推荐的最小可运行模板。这个模板默认你把 `loader.php` 放在项目 `bootstrap/` 目录；下面的业务代码示例统一假设业务脚本位于项目 `examples/` 目录。如果你的目录结构不同，只改入口文件里的 `require_once` 路径和 `$huifuSdkRoot` 这一行，不要改业务代码里的 request 类加载方式。

```php
<?php

declare(strict_types=1);

function requireEnv(string $key): string
{
    $value = getenv($key);
    if ($value === false || trim($value) === '') {
        throw new RuntimeException('缺少环境变量：' . $key);
    }
    return trim($value);
}

$huifuSdkRoot = getenv('HUIFU_SDK_ROOT') ?: dirname(__DIR__) . '/vendor/huifurepo/dg-php-sdk/BsPaySdk';
if (!is_file($huifuSdkRoot . '/init.php')) {
    throw new RuntimeException(
        '未找到 dg-php-sdk，请确认 HUIFU_SDK_ROOT 或 vendor/huifurepo/dg-php-sdk/BsPaySdk 路径'
    );
}

define('HUIFU_SDK_ROOT', rtrim($huifuSdkRoot, '/'));
require_once HUIFU_SDK_ROOT . '/init.php';

\BsPaySdk\core\BsPay::init([
    'sys_id' => requireEnv('HUIFU_SYS_ID'),
    'product_id' => requireEnv('HUIFU_PRODUCT_ID'),
    'rsa_merch_private_key' => requireEnv('HUIFU_RSA_PRIVATE_KEY'),
    'rsa_huifu_public_key' => requireEnv('HUIFU_RSA_PUBLIC_KEY'),
    'skill_source' => requireEnv('HUIFU_SKILL_SOURCE'),
], true);
```

这个模板解决 3 个运行问题：

1. 官方 SDK `init.php` 显式加载
2. request 类统一通过 `HUIFU_SDK_ROOT` 定位，不再依赖业务脚本自己的相对目录
3. `skill_source` 在初始化阶段显式注入，后续来源头自动补齐；缺失时直接抛错，不使用静默默认值
4. SDK 未安装或环境变量缺失时直接暴露错误，避免生成“看起来能跑”的空初始化代码

## 推荐调用方式

1. 业务层统一走官方 `BsPayClient::postRequest()`
2. 推荐使用“request 类提供 `funcCode` + `params` 数组承载实际字段”的写法
3. request 类可以帮助避免 `funcCode` 手写错误；`params` 数组则能覆盖官方 request 类中尚未显式暴露的字段
4. 不要在业务层散落 `BsPay::post(funcCode, ...)`

## 强制 HTTP 请求头

托管支付 PHP 走官方 SDK 时，HTTP 请求头由 SDK 自动生成；来源头规则见：

- `references/shared-request-header-policy.md`

当前版本固定要求：

| Header | 值 |
| --- | --- |
| `sdk_version` | 官方 SDK 默认值 `php#v2.0.27` |
| `charset` | 官方 SDK 默认值 `UTF-8` |
| `jpt-x-skill-source` | `MerConfig.skill_source` 非空时自动带 `<skill_source>` |
| `jpt-x-skill-huifu_id` | `MerConfig.skill_source` 已配置且 `data.huifu_id` 存在且非空时自动带 `<data.huifu_id>` |

`jpt-x-skill-source` 和 `jpt-x-skill-huifu_id` 都是 HTTP 请求头，不是 `data` 业务字段。

## 与官方 PHP SDK 的对齐要点

1. 当前 Skill 包对齐的官方 PHP SDK 主链路已在 `BsPay::post()` 中自动补 `jpt-x-skill-source`，并在 `huifu_id` 存在且非空时自动补 `jpt-x-skill-huifu_id`。
2. `BsPayClient::postRequest()` 走的就是这条官方主链路，不需要再为来源头做 patch。
3. 如果项目没有给 `MerConfig.skill_source` 赋值，SDK 不会带出来源头；这是初始化配置缺口，不是业务接口缺口。
4. 官方参数表里标注为 `String(JSON Object)` 的字段，例如 `hosting_data`、`app_data`、`miniapp_data`、`dy_data`、`acct_split_bunch`、`risk_check_data`、`terminal_device_data`，都要按 JSON 字符串上送。
5. 当前 Skill 包不再内置 PHP 模板资产；差异排查以共享协议文档和项目实际安装的官方 SDK 源码为准。
6. 业务代码里显式 `require_once` request 类不是退回手写 SDK；这是因为当前官方 Composer 包没有提供 request 类 autoload。

## 新增接口兼容性

| 接口 | PHP SDK 2.0.27 源码核对 | 输出规则 |
| --- | --- | --- |
| 抖音直连下单 | 使用托管预下单 `V2TradeHostingPaymentPreorderH5Request`；没有独立抖音直连 Request 类 | 调用 `setPreOrderType("4")`，并通过 `setExtendInfo(...)` / params 承载 `dy_data` 和 `notify_url`；不要生成不存在的 `Dypreorder` / `Douyin` 类 |
| 拆单支付订单查询 | 存在 `V2TradeHostingPaymentSplitpayQueryRequest` | 可使用官方 request 类；不要用普通 `V2TradeHostingPaymentQueryorderinfoRequest` 替代 |

## 启动示例

```php
<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/bootstrap/loader.php';
require_once HUIFU_SDK_ROOT . '/request/V2TradeHostingPaymentPreorderH5Request.php';

use BsPaySdk\core\BsPayClient;
use BsPaySdk\request\V2TradeHostingPaymentPreorderH5Request;

$request = new V2TradeHostingPaymentPreorderH5Request();
$client = new BsPayClient();

// 前提：loader.php 中已给 MerConfig.skill_source 赋真实来源值
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
    ],
]);
```

## 设计约束

1. PHP 侧统一走官方 `BsPayClient::postRequest()`，不要再默认生成 `HostingClient`、`curl_setopt` 或自写 HTTP 主链路。
2. 推荐“request 类 + params 数组”写法；不要把 `BsPay::post(funcCode, ...)` 散落到业务 service 中。
3. 请求体里的 JSON Object 字段一律先 `json_encode(..., JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)`，再交给官方 SDK 签名。
4. `req_seq_id`、`req_date`、原交易流水、退款流水等幂等键必须由业务侧持久化。
5. `project_id`、`project_title`、`callback_url`、`sub_openid` 等运行时值必须来自真实业务链路，禁止硬编码占位值上线。

## 场景入口

- 预下单：`references/hostingpay-preorder-php-scenarios.md`
- 查询 / 关单 / 对账：`references/hostingpay-query-php-scenarios.md`
- 退款：`references/hostingpay-refund-php-scenarios.md`
