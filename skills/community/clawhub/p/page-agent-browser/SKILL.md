---
name: page-agent-browser
description: 通过 page-agent CLI（CDP）驱动浏览器；CLI 当前仅从 GitHub Release 的 .tgz 安装（npm 官方包尚未发布）。
version: 1.0.0
allowed-tools: "Bash(page-agent:*), Bash(curl:*), Exec(tools:process:kill)"
metadata:
  openclaw:
    homepage: https://github.com/sdyuyouth/page-agent-cli/releases
    requires:
      anyBins:
        - page-agent
        - page-agent-cli
---

# Page Agent Browser Control

用 **page-agent** 连本机 Chrome/Edge 的远程调试端口，按 **`state` 给出的索引** 调用原语。**命令、选项、JSON 形状、退出码**一律以 `page-agent --help` 与 **`CLI_REFERENCE.md`** 为准；本文件只给 Agent 最短工作路径。

**阅读顺序**：`CLI_REFERENCE.md` → `ARCHITECTURE.md`（分层与本地 `platforms/`）→ 若做安全熟悉再读 `EXPLORATION_PROTOCOL.md`。自建站点包时读 `platforms/<site>/SKILL.md`（若有）。

---

## 安装 CLI（skill 内不含二进制）

Skill 只携带 Markdown 说明；**CLI 单独安装**。

**`@page-agent/cli` 尚未发布到 npm 公共 registry**；当前请**只从 GitHub Releases 附件**获取 `.tgz`，在**任意目录**安装（不要把 tgz 打进 skill 目录）：

```bash
# 示例：仓库与 Tag 以发布页为准（以下为常用 fork 线）
gh release download page-agent-cli-1.8.2 -R sdyuyouth/page-agent-cli -p "page-agent-cli-1.8.2.tgz"
npm install -g ./page-agent-cli-1.8.2.tgz
page-agent --version
```

无 `gh` 时：在发布页手动下载同名 `.tgz` 后执行 `npm install -g ./page-agent-cli-<version>.tgz`。

本 monorepo 内开发：`npm pack -w @page-agent/cli` 生成 tgz，再 `npm install -g ./<generated>.tgz`。

将来若 **`npm install -g @page-agent/cli`** 可用，以 README / Release 说明为准；届时可在此 skill 中补充 `metadata.openclaw.install`（`kind: node`）声明。

---

## 全局选项（常用）

| 选项 | 含义 |
|------|------|
| `--target <id>` | CDP `tabs list` 里的 Tab id |
| `--json` | 结果 JSON 在 stdout，日志在 stderr |
| `--cdp-url` | 覆盖 CDP（默认 `http://localhost:9222` / `PAGE_AGENT_CDP`） |
| `--no-mask` | 关闭指针/涟漪动画（`PAGE_AGENT_NO_MASK=1`） |

---

## 原语一览（与 CLI 一致）

| 命令 | 说明 |
|------|------|
| `tabs` | `list` / `open` / `close` |
| `state` | 取可交互元素 `[n]`；**依赖索引前**在探索/新流程上必须执行 |
| `click` / **`hover`** / `input` / `upload` / `select` / `scroll` | 索引均对应当前页**最近一次** `state`；`hover` 不点击，用于菜单/tooltip（见 `CLI_REFERENCE.md`） |
| `eval` / `goto` | JS 表达式 / 导航 |
| `run` | 内置 LLM 多步（需 `LLM_*`）；与外层 Agent 二选一 |
| `repl` / `teach` | REPL；阻塞式教学浮窗（**`teach` 全文见 `CLI_REFERENCE.md`**） |

**`upload`**：索引 `n` 为**锚点**（**最近一次 `state`**，不必是 `type=file` 行）。CLI 在**主文档可枚举**的 **`<input type=file>`** 中选与锚点 **DOM 树距离最近** 的一个（多 file 时同理；不穿透 Shadow、不跨 iframe）。常用：**`eval`/`click` 打开上传区** 后 **`upload n`**，使 `n` 尽量靠近目标 file。大改 DOM 后再 `state`。详见 **`CLI_REFERENCE.md`「upload」**。

**`teach`**：须 `--task` 或 `PAGE_AGENT_TEACH_TASK`；就绪后超时退出码 **124**；成功 JSON **无** `data` 包装；多 Tab、checkpoint、`steps` 里含 `hover`/`state_refresh` 等——细则见 **`CLI_REFERENCE.md`「teach」**与下节「**经验沉淀**」。站内 **pushState** 类 SPA 可能只有 CDP **`navigatedWithinDocument`**；CLI 会据此（debounce + URL 变化）再 reinject，避免 Facebook 等场景下浮窗被 DOM 重写后无法恢复。

---

## `teach` → 经验沉淀（Agent 必读）

CLI **不会**在「结束录制」时向 **stdout** 输出整段会话 JSON；该步只写**检查点文件**（`--checkpoint-file` / `PAGE_AGENT_TEACH_CHECKPOINT_FILE`，默认工作目录下 `.page-agent-teach-checkpoint.json`），stderr 可出现 **`[teach] checkpoint written`** 或 **`checkpoint write failed`**。

