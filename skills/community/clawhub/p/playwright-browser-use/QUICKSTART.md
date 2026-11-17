# pw-browser 快速上手 Cookbook

> 面向 AI Agent / 脚本的端到端示例集。每个示例都可直接照抄执行。
> 约定：下文用 `pw-browser` 表示完整命令
> `NODE_PATH="<SKILL_DIR>/node_modules" node "<SKILL_DIR>/pw-browser.js"`。
> 所有示例默认 daemon 已在后台启动（`pw-browser daemon &`）。

---

## 示例 1：填写表单并提交（最常用）

目标：打开一个页面，定位输入框与按钮，填入文本并提交。

```bash
# 打开页面
pw-browser open https://example.com/login

# 必须先 snap，拿到 ref 表
pw-browser snap
# → e1 input placeholder="用户名"
# → e2 input placeholder="密码"
# → e5 button "登录"

# 填写并点击（基于 snap 给的 ref）
pw-browser fill e1 "alice"
pw-browser fill e2 "s3cret"
pw-browser click e5

# 验证结果
pw-browser wait-for "text=欢迎" --timeout 8000
pw-browser snap
```

要点：`snap` 之后才能 `click`/`fill`，且 ref 跨多次 snap 保持稳定（本次的 e1 下次仍是 e1）。

---

## 示例 2：文件上传 + 下载闭环

目标：上传一个本地文件，再触发一次下载，确认文件落盘。

```bash
pw-browser open https://example.com/upload

pw-browser snap
# → e3 input type=file "选择文件"
# → e4 button "开始上传"

# 上传（支持多文件，空格或逗号分隔）
pw-browser upload e3 /tmp/report.pdf /tmp/appendix.xlsx
pw-browser click e4

# 等待上传完成
pw-browser wait-for "text=上传成功" --timeout 10000

# 触发下载：点击某个会下载的链接/按钮，保存到指定目录
pw-browser snap
# → e9 a "导出 CSV"
pw-browser download e9 --path /tmp/downloads --timeout 30000
# → { "ok": true, "savedPath": "/tmp/downloads/export.csv", "suggestedFilename": "export.csv" }
```

说明：`download` 对称于 `upload`；不传 `--path` 时存到当前工作目录。也可作为 `act` 动作：
`{"action":"download","ref":"e9","path":"/tmp/downloads"}`。

> 🔒 v1.3.10+：`suggestedFilename` 由网页决定，属不可信输入。当 `--path` 是目录时，该名字会被取 `basename` 并限制在目录内，越界返回 `PathTraversal`。

---

## 示例 3：Shadow DOM / iframe 穿透

目标：页面里有些元素藏在 shadow root 或同源 iframe 内，普通选择器够不着——本工具会自动穿透。

```bash
pw-browser open https://example.com/widget

pw-browser snap
# → e2 button "内部按钮"  inShadow:true
# → e7 button "iframe 里的提交"  frameChain:[{sel:"iframe#frame1"}]

# 直接点！定位由 css >>> 穿透 + frameLocator 自动完成，外部无感知
pw-browser click e2
pw-browser click e7
```

要点：
- `inShadow: true` 表示元素在 shadow root 内；`frameChain` 非空表示在 iframe 内。
- `--annotate` 截图**只**标注主文档元素（shadow/iframe 元素无法用 xpath 定位标注，但文本快照里照常可点）。
- 跨域 iframe 不可访问，会自动跳过。

---

## 示例 4：Cookie / localStorage 提取与会话恢复

目标：登录后把会话备份下来，下次免登录直接恢复。

```bash
pw-browser open https://example.com/dashboard
# （先手动或通过示例 1 完成登录）

# 备份 cookie（默认写入 ~/.pw-browser/cookies.json，受目录限制保护）
pw-browser cookies export
# → { "ok": true, "exported": "~/.pw-browser/cookies.json", "count": 12,
#     "warning": "SECURITY: this file holds live session credentials ..." }

# 备份 localStorage（默认写入 ~/.pw-browser/localStorage.json）
pw-browser storage export

# —— 下次新会话 ——
pw-browser open https://example.com/dashboard
pw-browser cookies import          # 读取默认路径 ~/.pw-browser/cookies.json
pw-browser storage import          # 读取默认路径 ~/.pw-browser/localStorage.json

# 刷新后已是登录态
pw-browser reload
pw-browser snap
```

> ⚠️ `cookies` / `storage` 依赖真实 http/https 页面源；`file://` 与 `data:` 页面不支持 cookie，`localStorage` 行为也不可靠。

