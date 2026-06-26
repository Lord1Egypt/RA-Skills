# 汇付共享资料总览

这份总览用于帮助 AI 在单 Skill 结构下快速定位共享规则、产品线和引用顺序。

详细子文档由对应入口继续路由，这里只保留共享层和主入口，不重复抄整套 reference 清单。

## 目录

- 什么时候先读这里
- 接入副驾驶地图
- 共享资料地图
- 产品线判断树
- 推荐阅读顺序
- 当前版本事实
- PHP 官方 SDK 口径
- 全局边界

## 什么时候先读这里

- 第一次接入汇付支付，需要先判断聚合支付、托管支付和前端收银台的关系
- 需要先确认签名、异步通知、请求头、多语言边界或版本口径
- 用户询问 Skill 版本、如何更新、是否最新版、能力缺失是否需要升级，或排查后需要官方 AI 技能包技术支持
- 准备写代码，但还不确定应该先读哪份 `references/*.md`

## 接入副驾驶地图

| 文件 | 用途 |
| --- | --- |
| `references/official-service-source-index.md` | 业务指引、联调攻略、FAQ、AI 技能包技术支持联系方式的官方资料源索引和脱敏采集边界 |
| `references/copilot-onboarding.md` | 首次接入 / 存量系统接入识别和接入判断卡 |
| `references/copilot-solution-selection.md` | 聚合支付、托管支付、checkout-js 和存量增量接入的推荐规则 |
| `references/copilot-solution-cards.md` | 18 张联调方案卡的统一模板和 P0/P1 清单 |
| `references/copilot-existing-system.md` | 已有订单系统、回调、退款和状态机的保守改造口径 |
| `references/copilot-troubleshooting-playbooks.md` | 高频联调问题、开发问题和升级人工 Playbook |
| `references/copilot-parameter-review.md` | 请求参数、返回参数和代码片段检查规则 |
| `references/copilot-go-live-checklist.md` | 通用和存量系统上线检查、必测项、升级材料 |
| `references/canonical-regression-prompts.md` | 安装后可随 Skill 分发的 5 条最小回归 Prompt |
| `references/hostingpay-preorder-douyin-direct.md` | 托管支付抖音直连下单字段与返回 |
| `references/hostingpay-query-splitpay.md` | 拆单支付订单查询字段与返回 |

## 共享资料地图

| 文件 | 用途 |
| --- | --- |
| `references/shared-signing-v2.md` | V2 加签与验签公共规则 |
| `references/shared-async-notify.md` | 接口 `notify_url` 异步通知、RSA 验签、幂等和回包要求 |
| `references/shared-webhook-signing.md` | 控台 Webhook 终端密钥、MD5 验签和原始请求体边界 |
| `references/shared-request-header-policy.md` | 服务端请求头强制约束 |
| `references/shared-server-sdk-matrix.md` | 服务端语言能力边界和模板入口 |
| `references/shared-frontend-sdk-matrix.md` | 前端收银台 JS SDK 能力边界 |
| `references/shared-versioning-policy.md` | 当前版本治理口径 |
| `references/skill-version-policy.md` | 用户侧版本提示、更新方式和能力缺失升级口径 |
| `references/shared-release-checklist.md` | 发版前检查项 |
| `references/shared-credential-boundary.md` | 凭据存放、注入与使用边界 |
| `references/shared-copyright-notice.md` | 版权说明和引用边界 |

## 产品线判断树

```text
你现在要解决什么？
├─ 标准服务端收款，优先快速接入
│  └─ 走聚合支付：aggregation-base -> aggregation-order -> aggregation-query -> aggregation-refund
├─ 项目制预下单、托管收银台、完整服务端闭环
│  └─ 走托管支付：hostingpay-base -> hostingpay-preorder -> hostingpay-query -> hostingpay-refund
│     ├─ 抖音直连下单：hostingpay-preorder-douyin-direct
│     └─ 拆单支付订单查询：hostingpay-query-splitpay
└─ 商户自有页面嵌入 checkout 或单支付按钮
   └─ 先接 hostingpay-preorder，再读 checkout-js，最后回到 hostingpay-async-webhook + hostingpay-query 做服务端最终确认闭环
```

