# page-agent CLI 参考

与 **`page-agent --help`** / **`page-agent <cmd> --help`** 对齐；执行前可再跑 help 核对版本。

---

## 全局选项

| 选项 | 说明 |
|------|------|
| `--cdp-url` | CDP URL（默认 `http://localhost:9222`，环境变量 `PAGE_AGENT_CDP`） |
| `--target` | Tab 的 CDP target id（`tabs list`）；缺省取第一个 page |
| `--json` | 成功体在 stdout；日志在 stderr |
| `--no-mask` | 关闭指针/涟漪（`PAGE_AGENT_NO_MASK=1`） |

---

## 命令一览

| 命令 | 作用 |
|------|------|
| `state` | 可交互元素 `[n]`，供 `click`/`hover`/`input`/`upload`/`select` |
| `click` / `hover` | 点击 / **指针悬停不点击**（菜单、tooltip；索引同 `click`） |
| `input` / `upload` / `select` | 文本替换 / **file input 多路径** / 原生 `<select>` |
| `scroll` | `--pages` \| `--pixels` \| `--up` \| `--index` |
| `eval` / `goto` | JS 表达式 / 导航 |
| `tabs` | `list` \| `open` \| `close` |
| `run` | 内置 LLM 多步（`LLM_*`） |
| `repl` / `teach` | REPL；阻塞式教学浮窗 |

---

## `hover`

索引 = 当前页**最近一次** `state`。导航或大改 DOM 后先 `state`。与 `click` 共用 `--no-mask` 规则。`teach` 里可选「悬停」，`action`=`hover`，页内需注入的 `PageController` 含 **`hoverElement`**（CLI CDP 默认有）。

---

## `upload`

**前提**：本 Tab 上至少跑过一次 **`state`**，页内才有当前 **`selectorMap`**；大导航 / 整页 DOM 重写后应再 **`state`** 再 `upload`，避免索引漂移。

**`[n]` 不必是 `state` 文本里的 `type=file` 行**：`n` 来自**最近一次 `state` 的编号**，作为**锚点**。CLI 在整页所有 **`<input type="file">`** 中选取与锚点 **DOM 树无向距离最短** 的一个（沿 **`parentElement`** 走到最近公共祖先再折返；等价于「树上半径最小」）。**距离相同**时取 **文档顺序更靠前** 的那个。与「DOM 里第几个 file」不是同一计数。

**推荐流程**：`state` → 用 **`eval` / `click` / `hover`** 让锚点落在目标上传控件附近（同一 composer / 弹层 subtree 更佳）→ **`upload n`**。页面上**多个** file 时，应保证所选 **`n`** 在树上离目标 file **比离其它 file 更近**；否则换锚点、`state` 或 **`teach`**。

路径建议绝对路径；多文件空格分隔。失败时核对文件存在、`n` 是否仍对应最新 `state`。

**限制**：候选 file 为当前主文档 **`document.querySelectorAll('input[type="file"]')`** 能枚举到的节点（与常见 `state` 一致）；**不穿透 open shadow、不跨 iframe**。

---

## `state` 与何时刷新

- 默认可交互步后、若下一步要**另一索引**：先 `state`。纯 `hover` 未改 DOM 可省一次；**新菜单出现**则必须 `state`。  
- **探索 / 新站**：每步依赖索引前必须 `state`。  
- **有 teach/recipe 且写明可省**：可少跑；异常则回到默认。

---

## `input` / `select` / `scroll`

- **input**：仅 `input`/`textarea`/`contenteditable`。  
- **select**：仅原生 `<select>`；自定义下拉用 `click`+`state`。  
- **scroll**：滚后通常 `state`（索引易变）。

---

## `teach`

浮窗按 **`state` 索引** 录步（含 `state_refresh`）；阻塞至确认/取消/超时。

```bash
page-agent --json --target "$TID" teach --task my-task --reason "demo"
page-agent --json teach --teach-ui-targets ID_A,ID_B --reason "multi-tab"
```

| 选项 | 说明 |
|------|------|
| `--task` / `PAGE_AGENT_TEACH_TASK` | 任务名（缺省 `untitled`） |
| `--site` | 站点 slug（默认主机名） |
| `--reason` | 浮窗说明 |
| `--timeout` / `--ready-timeout` | 就绪后超时（默认 600）/ 注入等待（默认 180）；超时无恢复 → **124** |
| `--checkpoint-file` / `PAGE_AGENT_TEACH_CHECKPOINT_FILE` | 原子检查点（默认 `./.page-agent-teach-checkpoint.json`） |
| `--teach-targets` / `--teach-ui-targets` / `--teach-all-page-tabs` | 多 Tab：参与集 / 注入浮窗子集 / 枚举 page 型 target |

**成功 `--json`**：仅在用户于浮窗 **「步骤」** 中点击 **「确认写入 Agent 经验」** 且进程 **exit 0** 时，**stdout** 才输出**整段** teach 成功 JSON：顶层 `success` + `steps` + `operationLog`（**无** `data`）；`steps[].action` ∈ `click`|`hover`|`input`|`select`|`upload`|`state_refresh`；多 Tab 步可有 `targetId`；多浮窗时可有 `teachUiTargetIds`。

**「结束录制」≠  stdout 结果**：该操作触发 CLI 写 **`--checkpoint-file`**（原子检查点草稿），stderr 可出现 **`[teach] checkpoint written`**；**不要把检查点文件误当成已提交的 teach stdout JSON**。断点续录、崩溃恢复时再读检查点。

**Agent 落盘**：对一次完整 `teach`，在命令末尾 **`> path/to/lesson.json`**，并 **`2> teach.log`**，保证 JSON 文件**只含 stdout**；进程退出后再解析 JSON 并合并进自建 **`platforms/<site>/`** 经验树（见 **`EXPERIENCE_SCHEMA.md`**）。宿主若对子进程 **SIGKILL** 超时，会导致**拿不到 stdout**——须为 `teach` 单独放宽或禁用该超时。

取消：`success:false`，退出 **1**。stderr 为 `[teach]` 日志。

多 Tab 细节与 Hub 行为以 **`page-agent teach --help`** 与仓库 `packages/cli/DEVELOPMENT.md` 为准。重度 SPA 站内路由可能只触发 CDP **`Page.navigatedWithinDocument`**（不发主框架 **`Page.frameNavigated`**）；CLI 对该事件做 debounce 与 **`location.href`** 变化检测后再 reinject，以便浮窗在 DOM 被站点重写后仍能 **`restore()`**。

---

## `tabs`

```bash
page-agent --json tabs list
page-agent --json tabs open https://example.com
page-agent --json tabs close <targetId>
```

后续命令固定同一 `--target`。

---

## `run` vs 原语

- **`run`**：已配 LLM、多步开放任务、单次长连接。  
- **原语**：外层 Agent 已拆好步、只需 CDP。默认优先原语 + 本地经验。

---

## 环境变量（节选）

`PAGE_AGENT_CDP`、`PAGE_AGENT_NO_MASK`、`PAGE_AGENT_TEACH_TASK`、`PAGE_AGENT_TEACH_CHECKPOINT_FILE`、`LLM_BASE_URL`、`LLM_API_KEY`、`LLM_MODEL_NAME`（详见 `page-agent run --help`）。

---

## 退出码

**0** 成功；**1** 失败（`--json` 常伴 `success:false`）；**124** 仅 **`teach`** 就绪后超时且无恢复数据。

子命令均**同步**：进程结束即该步完成；页面可能已变则再 `state`。