> 📁 **路径限制**：`cookies` / `storage` 的 `export`/`import` 默认被限制在 `~/.pw-browser/` 目录内——这是刻意的安全设计，防止凭证被静默散落到 `/tmp` 或加载来自任意路径的攻击者构造文件。自定义路径也必须位于 `~/.pw-browser/` 之下（路径经 realpath 解析，用符号链接也逃不出去）。
>
> 🛡️ **越界解除权归操作者，不归调用方（v1.3.8）**：早期版本只要调用方自己加 `--unsafe` 就能解除限制——等于把护栏的钥匙交给被约束的一方。现在必须**同时**满足两个条件才放行：① 操作者（人）以 `PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1` 启动 daemon（进程环境变量，发 HTTP 命令的一方改不了）；② 调用方显式传 `--unsafe`（表达意图）。只传 `--unsafe` 会被拒绝并返回 `UnsafeOverrideNotPermitted`。命令返回带 `confined`（是否仍在受限目录内）与 `warning` 字段，daemon stderr 会记录每一次凭证路径访问，便于事后审计。

> 🔒 **安全提醒（务必读完）**：导出的 `cookies.json` / `localStorage.json` 含有**完整登录会话凭证**——可能包括 `HttpOnly` cookie、Bearer/会话令牌、CSRF token 等敏感状态。文件一旦泄露，任何人拿到即可**冒用你的身份**登录对应站点。本工具的 daemon 会在多次命令间**持久化浏览器状态**，且工具另提供 `eval` / `run-code` 代码执行能力（可在页面上下文读取 cookie/storage），因此落盘的会话文件被误读、被错用或在本地环境外泄的风险更高。
> - **不要**把导出的文件提交进 git、上传到网盘或分享给他人。
> - 用完即删（`rm`）；若需暂存，放在默认的 `~/.pw-browser/` 内即可——自 v1.3.9 起该目录以 `0700` 创建、凭证文件以 `0600` 写入（连 daemon 认证 token 也是），**不必再手工 `chmod`**。Windows 上 POSIX 权限位不由系统强制，依赖用户目录 ACL。
> - 若整条流程都不该让凭证落盘：操作者用 `PW_BROWSER_CRED_PERSIST=off` 启动 daemon，`export`/`import` 会被**强制拒绝**（`CredentialPersistenceDisabled`），而 `cookies list` / `storage get|set|clear` 等内存态操作不受影响。这比 `PW_BROWSER_SAFE_MODE=1`（整体禁用凭证原语与代码执行）粒度更细。
> - 同一份会话文件**只应在你自己的本机、同一站点**恢复，切勿跨环境/跨账号复用。
> - **导入（恢复）同样高风险**：恢复会话即赋予对应站点的登录态/特权访问。切勿从不可信路径自动导入；在 Agent / 自动化流程里，**不要**默认把凭证材料在多次运行之间持久化，以免意外固化特权访问或导致会话被盗用——只在明确需要、且受控的前提下才恢复。
> - **面向不完全可信的 agent**：用 `PW_BROWSER_SAFE_MODE=1` 启动 daemon——自 v1.3.2 起安全模式会**整体禁用**全部 `cookies` / `storage` 子命令（与 `eval`/`run-code` 同级拦截），从根上关闭会话凭证读写面。

---

## 示例 5：`act` 多步 + 自纠错（推荐用于 Agent）

目标：把一连串操作一次性发给 daemon，过程中若页面 DOM 变化（例如点了按钮弹出新菜单），daemon 自动中断并返回最新快照，供你重新规划。

```bash
pw-browser open https://example.com/form

pw-browser snap
# → e1 input "标题"
# → e2 button "下一步"   (点了会动态出现 e3/e4 新字段)

# 一次性下发动作序列
pw-browser act '[
  {"action":"fill","ref":"e1","text":"月度报告"},
  {"action":"click","ref":"e2"}
]'
# 若点击 e2 后页面出现新元素 → 返回 { interrupted: true, snap: <最新快照> }
# 此时用返回的 snap 里的新 ref 继续：
#   pw-browser act '[{"action":"fill","ref":"e3","text":"..."},{"action":"click","ref":"e4"}]'

# 失败的动作会附带 diagnosis（ref 是否还在、相似 ref 建议），便于自愈
```

省 token 提示：`1 次 snap → 1 次 act → 完事`，中间不回模型。

---

## 故障排查速查

| 现象 | 处理 |
|------|------|
| 连接拒绝 | daemon 没起 → `pw-browser daemon &`；或旧进程残留 → 清 `~/.pw-browser/daemon.json` + 杀 19223 端口后重启 |
| `ElementNotFound` | ref 失效 → 重新 `snap` 拿新 ref |
| `NavigationTimeout` | 页面加载慢 → 先 `snap` 看实际状态，或调大 `--timeout` |
| 快照被截断（`⚠ snapshot truncated`） | 页面元素过多触发上限 → 调大 `PW_BROWSER_SNAP_LIMIT` 或先交互缩小页面范围 |

详细规则与完整命令表见 `SKILL.md` 与 `README.md`。
