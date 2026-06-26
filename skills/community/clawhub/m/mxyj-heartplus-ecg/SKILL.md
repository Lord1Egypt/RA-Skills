---
name: mxyj-heartplus-ecg
description: "这是一个用于心脏+ App 的心电健康管理技能，主要功能包括：1.发送心电检测通知并联动 Apple Watch 获取心电时序数据；2.基于心电时序数据通过心电分析算法输出报告与解读；3.查询已生成的心电分析报告（历史、最新、指定报告）。本技能需与心脏+ App 配合使用，使用前请先在 iPhone 上安装并登录“心脏+”应用，且将心脏+ App 升级至 1.6.0 或以上版本；当前仅支持中国大陆手机号用户使用本服务。"
metadata: { "openclaw": { "emoji": "🫀📱","requires": { "bins": [ "uv" ] },"install": [ { "id": "brew-uv","kind": "brew","formula": "uv","bins": [ "uv" ],"label": "Install uv (brew)","os": [ "darwin" ] }, { "id": "download-uv-linux","kind": "download","url": "https://astral.sh/uv/install.sh","bins": [ "uv" ],"label": "Install uv (linux)","os": [ "linux" ] }, { "id": "download-uv-win32","kind": "download","url": "https://astral.sh/uv/install.ps1","bins": [ "uv" ],"label": "Install uv (windows)","os": [ "win32" ] } ] } }
---

# 心脏+ 龙虾版

## 声明
本技能仅支持中国大陆用户和持有中国大陆手机号的用户使用。

## 技能定位

本技能用于“心脏+”业务链路中的四类核心动作：

- 绑定与复用手机号
- 发送 App 授权通知并在用户确认后轮询授权状态
- 校验安全状态与安全通信链路
- 查询心电报告列表、最新报告、指定编号报告

对用户能力说明统一使用以下顺序与口径：

1. 测心电（发送检测通知到心脏+ App，联动 Apple Watch 获取心电时序数据）
2. 心电解读（基于采集到的心电时序数据，通过心电分析算法输出报告与解读）
3. 查报告（查看已生成的心电分析报告：历史、最新、指定报告）

## 产品定位与价值主张

- 目标用户：拥有 Apple Watch 且设备支持 ECG 功能的 iPhone 用户
- 核心痛点：胸闷、心慌等不适出现时，缺少极简可用的心电结果解读方式
- 核心差异点：自然对话触发 + 免手动上传，用户说一句需求即可进入测量或解读链路
- Slogan：说出你的心声，读懂你的心电。
- 一句话价值主张：为佩戴 Apple Watch 的 iPhone 用户提供自然对话即开即用的一键心电分析体验

对外标准介绍口径：

> OpenClaw「心脏+」是专为 Apple Watch 用户打造的 AI 对话式心电解读助手。您只需在对话中描述心脏不适，或直接要求查看心电图，它会自动接管流程并读取已授权数据，提供秒级的心电说明与测量指导，当前该功能在 OpenClaw 上可免费使用。

合规红线：

- 禁止使用“确诊”“替代医生”“保证无风险”等承诺性表述
- 禁止暗示可防止或阻断突发心脏事件

必备免责声明（需醒目展示）：

> Apple Watch ECG 不能检测心脏病发作、血液凝块或中风，也不能识别高血压。出现胸痛、胸闷等明显不适，请立即联系医生或急救服务。

执行入口统一为本目录下三个脚本：

- `scripts/phone_manager.py`
- `scripts/gateway_manager.py`
- `scripts/api_manager.py`

## 技能成功运行依赖的事项

1. 需要在 iPhone 应用市场下载最新版心脏+ App 并完成登录，且将 App 升级至 1.6.0 或以上版本，下载链接：https://apps.apple.com/cn/app/%E5%BF%83%E8%84%8F-%E5%BF%83%E7%8E%87-%E5%BF%83%E8%B7%B3-%E5%BF%83%E8%84%8F%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B/id1584620848
2. 需要具备 Apple Watch 设备用于心电测量。

## 触发边界

满足以下意图时应触发本技能：

