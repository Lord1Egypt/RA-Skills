---
name: jqopenclaw-node-invoker
description: 统一通过 Gateway 的 node.invoke 调用 JQOpenClawNode 能力（file.read、file.write、process.exec、process.manage、system.run、process.which、system.info、system.screenshot、system.notify、system.clipboard、system.input、node.selfUpdate）。当用户需要远程文件读写、文件移动/删除、目录创建/删除、进程管理（列表/搜索/终止）、远程进程执行、命令可执行性探测、系统信息采集、截图采集、系统弹窗、系统剪贴板读写、输入控制（鼠标/键盘）、节点自更新、节点命令可用性排查或修复 node.invoke 参数错误时使用。
---

# JQOpenClaw Node Invoker

## 快速流程

1. 确定目标 `nodeId`（用户给定优先）。
2. 调用 `node.describe` 检查节点在线状态，并按“节点识别规则”确认是否为 JQOpenClawNode。
3. 若命令未声明或被网关策略拦截，先输出阻断原因，再给修复建议。
4. 按 [references/command-spec.md](references/command-spec.md) 构造 `node.invoke` 请求。
5. 每次调用使用新的 `idempotencyKey`（UUID）。
6. 输出结果时先给结论，再给关键字段，不直接堆原始 JSON。

## 节点识别规则

- 先读 `node.describe` 返回的 `modelIdentifier`、`commands`、`displayName`、`nodeId`。
- 强匹配（可直接判定为 JQOpenClawNode）：
  - `modelIdentifier` 非空，且满足以下任一条件：
    - 等于 `JQOpenClawNode`。
    - 以 `JQOpenClawNode` 开头（如 `JQOpenClawNode(Qt/C++)`）。
- 弱匹配（仅在 `modelIdentifier` 为空时使用）：
  - `commands` 同时包含：`file.read`、`file.write`、`process.exec`、`process.manage`、`system.run`、`process.which`、`system.info`、`system.screenshot`、`system.notify`、`system.clipboard`、`system.input`、`node.selfUpdate`。
  - 且 `displayName` 或 `nodeId` 包含 `JQOpenClaw`。
- 拒绝匹配：
  - `modelIdentifier` 明确存在但不匹配 `JQOpenClawNode*`，即使命令集合相似也不按本技能处理。
- 不确定处理：
  - 若仅满足部分条件，先明确告知“节点类型不确定”，并要求用户指定目标 `nodeId` 或修正节点 `modelIdentifier` 后再执行。

## 命令映射

- 文件读取：`file.read`
- 文件写入/移动/删除/目录增删：`file.write`
- 进程执行（program/arguments/detached）：`process.exec`
- 进程管理（枚举/搜索/终止）：`process.manage`
- 远程进程执行（OpenClaw 标准参数）：`system.run`
- 可执行命令探测：`process.which`
- 系统基础信息：`system.info`
- 屏幕截图：`system.screenshot`
- 系统弹窗：`system.notify`
- 系统剪贴板：`system.clipboard`
- 输入控制：`system.input`
- 节点自更新：`node.selfUpdate`

## 调用规则

- 统一使用 `node.invoke`。
- `params` 必须是对象，字段类型严格匹配。
- 节点侧仅接受 `node.invoke.request.payload.paramsJSON`，且 `paramsJSON` 必须解析为对象。
- `paramsJSON` 缺失或 `null` 时按空对象处理；若存在但不是字符串、为空字符串、或解析后不是对象，按 `INVALID_PARAMS` 处理。
- `file.write` 必须显式传 `allowWrite=true` 才允许执行；未显式授权时应返回阻断提示。
- `timeoutMs` 需按任务复杂度设置：
  - `file.read` / `file.write`：5000-30000
  - `process.exec`：5000-120000（`detached=false` 时生效）
  - `process.manage`：5000-30000（`kill` 场景应确保 `timeoutMs >= waitMs`）
  - `system.run`：5000-120000
  - `process.which`：5000-15000
  - `system.info`：30000
  - `system.screenshot`：60000
  - `system.notify`：5000-15000（仅参数校验与弹窗投递，弹窗异步展示）
  - `system.clipboard`：5000-15000（读写系统剪贴板文本）
  - `system.input`：5000-15000（仅参数校验与入队，动作异步执行）
  - `node.selfUpdate`：30000-300000（下载+校验+脚本启动；成功后节点会退出重启）
