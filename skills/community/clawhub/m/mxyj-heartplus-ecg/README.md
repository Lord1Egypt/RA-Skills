# 心脏+ 龙虾版

## 声明
本技能仅支持中国大陆用户和持有中国大陆手机号的用户使用。

## 产品定位

- 目标用户：拥有 Apple Watch 且设备支持 ECG 功能的 iPhone 用户
- 核心价值：自然对话触发 + 授权后免上传查看，快速获得心电结果解读
- Slogan：说出你的心声，读懂你的心电。

必备免责声明：

Apple Watch ECG 不能检测心脏病发作、血液凝块或中风，也不能识别高血压。出现胸痛、胸闷等明显不适，请立即联系医生或急救服务。

## 业务背景

本技能用于心脏+ App 场景的命令化执行，覆盖从身份准备到报告查看的完整链路：

- 手机号配置与复用
- App 授权通知与授权状态查询
- 安全校验状态核验
- 心电检测通知
- 报告列表与详情查询

## 文档优先级与阅读顺序

触发本技能后，先阅读 `references` 再执行脚本，顺序如下：

1. `references/SessionKey获取说明.md`：确认 SessionKey 解析优先级、反例与失败回退
2. `references/报告输出说明.md`：确认报告输出直通规则与自检清单
3. `references/交互话术库.md`：确认用户沟通措辞、提问方式与拒绝场景处理话术
4. `references/脚本与流程说明.md`：确认命令调用顺序、动作边界与参数口径
5. 返回本文档的“最小可执行步骤”或“推荐流程”执行命令

维护原则：

- `references` 是业务话术与流程细节的权威来源
- README 与 `SKILL.md` 仅保留摘要与入口，不复制 `references` 全文

## 会话与路由约束

- 所有业务命令都必须显式传入 `--session-key`
- `sessionKey` 获取优先级固定为：用户显式提供 > `session_status` 的 `Session:` 字段 > 失败提示
- 禁止从 UI 标签、渠道名、会话昵称、会话标题推断 `sessionKey`
- 显式值与 `session_status` 的 `Session:` 字段均不可用时，返回：`未获取到有效会话标识。请提供可用的 sessionKey（例如 agent:main:main）后重试。`
- 会话解析与预检属于内部流程，禁止向用户逐步播报

## 执行前 5 项自检

1. `sessionKey` 是否按“显式提供 > `session_status` 的 `Session:` 字段 > 失败提示”获取  
2. 本轮所有业务命令是否透传同一个 `--session-key`  
3. 是否已执行 `phone_manager get` 与 `gateway_manager check_factory`  
4. `check_factory != True` 时是否先执行 `send_authorize_notify` 并按 `next_action` 分流（App 授权需等用户确认后再轮询）  
5. `send_authorize_notify` 与 `poll_authorization` 是否使用 `mini/api` 明文接口且不依赖安全校验状态  

## 快速开始

### 前置条件

- 已安装 `uv`
- 用户已在 iOS 设备安装并登录心脏+ App，且 App 版本为 1.6.0 或以上
- 当前仅支持中国大陆手机号用户使用本服务。
- 网络环境允许访问安全程序下载地址及业务接口

### 最小可执行步骤

1. 保存手机号（按会话 Key 隔离）

```bash
uv run scripts/phone_manager.py --action save --phone 13800138000 --session-key "agent:main:main"
```

1. 发送 App 授权通知

```bash
uv run scripts/api_manager.py --action send_authorize_notify --session-key "agent:main:main"
```

1. 按授权方式继续

- 若返回 `next_action=wait_user_confirm_then_poll_authorization`（`status=1`），先提示用户在 App 完成授权并回复“已授权”，再轮询授权状态并完成校验：

```bash
uv run scripts/api_manager.py --action poll_authorization --max-wait-seconds 45 --interval-seconds 3 --session-key "agent:main:main"
```

- 若返回 `next_action=ask_user_sms_code_then_verify`（`status=0`），先让用户输入短信验证码，再执行：

```bash
uv run scripts/api_manager.py --action verify_code --code 123456 --session-key "agent:main:main"
```

- 支持多会话并存手机号绑定；每个会话独立授权，新会话或变更手机号后需重新完成本会话授权校验

