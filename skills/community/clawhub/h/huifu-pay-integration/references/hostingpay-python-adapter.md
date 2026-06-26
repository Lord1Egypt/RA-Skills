# Python 适配说明

本文件对应托管支付 Python 接入。

## 目录

- 适用范围
- 官方 SDK 入口
- 安装与环境变量前置检查
- 初始化模板
- 推荐调用方式
- 强制 HTTP 请求头
- JSON 字段约束
- 新增接口兼容性
- checkout-js 协同边界
- 设计约束
- 场景入口

## 适用范围

- 托管支付 H5 / PC 预下单
- 托管支付微信小程序预下单
- 托管支付支付宝小程序预下单
- 托管支付查单 / 关单 / 对账
- 托管支付退款 / 退款查询

本文件只负责托管支付 Python。聚合支付 Python 另见 `references/aggregation-python-adapter.md`。

## 官方 SDK 入口

托管支付 Python 默认使用官方 pip 包：

- 包名：`dg-sdk`
- import 名：`dg_sdk`
- 当前 Skill 包基线：`2.0.22`
- 源码级差异以项目实际安装包复核为准

业务入口优先使用官方 request 类：

- `V2TradeHostingPaymentPreorderH5Request`
- `V2TradeHostingPaymentPreorderWxRequest`
- `V2TradeHostingPaymentPreorderAliRequest`
- `V2TradeHostingPaymentQueryorderinfoRequest`
- `V2TradeHostingPaymentCloseRequest`
- `V2TradeHostingPaymentHtrefundRequest`
- `V2TradeHostingPaymentQueryrefundinfoRequest`
- `V2TradeHostingPaymentSplitpayQueryRequest`
- `V2TradeCheckFilequeryRequest`

这些 request 类通过 `.post({})` 发起调用。

当前官方 Python SDK 源码未发现以下独立 request 类：

- 抖音直连下单独立 Request 类；该场景使用 `V2TradeHostingPaymentPreorderH5Request` + `pre_order_type="4"` 承载

## 安装与环境变量前置检查

输出 Python 可运行代码时，必须先给出 SDK 安装和环境变量准备。

```bash
python3 -m pip install "dg-sdk==2.0.22"
python3 -c "import dg_sdk; print(dg_sdk.DGClient.__version__)"
```

运行前至少准备：

```bash
export HUIFU_SYS_ID="渠道商或商户系统号"
export HUIFU_PRODUCT_ID="汇付产品号"
export HUIFU_RSA_PRIVATE_KEY="商户 RSA 私钥"
export HUIFU_RSA_PUBLIC_KEY="汇付 RSA 公钥"
export HUIFU_SKILL_SOURCE="hfps/1.3.0"
export HUIFU_MERCHANT_ID="本次请求的 huifu_id"
export HUIFU_NOTIFY_URL="https://your-domain.example/huifu/notify"
export HUIFU_PROJECT_ID="统一收银台托管项目号"
export HUIFU_PROJECT_TITLE="统一收银台托管项目标题"
export HUIFU_CALLBACK_URL="https://your-domain.example/pay/callback"
export HUIFU_RISK_CHECK_DATA_JSON="业务风控模块生成的 risk_check_data JSON 字符串"
export HUIFU_TERMINAL_DEVICE_DATA_JSON="终端/设备模块生成的 terminal_device_data JSON 字符串"
export HUIFU_DG_ENV="prod"
```

上面只给生产环境变量清单，不提供独立 env 示例文件；不要把真实私钥或商户凭据写入仓库。

安装或版本核对失败时必须显式报错并停止。不要静默改成无版本安装或降级。

## 初始化模板

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

`MerConfig` 的第五个参数是 `jpt_x_skill_source`。`dg-sdk 2.0.22` 会从最终请求参数 `data.huifu_id` 自动推导 `jpt-x-skill-huifu_id` 请求头；同一进程请求多个商户号时，不需要为 huifu 头重置 `DGClient.mer_config`，但每个 request 对象必须写入本次真实 `huifu_id`。

