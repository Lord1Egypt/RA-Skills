# 余额支付 PHP SDK 适配

使用官方 `huifurepo/dg-php-sdk 2.0.31`；初始化复用 `hostingpay-php-adapter.md`。在加载任何SDK文件前固定 `DEBUG=false`，不使用会启用调试的Demo入口。已知SDK peer TLS校验问题按 `shared-server-sdk-matrix.md` 提醒，不新增关闭校验设置。

字段和条件先按 `payment-complete-field-catalog.md`、`balancepay-field-contracts.md` 校验；六个专属类见 `balancepay-sdk-matrix.md`，各语言声明字段对应setter，扩展用 `setExtendInfo` 并拒绝覆盖。String(JSON)编码使用 `json_encode(..., JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR)` 一次，不把整个业务data编码成字符串。

## 查单与短信

以下入口假定安全初始化已完成、输入已经过接口字段校验。`HUIFU_SDK_ROOT`由服务端配置指定为BsPaySdk目录。

```php
use BsPaySdk\core\BsPayClient;
use BsPaySdk\request\V2TradeAcctpaymentPayQueryRequest;

require_once HUIFU_SDK_ROOT . '/request/V2TradeAcctpaymentPayQueryRequest.php';

function queryBalancePayment(string $initiatorId, string $originalDate,
                             string $originalRequestId): array {
    $request = new V2TradeAcctpaymentPayQueryRequest();
    $request->setHuifuId($initiatorId);
    $request->setOrgReqDate($originalDate);
    $request->setExtendInfo(['org_req_seq_id' => $originalRequestId]);
    $result = (new BsPayClient())->postRequest($request, false);
    return checkedBalanceResponse($result);
}

function sendBalanceSms(array $validatedSmsData): array {
    $result = (new BsPayClient())->postRequest([
        'funcCode' => 'v2/trade/sms/verifycode/send',
        'params' => $validatedSmsData,
    ], false);
    return checkedBalanceResponse($result);
}

function checkedBalanceResponse($result): array {
    if ($result === null || $result->isError()) {
        throw new RuntimeException('SDK请求或响应验签失败，拒绝处理业务结果');
    }
    $envelope = $result->getRspDatas();
    if (!is_array($envelope) || !isset($envelope['data']) || !is_array($envelope['data'])) {
        throw new RuntimeException('SDK响应缺少合法业务data');
    }
    return $envelope['data'];
}
```

SDK返回响应对象或null；上述包装在检查SDK错误和信封类型后才返回业务data数组，调用方再检查resp_code及接口状态。异常边界必须处理，不消费未验签响应或将缺失结果当成功。查询原全局流水分支仅使用 `org_hf_seq_id`。短信映射只有五个正式业务字段，不含sign信封、needSign/needVerfySign控制项或额外huifu_id。

## 签验与条件

付款关系 `pay_relations` 请求是JSON数组字符串。SDK反射和 `array_merge` 不能充当业务校验器；条件不成立时不要为C字段填空值或伪造默认值。

通用调用为SDK自带 `postRequest` 数组入口，保持 `tag=false` 的JSON加签/验签。不得用 `tag=true` 页面模式、CURLFile上传模式或手写curl替代常规余额支付。通知及严格响应的未知部分只提供独立适配点。
