---
name: mearl
description: Use when/适用于以下三个场景：1) 需要登录态的请求 —— 复用浏览器已登录的 Cookie/签名调用接口（mtop/http 请求）；2) 操作浏览器 —— 打开/切换/关闭标签页、点击、输入、滚动、按键、导航、上传文件、执行 JS、截图、页面快照等；3) 调试页面 —— 获取页面请求/控制台日志/埋点事件、查看与设置 mock、添加请求规则（重定向/改请求头）、获取 API schema、查看选中元素信息。通过统一的 mearl CLI 调用 Mearl 能力，兼容本地、CDP 直连与云端连接。
metadata:
  version: "2.0.0"
---

# Mearl 技能

## 🚀 快速开始

正常任务直接调用，本地与云端命令一致：

```bash
mearl get_requests --payload '{"count": 5}'
mearl get_logs --payload '{"limit": 10}'
mearl page_snapshot --payload '{"tabId": 12345}'
mearl page_click --payload '{"tabId":12345,"selector":"#submit"}'
```

只有命令不可用或连接失败时才执行 `mearl check` 并读取 [连接故障排查](./references/troubleshooting.md)，其中包含本地、CDP 直连和云端建联方式；正常任务不要主动探测、重复安装或初始化。

## 页面操作参数契约

- `page_snapshot.query` 必须是对象，例如 `"query":{"text":"保存","role":"button"}`，不能直接传字符串。
- `page_click` 必须且只能使用 `selector` / `text` / `point` 之一。`selector` 接受 CSS 或最新快照的 `@ref`；`scope` 只用于配合 `text`，也只接受 CSS 或 `@ref`，不能传可见标题。`clickMode` 默认 `auto`：可见桌面页使用可信 mouse、移动模拟页使用可信 touch，隐藏页使用 DOM fallback，且不切换标签或还原窗口；响应返回 `dispatchMode` / `pointerType` / `fallbackReason`。仅在需要覆盖自动策略时使用 `dom` / `mouse` / `touch`。
- `page_scroll` 的距离字段是 `distance`。页面本身不动时，选择目标区域内的 CSS / `@ref`，并传 `containerPolicy: "nearest"` 定位最近的可滚动祖先。
- 每次 `page_snapshot` 都会刷新 `@ref`。重复目标位于带标题的结构化区域时，先用 `query` 定位标题，再把返回的 ref 作为 `rootRef` 并配合 `ancestorDepth` 获取局部上下文，最后点击目标的新 ref。

其他参数不确定时先运行 `mearl <action> --help` 或读取 [API 参数说明](./references/api-reference.md)，不要猜测字段名或类型。

## 浏览器控制默认工作流

1. **确认环境**：在首次快照前判断页面形态。用户明确要求移动端/H5，或目标明确是触屏专用页面但当前仍为桌面视口时，先进入移动模拟：新建页面在 `tab_open` 中传 `emulation`；已打开页面调用 `set_device_emulation`，默认 reload 后再建立快照。不要仅凭响应式布局或单一 URL 特征切换模拟。
2. **建立基线**：首次进入页面或导航完成后调用一次 `page_snapshot`。长列表优先 `mode: "viewport"`；已知区域时用 `rootSelector` / `rootRef`；只找单个文案或角色时用 `query`；只有需要全貌时才用 `full`。`interactive` 只保留当前视口内的 AX 语义控件；视口内缺少控件语义时会回退到 viewport，并返回 `fallbackMode`。
3. **执行并判断**：直接调用带内置观察的页面动作。先检查 `action.success`，再用 `requestedTarget` / `resolvedTarget` 判断实际目标，并结合 `observation.changed` 或 `navigation` 判断业务效果。`delta` 观察读取 `effects`；`navigation` 检查 `ready` / `settledBy` 后用新 URL 重建快照。
4. **按需补充观察**：仅当 `fullSnapshotRecommended` 为 `true` 时，根据 `snapshotReasons` 获取最小范围快照，优先顺序为 `rootRef`、`rootSelector`、`query`、`viewport`、`full`。`page_scroll` 的 `moved` 只证明位置变化；下一步需要读取新视口内容时，即使没有推荐回退，也按需获取 viewport 快照。视觉任务、Canvas、跨域 iframe 或纯视觉变化使用 `page_screenshot`。`changed: true` 但 effects 为空不代表失败。
5. **验证终态**：对照用户要求检查当前 URL、标题和必要范围的快照；视觉终态使用截图。动作成功、发生导航或到达中间页面都不能单独证明任务完成。

