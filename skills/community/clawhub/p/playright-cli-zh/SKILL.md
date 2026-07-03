---
name: playwright-cli
description: 自动化浏览器交互、测试网页以及使用 Playwright 测试。
allowed-tools: Bash(playwright-cli:*) Bash(npx:*) Bash(npm:*)
---

# 使用 playwright-cli 进行浏览器自动化

## 快速开始

```bash
# 有头模式打开新浏览器
playwright-cli --headed open
# 无头模式打开新浏览器
playwright-cli  open
# 导航到页面
playwright-cli goto https://playwright.dev
# 使用快照中的 ref 与页面交互
playwright-cli click e15
playwright-cli type "page.click"
playwright-cli press Enter
# 截图（较少使用，快照更常见）
playwright-cli screenshot
# 关闭浏览器
playwright-cli close
```

## 命令

### 核心命令

```bash
playwright-cli --headed open
playwright-cli open
# 打开并立即导航
playwright-cli --headed open https://example.com/
playwright-cli  open https://example.com/
playwright-cli goto https://playwright.dev
playwright-cli type "搜索查询"
playwright-cli click e3
playwright-cli dblclick e7
# --submit 在填写元素后按 Enter
playwright-cli fill e5 "user@example.com"  --submit
playwright-cli drag e2 e8
# 从页面外部拖放文件/数据到元素上
playwright-cli drop e4 --path=./image.png
playwright-cli drop e4 --data="text/plain=hello world"
playwright-cli hover e4
playwright-cli select e9 "option-value"
playwright-cli upload ./document.pdf
playwright-cli check e12
playwright-cli uncheck e12
playwright-cli snapshot
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
# 获取元素 id、class 或快照中不可见的属性
playwright-cli eval "el => el.id" e5
playwright-cli eval "el => el.getAttribute('data-testid')" e5
playwright-cli dialog-accept
playwright-cli dialog-accept "确认文本"
playwright-cli dialog-dismiss
playwright-cli resize 1920 1080
playwright-cli close
```

### 导航

```bash
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
```

### 键盘

```bash
playwright-cli press Enter
playwright-cli press ArrowDown
playwright-cli keydown Shift
playwright-cli keyup Shift
```

### 鼠标

```bash
playwright-cli mousemove 150 300
playwright-cli mousedown
playwright-cli mousedown right
playwright-cli mouseup
playwright-cli mouseup right
playwright-cli mousewheel 0 100
```

### 另存为

```bash
playwright-cli screenshot
playwright-cli screenshot e5
playwright-cli screenshot --filename=page.png
playwright-cli pdf --filename=page.pdf
```

### 标签页

```bash
playwright-cli tab-list
playwright-cli tab-new
playwright-cli tab-new https://example.com/page
playwright-cli tab-close
playwright-cli tab-close 2
playwright-cli tab-select 0
```

### 存储

```bash
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

### 网络

```bash
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'
playwright-cli route-list
playwright-cli unroute "**/*.jpg"
playwright-cli unroute
```

### 开发者工具

```bash
playwright-cli console
playwright-cli console warning
playwright-cli requests
playwright-cli request 5
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
playwright-cli run-code --filename=script.js
playwright-cli tracing-start
playwright-cli tracing-stop
playwright-cli video-start video.webm
playwright-cli video-chapter "章节标题" --description="详细信息" --duration=2000
playwright-cli video-stop

# 启动仪表板用于 UI 审查/设计反馈 — 用户在页面上标注，你收到带标注的截图、快照和备注
playwright-cli show --annotate

# 根据 ref 或选择器生成 Playwright 定位器
playwright-cli generate-locator e5 --raw

# 为元素显示持久高亮叠加层，可自定义样式
playwright-cli highlight e5
playwright-cli highlight e5 --style="outline: 3px dashed red"
# 隐藏单个元素高亮，或未指定目标时隐藏所有页面高亮
playwright-cli highlight e5 --hide
playwright-cli highlight --hide
```

## 原始输出

全局 `--raw` 选项会从输出中剥离页面状态、生成的代码和快照部分，仅返回结果值。用于将命令输出管道传递给其他工具。不产生输出的命令返回空。

```bash
playwright-cli --raw eval "JSON.stringify(performance.timing)" | jq '.loadEventEnd - .navigationStart'
playwright-cli --raw eval "JSON.stringify([...document.querySelectorAll('a')].map(a => a.href))" > links.json
playwright-cli --raw snapshot > before.yml
playwright-cli click e5
playwright-cli --raw snapshot > after.yml
diff before.yml after.yml
TOKEN=$(playwright-cli --raw cookie-get session_id)
playwright-cli --raw localstorage-get theme
```

使用 `--json` 可将每条回复包装为 JSON 结构化输出：
```bash
playwright-cli list --json
```

## Open 参数
```bash
# 创建会话时指定浏览器
playwright-cli open --browser=chrome
playwright-cli open --browser=firefox
playwright-cli open --browser=webkit
playwright-cli open --browser=msedge

