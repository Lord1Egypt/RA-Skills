# 余额支付 Python SDK 适配

使用官方 `dg-sdk==2.0.28`，import为 `dg_sdk`；初始化复用 `hostingpay-python-adapter.md`。固定 `DGClient.env="prod"`，服务端配置构造 `MerConfig(private_key=private_key, public_key=public_key, sys_id=sys_id, product_id=product_id, sign_type="RSA", jpt_x_skill_source=skill_source)`；六参全部使用关键字，防止同类型位置参数把密钥错放进sys_id/product_id；第五参数不是来源头。

完整字段及条件联读 `payment-complete-field-catalog.md`、`balancepay-field-contracts.md`，专属类见 `balancepay-sdk-matrix.md`。String(JSON)使用 `json.dumps(value, ensure_ascii=False, separators=(",", ":"))` 编码一次；解码后的[]不变成wire字段名。

## 查单与短信

```python
import dg_sdk
from dg_sdk.request.v2_trade_acctpayment_pay_query_request import (
    V2TradeAcctpaymentPayQueryRequest,
)


def query_balance_payment(initiator_id: str, original_date: str,
                          original_request_id: str):
    request = V2TradeAcctpaymentPayQueryRequest()
    request.huifu_id = initiator_id
    request.org_req_date = original_date
    return request.post({"org_req_seq_id": original_request_id})


def send_balance_sms(validated_sms_data: dict):
    # 已校验的五个正式字段，复制映射避免SDK修改调用方输入。
    return dg_sdk.DGTools.request_post(
        "/v2/trade/sms/verifycode/send", dict(validated_sms_data)
    )
```

本例不创建或重写调用方流水、日期；查询另一个定位分支只传 `org_hf_seq_id`。短信没有专属Request，商户短信Request不能替代。`DGTools.request_post` 是官方通用入口，其签名不接收 `need_sign` 等关键字；不关闭底层默认签验。

## 专属 Request 的条件差异

Python支付Request会把声明的 `fund_type/trans_fee_take_flag/verify_value` 无条件放入 `required_params`，默认空字符串；这只是生成类行为，不是官方全部必填。按业务条件给定值；不应发送的字段可使用SDK原生 `DGTools.request_post` 发送经过验证的精确映射，不能为移除空字段换成requests/httpx客户端。

专属Request的 `required_params.update(extend_infos)` 可覆盖声明字段，适配器须在调用前拒绝重叠；查询新增定位字段通过扩展字典，退款查询扩展为空。同步返回签验由SDK承担；业务仍按状态及订单一致性校验。余额支付通知未明确的包装/ACK不复制聚合或托管实现。