不要在每次动作后固定执行 `page_wait`、`page_snapshot` 或 `page_screenshot`。无需观察结果或排障时可传 `observe: false` 只执行裸动作；无前置动作的独立等待继续使用 `page_wait`。详细参数和响应见 [API 参数说明](./references/api-reference.md)。

## 🎯 意图识别与支持的操作

根据用户的描述，选择对应的操作和参数：

### API 调试

| 用户说的话（示例）                      | 操作                                  | 说明                                                          |
| --------------------------------------- | ------------------------------------- | ------------------------------------------------------------- |
| 获取最近的请求、看下刚才发了什么        | `get_requests`                        | 获取请求，默认返回 mtop；可传 `tabId` 指定页面                |
| 获取 mtop 接口请求                      | `get_requests` + `source: "mtop"`     | 强制获取 mtop 接口                                            |
| 获取普通 HTTP 请求（xhr/fetch）         | `get_requests` + `source: "requests"` | 强制获取非 mtop 请求                                          |
| 看下控制台日志、报了什么错              | `get_logs`                            | 获取浏览器控制台日志                                          |
| 看下埋点数据、RUM/aplus/ARMS 上报了什么 | `get_events`                          | 获取后台采集的埋点事件，可传 `tabId`，无需打开 DevTools panel |
| 获取接口 schema、接口出入参是什么       | `get_api_schema`                      | 获取 API 接口 schema，可选择返回 schema、hsf 或全部           |

### Mock & 请求规则

| 用户说的话（示例）                             | 操作        | 说明                                      |
| ---------------------------------------------- | ----------- | ----------------------------------------- |
| mock 掉某个接口、让接口返回 xxx                | `set_mock`  | 设置 API mock 数据                        |
| 查看当前有哪些 mock                            | `get_mocks` | 查看当前生效的 mock                       |
| 添加请求规则、重定向请求、修改请求头、拦截请求 | `set_rule`  | 添加 Chrome declarativeNetRequest 规则    |
| 查看当前有哪些请求规则、规则生效了吗           | `get_rules` | 查看全部请求规则（含 Options 面板配置的） |

### 网络请求代理

| 用户说的话（示例）                                                                                      | 操作                        | 说明                                                                                   |
| ------------------------------------------------------------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------- |
| 调用某个接口、带上 Cookie 发一个 HTTP 请求                                                              | `send_request`              | 代理请求，自动携带浏览器 Cookie                                                        |
| 调用某个 mtop 接口、发一个 mtop 请求                                                                    | `send_mtop_request`         | 在页面上下文中发起 mtop 请求，自动处理签名和 token                                     |
| 申请域名权限、授权某个域名（`send_request` 报 `Cookie access not authorized` / `Permission denied` 时） | `request_domain_permission` | 弹窗让用户授权指定域名（host permission），授权后 `send_request` 才能携带该域名 Cookie |

### 浏览器操作