## 推荐调用方式

1. 业务层统一使用官方 `dg_sdk` request 类。
2. request 对象字段承载必填参数，`.post({})` 承载扩展字段。
3. 对官方参数表标注为 `String(JSON Object)` 的字段，先在业务层建对象，再在 SDK 边界序列化为 JSON 字符串。
4. 不要在业务层散落手写 URL 或自维护 HTTP client。

## 强制 HTTP 请求头

Python 官方 SDK 会生成以下请求头：

| Header | 值 |
| --- | --- |
| `jpt-sdk_version` | `python_2.0.22` |
| `jpt-x-skill-source` | `MerConfig.jpt_x_skill_source` |
| `jpt-x-skill-huifu_id` | SDK 从最终请求参数 `data.huifu_id` 自动取值；没有 `huifu_id` 时为空 |
| `Content-Type` | 非文件请求为 `application/json;charset=utf-8` |

`jpt-x-skill-source` 和 `jpt-x-skill-huifu_id` 都是 HTTP 请求头，不是 `data` 业务字段。

## JSON 字段约束

以下字段属于 `String(JSON Object)`，传给 SDK 时应是 JSON 字符串，不要直接传 Python dict：

- `hosting_data`
- `miniapp_data`
- `app_data`
- `dy_data`
- `acct_split_bunch`
- `risk_check_data`
- `terminal_device_data`
- `bank_info_data`
- `biz_info`

推荐序列化方式：

```python
json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
```

## 新增接口兼容性

| 接口 | Python `dg-sdk 2.0.22` / 官方源码核对 | 输出规则 |
| --- | --- | --- |
| 抖音直连下单 | 使用 `V2TradeHostingPaymentPreorderH5Request`，共用 `preorder` 端点 | 设置 `request.pre_order_type = "4"`；`dy_data` 必须先 `json.dumps(...)`，再通过 `.post(extend_infos)` 传入；不要生成独立抖音 request 类 |
| 拆单支付订单查询 | 存在 `V2TradeHostingPaymentSplitpayQueryRequest` 和 `V2_TRADE_HOSTING_PAYMENT_SPLITPAY_QUERY` 常量 | 可生成官方 request 类代码；字段为 `req_date`、`req_seq_id`、`huifu_id`、`org_req_date`、`org_req_seq_id` |

## checkout-js 协同边界

checkout-js 不能单独成立。服务端必须先完成托管预下单，再由前端组件拿到预下单结果完成渲染。

前端 callback 不等于最终支付成功。Python 服务端仍必须完成托管交易查询和异步通知闭环：异步通知先验签/幂等，必要时通过查单二次确认或补偿查询。

## 设计约束

1. 托管支付 Python 已覆盖预下单、查询、关单、退款、退款查询、对账和拆单支付订单查询；抖音直连按托管预下单 `pre_order_type="4"` 场景处理。
2. 所有 Python 代码必须体现官方 `dg-sdk` / `dg_sdk`。
3. `req_seq_id`、`req_date`、原交易流水、退款流水等幂等键必须由业务侧持久化。
4. `project_id`、`project_title`、`callback_url`、`sub_openid` 等运行时值必须来自真实业务链路。
5. 官方 SDK 未提供独立 request 类时，不要编造类名；抖音直连使用托管预下单 request，不需要手写 URL。
6. 不要复制官方 SDK `README.rst` 示例里的测试私钥。

## 场景入口

- 预下单、查询、关单、退款、对账：`references/hostingpay-python-scenarios.md`
- checkout-js 页面接入：`references/checkout-js.md`
- checkout-js 回调与最终确认：`references/checkout-js-callback-and-confirmation.md`
- 接口 `notify_url` 验签：`references/shared-signing-v2.md`
- 控台 Webhook 验签：`references/shared-webhook-signing.md`
