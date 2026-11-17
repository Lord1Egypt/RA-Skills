# Agent 编排与 MCP

本项目不只是提示词式 Skill。`human-writing-mcp` 可以把已验证的长篇审查包变成一个小型
协作界面，让多个 Agent 共用同一份计划、账本与回执，而不必把整部作品塞进每个会话。

## 服务做什么

服务只访问明确指定的项目根目录；不会自行调用模型，也不会上传草稿。它提供长篇协作、
单篇分析与编辑指令编译工具：

| 工具 | 作用 |
| --- | --- |
| `plan_long_form_writing` | 从大纲规划长文写作和逐块审稿依赖。 |
| `list_writing_tasks` / `claim_writing_task` | 查看就绪角色，领取提示和结果 schema。 |
| `submit_writing_result` | 保存结构化结果、证据与返修请求。 |
| `verify_writing_project` / `assemble_writing_project` | 全部块与相邻衔接通过后组装正文。 |
| `plan_long_form_audit` | 生成分块审查包与任务图。 |
| `list_audit_tasks` | 查看依赖、领取状态、回执有效性与可执行状态。 |
| `claim_audit_task` | 把一个完整且有边界的任务交给一名 Agent。 |
| `submit_audit_report` | 只有回执声明完整覆盖时才保存报告。 |
| `verify_audit_coverage` | 对所有必需报告做统稿前门禁。 |
| `get_reconciliation_task` | 门禁通过后才返回跨章统稿任务。 |
| `read_project_context` | 读取有长度上限的账本、大纲、资料说明或文风参考。 |
| `lint_text` | 对传入文本返回本地确定性发现项与证据位置。 |
| `get_style_statistics` | 返回句长变化、MATTR 与转折词密度。 |
| `verify_protected_content` | 比对原文与改写稿的受保护值和术语。 |
| `compile_humanize_prompt` / `compile_audit_prompt` | 为单篇文本编译有边界的 Prompt。 |
| `compile_ledger_extraction` | 编译带证据的待确认账本提取 Prompt。 |

所有越出根目录的路径都会被拒绝。回执必须带任务 ID、`Coverage: complete`、检查单元、发现
项以及 `Unchecked or blocked material: none`。漏审、阻塞或只审了一部分，均不能进入统稿。

## 从大纲开始写作

新稿使用[五角色长篇写作流程](long-form-writing.zh-CN.md)，区分连续剧情与显式独立并行块，
交接累计事实状态和待承接事项，并要求作者、逐块编辑与统稿具有相应的独立身份。
`read_project_context` 支持 `offset` / `next_offset` 分页读取大型索引；实际子 Agent 由宿主提供。

## 原生 Prompt 菜单

支持 MCP Prompts 的客户端可通过 `prompts/list` 发现菜单，并通过 `prompts/get` 获取 Prompt。
服务提供的是任务级快捷入口，而不是把全部内部模块暴露成冗长列表：`humanize-quick`、
`humanize-deep`、`dialogue-audit`、`continuity-audit`、`style-match`、`serious-rewrite` 与
`extract-ledger`。客户端是否将其显示为斜杠命令取决于客户端 UI；所有 Prompt 都要求传入正文，
不会自行调用外部模型。

## 本地 stdio 接入

先安装本项目，再在支持 MCP 的 Agent 中配置：

```text
command: python
args: ["-m", "humanwriting.mcp_server", "--root", "C:/writing-project"]
```

根目录中应包含稿件、人物/世界账本或报告计划，以及生成的审查目录。所有工具调用都使用项目
相对路径。同一服务可供 Codex、Claude Code、OpenCode、DeepSeek Harness 与 Hermes 共用。

## 远程 HTTP 接入

只接受远程 MCP 的平台，可在自有 HTTPS 反向代理后启动：

```powershell
human-writing-mcp --root C:\writing-project --http --host 127.0.0.1 --port 8765 --auth-token <long-random-token>
```

可选 HTTP 接口面向原生 MCP 客户端，要求 `application/json`，请求体上限为
1 MiB；拒绝携带浏览器 `Origin` 的请求，不提供 CORS 或 SSE 流。
通知返回 202，GET 返回 405。DSH 使用 stdio，无须启动 HTTP 接口。

仅通过 HTTPS 暴露 `POST /mcp`，并保留 `Authorization: Bearer` 请求头。非本机地址未提供
`--auth-token` 时会被拒绝。不要为了连接远程 Agent 而把小说或资料目录裸露在公网。

## 长篇可靠运行流程

1. 用 `agent_mode: "deep"` 调用 `plan_long_form_audit`。
2. 先由一名 Agent 领取并提交 `baseline`。
3. 对已就绪任务启动独立会话或子 Agent；每个任务只带正文块、只读前文、压缩账本和专项规则。
4. Agent 必须提交报告，不能只口头声称“已经审完”。
5. 调用 `verify_audit_coverage`，修复全部缺失或无效回执。
6. 只有验证通过后，才领取 `get_reconciliation_task` 做跨章统稿。

这套流程不绑定模型：可以是本地子 Agent、API 任务或多段独立会话。真正的权威是项目审查包，
不是某一个对话窗口逐渐衰减的记忆。

## 平台适配

- **Codex：** 在写作项目旁保留简短 `AGENTS.md`，Skill 负责发现工作流，MCP 负责共享状态。
- **Claude Code：** 在 `CLAUDE.md` 放同一份项目契约；用子 Agent 审就绪任务，并在最终交稿前执行
  覆盖验证。
- **OpenCode：** 可直接发现现有 `.agents/skills`；再接入同一条 MCP 命令共享队列。
- **DeepSeek Harness：** 使用仓库内 `plugins/deepseek-harness` 的 npm Bundle；它会挂载官方 DSH
  MCP 客户端并为工作区启动本服务。
- **Manus：** 现在可直接从 GitHub 导入 Skill。需要 MCP 时，在自有 HTTPS 与 Bearer 鉴权后部署
  HTTP 模式，且该服务根目录必须包含实际项目文件。
- **Hermes Agent：** 从 GitHub 或技能源安装 Skill，再接入 stdio 或受保护 HTTP MCP；子 Agent 可
  分别领取已就绪任务。

`integrations/project-context/AGENTS.md.example` 故意保持很短：它只指向账本与 MCP 流程，避免把
全部规则重复塞入每个对话上下文。
