---
name: mtop-devtools-socket
description: Use when/适用于以下三个场景：1) 需要登录态的请求 —— 复用浏览器已登录的 Cookie/签名调用接口（mtop/http 请求）；2) 操作浏览器 —— 打开/切换/关闭标签页、点击、输入、滚动、按键、导航、上传文件、执行 JS、截图、页面快照等；3) 调试页面 —— 获取页面请求/控制台日志/埋点事件、查看与设置 mock、添加请求规则（重定向/改请求头）、获取 API schema、查看选中元素信息。通过 CDP 或本地 socket 调用 Mtop DevTools 能力。
argument-hint: <action> [--payload <json> | --payload-file <path>] [--output <path>]
---

# Mtop DevTools Socket 技能

## 📦 前置条件

本技能支持两种连接模式，满足其中**任意一种**即可：

### 模式一：浏览器插件（推荐，功能最完整）

安装 [Mtop DevTools 浏览器插件](https://chromewebstore.google.com/detail/mtop-devtools/aoehhjnofngknnjefamjbplchbolghkm)，打开 Chrome DevTools 应能看到 `Mtop` 标签页。

### 模式二：Chrome CDP 直连（无需插件，Chrome 145+）

无需安装浏览器插件：
1. 打开 Chrome，访问 `chrome://inspect/#remote-debugging`
2. 勾选 "Discover network targets"（Chrome 会弹出授权提示，点击允许）
3. Chrome 会自动写入 `DevToolsActivePort` 文件，native host 读取该文件自动连接

## 🚀 快速开始

安装完成并连接 Chrome 后即可直接调用：

```bash
mtop-devtools get_requests --payload '{"count": 5}'
mtop-devtools get_logs --payload '{"limit": 10}'
mtop-devtools get_screenshot --output ./screenshot.png
```

如命令不可用或连接失败，参考 [socket 故障排查](./references/troubleshooting.md)。

## 🔄 更新 Skill

如果本地安装的 skill 内容过旧，重新获取并按照安装引导覆盖安装即可：

https://mtop-devtools.io.alibaba-inc.com/skill-setup.txt

## 🎯 意图识别与支持的操作

根据用户的描述，选择对应的操作和参数：

### API 调试

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| 获取最近的请求、看下刚才发了什么 | `get_requests` | 获取请求，默认返回 panel 当前模式（mtop 或普通请求） |
| 获取 mtop 接口请求 | `get_requests` + `source: "mtop"` | 强制获取 mtop 接口 |
| 获取普通 HTTP 请求（xhr/fetch） | `get_requests` + `source: "requests"` | 强制获取非 mtop 请求 |
| 看下控制台日志、报了什么错 | `get_logs` | 获取浏览器控制台日志 |
| 看下埋点数据、RUM 事件、aplus 上报了什么 | `get_events` | 获取 RUM/aplus 埋点事件 |
| 获取接口 schema、接口出入参是什么 | `get_api_schema` | 获取 API 接口 schema，可选择返回 schema、hsf 或全部 |

### Mock & 请求规则

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| mock 掉某个接口、让接口返回 xxx | `set_mock` | 设置 API mock 数据 |
| 查看当前有哪些 mock | `get_mocks` | 查看当前生效的 mock |
| 添加请求规则、重定向请求、修改请求头、拦截请求 | `add_rule` | 添加 Chrome declarativeNetRequest 规则 |

### 网络请求代理

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| 调用某个接口、带上 Cookie 发一个 HTTP 请求 | `proxy_request` | 代理请求，自动携带浏览器 Cookie |
| 调用某个 mtop 接口、发一个 mtop 请求 | `send_mtop_request` | 在页面上下文中发起 mtop 请求，自动处理签名和 token |
| 申请域名权限、授权某个域名（`proxy_request` 报 `Cookie access not authorized` / `Permission denied` 时） | `request_domain_permission` | 弹窗让用户授权指定域名（host permission），授权后 `proxy_request` 才能携带该域名 Cookie |

### 浏览器操作

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| 打开一个页面、新建标签页 | `tab_open` | 在浏览器中打开新 Tab 并等待加载完成 |
| 关闭标签页 | `tab_close` | 关闭指定 tabId 的标签页 |
| 列出所有标签页、看下打开了哪些页面 | `tab_list` | 获取当前窗口所有标签页列表 |
| 点击按钮、点击元素、点一下某个东西 | `page_click` | 点击页面元素。可按 selector / text / point 三选一定位，默认走 CDP 真实事件（移动端 H5 可靠） |
| 输入文字、填写表单、在输入框里输入 | `page_type` | 向输入框填写文本，兼容 React 受控组件 |
| 滚动页面、翻到底部、往下翻 | `page_scroll` | 滚动页面，支持 up/down/top/bottom 四个方向 |
| 悬停、鼠标移上去、鼠标放元素上 | `page_hover` | 将鼠标悬停在元素上，触发 hover 效果（如下拉菜单、提示信息） |
| 执行 JS、在页面上运行脚本 | `page_eval` | 在页面上下文中执行任意 JavaScript 表达式 |
| 按键、按回车、按 Tab | `page_press` | 在页面中按下键盘按键（Enter/Tab/Escape 等） |
| 等待页面加载、等元素出现 | `page_wait` | 等待指定时间或等待某个元素出现 |
| 在当前标签页导航、跳转页面 | `page_navigate` | 在当前标签页内导航到新 URL |
| 上传文件、选择文件、文件上传 | `page_upload` | 向 `<input type="file">` 元素上传本地文件 |

### 组合调用

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| 滚动后截图、点击然后等待、先滚动再点击再截图、批量操作 | `run_actions` | 批量顺序执行多个 action，一次调用完成组合流程，减少往返延迟。遇错即停 |

### 移动端模拟

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| 切到 iPhone / Android 模拟、调试 H5 移动页面、模拟手机视口 | `set_device_emulation` + `enabled: true, preset: "iphone-15-pro"` | 把目标 tab 切换为移动端模拟态（视口/UA/触摸），等价 DevTools 设备工具栏，作用域 per-tab。启用后默认 reload 让页面以移动模式重新初始化 |
| 关闭移动模拟、恢复桌面视图 | `set_device_emulation` + `enabled: false` | 清除当前 tab 的移动端模拟，回到桌面态 |

### 页面感知

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| 获取页面结构、看下页面上有什么元素、页面快照 | `page_snapshot` | 获取页面无障碍树快照，返回所有可交互元素的结构化文本 |
| 截图、获取当前页面截图、看一下页面长什么样 | `get_screenshot`，保存文件时加 `--output <path>` | 获取当前浏览器标签页的页面截图；未指定 `--output` 时返回 base64，指定后保存到本地文件 |
| 截图某个元素、只截这个组件的图、看一下这个区域 | `get_screenshot` + `selector: "<css>"` | 对指定 CSS 选择器匹配的元素截图（类似 DevTools "Capture node screenshot"） |
| 获取选中元素、看一下这个元素的布局/样式、分析元素 | `get_selected_element` | 获取 Elements 面板当前选中元素的详细信息；指定 `--output <path>` 时自动截图并保存到本地文件 |
| 列出页面所有 frame、看下有哪些 iframe | `page_frames` | 获取当前页面的 frame 树（主 frame + 所有 iframe），返回 frameId / url / name / isMainFrame |

### 用户信息

| 用户说的话（示例） | 操作 | 说明 |
|---|---|---|
| 获取用户工号、获取当前登录用户 ID | `get_user_info` | 默认只返回工号（userId） |
| 获取用户详细信息、获取用户信息、看下用户资料 | `get_user_info` + `detail: true` | 返回完整的用户信息（姓名、花名、部门、BU 等） |
| 获取/切换 TDBank 账号、快速借用账号 | `tdbank_account` | 支持 current/list/switch/borrow，需要浏览器已登录 tdbank.alibaba-inc.com |

## 📚 参考文档

- [使用示例](./references/examples.md)（各操作的完整 CLI 调用示例）
- [API 参数详细说明](./references/api-reference.md)（set_mock / proxy_request / get_requests / get_events / get_screenshot / get_selected_element / tdbank_account 完整参数表及响应结构）
- [socket 故障排查](./references/troubleshooting.md)