# 使用持久化配置（默认为内存配置）
playwright-cli open --persistent
# 使用自定义目录的持久化配置
playwright-cli open --profile=/path/to/profile

# 通过 Playwright 扩展连接浏览器
playwright-cli attach --extension=chrome

# 通过 channel 名称连接运行中的 Chrome 或 Edge
playwright-cli attach --cdp=chrome
playwright-cli attach --cdp=msedge

# 通过 CDP 端点连接运行中的浏览器
playwright-cli attach --cdp=http://localhost:9222

# 使用配置文件启动
playwright-cli open --config=my-config.json

# 关闭浏览器
playwright-cli close
# 断开已连接的浏览器（外部浏览器保持运行）
playwright-cli -s=msedge detach
# 删除默认会话的用户数据
playwright-cli delete-data
```

## 快照

每个命令执行后，playwright-cli 会提供当前浏览器状态的快照。

```bash
> playwright-cli goto https://example.com
### Page
- Page URL: https://example.com/
- Page Title: Example Domain
### Snapshot
[Snapshot](.playwright-cli/page-2026-02-14T19-22-42-679Z.yml)
```

你也可以使用 `playwright-cli snapshot` 命令按需获取快照。以下选项可自由组合。

```bash
# 默认 — 以时间戳命名保存到文件
playwright-cli snapshot

# 保存到指定文件（当快照是工作流结果的一部分时使用）
playwright-cli snapshot --filename=after-click.yaml

# 快照某个元素而非整个页面
playwright-cli snapshot "#main"

# 限制快照深度以提高效率，之后进行局部快照
playwright-cli snapshot --depth=4
playwright-cli snapshot e34

# 包含每个元素的边界框 [box=x,y,width,height]
playwright-cli snapshot --boxes
```

## 定位元素

默认情况下，使用快照中的 ref 与页面元素交互。

```bash
# 获取带 ref 的快照
playwright-cli snapshot

# 使用 ref 交互
playwright-cli click e15
```

你也可以使用 CSS 选择器或 Playwright 定位器。

```bash
# CSS 选择器
playwright-cli click "#main > button.submit"

# 角色定位器
playwright-cli click "getByRole('button', { name: 'Submit' })"

# 测试 ID
playwright-cli click "getByTestId('submit-button')"
```

## 浏览器会话

```bash
# 创建名为 "mysession" 的浏览器会话（带持久化配置）
playwright-cli -s=mysession open example.com --persistent
# 手动指定配置目录（仅在明确要求时使用）
playwright-cli -s=mysession open example.com --profile=/path/to/profile
playwright-cli -s=mysession click e6
playwright-cli -s=mysession close  # 停止命名浏览器
playwright-cli -s=mysession delete-data  # 删除持久化会话的用户数据

playwright-cli list
# 关闭所有浏览器
playwright-cli close-all
# 强制终止所有浏览器进程
playwright-cli kill-all
```

## 安装

如果全局 `playwright-cli` 命令不可用，尝试通过 `npx playwright-cli` 使用本地版本：

```bash
npx --no-install playwright-cli --version
```

本地版本可用时，所有命令使用 `npx playwright-cli`。否则，全局安装 `playwright-cli`：

```bash
npm install -g @playwright/cli@latest
```

## 示例：表单提交

```bash
playwright-cli open https://example.com/form
playwright-cli snapshot

playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3
playwright-cli snapshot
playwright-cli close
```

## 示例：多标签页

```bash
playwright-cli open https://example.com
playwright-cli tab-new https://example.com/other
playwright-cli tab-list
playwright-cli tab-select 0
playwright-cli snapshot
playwright-cli close
```

## 示例：使用开发者工具调试

```bash
playwright-cli open https://example.com
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli console
playwright-cli requests
playwright-cli close
```

```bash
playwright-cli open https://example.com
playwright-cli tracing-start
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli tracing-stop
playwright-cli close
```

## 示例：交互式会话

请求用户进行 UI 审查或设计反馈。用户在实时页面上绘制标注并输入评论；你收到带标注的截图、标注区域的快照以及用户备注。当用户请求"UI 审查"、"设计反馈"或"询问用户想法/意图"时使用：

```bash
playwright-cli open https://example.com
playwright-cli show --annotate
```

## 具体任务

* **运行和调试 Playwright 测试** [references/playwright-tests.md](references/playwright-tests.md)
* **请求模拟** [references/request-mocking.md](references/request-mocking.md)
* **运行 Playwright 代码** [references/running-code.md](references/running-code.md)
* **浏览器会话管理** [references/session-management.md](references/session-management.md)
* **规格驱动测试（规划/生成/修复）** [references/spec-driven-testing.md](references/spec-driven-testing.md)
* **存储状态（Cookies、localStorage）** [references/storage-state.md](references/storage-state.md)
* **测试生成** [references/test-generation.md](references/test-generation.md)
* **追踪** [references/tracing.md](references/tracing.md)
* **视频录制** [references/video-recording.md](references/video-recording.md)
* **检查元素属性** [references/element-attributes.md](references/element-attributes.md)