1. 查询报告列表

```bash
uv run scripts/api_manager.py --action report_list --page-num 0 --page-size 10 --session-key "agent:main:main"
```

1. 按最近列表序号查询详情

```bash
uv run scripts/api_manager.py --action report_detail --index 1 --session-key "agent:main:main"
```

1. 查询最新报告

```bash
uv run scripts/api_manager.py --action latest_report --session-key "agent:main:main"
```

## 推荐流程

```bash
uv run scripts/phone_manager.py --action get --session-key "agent:main:main"
uv run scripts/gateway_manager.py --action ensure --session-key "agent:main:main"
uv run scripts/gateway_manager.py --action check_factory --session-key "agent:main:main"
uv run scripts/api_manager.py --action send_authorize_notify --session-key "agent:main:main"
# 用户回复“已授权”后，再执行：
uv run scripts/api_manager.py --action poll_authorization --max-wait-seconds 45 --interval-seconds 3 --session-key "agent:main:main"
uv run scripts/api_manager.py --action measure_notify --session-key "agent:main:main"
uv run scripts/api_manager.py --action report_list --page-num 0 --page-size 10 --session-key "agent:main:main"
uv run scripts/api_manager.py --action report_detail --index 1 --session-key "agent:main:main"
uv run scripts/api_manager.py --action latest_report --session-key "agent:main:main"
```

## 脚本职责速览

### phone_manager.py

- `--action get`：读取已保存手机号
- `--action save --phone`：保存手机号

### gateway_manager.py

- `--action platform`：输出当前平台标识
- `--action ensure`：确保安全校验程序可用，必要时自动下载
- `--action check_factory`：检查安全校验状态
- `--action verify --code`：提交授权码

### api_manager.py

- `--action send_authorize_notify`：发送 App 授权通知
- `--action send_code`：发送短信验证码
- `--action verify_code --code`：使用用户短信验证码执行授权校验
- `--action query_authorization`：查询授权状态（兼容动作，非标准流程不推荐）
- `--action poll_authorization`：轮询授权状态
- `--action measure_notify`：下发心电检测通知
- `--action report_list`：查询并渲染报告列表，并写入 `report_list_cache.json` 的会话分区
- `--action latest_report`：查询并渲染最新报告
- `--action report_detail --report-no`：按报告编号查询并渲染指定报告（`--report-id/--reportId` 仅兼容不推荐）
- `--action report_detail --index`：按最近列表序号查询并渲染指定报告
- 报告详情参数建议优先使用 `--index` 或 `--report-no`

## 常见问题与排查

### 提示“未配置手机号，请先保存手机号”

先执行：

```bash
uv run scripts/phone_manager.py --action save --phone 13800138000 --session-key "agent:main:main"
```

### verify 返回 False 或提示安全校验未通过

这通常表示授权未完成或安全校验状态已过期。按顺序重试：

```bash
uv run scripts/api_manager.py --action send_authorize_notify --session-key "agent:main:main"
# 用户回复“已授权”后，再执行：
uv run scripts/api_manager.py --action poll_authorization --max-wait-seconds 45 --interval-seconds 3 --session-key "agent:main:main"
```

- 授权码仅用于内部校验，不在用户可见回复中展示。

### report_detail 报错缺少参数

请补充 `--report-no` 或 `--index`：

```bash
uv run scripts/api_manager.py --action report_detail --report-no 报告编号 --session-key "agent:main:main"
uv run scripts/api_manager.py --action report_detail --index 1 --session-key "agent:main:main"
```

若使用 `--index`，需先执行一次：

```bash
uv run scripts/api_manager.py --action report_list --page-num 0 --page-size 10 --session-key "agent:main:main"
```

### 报告详情输出必须直通脚本正文

- 禁止在正文前后增加“我帮你总结”“查询完成”等附加文本
- 若用户追问指标解释，另开一条解释回复，不改写原报告正文

### 时间筛选参数格式错误

`--take-time-copy` 和 `--take-time-over` 必须是：

- `YYYY-MM-DD HH:mm:ss`

示例：

```bash
uv run scripts/api_manager.py --action report_list --take-time-copy "2026-03-06 00:00:00" --take-time-over "2026-03-06 23:59:59" --session-key "agent:main:main"
```
