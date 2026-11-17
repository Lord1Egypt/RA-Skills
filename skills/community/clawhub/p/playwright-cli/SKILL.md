---
name: playwright-cli
description: 基于微软 Playwright CLI 的浏览器自动化技能。用于 Web 测试、页面交互、自动化工作流。当用户提到 playwright、browser automation、Web 测试、E2E 测试时触发。
allowed-tools: Bash(playwright-cli:*) Bash(npx:*) Bash(npm:*)
---

# Playwright CLI - 浏览器自动化

## OpenClaw 集成

### 安装

```bash
# 全局安装
npm install -g @playwright/cli@latest

# 或使用 npx（无需安装）
npx --no-install playwright-cli --version
```

### 与 OpenClaw browser 工具的关系

| 特性 | OpenClaw browser | playwright-cli |
|------|------------------|----------------|
| 定位 | 内置工具，快速网页操作 | 外部 CLI，复杂测试/自动化 |
| 适用场景 | 简单截图、表单填写 | E2E 测试、多标签页、网络拦截 |
| 会话管理 | 单会话 | 多 session 支持 |
| 测试生成 | 无 | 支持规格驱动测试 |

**两者互补，不冲突**。简单任务用 browser 工具，复杂测试用 playwright-cli。

### 在 coding-framework 中的使用

当任务涉及 Web 测试/自动化时：
1. 检测关键词：`test` / `playwright` / `browser automation` / `E2E`
2. 加载 playwright-cli skill
3. 使用 CLI 命令执行操作

---

## Quick Start

```bash
# 打开浏览器
playwright-cli open

# 导航到页面
playwright-cli goto https://example.com

# 交互（使用 snapshot 中的 ref）
playwright-cli click e15
playwright-cli type "search query"
playwright-cli press Enter

# 截图
playwright-cli screenshot

# 关闭浏览器
playwright-cli close
```

---

## 核心命令

### Core（核心操作）

```bash
# 打开浏览器（可带 URL）
playwright-cli open
playwright-cli open https://example.com/

# 导航
playwright-cli goto https://playwright.dev

# 文本输入
playwright-cli type "search query"

# 点击
playwright-cli click e3
playwright-cli dblclick e7

# 表单填充（--submit 表示填充后按 Enter）
playwright-cli fill e5 "user@example.com" --submit

# 拖拽
playwright-cli drag e2 e8

# 文件/数据拖放
playwright-cli drop e4 --path=./image.png
playwright-cli drop e4 --data="text/plain=hello world"

# 悬停
playwright-cli hover e4

# 下拉选择
playwright-cli select e9 "option-value"

# 文件上传
playwright-cli upload ./document.pdf

# 复选框
playwright-cli check e12
playwright-cli uncheck e12

# 获取页面快照
playwright-cli snapshot

# 执行 JavaScript
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
playwright-cli eval "el => el.getAttribute('data-testid')" e5

# 对话框处理
playwright-cli dialog-accept
playwright-cli dialog-accept "confirmation text"
playwright-cli dialog-dismiss

# 调整窗口大小
playwright-cli resize 1920 1080

# 关闭
playwright-cli close
```

### Navigation（导航）

```bash
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
```

### Keyboard（键盘）

```bash
playwright-cli press Enter
playwright-cli press ArrowDown
playwright-cli keydown Shift
playwright-cli keyup Shift
```

### Mouse（鼠标）

```bash
playwright-cli mousemove 150 300
playwright-cli mousedown
playwright-cli mousedown right
playwright-cli mouseup
playwright-cli mouseup right
playwright-cli mousewheel 0 100
```

### Save（保存）

```bash
# 截图（整个页面或元素）
playwright-cli screenshot
playwright-cli screenshot e5
playwright-cli screenshot --filename=page.png

# PDF
playwright-cli pdf --filename=page.pdf
```

### Tabs（标签页）

```bash
playwright-cli tab-list
playwright-cli tab-new
playwright-cli tab-new https://example.com/page
playwright-cli tab-close
playwright-cli tab-close 2
playwright-cli tab-select 0
```

### Storage（存储）

```bash
# 状态保存/加载
playwright-cli state-save
playwright-cli state-save auth.json
playwright-cli state-load auth.json

# Cookies
playwright-cli cookie-list
playwright-cli cookie-list --domain=example.com
playwright-cli cookie-get session_id
playwright-cli cookie-set session_id abc123
playwright-cli cookie-set session_id abc123 --domain=example.com --httpOnly --secure
playwright-cli cookie-delete session_id
playwright-cli cookie-clear

# LocalStorage
playwright-cli localstorage-list
playwright-cli localstorage-get theme
playwright-cli localstorage-set theme dark
playwright-cli localstorage-delete theme
playwright-cli localstorage-clear

# SessionStorage
playwright-cli sessionstorage-list
playwright-cli sessionstorage-get step
playwright-cli sessionstorage-set step 3
playwright-cli sessionstorage-delete step
playwright-cli sessionstorage-clear
```

### Network（网络）

```bash
# 路由拦截
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'
playwright-cli route-list
playwright-cli unroute "**/*.jpg"
playwright-cli unroute
```

### DevTools（开发者工具）