| 用户说的话（示例）                     | 操作            | 说明                                                                                                                                                                                               |
| -------------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 打开页面、新建或复用标签页             | `tab_open`      | 默认新建；传 `reuse: "prefer"` 可按 URL 规则优先复用，`reuse: "require"` 可限制为只复用。新开 active Tab 可用 `restoreFocusOnClose` 在关闭后恢复原焦点；`emulation` 支持首屏即移动态               |
| 关闭标签页                             | `tab_close`     | 关闭指定 tabId 的标签页                                                                                                                                                                            |
| 列出所有标签页、看下打开了哪些页面     | `tab_list`      | 获取当前窗口所有标签页列表                                                                                                                                                                         |
| 点击按钮、点击元素、点一下某个东西     | `page_click`    | 点击、等待异步稳定并返回高置信度页面信号；selector / text / point 三选一定位；可见页默认可信输入，隐藏页自动 DOM fallback 且不改变窗口焦点，checkbox/radio 校验前后状态；重复文本可用 `scope` 消歧 |
| 输入文字、填写表单、在输入框里输入     | `page_type`     | 输入并观察校验提示等变化，兼容 React 受控组件                                                                                                                                                      |
| 滚动页面或容器、翻到底部、往下翻       | `page_scroll`   | 滚动并观察懒加载内容，支持 up/down/top/bottom；滚动距离用 `distance`，可用 CSS selector 或 @ref 指定滚动容器                                                                                       |
| 悬停、鼠标移上去、鼠标放元素上         | `page_hover`    | 悬停并观察下拉菜单、提示信息等变化                                                                                                                                                                 |
| 执行 JS、在页面上运行脚本              | `page_eval`     | 在页面上下文中执行任意 JavaScript 表达式；默认裸执行，仅在表达式会修改页面且需要结果信号时显式传 `observe: {}`                                                                                     |
| 按键、按回车、按 Tab                   | `page_press`    | 按键并观察提交、关闭弹窗等结果                                                                                                                                                                     |
| 没有前置动作，等待时间、元素或页面条件 | `page_wait`     | `time` / `selector` / `condition` 三选一；条件表达式返回 truthy 时结束。动作后的异步稳定判断由页面动作内置的观察完成                                                                               |
| 在当前标签页导航、刷新、后退或前进     | `page_navigate` | URL 导航、`refresh: true`、`history: "back" / "forward"` 三种模式互斥；历史回退不要用组合键或 `page_eval history.back()`                                                                           |
| 上传文件、选择文件、文件上传           | `page_upload`   | 上传并观察进度、成功提示等变化                                                                                                                                                                     |

### 组合调用

| 用户说的话（示例）                       | 操作          | 说明                                                                                                                |
| ---------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------- |
| hover 后立即点击、无需中间判断的批量操作 | `run_actions` | 批量顺序执行紧密连续的原子 action，步骤内页面动作不带内置观察。需要根据每一步页面变化决策时逐步调用带观察的页面动作 |

### 环境模拟

| 用户说的话（示例）                                         | 操作                                                              | 说明                                                                                                                                                                                                                        |
| ---------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 切到 iPhone / Android 模拟、调试 H5 移动页面、模拟手机视口 | `set_device_emulation` + `enabled: true, preset: "iphone-15-pro"` | 把目标 tab 切换为移动端模拟态（视口/UA/触摸），等价 DevTools 设备工具栏，作用域 per-tab。启用后默认 reload 让页面以移动模式重新初始化。若是**新开**页面，优先用 `tab_open` 的 `emulation` 参数，首屏即移动态、省一次 reload |
| 关闭移动模拟、恢复桌面视图                                 | `set_device_emulation` + `enabled: false`                         | 清除当前 tab 的移动端模拟，回到桌面态                                                                                                                                                                                       |
| 模拟其他时区、测试跨时区日期逻辑                           | `set_timezone` + `timezone: "America/New_York"`                   | 按 tab 覆盖页面时区，立即影响 Date / Intl；支持任意 IANA 时区                                                                                                                                                               |
| 恢复浏览器默认时区                                         | `set_timezone` + `timezone: ""`                                   | 清除目标 tab 的时区覆盖                                                                                                                                                                                                     |

### 页面感知

| 用户说的话（示例）                                | 操作                                                  | 说明                                                                                        |
| ------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 首次获取页面结构、重新建立页面全貌                | `page_snapshot`                                       | 默认 `mode: "full"`，获取完整无障碍树和 `@ref`                                              |
| 获取当前屏幕内的长列表内容                        | `page_snapshot` + `mode: "viewport"`                  | 只保留当前视口 AX 分支，滚动后可重新获取                                                    |
| 获取弹层、表单或指定区域                          | `page_snapshot` + `rootSelector` / `rootRef`          | 用 CSS 或已有 ref 获取 AX 子树；`rootRef` 可配 `ancestorDepth` 向上扩展上下文               |
| 在大型 AX 树中查找特定文案或角色                  | `page_snapshot` + `query`                             | 传 `{ text?, role?, exact? }` 对象，服务端只返回命中节点和祖先路径                          |
| 截图、视觉判断、Canvas、查看页面长什么样          | `page_screenshot`，CLI 查看时加 `--output <绝对路径>` | 保存后交给图像查看能力，不要读取或截断 base64 stdout；不作为每次动作后的固定步骤            |
| 截图某个元素、只截这个组件的图、看一下这个区域    | `page_screenshot` + `selector: "<css>"`               | 对指定 CSS 选择器匹配的元素截图（类似 DevTools "Capture node screenshot"）                  |
| 获取选中元素、看一下这个元素的布局/样式、分析元素 | `page_selected_element`                               | 获取 Elements 面板当前选中元素的详细信息；指定 `--output <path>` 时自动截图并保存到本地文件 |
| 列出页面所有 frame、看下有哪些 iframe             | `page_frames`                                         | 获取当前页面的 frame 树（主 frame + 所有 iframe），返回 frameId / url / name / isMainFrame  |

