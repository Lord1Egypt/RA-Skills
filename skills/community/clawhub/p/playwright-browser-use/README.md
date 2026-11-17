# pw-browser

> 基于 Playwright 的浏览器自动化 CLI — daemon + client 架构，直接使用系统 Chrome/Edge，无需下载额外浏览器。

> 📘 简体中文文档（本文件）。English documentation: [`README.en.md`](./README.en.md)。端到端示例见 [`QUICKSTART.md`](./QUICKSTART.md)（含 [`QUICKSTART.en.md`](./QUICKSTART.en.md)）。

> ⚠️ **完整能力（含代码执行与凭证操控）**：本工具**不只是"点开网页"**——它内置 `eval`（页面上下文**任意 JavaScript** 执行）与 `run-code`（守护进程上下文执行 Playwright/Node 代码）两项**代码执行**能力，以及 `cookies` / `storage` **凭证读写原语**（可**无需代码执行**即提取/注入登录态与会话令牌）。全部经持久化本地守护进程（127.0.0.1:19223）控制，受 daemon token 认证保护；`PW_BROWSER_SAFE_MODE=1` 可**彻底禁用**代码执行与凭证读写（v1.3.2+）。请先阅读下方「🔐 权限模型与最低特权」与「⚠️ 安全边界与使用场景」了解完整攻击面与适用边界，再决定是否授权。

## 特性

- **系统浏览器复用**：通过 Playwright `channel: 'chrome'` 连接系统已安装的 Chrome 或 Edge，不下载 Chromium
- **跨平台**：支持 Windows、macOS、Linux
- **持久化会话**：daemon 保持浏览器状态跨命令存活，无需每次重启
- **可访问性快照**：`snap` 命令生成页面元素树，带 ref 引用，无需写 CSS 选择器
- **非 headless**：浏览器窗口始终可见，用户可实时监控所有操作
- **人机协作**：遇到登录/验证码时自动交接给用户操作

## 安装

```bash
git clone <repo-url> pw-browser
cd pw-browser
npm install
```

