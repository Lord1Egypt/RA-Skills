# Cron Setup

这份文档用于说明 OpenClaw 应如何为 `keplerjai-bulletin-publish` 这份 skill 创建或修复定时任务。

理想目标是：OpenClaw 在新机器上学习这份 skill 后，也能够正确完成定时任务配置，而不需要用户手工修改路径、文件夹名称或 agent 名称。

## 可迁移术语

- `<skill_root>`：这份 skill 所在的目录
- `<agent_workspace>`：应当归属该定时任务的目标 agent workspace
- `<output_dir>`：`<agent_workspace>/keplerjai-bulletin-publish`
- `<log_file>`：`<output_dir>/pipeline.log`

定时任务应根据这些关系来创建，而不是直接复制另一台电脑上的绝对路径。
在可能的情况下，OpenClaw 应自行从本地安装位置和本地目标 workspace 中推导出这些值。

## 归属规则

当这份 skill 被安装到一台存在 `admin-expert` agent 的机器上时，定时任务应归属于该 agent，并把运行产物写入该 agent 的 workspace。

如果本地环境使用的是不同的 agent 名称，OpenClaw 也应自动改用对应的本地目标 workspace。核心原则是：任务 owner 和输出目录必须始终保持一致。

手工修改路径或名称只能作为兜底方式，而不应成为正常配置流程。

## 工作流形态

应采用以下流程：

1. 读取 `stage1-task-prompt.txt`
2. 由 OpenClaw 直接完成 stage1 采集
3. 将采集结果写入 `<output_dir>/stage1-output.txt`
4. 运行：
   - `scripts/validate_stage1_json.py`
   - `scripts/publish_bulletins.py`
   - `scripts/format_bulletins.py`
5. 在整个运行过程中持续向 `<log_file>` 追加进度日志
6. 成功时仅返回最终摘要文本

这意味着定时任务本身应直接拥有采集步骤。
它不应通过再启动一个完整的 OpenClaw agent 运行来转交这一步。

## 通用约束

1. 工作流应保持单层且便于追踪。
2. 不要在定时任务内部再嵌套启动一个完整 agent 调用。
3. 不要把 `scripts/run_saved_pipeline.py` 当作定时任务的执行路径。
4. 不要在定时任务内部通过 `openclaw agent ...` 来执行 stage1 采集。
5. 优先使用直接脚本调用，而不是依赖特定终端行为的 shell 组合写法。
6. 路径应从 `<skill_root>` 和 `<output_dir>` 推导，而不是绑定某一个固定绝对路径。
7. 认证信息应视为环境配置，而不是 skill 内部拷贝的文件。

如果人工操作者为了调试而手动运行 `scripts/run_saved_pipeline.py`，这是允许的独立手动行为。
但这种手动调试路径绝不能被学习成标准的定时任务方案。

## 输出约定

所有运行产物都应写入 `<output_dir>`：

- `stage1-output.txt`
- `stage1-output.normalized.json`
- `publish-result.json`
- `final-message.txt`
- `pipeline.log`

skill 目录本身应继续作为提示词、脚本和文档的来源，而不是主要运行输出目录。

## 日志约定

定时任务应在 `<output_dir>` 中生成可读的 `pipeline.log`。

至少应记录：

1. workflow start
2. stage1 output written
3. validation completed
4. publish result written
5. final message written
6. workflow end
7. 当某一步失败时的主要错误原因

## 交付约定

如果工作流成功，最终回复应当严格等于 `final-message.txt` 的文本内容。

不要在最终回复外层再额外包裹：

- 执行表格
- 步骤摘要
- 文件路径列表
- 简讯 ID 列表
- 额外标题
- 额外说明文字

如果工作流失败，则返回一条简短的纯文本失败消息，并说明主要原因。

## 认证约定

`publish_bulletins.py` 应从环境变量中读取认证信息。

优先使用：

```text
KEPLERAI_API_KEY
```

兼容使用：

```text
KEPLERJAI_BEARER_TOKEN
```

## 创建后检查清单

在创建或修复定时任务后，应检查：

1. 目标 agent 与输出目录是否属于同一个 workspace
2. 提示词使用的 skill 根目录是否与本地已安装 skill 目录一致
3. 所有运行产物是否都落在 `<output_dir>`
4. 工作流是否持续向 `pipeline.log` 写入进度
5. 成功时面向用户的最终回复是否只有最终摘要文本
6. 定时任务是否没有调用 `scripts/run_saved_pipeline.py`
7. 定时任务是否没有启动 `openclaw agent`