- 调用 `node.selfUpdate` 时，`md5` 为必填（32 位十六进制）；缺失或格式错误按 `INVALID_PARAMS` 处理。
- `node.invoke.timeoutMs` 可省略；若传入，必须为非负整数（毫秒），否则按 `INVALID_PARAMS` 处理。其中 `0` 视为立即超时。
- `node.invoke.timeoutMs` 会参与请求预算裁剪；当前节点会将 `system.run.params.timeoutMs`、`process.exec.params.timeoutMs`（`detached=false`）与 `file.read(operation=rg)` 的内部超时裁剪到该预算内（取更小值）。
- 即便省略 `node.invoke.timeoutMs`，网关/调用端仍有等待超时（当前 OpenClaw 常见默认约 `30000ms`，CLI `openclaw nodes invoke` 默认 `15000ms`）。
- 实际可用执行时长取决于最先触发的超时层：调用端/网关等待超时、`node.invoke.timeoutMs`（若传入）、能力内部超时。
- `process.manage` 当前仅支持 Windows；非 Windows 环境调用会返回 `PROCESS_MANAGE_FAILED`。
- `process.manage`：
  - `operation=list/search/kill`，默认 `list`。
  - `search` 必须提供 `query`（或 `keyword`）与 `pid` 之一。
  - `kill` 必须提供 `pid`，可选 `waitMs` 范围 `[0, 30000]` 与 `force`（默认 `true`）；`force=false` 为非强杀退出请求（仅对具有顶层窗口的进程生效）；`waitMs` 当前不会被 `node.invoke.timeoutMs` 自动裁剪。
  - `kill` 默认拒绝终止关键进程（critical process）；仅当目标 PID 为当前节点进程时允许。
- `process.exec` 使用 `program + arguments`，支持 `detached`；用于兼容历史调用方。
- `system.run` 对齐 OpenClaw：仅使用 `command`（argv 数组）、`rawCommand`、`cwd`、`env`、`timeoutMs`、`needsScreenRecording`。
- `process.which` 支持 `program`（单个）或 `programs`（数组）探测；未命中返回 `found=false`，不作为命令失败。
- `file.read` 支持 `operation=read/lines/list/rg/stat/md5`。大文件建议使用 `read + offsetBytes + maxBytes` 分块读取（`maxBytes` 上限 `2097152`）；按行区间读取使用 `lines + startLine/endLine`；目录遍历可用 `list + recursive + glob`；元信息查询使用 `stat`；文件指纹可用 `md5`。
- `file.write` 默认禁用；需显式 `allowWrite=true`。开启后默认 `operation=write`；移动用 `operation=move`（配 `destinationPath`/`toPath`）；删除用 `operation=delete`（走回收站删除）；目录创建用 `operation=mkdir`；目录删除用 `operation=rmdir`。

## 网关阻断处理

- `command not allowlisted`：
  - 说明这是 Gateway 策略拦截。
  - 提示管理员在 Gateway 配置添加 `gateway.nodes.allowCommands`（如 `file.read`、`file.write`、`process.exec`、`process.manage`、`system.run`、`process.which`、`system.notify`、`system.clipboard`、`system.input`、`node.selfUpdate`）。
- `command not declared by node` / `node did not declare commands`：
  - 先看 `node.describe.commands`。
  - 要求节点端先声明命令再调用。

## 错误处理规范

- `INVALID_PARAMS`：参数缺失、类型不匹配或超出范围（含 `file.read` / `file.write` / `process.exec` / `process.manage` / `system.run` / `process.which` / `system.notify` / `system.clipboard` / `system.input` / `node.selfUpdate` 的参数校验失败，例如 `node.selfUpdate` 缺失必填 `md5`）。指出具体字段问题并给出可直接重试的参数。
- `TIMEOUT`：可能为网关等待超时，或显式传入 `timeoutMs=0` 触发立即超时。建议增大 `timeoutMs` 或缩小任务范围。
- `FILE_READ_FAILED` / `FILE_WRITE_FAILED`：用于非参数类失败。输出失败原因并给路径、权限、目录存在性、回收站可用性等排查建议。
- `PROCESS_MANAGE_FAILED`：用于非参数类失败（目标进程不存在、权限不足、非 Windows 平台、命中关键进程保护、终止或等待过程失败）。输出节点返回错误并给 PID、权限、平台和进程存活状态排查建议。
- `PROCESS_EXEC_FAILED`：用于 `process.exec` 的非参数类失败（程序不存在、权限不足、启动失败等无法产出结构化执行结果）。输出节点返回错误并给 `program`、`workingDirectory`、权限排查建议。
- `SYSTEM_RUN_FAILED`：用于 `system.run` 的非参数类失败（命令非法、程序不存在、权限不足、启动失败等无法产出结构化执行结果）。输出节点返回错误并给 `command`、`cwd`、权限、目标进程状态排查建议。
- `PROCESS_WHICH_FAILED`：用于非参数类失败（探测流程内部异常）。输出节点返回错误并建议重试或检查节点日志。
- `SYSTEM_INFO_FAILED`：系统信息采集失败。建议检查节点系统命令可用性与权限。
- `SCREENSHOT_CAPTURE_FAILED` / `SCREENSHOT_UPLOAD_FAILED`：截图采集或上传失败。建议检查显示环境、`file-server-uri`、`file-server-token` 与网络连通性。
- `SYSTEM_INPUT_FAILED`：`system.input` 投递或平台能力失败。建议检查平台是否为 Windows、线程池状态与节点日志。
- `SYSTEM_NOTIFY_FAILED`：`system.notify` 投递失败。建议检查应用实例状态与 UI 线程分发日志。
- `SYSTEM_CLIPBOARD_FAILED`：`system.clipboard` 执行失败。建议检查节点应用实例、图形环境与剪贴板访问能力。
- `NODE_SELF_UPDATE_FAILED`：`node.selfUpdate` 执行失败（下载失败、HTTP 状态异常、落盘失败、脚本启动失败等）。建议检查下载地址可达性、磁盘空间与杀毒拦截。
- `NODE_SELF_UPDATE_MD5_MISMATCH`：`node.selfUpdate` 下载成功但 MD5 校验不匹配。建议核对必填 `md5` 与发布包内容。
- `COMMAND_NOT_SUPPORTED`：改用已声明命令或升级节点版本。