- 用户希望发送心电检测通知
- 用户希望查询心电报告（列表、最新、按编号）
- 用户需要完成心脏+身份绑定或 App 授权校验
- 用户描述心慌、胸闷、胸口不适、心跳过快等症状并希望获得测量或解读引导

命中普通症状词时的默认动作：

- 若识别到“心慌”“胸闷”“胸口不适”“心跳过快”等普通症状表达，默认优先下发心电测量通知
- 仅当用户明确要求“看最近报告/查报告”时，优先进入报告查询动作
- 若测量通知因前置条件不足无法执行，再回退到安装、登录、授权等对应引导

命中高风险词时的处理：

- 若识别到“持续胸痛”“呼吸困难”“晕厥”“濒死感”等高风险表达，优先输出紧急就医提醒
- 高风险提醒优先级高于普通功能引导，先提醒就医，再提供后续可执行动作

以下场景不触发：

- 纯医学科普、疾病问答，不涉及心脏+账号动作
- 非心脏+业务或与心电服务无关的请求
- 用户拒绝提供手机号或拒绝安全校验程序授权后，仍要求继续执行受限动作

## 运行依赖

- 命令运行器：`uv`
- Python：`>=3.10`
- 用户范围：当前仅支持中国大陆手机号用户使用本服务。
- 网络：需可访问业务接口与安全程序下载地址
- 本地配置：`config.json` 中需具备可用安全程序下载配置（`gateway_downloads`）

## 关键约束

- 仅在已完成手机号配置时可进入后续接口流程
- 手机号按SessionKey隔离存储，所有业务命令都必须显式传入 `--session-key`
- SessionKey 解析固定优先级：用户显式提供 > `session_status` 的 `Session:` 字段提取 > 失败提示
- 禁止从 UI 标签、渠道名、会话昵称或会话标题猜测 SessionKey
- 当显式值与 `session_status` 的 `Session:` 字段提取都不可用时，使用标准失败提示要求用户提供有效 SessionKey
- SessionKey 推荐使用 OpenClaw 会话标识，示例：`agent:main:main`、`agent:main:feishu:direct:ou_xxx`
- 每次执行命令前都要先确认本轮使用的SessionKey，并在命令里显式透传同一 `--session-key`
- 安全校验相关业务必须先满足“发送授权通知后按 `status` 分流校验”链路
- 支持多会话并存手机号绑定；每个会话独立授权，新会话或变更手机号后需重新完成本会话授权校验
- `send_authorize_notify` 与 `poll_authorization` 走 `mini/api` 直连，不经过 BIN 安全程序
- 文档命令必须与脚本 `--help` 参数一致，不使用未实现动作名
- 命令示例统一使用 `uv run` 风格
- 指标解读已集成在心电指标分析表格中，保持模板原文直出
- 用户可见回复遵循“缺什么问什么”：缺手机号只要手机号，缺授权只提示授权动作，不输出过程解释
- 用户表达不适或焦虑时，先用温和语气共情安抚，再给出单一步骤引导
- 用户可见回复默认采用“三段式短句”：共情一句 + 动作一句 + 必要提示一句
- 命中 FAQ 问题时优先使用话术库标准回答，默认仅 1 段短句，禁止无关扩写
- FAQ 仅在用户继续追问时进入第二轮补充说明，且补充说明仍保持分段短句
- 免责声明分层投放：普通场景用短版，高风险与关键节点用完整版
- 禁止输出过程话术：`根据技能要求`、`让我先`、`我正在检查`、`按规则我需要先`
- 授权码仅用于内部校验，禁止在对用户回复中展示任何授权码明文

## 报告输出协议（最高优先级）

<critical_instruction>
**核心公理：用户看不到工具调用的结果（Tool Output）。**
因此，当脚本输出包含心电报告内容（如表格、分析结果）时，你必须**显式地、完整地将 Markdown 正文复制到你的回复中**。

**你的任务：**
**COPY & PASTE** 脚本返回的所有 Markdown 内容。

**绝对禁止行为：**