> 前提：系统已安装 [Node.js](https://nodejs.org/) 18+ 和 Chrome 或 Edge 浏览器。

## 快速开始

```bash
# 1. 启动 daemon（后台运行）
node pw-browser.js daemon &

# 2. 等待 daemon 就绪
sleep 4

# 3. 打开页面
node pw-browser.js open https://www.baidu.com

# 4. 获取页面快照（必须！每次交互前都要 snap）
node pw-browser.js snap

# 5. 交互 — 基于快照中的 e0, e1, e2... ref
node pw-browser.js fill e12 "天气预报"
node pw-browser.js click e13

# 6. 查看结果
sleep 2
node pw-browser.js snap

# 7. 关闭
node pw-browser.js close --all
```

## 命令一览

| 类别 | 命令 | 说明 |
|------|------|------|
| 生命周期 | `init` / `open <url>` / `close` / `close --all` / `recover` | 启动、导航、关闭、恢复 |
| 状态感知 | `snap` / `wait-for <target>` | 快照（**ref 跨多次 snap 保持稳定**，同元素同 ref） |
| 交互 | `click <ref>` / `fill <ref> "text"` / `type "text"` / `press <key>` / `hover <ref>` / `select <ref> <opt>` / `check <ref>` / `uncheck <ref>` / `upload <ref> <file...>` / `drag <ref源> <ref目标>` / `download <ref> [--path dir]` | 点击、填写、按键、上传、拖拽、下载等 |
| Cookie/存储 | `cookies list` / `export [--path f]` / `import <file>` / `clear` / `set <name> <value> [--domain d]` · `storage get [key]` / `set <k> <v>` / `clear` / `export [--path f]` / `import <file>` | 读写 cookie 与 localStorage（需先 `open` 真实 http/https 页面） |
| 导航 | `goto <url>` / `go-back` / `go-forward` / `reload` | 页面导航控制 |
| Tab | `tab list` / `tab select <idx>` / `tab close <idx>` | 多标签页管理 |
| 批量 | `act '[{"action":"click","ref":"e13"}, ...]'` | 一次性执行动作序列，中途检测 DOM 变化自动中断重规划 |
| 历史 | `history [--limit N] [--clear]` | 查看/清空操作历史 |
| 高级 | `screenshot [--annotate]` / `mousewheel <dx> <dy>` / `eval "<expr>" [ref]` ⚠️ / `run-code "<code>"` ⚠️ | 截图（`--annotate` 叠加与 ref 对应编号框）、滚动、代码执行。`eval` 不带 `ref` 时在页面全局求值（`scope: "page"`）；带 `ref` 时标识符 **`el`** 绑定到该 DOM 节点（`scope: "element"`），如 `eval "el.textContent" e3`。返回值须可 JSON 序列化 |
| 延时 | `sleep <seconds>` | 等待 |
| 对话框 | `dialog-accept [text]` / `dialog-dismiss` | 处理原生 alert/confirm/prompt 对话框 |
| 守护进程 | `shutdown` | 关闭持久化 daemon，释放浏览器进程 |

> ⚠️ `eval` 在**浏览器上下文**执行 JS（无 Node 权限）；`run-code` 在 daemon 的**受限沙箱（`vm`）**中执行 Playwright 代码（无直接 Node `fs`/`process`/`child_process` 权限，但可经浏览器下载/上传读写本地文件、发起任意网络请求）。二者均拥有完整浏览器控制权。仅在用户明确指定的任务中使用。

## 架构

```
┌──────────────┐     HTTP (localhost:19223)     ┌──────────────┐
│  pw-browser  │ ──────────────────────────────→│   Daemon     │
│  (CLI 客户端) │                                │  (浏览器进程)  │
└──────────────┘                                └──────┬───────┘
                                                       │
                                                       ├─ Playwright
                                                       ├─ Chrome / Edge
                                                       └─ 页面状态持久化
```

daemon 启动后持续运行，浏览器和页面状态跨命令保持。CLI 每次通过 HTTP 调用 daemon。

## 工作流核心规则

1. **先观察再操作**：每次交互前必须 `snap`，基于快照 ref 操作
2. **登录交接**：遇到登录/验证码页面时，告知用户手动操作，用户确认后继续
3. **翻页前先识别类型**：页码分页 / 无限滚动 / 加载更多，对应不同翻页方式
4. **daemon 故障恢复**：连接错误时杀端口 19223 进程 → 删 daemon.json → 重启

详细规则和示例见 `SKILL.md`。

## 增强能力（借鉴 browser-use）

本工具的设计定位是「**安全可控的浏览器 CLI 基座 + 持久 daemon，规划交给外部 AI**」，而非 browser-use 那种「大脑+手一体」的 Agent 框架。我们从 browser-use 借鉴了四项对 CLI 基座同样有价值的能力：

### A. 稳定的元素引用（stable ref）
- `snap` 不再每次重排 ref，而是按元素的**语义身份**（有文本/placeholder/aria-label 用 `tag|text|placeholder|aria`；否则回退到 DOM 分支路径哈希）建立 `stableKey → ref` 持久映射。
- **同一逻辑元素跨多次 snap 保持同一 ref**，外部 AI 不必每步重新 `snap`，可直接复用之前的 ref 继续交互（典型场景：填完表单再点提交，e13 还是那个提交按钮）。
- `findElement` 新增 **Strategy 0：xpath 精确定位优先**——用快照里记录的精确 xpath 钉住元素，彻底解决纯语义查找「同名元素误点」的歧义。

### B. 视觉辅助截图（`screenshot --annotate`）
- `screenshot --annotate` 会在页面上注入覆盖层，为**每个与 snap ref 对应的元素**叠加红色边框 + 编号 label（用 `document.evaluate(xpath)` 精确定位）。
- 截图后自动移除覆盖层。多模态 AI 可「看图读编号」直接定位 `e13` 在页面哪个位置，弥补纯文本快照缺少空间信息的短板。

### C. 动作序列 + 自纠错（`act`）
- `act '[{"action":"click","ref":"e13"}, ...]'` 一次性下发动作序列，复用 `executeSingle` 逐个执行。
- 每个非首动作执行前重新 `snap` 并比对 `branchPathHash` 集合：若检测到页面出现**新元素**（DOM 变化），立即 `interrupted=true` 并返回最新快照，交由外部 AI 重新规划——这对应 browser-use 的 `multi_act` 中途中断重规划。
- 失败的动作会附带 `diagnosis`（ref 是否仍在、相似 ref 建议），便于自愈。

### D. 结构化输入 + 操作历史（`history`）
- `act` 接受结构化 JSON 动作数组（而非零散子命令），降低外部 AI 拼 CLI 参数的出错率。
- `history` 记录每次操作的 `{ ts, cmd, params（已过滤 token）, ok, elapsedMs }`，上限 500 条，可 `--clear`。外部 AI 可回溯「刚才点了什么、哪步失败」，实现上下文压缩与复盘——对应 browser-use 用 Mem0 压缩历史上下文的思路（此处用轻量本地历史替代向量库）。

### E. Shadow DOM / iframe 穿透
- 快照递归进入 **open shadow root** 与 **同源 iframe**，这些元素同样出现在 ref 表中并可直接 `click`/`fill`/`upload`/`drag`。
- ref 信息带 `inShadow: true`（shadow 内）或 `frameChain`（iframe 链）标记；定位由 `css >>>` 穿透 + `frameLocator` 自动完成，外部 AI 无感知。
- 跨域 iframe 不可访问，自动跳过；`--annotate` 截图仅标注主文档元素（shadow/iframe 元素无法用 xpath 定位标注，但文本快照中仍可点）。

### F. 文件上传与拖拽
- `upload <ref> <file1> [file2 ...]`：对 `<input type="file">` 设置文件（支持多文件）。
- `drag <ref源> <ref目标>`：基于 Playwright `dragTo` 实现拖拽。
- `download <ref> [--path dir]`：对称于 `upload`——可选点击 `<ref>` 触发下载，保存到 `--path`（默认当前目录）；亦可作为 `act` 动作。
  > 🔒 v1.3.10+：网页给出的建议文件名会被强制取 `basename` 并限制在 `--path` 目录内（越界返回 `PathTraversal`），恶意页面无法借 `../../` 之类的文件名写到目录之外。`--path` 若指向具体文件则按原样使用。

### G. Cookie 与本地存储（一等命令）
- `cookies list|export|import|clear|set`：读写当前上下文 cookie，不再需要靠 `eval` 曲线救国。
- `storage get|set|clear|export|import`：基于 `localStorage` 的读写（依赖真实 http/https 页面源）。
- 典型用法：登录后 `cookies export` 备份会话，下次 `cookies import` 直接恢复，免去重复登录。
- 📁 **路径限制（操作者门禁）**：`export`/`import` 默认限制在 `~/.pw-browser/` 目录内（防凭证散落 `/tmp` 或加载外部攻击者构造文件；路径经 realpath 解析，软链无法逃逸）。自 v1.3.8 起**该限制不可由调用方自行解除**——越界需**同时**满足：① 操作者以 `PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1` 启动 daemon；② 调用方显式传 `--unsafe`。仅传 `--unsafe` 会返回 `UnsafeOverrideNotPermitted`。命令返回带 `confined` 与 `warning` 字段，daemon stderr 记录每次凭证路径访问。
- 🔒 **会话持久化风险（Rogue Agent / 中危）**：`export`/`import` 让登录态可落盘、跨运行恢复——便利，但失控/恶意 Agent 可用它做"特权访问持久化"。导出的会话文件等同密钥：用完即删；暂存留在 `~/.pw-browser/` 内即可——自 v1.3.9 起该目录 `0700`、凭证文件与 daemon token 均 `0600` 写入，无需手工 `chmod`（Windows 上依赖用户目录 ACL）。不想让凭证落盘的场景，用 `PW_BROWSER_CRED_PERSIST=off` 启动 daemon：**强制禁用** `export`/`import`（`CredentialPersistenceDisabled`），保留 `list`/`get`/`set`/`clear` 内存态操作——比安全模式粒度更细，适合需要完整自动化但禁止会话跨运行留存的长驻 agent。不用时 `cookies clear`/`storage clear` 并 `shutdown` 关 daemon（空闲默认 15min 自动退出）。对不完全可信的调用方，用 `PW_BROWSER_SAFE_MODE=1` 启动 daemon——自 v1.3.2 起它会**整体禁用**全部 cookies/storage 子命令（凭证原语与代码执行同级拦截），必要时再配合沙箱隔离。

## 省 Token 与 Daemon 生命周期

**没有「每步调 LLM」的 token 黑洞**：本 skill 只是确定性执行器 + 持久 daemon，大模型只在外部编排层、且仅在主动调用时产生 token。保持以下用法即持续省 token：

- 用文本 `snap`（ref 表，几十 token）规划，而非每步 `screenshot`（数百 KB base64）喂视觉模型；
- 复用跨 snap 稳定的 ref，不必每步重新 `snap`；
- 把一连串操作攒成一次 `act '<json>'`，daemon 内部自纠错，中间不回模型。

**daemon 是故意持久化的**（跨命令复用同一浏览器，避免每次重开 Chrome）。因此：

- 任务结束后浏览器窗口还在是正常的——daemon 进程仍持有它；
- 显式停止：`pw-browser shutdown`（已加固，`browser.close()` 卡住也会超时兜底退出，不会退不出/卡客户端）；
- **空闲自动退出**：默认 **15 分钟无命令** 即自动关浏览器并退出，环境变量 `PW_BROWSER_IDLE_MS` 可调整（设为 `0` 关闭）。走开后无需手动清理；
- **监听端口可配 + 冲突避让**：默认 `127.0.0.1:19223`，可用 `PW_BROWSER_PORT` 覆盖。启动时若目标端口已有 daemon 存活则直接退出（避免双开）；若被其它进程占用则自动递增端口，并把实际端口写回 `~/.pw-browser/daemon.json`，客户端自动读取。
- 优先用 `shutdown` 或等空闲退出，避免直接强杀进程导致浏览器子进程残留。

## 安全说明

- daemon 监听 `127.0.0.1:19223`，仅本机可访问
- **命令认证**：除 `/health` 存活探针外，所有 daemon 命令都要求随机 `token`。token 在 daemon 启动时生成，写入 `~/.pw-browser/daemon.json`（默认仅当前用户可读），CLI 自动携带。未读取该文件的本地进程无法调用——这关闭了"无认证 HTTP 端点 = RCE 界面"的缺口
- **安全模式**：`PW_BROWSER_SAFE_MODE=1 node pw-browser.js daemon` 可彻底禁用 `run-code` / `eval` **以及全部 `cookies` / `storage` 凭证原语**（v1.3.2+），仅保留 snap/click/fill 等白名单命令——适合接入来源不完全可信的 agent
- `eval` 运行在浏览器上下文；`run-code` 运行在 `vm` 受限沙箱（无直接 Node 系统 API，但可经浏览器下载/上传读写本地文件），仅限本地信任环境使用
- 浏览器以非 headless 模式运行，用户可实时监控
- 不推荐作为公开 API 服务暴露，如需请加认证和操作白名单
- **权限模型说明**：frontmatter 的 `capabilities` / `allowed-tools` 是**自由文本元数据**，描述本技能的攻击面，**不是权限授予或沙箱边界**——拥有某项能力意味着技能*可以*做它，而非*只能*做它。本技能**没有**独立于 daemon token / 安全模式 / 路径限制之外的形式化权限系统；任何"最小权限"诉求须通过**部署模式选择（安全模式 + 沙箱）+ 操作范围约定**在编排层落实。详见 SKILL.md「🔐 权限模型与最低特权」。

### 依赖安全说明（CVE-2025-59288）

本项目直接依赖 `playwright-core@1.61.1`（Playwright 核心库，无浏览器下载逻辑，≥ 1.55.1）。CVE-2025-59288 影响的是完整 `playwright` 包**下载并安装浏览器**的安装脚本（`curl -k` 未校验证书）；本工具仅依赖 `playwright-core`，**根本不包含浏览器下载代码**，且运行时通过 `channel: 'chrome'` 复用系统已安装的 Chrome/Edge，因此该漏洞在本工具的使用路径上完全不可触发。

## 作为 AI Skill 使用

本工具可作为 AI 助手的 skill 使用。将整个目录放入 skill 安装路径，AI 助手通过 `SKILL.md` 中的规则指导自动化操作。

## License

[MIT](LICENSE)
