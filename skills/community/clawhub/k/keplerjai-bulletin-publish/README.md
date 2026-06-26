# keplerjai-bulletin-publish

这份 skill 用于支持 KeplerJAI 简讯工作流，并明确区分各部分职责：

1. OpenClaw 负责执行 stage1 新闻采集。
2. Python 脚本负责校验、发布和整理最终结果。

## 这里应当放什么

skill 目录本身应当作为以下内容的来源：

- 提示词
- 脚本
- 配置说明
- 可复用的工作流规则

它不应被当作主要的运行产物输出目录。

这份 skill 的设计目标，是让 OpenClaw 在另一台机器上也能直接学习并使用，尽量减少人工部署步骤。正常情况下，应由 OpenClaw 自动推导本地 skill 路径和目标 workspace，而不是要求用户手工修改路径。

## 运行产物原则

运行产物应统一写入目标 agent 的 workspace 下、与 skill 同名的目录中：

`<agent_workspace>/keplerjai-bulletin-publish`

常见输出包括：

- `stage1-output.txt`
- `stage1-output.normalized.json`
- `publish-result.json`
- `final-message.txt`
- `pipeline.log`

## 主要文件

- `stage1-task-prompt.txt`
  stage1 采集规则与所需 JSON 结构
- `scripts\validate_stage1_json.py`
  校验并归一化 stage1 JSON
- `scripts\publish_bulletins.py`
  调用 KeplerJAI 简讯发布 API
- `scripts\format_bulletins.py`
  生成最终摘要文本
- `scripts\run_saved_pipeline.py`
  仅供本地一次性手动调试使用的辅助脚本
- `scripts\append_pipeline_log.py`
  向 `pipeline.log` 追加带时间戳的进度日志
- `CRON_SETUP.md`
  定时任务创建与修复说明

## 认证

脚本应从环境变量中读取认证信息。

优先使用：

```text
KEPLERAI_API_KEY
```

兼容使用：

```text
KEPLERJAI_BEARER_TOKEN
```

## 手动运行

在 skill 根目录下执行：

```powershell
pip install -r requirements.txt
python scripts\run_saved_pipeline.py --collect-stage1
```

这条手动路径适合本地调试和人工排查。

## 仅限手动脚本的边界

`scripts\run_saved_pipeline.py` 是给人工操作者使用的本地一次性调试辅助脚本。

它不应成为 OpenClaw 学习这份 skill 后默认采用的执行方案。

当 OpenClaw 学习这份 skill，并在之后以 agent 工作流或定时任务方式执行时：

1. 不要把 `run_saved_pipeline.py` 当成主执行路径。
2. 不要在已学习的工作流内部再启动嵌套的 `openclaw agent ...` 调用。
3. 不要创建“为了做 stage1 采集而再启动一个完整 agent 会话”的工作流。

学习后的工作流应保持单层结构：

1. OpenClaw 自己完成 stage1 采集。
2. OpenClaw 写出 `stage1-output.txt`。
3. OpenClaw 顺序运行 Python 脚本完成校验、发布和最终摘要整理。

## 定时任务指导

当 OpenClaw 学习这份 skill 并据此创建定时任务时，该任务应遵循以下原则：

1. 任务归属的 owner 与输出 workspace 必须保持一致。
2. 路径应从本地已安装的 skill 目录和目标 workspace 自动推导。
3. 工作流应保持简单、可追踪。
4. 进度应写入 `pipeline.log`。
5. 成功时，对用户的最终回复应只包含最终摘要文本。
6. 定时任务不应使用 `scripts\run_saved_pipeline.py`。
7. 定时任务不应为了执行 stage1 采集而再启动一个 `openclaw agent` 进程。

手工改路径、改文件夹名或改 agent 名称只能作为兜底方案，不应成为标准安装流程的一部分。

完整的定时任务约束见 [CRON_SETUP.md](C:\Users\Kvyain\.openclaw\workspace\keplerjai-bulletin-publish\CRON_SETUP.md)。
