# 本地沙箱联调入口

本文件定义支付 Skill `1.6.0` 对 `hf-payment-local-sandbox` 的使用边界、路由和最小操作口径。它只用于本地协议模拟、闭环演练和自检报告，不替代汇付官方联调环境或生产上线验收。

## 目录

- [什么时候读取](#什么时候读取)
- [当前版本口径](#当前版本口径)
- [固定边界](#固定边界)
- [最小使用流程](#最小使用流程)
- [常用演练能力](#常用演练能力)
- [与正式联调的关系](#与正式联调的关系)
- [输出规则](#输出规则)
- [推荐短句](#推荐短句)

## 什么时候读取

- 用户询问本地沙箱、local-sandbox、本地模拟支付、本地联调、沙箱报告或故障注入。
- 用户已经完成代码接入，想在正式联调前做本地闭环演练。
- 用户需要解释 `hf-payment-local-sandbox` 的启动命令、测试凭据、回调重放、报告或边界。
- 用户把本地沙箱通过误认为官方联调通过、生产可上线或通道验收通过时。

普通聚合支付、托管支付、checkout-js 字段和 SDK 代码问题，不因为存在本地沙箱而强行读取本文件；先按产品线文档处理。

## 当前版本口径

| 项目 | 当前口径 |
| --- | --- |
| 支付 Skill 版本 | `1.6.0` |
| 本地沙箱源码候选 | `hf-payment-local-sandbox 1.0.1`，report schema `1.8` |
| 当前公开 preview | `hf-payment-local-sandbox 1.0.0`；`1.0.1` 发布前不得称公开包已升级 |
| Contract bundle | `huifu-pay-integration-1.3.0-r4` |
| 推荐凭证 Profile | `official-demo` |
| 数据来源 | 合成数据和脱敏样例派生 fixture |
| 报告性质 | 本地自检报告，不是官方认证 |
| 预览总包下载 | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest-preview.zip` |
| 公开更新索引 | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest.json` |
| 下载包内容 | 构建后的 preview 总包，内含各平台 archive、启动器、`USAGE.md`、SBOM、provenance、manifest 和 SHA256 清单 |
| 分发状态 | 公开预览下载可用；正式公开上线仍需签名、公证、授权和版本固定下载 URL 证据 |

`1.0.1` 源码候选的协议契约仍锁定 `huifu-pay-integration-1.3.0-r4`，这是支付协议冻结快照；支付 Skill `1.6.0` 不修改该契约。`1.0.1` 只把冻结快照证据显式报告为 `frozen_snapshot`，并用 report schema `1.8` 标识这项报告行为变化。

预览总包 URL 当前对应维护者构建出的 `hf-payment-local-sandbox-1.0.0-preview.zip` 重命名分发包。`latest-preview.zip` 是便于官网文档长期引用的预览别名；在 `1.0.1` 完成构建、签名与发布证据前，只能称其为源码/提测候选，不能把公开 URL 描述为 `1.0.1`。如果用户要正式上线证据或不可变归档，应使用带版本号的固定下载 URL、SHA256 和发布记录。

### 2026-07-28 官方合同差异硬停

`r4` 是历史冻结快照，不随本轮官方接口页刷新。首轮复审确认下列行为与 `2026-07-28` 官方合同不一致；在新沙箱版本和新 contract bundle 完成发布前，禁止用当前沙箱为这些规则出具“通过”结论：

| 场景 | 当前冻结沙箱偏差 | 官方合同 | 使用结论 |
| --- | --- | --- | --- |
| 支付宝/微信小程序预下单 | 对 `pre_order_type=2/3` 错误要求 `hosting_data` | `hosting_data` 为 H5/PC 统一收银台扩展参数，小程序预下单不应因缺失它失败 | 小程序该字段校验转正式联调 |
| 对账查询 | `file_details`、`task_details` 可能返回 Object/map | 两字段类型均为 Array；空值也必须按数组语义处理 | 不用当前沙箱验证数组类型和反序列化 |
| 聚合主动关单 | 未完整保护一分钟内订单、银联订单和成功/失败终态 | 仅微信/支付宝非终态且订单超过一分钟可发起；银联不支持，成功/失败终态不得关单 | 不用当前沙箱验证关单准入或状态机 |
| 托管关单 | 可能允许已成功订单关单并改变终态 | 原订单成功/失败终态不得再次关单或发生回退 | 不用当前沙箱验证终态保护 |

这里的硬停不授权改写 `r1-r4` 或同名样例包。修复运行时必须发布新的沙箱版本和新的 contract bundle，并重新生成 fixture、摘要和兼容性报告；在此之前，以对应支付原子 reference 和官方联调结果为准。

## 固定边界

必须长期保留这些结论：

- 本地联调通过，不代表官方联调通过。
- 本地联调通过，不代表具备生产上线条件。
- local-sandbox 不创建真实交易，不验证真实商户权限、通道、费率、风控或资金结果。
- 不把真实商户私钥、真实订单号、真实流水、真实 openid 或生产配置写入沙箱报告、Skill 包或前端代码。
- 不使用 local-sandbox 报告对生产事故定责。

## 最小使用流程

面向客户时，默认让用户下载构建后的预览总包，而不是使用仓库里的本地编译二进制，也不要要求客户安装 Go 后自行构建。维护者排障或二次开发时才从源码执行 `go build`。

预览总包下载地址：

```text
https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest-preview.zip
```

下载后，先解压外层 `hf-payment-local-sandbox-latest-preview.zip`，再从 `dist/` 中选择当前系统对应的平台包：

- Windows：解压 `hf-payment-local-sandbox_1.0.0_windows_amd64.zip`
- macOS Intel：解压 `hf-payment-local-sandbox_1.0.0_darwin_amd64.tar.gz`
- macOS Apple Silicon：解压 `hf-payment-local-sandbox_1.0.0_darwin_arm64.tar.gz`
- Linux x86_64：解压 `hf-payment-local-sandbox_1.0.0_linux_amd64.tar.gz`

如果用户只想快速开始，预览包里已带启动器：Windows 双击 `start-local-sandbox.cmd`，macOS 双击 `start-local-sandbox.command`，Linux 在终端运行 `./start-local-sandbox.sh`。启动器会使用 `official-demo`，默认打开 `http://127.0.0.1:8765/` 控制台，并把本地网关固定在 `http://127.0.0.1:8766`。测试期间不要关闭启动窗口；停止时按 `Ctrl+C`。

1. 先核对版本和契约：

```bash
hf-payment-local-sandbox version --json
hf-payment-local-sandbox doctor --json
hf-payment-local-sandbox validate contract
```

2. 启动本地服务。默认控制面只监听本机，协议面默认 `127.0.0.1`：

```bash
hf-payment-local-sandbox serve \
  --control-port 8765 \
  --gateway-port 8766 \
  --credential-profile official-demo \
  --print-json \
  --report-dir ./sandbox-report
```

`--print-json` 会输出 `control_url`、`gateway_url`、`health_url`、`mode`、`credential_profile`、`signature_model`、`admin_token` 和 `csrf_token`。这些 token 只用于本机控制面，不要写入仓库、聊天记录或可分享报告。公开健康检查和页面状态接口不返回 `admin_token`、`csrf_token` 或 Webhook 端点密钥。

启动后可以直接在浏览器打开 `control_url`。首次进入控制台会展示本地沙箱服务使用声明；默认勾选“不再提示”，同意后继续使用，拒绝后停止本地沙箱服务并尝试关闭当前页面。本地控制台会自动刷新运行状态，展示接入信息、可复制的 `gateway_url`、支付/退款/关单/对账记录、事件流、Notify/Webhook 投递记录和安全发现。页面“项目接入配置”提供“导出凭证”、“复制配置”、“显示 Webhook Key”、“保存 Webhook”和“使用说明”；导出凭证和显示 Webhook Key 都需要输入启动输出中的 `admin_token`，浏览器会下载 `sandbox-credentials.json` 或在页面显示本次运行的 `webhook_endpoint_key`。托管支付记录可点击“模拟成功”，用于把本地预下单状态推进为支付成功并触发后续查单、Notify 或 Webhook 演练；手动 Notify/Webhook 只做投递测试，不直接改业务主记录。Webhook 目标可在页面输入本机接收地址并保存，本次运行内业务状态里的 Webhook 成功/失败按钮会变为可用；外部 Webhook 地址仍需启动时通过 `--notify-allow` 精确放行。生成报告或停止服务同样需要 `admin_token`；页面不会持久化保存 token，页面状态接口不返回 `admin_token`、`csrf_token`、完整私钥、Webhook 端点密钥或回调 URL query 明文。

控制台“接入信息”区域会从公开索引 `hf-payment-local-sandbox-latest.json` 检查更新。检查更新不需要 `admin_token`，不上传私钥、公钥、`sys_id`、`product_id`、`huifu_id`、请求日志、报告、Webhook 地址或 Notify 地址；只读取公开 JSON，并在有新版时展示当前平台下载地址、文件名、大小和 SHA256。沙箱不做静默自动安装，用户下载新版后手动解压并重新启动。

3. 查看或导出 `official-demo` Profile。普通用户优先通过页面“导出凭证”下载 `sandbox-credentials.json`；命令行导出只作为维护者排障能力。无论哪种方式，都不要在文档、日志和报告里回显完整私钥。

`official-demo` 用户可见字段固定为 `product_id`、`sys_id`、商户请求签名私钥、沙箱响应验签公钥和 Webhook 终端密钥。预览包不内置完整私钥；首次使用时会在本机生成或读取 `sandbox-data/credentials/official-demo-merchant-private.pem` 和 `sandbox-data/credentials/official-demo-sandbox-private.pem` 两套 RSA 私钥。本地沙箱模式下，请求签名使用导出的商户私钥；沙箱用本机保存的商户请求验签公钥验请求签名；响应和通知由本机沙箱私钥加签；客户项目优先用导出的 `merchant_public_key` 验响应和通知签名。页面导出的 `sandbox-credentials.json` 只面向商户项目配置，和“复制配置”保持同一套扁平英文 key：`gateway_url`、`sys_id`、`product_id`、`huifu_id`、`skill_source`、`merchant_private_key`、`merchant_public_key`、`webhook_endpoint_key`、`signature_model`、`usage`，不再包含重复的 `merchant_config`、`sandbox_config` 或说明型嵌套层。官方 SDK 优先字段为无 PEM 头尾、无换行的 PKCS8 Base64 `merchant_private_key` 和 X509 Base64 `merchant_public_key`；Webhook 验签使用 `webhook_endpoint_key` 计算大写 `MD5(raw_body + webhook_endpoint_key)`，业务代码可用大小写不敏感比较兼容历史实现；本地配置直接给出样例 `huifu_id = 6666000100000001`。本地沙箱模式下 `skill_source` 固定使用 `hfps/1.3.1;sandbox/1.0.1`；官方联调或生产环境使用 `hfps/1.6.0`，不要携带 `;sandbox/...` 后缀。报告中必须保留 `signature_model = dual_key_local_sandbox`。

4. 已有项目使用本地沙箱时，不是另写一套“SDK 接入指南”，而是在项目现有支付出口层增加仅本地启用的 `local-sandbox` 运行模式。先尝试把官方 SDK 的网关基础地址、base URL、endpoint 或 HTTP client 配置为 `gateway_url`；如果 SDK 没有暴露这类配置项，则保留生产路径继续走官方 SDK，只在项目自己的支付网关封装层增加本地分支：复用原有订单组装、字段校验、幂等键和请求对象，发送阶段按汇付 envelope POST 到 `gateway_url + 接口路径`，响应再转换回项目原有业务服务接口。不要改官方 SDK 源码，不要用 hosts 劫持官方域名到本机，也不要让本地分支在生产环境默认启用。

5. 演练后生成和校验报告：

```bash
hf-payment-local-sandbox validate report --path ./sandbox-report
hf-payment-local-sandbox report --report-dir ./sandbox-report --format md --output ./sandbox-report.md
```

报告中重点看 `scenario-results.json`、`endpoint-coverage.json`、`fixture-coverage.json`、`sample-coverage.json`、`sample-import-report.json`、`sandbox-scope-boundaries.json`、`security-findings.json` 和 `secret-scan.json`。

## 常用演练能力

| 目标 | 命令或方式 | 注意 |
| --- | --- | --- |
| 核对工具版本 | `version --json` | 看 `version`、`contract_bundle`、`contract_digest` |
| 自检契约 | `validate contract` | 不访问公网 |
| 跑内置场景 | `validate scenarios --report-dir <dir> --print-json` | 用于验证沙箱自身完整性 |
| 查看单 Profile 指纹 | `credentials show-profile official-demo` | 只展示指纹，不展示完整私钥 |
| 打开交互控制台 | 浏览器访问启动输出中的 `control_url` | 查看业务状态、事件流、Notify/Webhook 和安全发现 |
| 推进托管支付成功 | 支付记录点击“模拟成功” | 只对本地托管预下单记录生效，用于查单、通知和 Webhook 闭环演练 |
| 检查版本更新 | 控制台点击“检查更新” | 读取 `hf-payment-local-sandbox-latest.json`，只提示下载，不静默替换程序 |
| 双击启动预览版 | Windows 用 `start-local-sandbox.cmd`；macOS 用 `start-local-sandbox.command` | 本质仍是本机 CLI 服务，启动窗口要保持打开 |
| 已有项目访问沙箱 | 同机用 `http://127.0.0.1:8766`；容器内通常用宿主机地址；跨机器需显式开放 gateway | 不要把控制面 token 暴露到外网 |
| 静态建议扫描 | `validate code --path <project>` | advisory only，不能证明生产闭环正确 |
| 通知重放 | `replay --target <url> --report-dir <dir>` | 默认只允许 loopback，外部地址必须显式 allowlist |
| Webhook 重放 | `replay --kind webhook --target <url>` | 与接口 `notify_url` 验签边界不同 |
| 清理本地运行 | `purge --older-than 30d` 或 `purge --run-id <id>` | 只清理本地沙箱运行目录 |

## 与正式联调的关系

本地沙箱适合在正式联调前发现这些问题：

- 请求 envelope、签名、请求头、必填和条件字段是否基本正确。
- 异步通知验签、幂等、固定成功回包和查单补偿是否形成闭环。
- 支付、托管支付成功推进、退款、关单、对账等核心状态流转是否在本地可演练。
- 重复通知、超时、错误回包、处理中再查单等异常路径是否有保护。
- 报告是否能证明本地演练经过了哪些合成场景。

需要验证“用户应用使用真实汇付公钥验官方响应签名”时，应进入正式官方联调流程，使用官方联调/生产配置下发的真实公钥和证书材料；不要把本地沙箱导出的 `merchant_public_key` 和正式联调凭证混用。

它不能证明这些事项：

- 商户、服务商、`sys_id`、`product_id`、`huifu_id`、`project_id` 的真实权限已经开通。
- 微信、支付宝、银联、抖音等真实通道和 appid/openid 关系已可用。
- 费率、风控、分账准入、清结算、发票、取现或生产资金结果正确。
- 真实公网 `notify_url`、证书、网络策略、渠道配置和生产监控已经合格。

## 输出规则

回答本地沙箱问题时，必须：

- 列出本轮实际使用的 references，通常包含 `references/shared-local-sandbox.md`，再按场景补产品线、异步通知、上线检查或版本策略。
- 明确 local-sandbox 是本地协议模拟和报告工具，不是官方联调或生产准入结论。
- 如果用户要“上线证明”，必须转到 `references/copilot-go-live-checklist.md`、`references/official-service-source-index.md` 和真实签名/授权/公开下载证据。
- 如果用户要把真实密钥或真实生产流水放入沙箱，必须拒绝并要求脱敏或使用沙箱合成凭据。
- 如果用户问“已有 SDK 项目怎么使用本地沙箱”，回答重点应放在项目支付出口层的本地运行模式：能配置 SDK 网关就配置到 `gateway_url`；不能配置就加项目侧 local-sandbox 分支，而不是改官方 SDK 包。
- 如果用户只是在做普通代码接入，不主动要求安装或启动 local-sandbox。

## 推荐短句

```text
可以把 local-sandbox 当作正式联调前的本地闭环演练：它能检查请求、签名、通知、查单补偿和报告完整性，但不能证明官方联调通过，也不能证明生产可上线。
```

```text
当前支付 Skill 1.6.0 继续保留 local-sandbox 使用入口；沙箱 1.0.1 源码候选与当前公开 1.0.0 preview 的协议契约均仍是 `huifu-pay-integration-1.3.0-r4`，这是冻结兼容快照。默认 `skill_source` 为 `hfps/1.6.0`；显式合同值仍按请求头策略原样透传。
```