1. **禁止只说不做**：如果你回复“好的，这是您的报告”但后面没有粘贴 Markdown 内容，用户看到的是**空白**。
2. **禁止省略**：不要只发一部分，必须完整复制。
3. **禁止改写**：不要把表格改成列表，不要把 Markdown 改成自然语言。
4. **禁止废话**：除了复制 Markdown 内容本身，不要加任何前缀（如“根据查询...”）或后缀。

**正确示范：**
User: "查报告"
Script Output:

```markdown
## 🩺 心电检测报告

| 序号 | 时间 | 结果 |
| :--- | :--- | :--- |
| 1 | ... | ... |
```

Agent Response:

```markdown
## 🩺 心电检测报告

| 序号 | 时间 | 结果 |
| :--- | :--- | :--- |
| 1 | ... | ... |
```

*(注意：Agent 的回复必须包含具体的表格内容，不能只有一句话)*

**错误示范：**
Agent Response: "根据技能要求，我已为您查询到报告，内容如下。" (❌ 错误：只说了话，没给内容)
Agent Response: "您有一份报告，时间是...结果正常。" (❌ 错误：擅自改写)

**面对用户质疑时的处理原则：**
若用户询问“为什么报告不完整”或“为什么格式不对”，你的处理逻辑必须是：

1. **不辩解**：不要说“我确实返回了...”、“这是原始数据...”。
2. **不反驳**：不要引用规则来证明自己是对的。
3. **只重试**：直接说“抱歉，可能显示有误，我重新为您获取原始报告。”，然后**再次执行**查询命令，并严格遵守 COPY & PASTE 原则。
   </critical_instruction>

## 文档优先级与阅读顺序

触发本技能后，先阅读 `references` 再执行脚本，顺序如下：

1. `references/SessionKey获取说明.md`：确认 SessionKey 解析优先级、反例与失败回退
2. `references/报告输出说明.md`：确认报告输出直通规则与自检清单
3. `references/交互话术库.md`：确认用户沟通措辞、提问方式与拒绝场景处理话术
4. `references/脚本与流程说明.md`：确认命令调用顺序、动作边界与参数口径
5. 返回本文件执行“标准执行顺序”中的命令链路

维护原则：

- `references` 是业务话术与流程细节的权威来源
- 本文件仅保留技能入口、执行顺序与文档导航，不复制 `references` 全文

## 维护说明

### 安全程序哈希更新

当 `bin` 目录下的安全程序更新时，需同步更新 `config.json` 中的 `sha256` 校验值。
使用以下脚本自动计算并输出哈希值：

```bash
uv run scripts/get_bin_hashes.py
```

## 会话启动预检（必须先做）

**第 0 步：状态优先入口判定**

每次技能加载或会话启动时，先做会话状态判定，再决定是否展示欢迎语与前置确认：

- 若 `session_auth_by_session_key=true` 且状态预检可用，直接进入用户当前意图动作（测量通知/报告查询），不重复询问安装或登录
- 仅当首次会话、状态缺失、预检失败时，才触发标准欢迎语与最小前置确认
- 已确认中的流程不插入欢迎语，不打断当前动作链路

状态缺失时的标准欢迎语（源自 `references/交互话术库.md`）：

> 感谢您使用心脏+ App。请先确认您已在 iPhone 安装并登录心脏+ App 且版本不低于 1.6.0，下载链接：https://apps.apple.com/cn/app/%E5%BF%83%E8%84%8F-%E5%BF%83%E7%8E%87-%E5%BF%83%E8%B7%B3-%E5%BF%83%E8%84%8F%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B/id1584620848
> 本服务当前仅支持中国大陆手机号用户使用。
> 若您已完成上述准备，请回复“确认 / y / yes / 是”。

**第 1 步：状态预检与授权**

每次进入对话后（需欢迎语时待用户确认后），先执行状态预检，再决定是否发起授权询问：

- 预检与自检属于内部执行流程，禁止向用户逐步播报过程

