# Python 适配说明

本文件对应聚合支付 Python 接入。

## 目录

- 当前覆盖范围
- 官方 SDK 入口
- 安装与环境变量前置检查
- 初始化模板
- 强制 HTTP 请求头
- 聚合支付 SDK 映射
- 对账调用路径
- 与 README / 源码冲突的处理
- 设计约束
- 场景入口

## 当前覆盖范围

- 聚合支付下单：`dg_sdk.Payment.create()` + `PaymentCreateRequest`
- 扫码交易查询：`dg_sdk.Payment.query()` + `PaymentQueryRequest`
- 扫码交易关单：`dg_sdk.Payment.close()` + `PaymentCloseRequest`
- 扫码交易关单查询：`dg_sdk.Payment.close_query()` + `PaymentCloseQueryRequest`
- 扫码交易退款：`dg_sdk.Payment.refund()` + `PaymentRefundRequest`
- 扫码交易退款查询：`dg_sdk.Payment.refund_query()` + `PaymentRefundQueryRequest`
- 对账单查询：`V2TradeCheckFilequeryRequest().post({})`

## 官方 SDK 入口

聚合支付 Python 默认使用官方 pip 包：

- 包名：`dg-sdk`
- import 名：`dg_sdk`
- 当前 Skill 包基线：`2.0.22`
- 源码级差异以项目实际安装包复核为准

核心支付主链路优先走：

- `dg_sdk.Payment`
- `PaymentCreateRequest`
- `PaymentQueryRequest`
- `PaymentCloseRequest`
- `PaymentCloseQueryRequest`
- `PaymentRefundRequest`
- `PaymentRefundQueryRequest`

对账使用：

- `dg_sdk.V2TradeCheckFilequeryRequest().post({})`

不要绕开官方 `dg_sdk` 另写一套 Python HTTP / RSA client。

## 安装与环境变量前置检查

输出 Python 可运行代码时，必须先给出 SDK 安装和环境变量准备。

```bash
python3 -m pip install "dg-sdk==2.0.22"
python3 -c "import dg_sdk; print(dg_sdk.DGClient.__version__)"
```

安装或版本核对失败时，必须显式报错并停止；不得静默改用 `pip install dg-sdk` 无版本约束安装，也不得降级到更低版本。版本核对必须以 `dg_sdk.DGClient.__version__ == '2.0.22'` 输出为准。

运行前至少准备：

```bash
export HUIFU_SYS_ID="渠道商或商户系统号"
export HUIFU_PRODUCT_ID="汇付产品号"
export HUIFU_RSA_PRIVATE_KEY="商户 RSA 私钥"
export HUIFU_RSA_PUBLIC_KEY="汇付 RSA 公钥"
export HUIFU_SKILL_SOURCE="hfps/1.3.0"
export HUIFU_MERCHANT_ID="本次请求的 huifu_id"
export HUIFU_NOTIFY_URL="https://your-domain.example/huifu/notify"
export HUIFU_DG_ENV="prod"
```

上面只给生产环境变量清单，不提供独立 env 示例文件；不要把真实私钥或商户凭据写入仓库。

## 初始化模板

Python 示例必须显式失败，不允许静默默认。

```python
import os

import dg_sdk


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"缺少环境变量：{name}")
    return value


def init_huifu_sdk() -> None:
    dg_sdk.DGClient.env = "prod"
    dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(
        require_env("HUIFU_RSA_PRIVATE_KEY"),
        require_env("HUIFU_RSA_PUBLIC_KEY"),
        require_env("HUIFU_SYS_ID"),
        require_env("HUIFU_PRODUCT_ID"),
        require_env("HUIFU_SKILL_SOURCE"),
    )
```

`MerConfig` 的第五个参数对应 `jpt_x_skill_source`，最终成为 HTTP 请求头 `jpt-x-skill-source`，不是 `data` 业务字段。`dg-sdk 2.0.22` 不再接收 `jpt_x_skill_huifu_id` 初始化参数。

Python 示例统一固定为生产 `prod` 环境，不再生成联调环境切换函数；不要失败后自动降级。

