# Playwright CLI 命令完整参考

## 目录

1. [Core 核心命令](#core-核心命令)
2. [Navigation 导航](#navigation-导航)
3. [Keyboard 键盘](#keyboard-键盘)
4. [Mouse 鼠标](#mouse-鼠标)
5. [Save 保存](#save-保存)
6. [Tabs 标签页](#tabs-标签页)
7. [Storage 存储](#storage-存储)
8. [Network 网络](#network-网络)
9. [DevTools 开发者工具](#devtools-开发者工具)
10. [Session 会话管理](#session-会话管理)
11. [Open 参数](#open-参数)

---

## Core 核心命令

### `open` - 打开浏览器

```bash
playwright-cli open                              # 打开空白浏览器
playwright-cli open https://example.com          # 打开并导航
playwright-cli open --browser=chrome             # 指定浏览器
playwright-cli open --persistent                 # 持久化配置
playwright-cli open --profile=/path/to/profile   # 自定义配置目录
playwright-cli open --config=my-config.json      # 使用配置文件
```

### `goto` - 导航到 URL

```bash
playwright-cli goto https://playwright.dev
playwright-cli goto https://example.com/page?param=value
```

### `click` - 点击元素

```bash
playwright-cli click e3                          # 使用 ref
playwright-cli click "#main > button"            # CSS 选择器
playwright-cli click "getByRole('button', { name: 'Submit' })"  # Locator
```

### `dblclick` - 双击元素

```bash
playwright-cli dblclick e7
```

### `type` - 输入文本

```bash
playwright-cli type "search query"
playwright-cli type "hello world" --delay=100    # 每字符延迟
```

### `fill` - 填充表单

```bash
playwright-cli fill e5 "user@example.com"
playwright-cli fill e5 "user@example.com" --submit  # 填充后按 Enter
```

### `drag` - 拖拽

```bash
playwright-cli drag e2 e8                        # 从 e2 拖到 e8
```

### `drop` - 拖放文件/数据

```bash
playwright-cli drop e4 --path=./image.png        # 拖放文件
playwright-cli drop e4 --data="text/plain=hello" # 拖放文本
```

### `hover` - 悬停

```bash
playwright-cli hover e4
```

### `select` - 下拉选择

```bash
playwright-cli select e9 "option-value"
```

### `upload` - 文件上传

```bash
playwright-cli upload ./document.pdf
```

### `check` / `uncheck` - 复选框

```bash
playwright-cli check e12
playwright-cli uncheck e12
```

### `snapshot` - 获取页面快照

```bash
playwright-cli snapshot                          # 默认保存
playwright-cli snapshot --filename=after.yaml    # 指定文件名
playwright-cli snapshot "#main"                  # 快照元素
playwright-cli snapshot e34                      # 快照元素
playwright-cli snapshot --depth=4                # 限制深度
playwright-cli snapshot --boxes                  # 含边界框
```

### `eval` - 执行 JavaScript

```bash
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
playwright-cli eval "el => el.id" e5
playwright-cli eval "el => el.getAttribute('data-testid')" e5
```

### `dialog-accept` / `dialog-dismiss` - 对话框

```bash
playwright-cli dialog-accept
playwright-cli dialog-accept "confirmation text"
playwright-cli dialog-dismiss
```

### `resize` - 调整窗口大小

```bash
playwright-cli resize 1920 1080
```

### `close` - 关闭浏览器

```bash
playwright-cli close
playwright-cli -s=mysession close                # 关闭命名会话
```

---

## Navigation 导航

### `go-back` - 后退

```bash
playwright-cli go-back
```

### `go-forward` - 前进

```bash
playwright-cli go-forward
```

### `reload` - 刷新页面

```bash
playwright-cli reload
```

---

## Keyboard 键盘

### `press` - 按键

```bash
playwright-cli press Enter
playwright-cli press ArrowDown
playwright-cli press Tab
playwright-cli press Escape
```

### `keydown` / `keyup` - 按下/释放修饰键

```bash
playwright-cli keydown Shift
playwright-cli keyup Shift
```

---

## Mouse 鼠标

### `mousemove` - 移动鼠标

```bash
playwright-cli mousemove 150 300                 # x=150, y=300
```

### `mousedown` / `mouseup` - 按下/释放鼠标

```bash
playwright-cli mousedown
playwright-cli mousedown right                   # 右键
playwright-cli mouseup
playwright-cli mouseup right
```

### `mousewheel` - 滚轮

```bash
playwright-cli mousewheel 0 100                  # deltaX=0, deltaY=100
```

---

## Save 保存

### `screenshot` - 截图

```bash
playwright-cli screenshot                        # 整个页面
playwright-cli screenshot e5                     # 元素截图
playwright-cli screenshot --filename=page.png    # 指定文件名
```

### `pdf` - 导出 PDF

```bash
playwright-cli pdf --filename=page.pdf
```

---

## Tabs 标签页

### `tab-list` - 列出标签页

```bash
playwright-cli tab-list
```

### `tab-new` - 新建标签页

```bash
playwright-cli tab-new
playwright-cli tab-new https://example.com/page
```

### `tab-close` - 关闭标签页

```bash
playwright-cli tab-close                         # 当前标签页
playwright-cli tab-close 2                       # 指定索引
```

### `tab-select` - 切换标签页

```bash
playwright-cli tab-select 0                      # 切换到第一个
```

---

## Storage 存储

### 状态保存/加载

```bash
playwright-cli state-save                        # 保存到默认文件
playwright-cli state-save auth.json              # 指定文件名
playwright-cli state-load auth.json              # 加载状态
```

### Cookies

```bash
playwright-cli cookie-list                       # 列出所有
playwright-cli cookie-list --domain=example.com  # 按域名过滤
playwright-cli cookie-get session_id             # 获取值
playwright-cli cookie-set session_id abc123      # 设置
playwright-cli cookie-set session_id abc123 --domain=example.com --httpOnly --secure
playwright-cli cookie-delete session_id          # 删除
playwright-cli cookie-clear                      # 清空所有
```

### LocalStorage

```bash
playwright-cli localstorage-list
playwright-cli localstorage-get theme
playwright-cli localstorage-set theme dark
playwright-cli localstorage-delete theme
playwright-cli localstorage-clear
```

### SessionStorage

```bash
playwright-cli sessionstorage-list
playwright-cli sessionstorage-get step
playwright-cli sessionstorage-set step 3
playwright-cli sessionstorage-delete step
playwright-cli sessionstorage-clear
```

---

## Network 网络

### `route` - 路由拦截

```bash
playwright-cli route "**/*.jpg" --status=404     # 返回 404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'  # Mock 响应
```

### `route-list` - 列出路由

```bash
playwright-cli route-list
```

### `unroute` - 移除路由

```bash
playwright-cli unroute "**/*.jpg"                # 移除特定路由
playwright-cli unroute                           # 移除所有
```

---

## DevTools 开发者工具

### `console` - 控制台日志

```bash
playwright-cli console                           # 所有日志
playwright-cli console warning                   # 仅警告
```

### `requests` / `request` - 网络请求

```bash
playwright-cli requests                          # 列出所有请求
playwright-cli request 5                         # 查看第 5 个请求详情
```

### `run-code` - 运行自定义代码

```bash
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
playwright-cli run-code --filename=script.js
```

### `tracing-start` / `tracing-stop` - 追踪

```bash
playwright-cli tracing-start
# ... 执行操作 ...
playwright-cli tracing-stop
```

### `video-start` / `video-stop` - 视频录制

```bash
playwright-cli video-start video.webm
playwright-cli video-chapter "Chapter Title" --description="Details" --duration=2000
playwright-cli video-stop
playwright-cli video-show-actions --duration=600 --position=top-right
playwright-cli video-hide-actions
```

### `show` - 交互式标注

```bash
playwright-cli show --annotate                   # 用户可在页面上标注
```

### `generate-locator` - 生成 Locator

```bash
playwright-cli generate-locator e5 --raw
```

### `highlight` - 高亮元素

```bash
playwright-cli highlight e5
playwright-cli highlight e5 --style="outline: 3px dashed red"
playwright-cli highlight e5 --hide
playwright-cli highlight --hide
```

---

## Session 会话管理

### 全局选项

```bash
-s=<name>                                        # 指定会话名
--raw                                            # 原始输出（无状态/快照）
--json                                           # JSON 输出
```

### 会话命令

```bash
playwright-cli list                              # 列出所有会话
playwright-cli close-all                         # 关闭所有浏览器
playwright-cli kill-all                          # 强制终止所有进程
playwright-cli delete-data                       # 删除会话数据
```

### 使用示例

```bash
playwright-cli -s=mysession open --persistent
playwright-cli -s=mysession click e6
playwright-cli -s=mysession close
```

---

## Open 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--browser=<name>` | 指定浏览器 | `--browser=chrome` |
| `--persistent` | 持久化配置 | `--persistent` |
| `--profile=<path>` | 自定义配置目录 | `--profile=/path/to/profile` |
| `--config=<file>` | 配置文件 | `--config=my-config.json` |
| `--cdp=<target>` | 连接已运行浏览器 | `--cdp=chrome` / `--cdp=http://localhost:9222` |
| `--extension=<browser>` | 通过 Extension 连接 | `--extension=chrome` |

---

## Windows 特殊处理

### URL 中的 `&` 转义

**cmd.exe:**
```batch
playwright-cli goto "https://example.com/?a=1^&b=2"
```

**PowerShell:**
```powershell
playwright-cli --% goto "https://example.com/?a=1&b=2"
```