## 输出规范

- 成功时：
  - 先一句话结论。
  - 再列关键字段（例如 `bytesWritten`、`exitCode`、`timedOut`、`url`）。
  - 对 `process.manage`，优先展示 `operation`、`pid`、`returnedCount/totalMatched`、`waitResult`、`resultClass` 等字段。
  - 对 `system.run` / `process.exec`，若 `timedOut=true` 或 `resultClass=timeout`，按“命令超时”给出失败结论与重试建议（即使 `node.invoke` 本身返回成功结构）。
- 失败时：
  - 先给 `error.code`、`error.message`。
  - 再给一条可执行的下一步操作。

## 安全边界

- `file.write`、`process.exec`、`process.manage`、`system.run` 与 `process.which` 默认按最小必要原则执行。
- 对可能破坏状态的操作（删除、覆盖、重置、停服务、终止进程）先征得用户明确确认。
- 不自行提升权限，不绕过网关策略。

## system.notify

- 命令名：`system.notify`
- 用途：弹出系统消息提示框。
- 参数：
  - `message`：必填字符串，非空，长度范围 `[1, 4000]`
  - `title`：可选字符串，默认 `JQOpenClaw`，长度上限 `120`
- 返回字段：`operation=notify`、`title`、`message`、`shown=true`、`async=true`、`ok=true`
- 错误处理：
  - 参数错误返回 `INVALID_PARAMS`
  - 投递失败返回 `SYSTEM_NOTIFY_FAILED`

## system.clipboard

- 命令名：`system.clipboard`
- 用途：读取当前系统剪贴板文本，或写入文本到系统剪贴板。
- 参数：
  - `operation`：可选字符串，`read|write`，默认 `read`
  - `text`：当 `operation=write` 时必填字符串
- 返回字段（`operation=read`）：`operation=read`、`text`、`length`、`hasText`、`ok=true`
- 返回字段（`operation=write`）：`operation=write`、`written=true`、`length`、`hasText`、`ok=true`
- 错误处理：
  - 参数错误返回 `INVALID_PARAMS`
  - 执行失败返回 `SYSTEM_CLIPBOARD_FAILED`

## system.input

- 命令名：`system.input`
- 用途：按顺序执行输入动作数组，支持鼠标、键盘和延迟混排。
- 执行语义：参数校验通过后异步入队；`node.invoke` 立即返回。
- 调度策略：latest-wins。若新请求到达，会取消旧请求尚未完成的剩余动作；已执行动作不会回滚。
- 使用建议：`keyboard.down` / `keyboard.up` 尽量在同一请求内闭合配对，或优先使用 `keyboard.tap`。
- 入参要求：
  - `params.actions` 必须为数组，长度 `[1, 1000]`
  - 每个动作对象必须包含 `type`
  - 支持 `mouse.move`、`mouse.click`、`mouse.scroll`、`mouse.drag`、`keyboard.down`、`keyboard.up`、`keyboard.tap`、`keyboard.text`、`delay`
- 关键校验：
  - `mouse.move.mode`：`absolute|relative`
  - `mouse.click.button`：`left|right`
  - `mouse.scroll`：`delta` 或 `deltaY` 二选一必填，可选 `deltaX`
  - `mouse.drag`：`mode=absolute|relative`，可选 `button=left|right`
  - `keyboard.text.text`：非空字符串
  - `delay.ms`：`[0, 60000]`
- 错误处理：
  - 参数错误返回 `INVALID_PARAMS`
  - 投递失败返回 `SYSTEM_INPUT_FAILED`

## 参考

- [references/command-spec.md](references/command-spec.md)
