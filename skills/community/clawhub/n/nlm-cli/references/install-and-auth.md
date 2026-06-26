# 安装并认证 `notebooklm-mcp-cli`

当 `nlm` 尚未安装、需要在新机器上初始化 CLI、或遇到认证 / profile 问题时，读取本参考文件。

## 安装

推荐方式：

```bash
uv tool install notebooklm-mcp-cli
```

备选方式：

```bash
pip install notebooklm-mcp-cli
```

安装完成后，先验证：

```bash
nlm --help
nlm doctor
```

如果 CLI 不是全局安装，而是安装在某个项目本地环境中，优先使用以下任一方式：
- 设置 `NLM_BIN` 环境变量，指向 `nlm` 可执行文件的完整路径
- 在 `{baseDir}/.venvs/nlm-mcp/bin/nlm` 放置可执行文件，让 wrapper 自动发现
- 确保正确环境的 `bin` 目录已经加入 PATH

## 登录

```bash
node {baseDir}/scripts/nlm.mjs login
node {baseDir}/scripts/nlm.mjs login --check
```

使用命名 profile：

```bash
node {baseDir}/scripts/nlm.mjs login --profile work
node {baseDir}/scripts/nlm.mjs login switch <profile>
node {baseDir}/scripts/nlm.mjs login profile list
node {baseDir}/scripts/nlm.mjs login profile delete <name>
node {baseDir}/scripts/nlm.mjs login profile rename <old> <new>
```

使用 OpenClaw / 浏览器 CDP 登录：

```bash
node {baseDir}/scripts/nlm.mjs login --provider openclaw --cdp-url http://127.0.0.1:18800
```

说明：
- 每个 profile 都是独立的浏览器会话，因此可以同时保留多个 Google 账号
- 当前默认 profile 决定 NotebookLM 操作实际使用哪个账号
- 如果之前可用、现在突然失败，通常先检查认证状态；必要时重新执行 `login` 或 `login --check`

## MCP / AI 工具配置

当需要把 NotebookLM MCP server 配置给其他 AI 工具时，使用 `setup`：

```bash
node {baseDir}/scripts/nlm.mjs setup add claude-code
node {baseDir}/scripts/nlm.mjs setup add gemini
node {baseDir}/scripts/nlm.mjs setup add cursor
node {baseDir}/scripts/nlm.mjs setup add json
node {baseDir}/scripts/nlm.mjs setup list
```

当 CLI 提供的是面向某个工具的 skill / reference 安装，而不是 MCP transport 配置时，使用 `skill install`：

```bash
node {baseDir}/scripts/nlm.mjs skill list
node {baseDir}/scripts/nlm.mjs skill install codex
node {baseDir}/scripts/nlm.mjs skill install claude-code
```

## 排障

先从这里开始：

```bash
node {baseDir}/scripts/nlm.mjs doctor
node {baseDir}/scripts/nlm.mjs doctor --verbose
```

检查配置：

```bash
node {baseDir}/scripts/nlm.mjs config show
node {baseDir}/scripts/nlm.mjs config get auth.default_profile
```

常见修复思路：
- `nlm: command not found` → 先安装 CLI，或把 `NLM_BIN` 指向正确的可执行文件
- Google 账号不对 → 先执行 `login profile list`，再执行 `login switch <profile>`
- 来源导入后迟迟不可用 → `source add` 时加 `--wait`，然后检查 `source list` 或 `studio status`
- Notebook / 操作权限异常 → 重新执行 `login`，确认当前激活的是目标账号