### 托管浏览器与多账号

| 用户说的话（示例）                                       | 操作                                           | 说明                                                                                                                            |
| -------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 新开一个无头浏览器、启动独立浏览器                       | `browser_launch`                               | 启动独立 Profile 的 Chrome，默认 headless；返回唯一 browserId                                                                   |
| 新开浏览器并登录某个 TDBank 账号、登录 taobao.com 系页面 | `browser_launch` + `accountId`                 | 通过 TDBank SSO 在独立浏览器中登录测试账号，供 taobao.com 及其子域页面使用；控制浏览器需已登录 TDBank，SSO 票据只在本地内部传递 |
| 新开浏览器并复制某些站点登录态                           | `browser_launch` + `copyCookieDomains`         | 按域复制完整 Cookie 属性；非内置域需先调用 `request_domain_permission` 授权                                                     |
| 搜索/借用账号并在新浏览器登录                            | `browser_launch` + `query`                     | 快速借用匹配账号并登录新实例，不切换控制浏览器账号                                                                              |
| 查看浏览器及托管实例状态                                 | `browser_list`                                 | 返回所有浏览器的 browserId、类型和状态；托管实例同时包含运行模式和登录账号                                                      |
| 操作指定实例                                             | 任意浏览器 action + `--browser managed:<name>` | 不同实例 Cookie/Storage 完全隔离                                                                                                |
| 关闭托管浏览器                                           | `browser_close`                                | 临时 Profile 自动删除；持久化 Profile 可选择保留                                                                                |

## 💡 实用技巧（易踩的坑）

- **大体积 payload**：正文注入、base64 图片等大参数不要拼在命令行里——用 `--payload-file <path>` 从文件读取整个 payload；或把 payload 里某个字段写成 `"@<绝对路径>"`，该字段值会从文件读取（先按 JSON 解析、失败按原始文本）。
- **级联菜单 / 悬浮面板**（如多级下拉选择）：逐条发 `page_click` 时命令间隔会让面板收起。用 `run_actions` 把 hover/click/wait 序列放进**一次调用**顺序执行；悬浮展开用 `page_hover`。
- **`<select>` 下拉**：用 `page_click` 点选项文本——命中 `<option>` 时会自动改写父 `<select>` 的值并派发 `input`/`change`（兼容 React 受控组件），不需要手写 `page_eval`。
- **`page_eval` 支持 Promise**：表达式的值若是 Promise 会自动等待并返回 resolve 结果，`fetch(...).then(r=>r.json())` 可以直接作为表达式，不需要写全局变量轮询。
- **结构化能力不足时**：用单次只读 `page_eval` 集中返回最小必要的候选和状态，取得 selector 后立即回到 `page_click` / `page_scroll`；直接点击、滚动或修改 DOM 仅作最后手段，需要判断后续变化时传 `observe: {}`。
- **`tab_list` 同时返回 `id` 和 `tabId`**，两者值相同；传给其他 action 时使用 `tabId`。
- **复用标签页**：已知目标 URL 时优先调用一次 `tab_open` 并传 `reuse: "prefer"`，无需先 `tab_list` 再自行筛选。多个标签页匹配时默认报错，可缩小 `match.urlPattern` 或显式传 `match.onMultiple: "first"`。
- **自定义上传组件**：`page_upload` 直接把文件写入 `input[type=file]` 节点（`DOM.setFileInputFiles`），隐藏 input、点击不弹 file chooser 的组件也能上传。

## 📚 参考文档

- [使用示例](./references/examples.md)（各操作的完整 CLI 调用示例）
- [API 参数详细说明](./references/api-reference.md)（page_click / page_snapshot / set_mock / send_request / get_requests 等完整参数表及响应结构）
- [连接故障排查](./references/troubleshooting.md)