## 推荐阅读顺序

```text
1. 先读接入副驾驶层：向导、方案选择、方案卡、问题排查或上线检查
2. 再读共享层：签名、`notify_url`、控台 Webhook、请求头、语言矩阵
3. 再读对应产品线 base 文档
4. 再读具体业务场景文档：下单 / 预下单 / 查询 / 退款 / 前端组件
5. 最后把官方 SDK、环境变量和业务真实参数接到项目代码里
```

## 当前版本事实

| 项目 | 当前口径 |
| --- | --- |
| Skill 包版本 | `1.3.0` |
| 托管支付 Java SDK 常量版本 | `dg-java-sdk 3.0.38` |
| 聚合支付 Java SDK 版本 | `dg-lightning-sdk 1.0.5` |
| Python SDK 包 | `dg-sdk 2.0.22`，import 名为 `dg_sdk` |
| Python 生产环境变量 | 见 `aggregation-python-adapter.md` 与 `hostingpay-python-adapter.md` |
| 前端收银台 JS SDK | npm 包 `@dg-elements/js-sdk`，接入时以项目锁定版本为准，升级前查询 npm registry |
| `HUIFU_SKILL_SOURCE` 最终上送格式 | `<skill_source>` |

## PHP 官方 SDK 口径

PHP 场景默认以官方 Composer 包 `huifurepo/dg-php-sdk` 落地：

- 当前 Skill 包基线：`2.0.27`
- 新项目安装：`composer require "huifurepo/dg-php-sdk:^2.0.27"`
- 已安装旧版本时：先调整 `composer.json` 版本约束，再执行 `composer update huifurepo/dg-php-sdk --with-all-dependencies`
- 聚合支付核心主链路优先 `BsPaySdk\core\Payment`
- 聚合对账与托管支付优先 `BsPayClient::postRequest()`

如果 Composer 不可用，使用 `https://api.github.com/repos/huifurepo/bspay-php-sdk/zipball/refs/tags/2.0.27` 手动下载当前基线，解压后让 `HUIFU_SDK_ROOT` 指向实际 `BsPaySdk` 目录并校验 `init.php`。

当前 Skill 包不再内置 PHP 模板资产或非官方自维护 client。需要核对请求头、签名、HTTP 发送链路差异时，先读 `references/shared-request-header-policy.md` 与 `references/shared-signing-v2.md`；如果问题是控台 Webhook 验签，再读 `references/shared-webhook-signing.md`。必要时检查项目实际安装的官方 SDK 源码；不要用历史自维护实现替代官方 SDK 主链路。

## 全局边界

- `HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 只能留在服务端
- `project_id`、`callback_url`、`sub_openid`、`buyer_id`、`auth_code`、`devs_id` 等运行时值必须来自真实业务链路
- 前端回调不等于最终支付成功；最终状态必须经服务端闭环确认，异步通知需验签、事件级幂等和状态锁，并通过查单二次确认或补偿查询兜底
- PHP 如果使用当前 Skill 包对齐的官方 SDK 主链路，且初始化时已给 `MerConfig.skill_source` 赋值，SDK 会自动带出 skill 相关来源头
- Python 如果使用当前 Skill 包对齐的官方 `dg-sdk 2.0.22`，必须固定 `DGClient.env = "prod"`、显式传入 `MerConfig.jpt_x_skill_source`，并在每个 request 对象中设置本次真实 `huifu_id`；SDK 会从请求参数自动推导 `jpt-x-skill-huifu_id`，并使用 `jpt-sdk_version` 上送 SDK 版本。安装或版本核对失败时必须显式报错并停止，不要无版本安装或降级。
- 如果其他脚本语言没有官方 SDK 自动补头能力，或当前实现绕开了官方 SDK 主链路，必须按 `references/shared-request-header-policy.md` 手动补头
