# 仅有 CLI 时

没有 Paseo MCP 时使用本页；有 MCP 时以 [[paseo]] / [[paseo-handoff]] 为准。先看本机 `--help`，不要假设所有版本都支持相同 flags。

## 只读发现

在 zsh 环境先 `source ~/.zshrc`。Paseo Desktop 可能通过 AppImage 启动 CLI 并向 stdout 写启动日志；若会话提供有效的 `PASEO_CLI` 可执行路径，优先用它，避免把混入日志的输出直接交给 JSON parser。

```zsh
paseo_bin="${PASEO_CLI:-paseo}"
"$paseo_bin" --help
"$paseo_bin" host ls --json
"$paseo_bin" workspace ls --json
"$paseo_bin" project ls --json
"$paseo_bin" ls --global --json
"$paseo_bin" inspect <agent-id> --json
"$paseo_bin" logs <agent-id> --tail 12 --json
```

`ls` 默认受调用目录限制，Manager 找其他项目需加 `--global`，再按目标 workspace 筛选。普通列表不够时才用 `workspace ls --background` 或 `ls --all` 扩展线索。

注意版本差异：实测 0.13.0 的 `ls --json` / `inspect --json` 不提供 `workspaceId`，且两者字段大小写不同。多个 workspace 共用 cwd 时，不能凭这些输出声称 agent 属于其中某一个；需补充 MCP 归属证据，无法取得就说明限制并消歧。仅当确认没有同任务 agent 时才在已选 workspace 新建，避免重复任务。

CLI 的 `--host` 是连接端点，不是 MCP `serverId`。从已注册 host 的信息获得端点，不把 ID、label 或本机路径当远端端点。host 列表为空仅表示没有已注册的其他 host，不代表本机没有 workspace。

## 选择 profile

优先取得 MCP `list_profiles`。只有 CLI 且当前版本没有 profile 查询命令时，本机 daemon 可只读检查其实际 `PASEO_HOME/config.json` 的 `daemon.agentProfiles` 字段（默认 home 为 `~/.paseo`），**只提取该字段，不要输出整个配置**。这是持久配置的后备证据，不保证反映尚未持久化的状态；无法确认 daemon/home 对应关系时停止并说明限制。不要用本机配置冒充远端配置。

阅读所有 profile 的 notes 后，用 CLI 的 `--provider provider/model`、`--mode`、`--thinking` 表达选择。profile 含 CLI 无法表达的 `featureValues` 等设置时，改用 MCP；不要静默丢弃。只有确认没有合适 profile，才用 `provider ls`、`provider models <provider>` 做发现。

## 交接

先构造完整 briefing。多行内容可放在权限仅当前用户可读的临时文件，读回确认后传递；不要提交到 Manager 仓库，完成后删除。

```zsh
# 复用已核实的空闲 agent；不能据此抢占无关的活动任务。
"$paseo_bin" send <agent-id> --prompt-file <briefing-file> --behavior steer --no-wait --json

# 新建：参数来自 workspace 发现和 profile，不要照抄占位值。
"$paseo_bin" run --workspace <workspace-id> \
  --provider <provider/model> --mode <mode> \
  --title '[Handoff] <task>' --no-wait --json "$(cat <briefing-file>)"
```

两条命令都需 `--no-wait`，否则 CLI 可能等待完成。跨 host 时给发现、inspect、send/run 一致的 `--host <endpoint>`。保留调用会话的 Paseo 身份，不调用 `detach`；交接规则、回执与结果不明时的核实方式与主文一致。