| 用户操作 | CLI 行为 | Agent / 自动化应做什么 |
|----------|----------|------------------------|
| 浮窗 **「结束录制」** | 原子写入**检查点 JSON**（草稿）；**stdout 无**最终 `success` teach 体 | 仅当需要**断点续录 / 崩溃恢复**时读该路径；**不要**把检查点当已提交的正式经验 |
| 浮窗 **「确认写入 Agent 经验」** | **exit 0**，**`--json` 时整段 teach 成功 JSON 在 stdout**（与 `state` 等命令不同，**无** `data` 包装） | **必须**在 teach 进程**正常退出后**读取 **stdout** 整文件作为正式结果，再更新自建 **`platforms/<site>/`** 下的 **`elements.md` / `recipes/*.md`** 等（字段见 **`EXPERIENCE_SCHEMA.md`**） |

**推荐落盘（示例）**：

```bash
# 仅示例：site/task 请换成当次 teach 的 --site / --task；目录须已存在或由脚本 mkdir -p
page-agent --json --target "$TID" teach --site example.com --task post-image --reason "demo" \
  > "${PAGE_AGENT_LESSON_DIR:-./platforms/example.com/lessons}/post-image-$(date +%Y%m%d-%H%M%S).json" 2>./teach.stderr.log
```

- **`2>`**：把 **`[teach]`** 与 checkpoint 相关日志打到单独文件，**避免**混进 JSON。  
- **宿主 Exec 超时**：`teach` 在用户确认前会长时间阻塞；外层若 **SIGKILL** 超时，Agent **拿不到 stdout**——应放宽 teach 专用超时，或等用户确认后再杀。  
- 仓库内 **无** `PAGE_AGENT_TEACH_OUTPUT` 环境变量；正式结果**只靠进程结束时的 stdout**（或你方包装器在 exit 0 后拷贝/上传该缓冲）。

---

## CDP 与 Tab

```bash
curl -s http://localhost:9222/json/version   # 通则继续
page-agent --json tabs list
# 示例：按 URL 取 id（主机名换成目标站）
TID=$(page-agent --json tabs list | jq -r '.data[] | select(.url | contains("example.com")) | .id' | head -1)
```

浏览器需带 **`--remote-debugging-port`**（下文以 **9222** 为例）。**默认复用用户已有配置**：**不要**加 **`--user-data-dir`**，即与日常登录、扩展、Cookie 同一用户数据目录（先退出已在跑的同品牌浏览器，再带远程调试参数启动，以免「用户目录已被占用」）。仅在与主窗口**必须并行**等少数场景，才另起独立 **`--user-data-dir=...`**。

**按习惯选 Edge 或 Chrome**（Edge 在 Windows 上常与系统账号一致；Chrome 适合已有 Chrome 习惯的用户）。**Firefox 不支持**本 CLI 所用的 CDP 工作流。

**调试端口已被占用时**：先查占用者（如 Windows `Get-NetTCPConnection -LocalPort 9222` / `netstat`，Linux/macOS `ss` / `netstat`）。若是**已有浏览器调试实例**，应**结束对应浏览器进程**后，用目标参数重新启动；若**不是浏览器**（或其它服务误占），则为本机浏览器**另选端口**（如 9223）启动，并把 **`PAGE_AGENT_CDP`** / **`--cdp-url`** 设为同一地址（例如 `http://localhost:9223`），`curl` 与 `page-agent` 均用该端口。

### Windows（PowerShell / cmd）

**Edge（示例，路径以本机安装为准）**

```powershell
& "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe" `
  --remote-debugging-port=9222 --no-first-run --no-default-browser-check
```

**Chrome（示例）**

```powershell
& "$env:ProgramFiles\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 --no-first-run --no-default-browser-check
```

### macOS（示例）

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 &
# 或 Microsoft Edge
"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  --remote-debugging-port=9222 &
```

### Linux（示例）

```bash
google-chrome --remote-debugging-port=9222 &
# 或 chromium、microsoft-edge-stable 等发行包提供的可执行文件
```

### WSL 调用 Windows 浏览器

CLI 在 WSL 内调用 **`upload`** 时会把 **`/mnt/c/...`** 路径转成 Windows 路径供浏览器注入；浏览器本体仍在 **Windows** 侧启动；**`PAGE_AGENT_CDP` / `--cdp-url` 端口须与 Windows 侧实际监听端口一致**（若改用 9223 等，两处同步修改）。

---

## 工作流（摘要）

1. **先 `tabs list` → `--target`**，全程固定同一 Tab。  
2. **操作 → `state`**：探索/新站**每步依赖索引前**必须 `state`；有 teach/recipe 且写明可省略时可少跑，错位立即 `state`（规则见 `CLI_REFERENCE.md`「state 与何时刷新」）。  
3. **站点经验**：仅当你自建了 `platforms/<site>/` 时读其中 `recipes` / `elements` / `critical`；**仓库内 `platforms/` 仅占位 `.gitkeep**，不附带具体站数据。  
4. **关键点击**：`CRITICAL_ACTIONS.md` + 本地 `critical.md`；须 **`AskQuestion` 或用户文字确认**（宿主无则停顿要确认）。  
5. **复盘**：读本地 `health.md`、失败记录（若有）。

---

## 相关文件

| 文件 | 用途 |
|------|------|
| `CLI_REFERENCE.md` | **权威**：子命令、`teach`/`upload`/`hover`、环境变量、退出码 |
| `ARCHITECTURE.md` | 分层、复用、探索与权限 |
| `EXPERIENCE_SCHEMA.md` | 经验 Markdown 字段约定 |
| `CRITICAL_ACTIONS.md` | 全局 critical 关键词与策略 |
| `EXPLORATION_PROTOCOL.md` | active-safe 探索边界 |