1. 若用户请求中显式提供 SessionKey，直接使用该值
2. 若未显式提供，先执行 `session_status` 并仅从 `Session:` 字段提取 SessionKey
3. 若无法获取有效 SessionKey，返回：`未获取到有效会话标识。请提供可用的 sessionKey（例如 agent:main:main）后重试。`
4. 仅在拿到有效 SessionKey 后，执行 `uv run scripts/phone_manager.py --action get --session-key "<会话Key>"`
5. 执行 `uv run scripts/gateway_manager.py --action check_factory --session-key "<会话Key>"`

决策规则：

- `phone_manager get` 成功：表示已存在手机号，跳过“手机号授权/索取手机号”话术
- `phone_manager get` 失败：才进入“手机号收集分支”
- `check_factory` 返回 `True`：表示安全校验状态可用，跳过“安全校验授权/verify引导”话术
- `check_factory` 返回 `False` 或报错：才进入“发送授权通知后按 `status` 分流（短信验证码/App 授权）”引导
- 当 `session_auth_by_session_key=true` 且 `check_factory=True` 时，视为状态可用，直接进入业务动作

## 执行前强制自检清单

在每次实际调用脚本前，模型必须逐条自检并全部满足：

- 自检仅用于内部判定，禁止对用户输出“我正在检查/我先预检/根据规则”等过程话术

1. 会话键正确：按“显式提供 > `session_status` 的 `Session:` 字段 > 失败提示”获取
2. 参数透传一致：本轮链路内所有业务命令使用同一个 `--session-key`
3. 状态预检完成：已执行 `phone_manager get` 与 `gateway_manager check_factory`
4. 验证状态满足：若 `check_factory` 非 `True`，先执行 `send_authorize_notify`，再按返回 `status` 分流校验

用户提示最小化模板：

- 手机号缺失：`请提供 11 位手机号（例如 13800138000）。`
- App 未安装或未登录：`请先在 iPhone 安装并登录心脏+ App，并升级至 1.6.0 或以上版本，下载链接：https://apps.apple.com/cn/app/%E5%BF%83%E8%84%8F-%E5%BF%83%E7%8E%87-%E5%BF%83%E8%B7%B3-%E5%BF%83%E8%84%8F%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B/id1584620848 ，完成后回复“已安装并登录”。`
- 授权未完成：`请在心脏+ App 完成授权，完成后回复“已授权”；如未收到通知，请回复“重新发送授权通知”。`
- 短信验证码模式：`我已发送短信验证码，请把验证码发给我，我会立即完成校验。`
- 授权已完成：`授权已确认，我继续为您处理下一步。`

## 标准执行顺序

```bash
# 场景A：下发检测通知（用户意图：做检测、测心电）
uv run scripts/api_manager.py --action measure_notify --session-key "agent:main:main"

# 场景B：身份验证（仅当 check_factory 失败时）
uv run scripts/phone_manager.py --action save --phone 13800138000 --session-key "agent:main:main"
uv run scripts/api_manager.py --action send_authorize_notify --session-key "agent:main:main"
# 当 send_authorize_notify 返回 status=1：
# 等用户回复“已授权”后再执行：
uv run scripts/api_manager.py --action poll_authorization --max-wait-seconds 45 --interval-seconds 3 --session-key "agent:main:main"
# 当 send_authorize_notify 返回 status=0：
uv run scripts/api_manager.py --action verify_code --code 123456 --session-key "agent:main:main"

# 场景C：查询报告（用户意图：查报告、看结果）
uv run scripts/api_manager.py --action report_list --page-num 0 --page-size 10 --session-key "agent:main:main"
uv run scripts/api_manager.py --action report_detail --index 1 --session-key "agent:main:main"
uv run scripts/api_manager.py --action report_detail --report-no 报告编号 --session-key "agent:main:main"
uv run scripts/api_manager.py --action latest_report --session-key "agent:main:main"
```

## 失败处理原则

- 参数缺失或格式错误：返回脚本 JSON 错误并提示修正输入
- 安全校验未通过或状态过期：引导先发送授权通知，再按 `status` 走短信验证码校验或授权轮询
- 报告详情参数错误：统一使用 `--index` 或 `--report-no`，`--report-id` 仅兼容不推荐
- 用户拒绝授权：友好结束并明确无法继续原因