## 强制 HTTP 请求头

Python 官方 SDK 会生成以下请求头：

| Header | 值 |
| --- | --- |
| `jpt-sdk_version` | `python_2.0.22` |
| `jpt-x-skill-source` | `MerConfig.jpt_x_skill_source` |
| `jpt-x-skill-huifu_id` | SDK 从最终请求参数 `data.huifu_id` 自动取值；没有 `huifu_id` 时为空 |
| `Content-Type` | 非文件请求为 `application/json;charset=utf-8` |

`jpt-x-skill-source` 和 `jpt-x-skill-huifu_id` 都是 HTTP 请求头，不是 `data` 业务字段。

当前 Python SDK 会在 `ApiRequest._build_request_info()` 中执行 `params.get("huifu_id", "")`，并写入 `jpt-x-skill-huifu_id` 请求头。多商户或代调用场景不需要为 huifu 头重置 `DGClient.mer_config`，但每次业务请求对象必须设置本次真实 `huifu_id`。

## 聚合支付 SDK 映射

| 场景 | Python SDK 入口 |
| --- | --- |
| 下单 | `dg_sdk.Payment.create(PaymentCreateRequest)` |
| 扫码交易查询 | `dg_sdk.Payment.query(PaymentQueryRequest)` |
| 扫码交易关单 | `dg_sdk.Payment.close(PaymentCloseRequest)` |
| 扫码交易关单查询 | `dg_sdk.Payment.close_query(PaymentCloseQueryRequest)` |
| 扫码交易退款 | `dg_sdk.Payment.refund(PaymentRefundRequest)` |
| 扫码交易退款查询 | `dg_sdk.Payment.refund_query(PaymentRefundQueryRequest)` |

原交易定位键必须来自下单结果落库或上游响应，不要临时猜测 `req_date`、`req_seq_id`、`hf_seq_id`、`party_order_id`。

## 对账调用路径

对账走 `V2TradeCheckFilequeryRequest().post({})`。不要走 `dg_sdk.Payment`，也不要手写 URL。

## 与 README / 源码冲突的处理

`README.rst` 中示例仍把第五个 `MerConfig` 参数写成 `huifu_id`。本 Skill 的 `2.0.22` 口径要求第五个参数是 `jpt_x_skill_source`，不是商户号；源码 docstring 如仍残留 `jpt_x_skill_huifu_id` 说明，也要以实际安装包 / 本地源码的函数签名和 `api_request.py` 请求头构造逻辑为准。

## 设计约束

1. 聚合支付 Python 已覆盖核心支付主链路与对账；不要再把 Python 的下单、查单、退款误判为 unsupported。
2. 核心支付接口优先 `dg_sdk.Payment`；对账使用 request 类 `.post({})`。
3. 如果用户项目安装的 `dg-sdk` 版本不是 `2.0.22`，先验证实际版本和源码签名，再继续生成代码。
4. `T_JSAPI`、`T_MINIAPP`、`T_APP`、`T_MICROPAY`、`A_JSAPI`、`A_NATIVE`、`A_MICROPAY`、`U_JSAPI`、`U_NATIVE`、`U_MICROPAY` 这些值不是 `method_expand` 的 key；`method_expand` 的 JSON 内容直接是当前场景对象本身。
5. `tx_metadata` 本身不作为请求字段上送；交易能力扩展按能力名直接传 `acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info`。
6. `method_expand`、`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 等 JSON 字段应先在业务层建模，再在 SDK 边界转成 JSON 字符串。
7. 原交易定位键必须来自业务订单表或上游响应，不要照抄 demo 占位。
8. 不要复制官方 SDK `README.rst` 示例里的测试私钥。

## 场景入口

- 下单、查询、关单、退款、对账：`references/aggregation-python-scenarios.md`
- 接口 `notify_url` 验签：`references/shared-signing-v2.md`
- 控台 Webhook 验签：`references/shared-webhook-signing.md`，Python 端使用 `dg_sdk.DGTools.verify_webhook_sign(data, sign, key)`
