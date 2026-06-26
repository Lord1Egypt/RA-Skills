---
name: playwright-cli
description: Playwright CLI 自动化工具 - 浏览器自动化测试和网页交互。通过 CLI 命令控制浏览器、截图、填表、点击、执行代码等操作。支持多浏览器、会话管理、网络拦截、视频录制等功能。
---

# Playwright CLI

通过命令行控制浏览器执行自动化任务。适合测试、爬虫、页面交互等场景。

## 安装

```bash
# 安装 Playwright CLI
npm install -g @playwright/cli@latest

# 安装 skills（供 AI agent 使用）
playwright-cli install --skills

# 检查版本
playwright-cli --version
# 输出: 0.1.7
```

## 核心命令

### 浏览器控制

| 命令 | 说明 |
|------|------|
| `playwright-cli open <url>` | 打开浏览器访问 URL |
| `playwright-cli goto <url>` | 导航到指定 URL |
| `playwright-cli close` | 关闭当前页面 |
| `playwright-cli screenshot [ref]` | 截图（当前页面或指定元素） |
| `playwright-cli screenshot --filename=f` | 保存截图到指定文件 |
| `playwright-cli pdf` | 保存页面为 PDF |
| `playwright-cli pdf --filename=page.pdf` | 保存 PDF 到指定文件 |
| `playwright-cli resize <w> <h>` | 调整浏览器窗口大小 |
| `playwright-cli reload` | 刷新当前页面 |
| `playwright-cli go-back` | 后退 |
| `playwright-cli go-forward` | 前进 |

### 页面交互

| 命令 | 说明 |
|------|------|
| `playwright-cli click <ref>` | 点击元素 |
| `playwright-cli dblclick <ref>` | 双击元素 |
| `playwright-cli fill <ref> <text>` | 填写表单 |
| `playwright-cli fill <ref> <text> --submit` | 填写并回车 |
| `playwright-cli type <text>` | 输入文本 |
| `playwright-cli hover <ref>` | 鼠标悬停 |
| `playwright-cli drag <startRef> <endRef>` | 拖拽操作 |
| `playwright-cli select <ref> <val>` | 选择下拉选项 |
| `playwright-cli check <ref>` | 勾选复选框/单选框 |
| `playwright-cli uncheck <ref>` | 取消勾选 |
| `playwright-cli upload <file>` | 上传文件 |
| `playwright-cli press <key>` | 按键（如 Enter、ArrowLeft） |

### 键盘鼠标

| 命令 | 说明 |
|------|------|
| `playwright-cli keydown <key>` | 按下键盘按键 |
| `playwright-cli keyup <key>` | 释放键盘按键 |
| `playwright-cli mousemove <x> <y>` | 移动鼠标 |
| `playwright-cli mousedown [button]` | 鼠标按下 |
| `playwright-cli mouseup [button]` | 鼠标释放 |
| `playwright-cli mousewheel <dx> <dy>` | 滚动鼠标 |

### 元素定位

支持多种定位方式：

```bash
# CSS 选择器
playwright-cli click "#main > button.submit"

# Role 定位器
playwright-cli click "getByRole('button', { name: 'Submit' })"

# Test ID
playwright-cli click "getByTestId('submit-button')"

# 使用快照引用（推荐）
playwright-cli snapshot  # 获取快照，包含元素引用如 e15
playwright-cli click e15  # 点击引用编号
```

### 快照

```bash
# 获取页面快照（包含元素引用）
playwright-cli snapshot

# 保存到指定文件
playwright-cli snapshot --filename=after-click.yaml

# 快照特定元素
playwright-cli snapshot "#main"

# 限制快照深度
playwright-cli snapshot --depth=4
```

### Tab 页管理

```bash
playwright-cli tab-list    # 列出所有标签页
playwright-cli tab-new [url]  # 新建标签页
playwright-cli tab-close <index>  # 关闭标签页
playwright-cli tab-select <index>  # 切换标签页
```

### 存储状态

**Cookies:**
```bash
playwright-cli cookie-list [--domain]  # 列出 Cookies
playwright-cli cookie-get <name>       # 获取 Cookie
playwright-cli cookie-set <name> <val> # 设置 Cookie
playwright-cli cookie-delete <name>    # 删除 Cookie
playwright-cli cookie-clear           # 清除所有 Cookie
```

**LocalStorage:**
```bash
playwright-cli localstorage-list                   # 列出
playwright-cli localstorage-get <key>             # 获取
playwright-cli localstorage-set <k> <v>           # 设置
playwright-cli localstorage-delete <k>            # 删除
playwright-cli localstorage-clear                 # 清除
```

**保存/恢复状态:**
```bash
playwright-cli state-save [filename]   # 保存状态
playwright-cli state-load <filename>   # 加载状态
```

### 网络拦截