```bash
# 控制台日志
playwright-cli console
playwright-cli console warning

# 网络请求
playwright-cli requests
playwright-cli request 5

# 运行自定义代码
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
playwright-cli run-code --filename=script.js

# 追踪
playwright-cli tracing-start
playwright-cli tracing-stop

# 视频录制
playwright-cli video-start video.webm
playwright-cli video-chapter "Chapter Title" --description="Details" --duration=2000
playwright-cli video-stop
playwright-cli video-show-actions --duration=600 --position=top-right
playwright-cli video-hide-actions

# 交互式标注（用户可在页面上画框、写注释）
playwright-cli show --annotate

# 生成 Playwright locator
playwright-cli generate-locator e5 --raw

# 高亮元素
playwright-cli highlight e5
playwright-cli highlight e5 --style="outline: 3px dashed red"
playwright-cli highlight e5 --hide
playwright-cli highlight --hide
```

---

## 元素定位方式

### 1. 使用 ref（推荐）

从 snapshot 获取元素 ref，然后交互：

```bash
# 获取快照（含 ref）
playwright-cli snapshot

# 使用 ref 交互
playwright-cli click e15
playwright-cli fill e5 "text"
```

### 2. CSS 选择器

```bash
playwright-cli click "#main > button.submit"
playwright-cli snapshot "#main"
```

### 3. Playwright Locator

```bash
# Role locator
playwright-cli click "getByRole('button', { name: 'Submit' })"

# Test ID
playwright-cli click "getByTestId('submit-button')"
```

---

## 会话管理

支持多个浏览器会话并行：

```bash
# 创建命名会话
playwright-cli -s=mysession open https://example.com --persistent
playwright-cli -s=mysession click e6
playwright-cli -s=mysession close

# 列出所有会话
playwright-cli list

# 关闭所有浏览器
playwright-cli close-all

# 强制终止所有浏览器进程
playwright-cli kill-all

# 删除会话数据
playwright-cli -s=mysession delete-data
```

---

## Raw 输出模式

`--raw` 选项去除页面状态、生成代码和快照，只返回结果值。适合管道操作：

```bash
# 性能计时
playwright-cli --raw eval "JSON.stringify(performance.timing)" | jq '.loadEventEnd - .navigationStart'

# 提取链接
playwright-cli --raw eval "JSON.stringify([...document.querySelectorAll('a')].map(a => a.href))" > links.json

# 快照对比
playwright-cli --raw snapshot > before.yml
playwright-cli click e5
playwright-cli --raw snapshot > after.yml
diff before.yml after.yml

# 获取 cookie/token
TOKEN=$(playwright-cli --raw cookie-get session_id)

# JSON 输出
playwright-cli list --json
```

---

## 浏览器选项

```bash
# 指定浏览器
playwright-cli open --browser=chrome
playwright-cli open --browser=firefox
playwright-cli open --browser=webkit
playwright-cli open --browser=msedge

# 持久化配置（默认内存）
playwright-cli open --persistent
playwright-cli open --profile=/path/to/profile

# 连接已运行的浏览器
playwright-cli attach --cdp=chrome
playwright-cli attach --cdp=msedge
playwright-cli attach --cdp=http://localhost:9222

# 通过 Playwright Extension 连接
playwright-cli attach --extension=chrome

# 使用配置文件启动
playwright-cli open --config=my-config.json

# 分离（不关闭外部浏览器）
playwright-cli -s=msedge detach
```

---

## Windows 特殊处理

Windows 下 URL 中的 `&` 需要转义：

```batch
# cmd.exe
playwright-cli goto "https://example.com/?a=1^&b=2"
```

```powershell
# PowerShell
playwright-cli --% goto "https://example.com/?a=1&b=2"
```

---

## Snapshots（快照）

每次命令后自动提供快照，也可手动获取：

```bash
# 默认保存到文件（时间戳命名）
playwright-cli snapshot

# 指定文件名
playwright-cli snapshot --filename=after-click.yaml

# 快照特定元素
playwright-cli snapshot "#main"
playwright-cli snapshot e34

# 限制深度
playwright-cli snapshot --depth=4

# 包含边界框
playwright-cli snapshot --boxes
```

---

## 参考文档

- [命令完整参考](references/commands.md) - 所有命令及参数
- [规格驱动测试](references/spec-testing.md) - Plan → Generate → Heal 方法论
- [使用示例](references/examples.md) - 常见场景代码示例

---

## 具体任务

| 任务 | 说明 |
|------|------|
| 运行/调试 Playwright 测试 | `npx playwright test --debug=cli` + `playwright-cli attach tw-XXXX` |
| 请求模拟 | `playwright-cli route` 拦截和模拟 API 响应 |
| 运行自定义代码 | `playwright-cli run-code` 执行任意 Playwright 代码 |
| 会话管理 | 多 session 并行，持久化配置 |
| 规格驱动测试 | Plan → Generate → Heal 三阶段工作流 |
| 存储状态 | Cookie/localStorage/sessionStorage 操作 |
| 测试生成 | 从 CLI 操作自动生成 Playwright TypeScript |
| 追踪 | `tracing-start` / `tracing-stop` 捕获调试轨迹 |
| 视频录制 | `video-start` / `video-stop` 录制操作视频 |
| 元素属性检查 | `eval` 获取任意 DOM 属性 |