```bash
playwright-cli route <pattern> [opts]  # 拦截请求
playwright-cli route-list              # 列出拦截规则
playwright-cli unroute [pattern]       # 移除拦截
```

### 调试功能

```bash
playwright-cli console [min-level]  # 查看控制台消息
playwright-cli network              # 查看网络请求
playwright-cli run-code <code>      # 执行代码片段
playwright-cli run-code --filename=f  # 执行文件中的代码
```

### 录制追踪

```bash
playwright-cli tracing-start    # 开始录制
playwright-cli tracing-stop     # 停止录制
playwright-cli video-start [filename]  # 开始录像
playwright-cli video-chapter <title>   # 添加章节标记
playwright-cli video-stop      # 停止录像
```

### 浏览器选项

```bash
# 使用指定浏览器
playwright-cli open --browser=chrome  # chrome/firefox/webkit

# 有头模式（可见浏览器）
playwright-cli open <url> --headed

# 持久化配置文件
playwright-cli open --persistent

# 使用配置文件
playwright-cli open --config=file.json

# 连接已运行的浏览器
playwright-cli attach --extension
```

## 会话管理

```bash
# 列出所有会话
playwright-cli list

# 关闭所有浏览器
playwright-cli close-all

# 强制结束所有浏览器进程
playwright-cli kill-all

# 打开可视化仪表盘
playwright-cli show

# 操作指定会话
playwright-cli -s=name open https://example.com  # 在命名会话中打开
playwright-cli -s=name close                    # 关闭命名会话
playwright-cli -s=name delete-data               # 删除会话数据
```

## 输出模式

```bash
# 输出到文件（默认）
playwright-cli --config path/to/config.json open example.com

# 配置文件中设置
{
  "outputMode": "file",  // 或 "stdout"
  "outputDir": "./playwright-output"
}
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| PLAYWRIGHT_MCP_BROWSER | 浏览器类型 | chrome |
| PLAYWRIGHT_MCP_HEADLESS | 是否无头 | true |
| PLAYWRIGHT_MCP_CONSOLE_LEVEL | 控制台级别 | info |
| PLAYWRIGHT_MCP_TIMEOUT_ACTION | 操作超时(毫秒) | 5000 |
| PLAYWRIGHT_MCP_TIMEOUT_NAVIGATION | 导航超时(毫秒) | 60000 |
| PLAYWRIGHT_MCP_VIEWPORT_SIZE | 窗口大小 | 1280x720 |
| PLAYWRIGHT_MCP_OUTPUT_DIR | 输出目录 | ./output |
| PLAYWRIGHT_MCP_SAVE_VIDEO | 保存视频 | - |
| PLAYWRIGHT_MCP_SAVE_TRACE | 保存追踪 | - |

## 使用示例

### 基础操作流程

```bash
# 1. 打开页面
playwright-cli open https://demo.playwright.dev/todomvc/

# 2. 截图
playwright-cli screenshot

# 3. 填写待办事项
playwright-cli type "Buy groceries"
playwright-cli press Enter
playwright-cli type "Water flowers"
playwright-cli press Enter

# 4. 勾选完成
playwright-cli snapshot
playwright-cli check e21
playwright-cli check e35

# 5. 再次截图
playwright-cli screenshot
```

### 测试网页功能

```bash
# 打开测试页面
playwright-cli open https://demo.playwright.dev/todomvc/ --headed

# 获取快照查看元素
playwright-cli snapshot

# 执行操作并截图
playwright-cli click e15
playwright-cli screenshot
```

### 多会话管理

```bash
# 创建多个会话
playwright-cli open https://site1.com
playwright-cli -s=session2 open https://site2.com --persistent

# 切换会话
playwright-cli -s=session2 goto /page

# 查看所有会话
playwright-cli list

# 关闭所有
playwright-cli close-all
```

## 配置示例

创建 `.playwright/cli.config.json`:

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": {
      "headless": false
    },
    "contextOptions": {
      "viewport": {
        "width": 1280,
        "height": 720
      }
    }
  },
  "outputDir": "./playwright-output",
  "outputMode": "file",
  "console": {
    "level": "info"
  },
  "timeouts": {
    "action": 5000,
    "navigation": 60000
  }
}
```

## 适用场景

- ✅ 网页功能测试
- ✅ 自动填表、数据采集
- ✅ 页面截图、Pdf 生成
- ✅ 网络请求拦截/mock
- ✅ 浏览器会话录制
- ✅ AI Agent 浏览器控制
- ❌ 不适合复杂登录态维护（建议用 MCP）

## 注意事项

1. 元素引用（如 e15）来自快照，每次页面变化后需要重新获取快照
2. 默认无头模式，使用 `--headed` 可视化
3. 临时目录存储，浏览器关闭后数据丢失
4. 使用 `--persistent` 保存配置文件到磁盘