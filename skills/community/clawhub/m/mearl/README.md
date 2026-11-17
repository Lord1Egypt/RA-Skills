# Mearl Skill

连接 [Mearl](https://chromewebstore.google.com/detail/mearl/aoehhjnofngknnjefamjbplchbolghkm)，让 AI Agent 能够直接操控浏览器、调试 API、管理 Mock 和抓取页面数据。

支持两种使用方式：

- **本地使用**（Agent 与浏览器同机）：通过本地 Unix Socket 连接，浏览器侧用插件模式（推荐，功能最完整）或 CDP 模式（Chrome 145+ 开启 `chrome://inspect/#remote-debugging`，无需插件）。
- **云端使用**（Agent 在云端、浏览器在本地）：云端安装并后台运行 `@mearl/cloud-server` + `@mearl/cloud-client`，本地用 `@mearl/cloud-connector` 接入。

详见 [前置条件](./SKILL.md) 与 [故障排查](./references/troubleshooting.md)。

## 支持的能力

### 📊 数据获取

| 能力                      | 说明                                                                                                           |
| ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **get_requests**          | 获取浏览器网络请求，支持 mtop 和普通 HTTP 请求，可按数量、关键词过滤                                           |
| **get_logs**              | 获取浏览器控制台日志，支持按级别（error / warn / info）过滤                                                    |
| **get_events**            | 获取 RUM / aplus / ARMS 埋点事件，支持指定 tab、按来源、事件类型和关键词过滤，无需打开 DevTools panel          |
| **get_api_schema**        | 获取 mtop API 的 JSON Schema 和 HSF 接口信息（服务名、方法、版本）                                             |
| **page_screenshot**       | 获取当前页面截图，支持 PNG / JPEG 格式，可指定质量和保存路径                                                   |
| **page_selected_element** | 获取 Elements 面板当前选中元素的详细信息，包括布局、计算样式、DOM 属性，可附带节点截图                         |
| **get_user_info**         | 获取当前登录用户的信息，默认返回工号，支持获取完整用户信息（姓名、花名、部门、BU 等）                          |
| **tdbank_account**        | 通过 TDBank SSO 将测试账号登录到 taobao.com 及其子域页面，支持获取当前账号、账号列表、切换账号、快速借用并切换 |

### 🔧 Mock & 请求规则

| 能力             | 说明                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------- |
| **set_mock**     | 设置 API Mock 数据，支持按字段路径精确修改响应内容，也支持整体替换                       |
| **get_mocks**    | 查看当前所有生效的 Mock 配置                                                             |
| **set_rule**     | 添加 Chrome declarativeNetRequest 规则，支持请求重定向、修改请求头、拦截阻断             |
| **send_request** | 代理 HTTP 请求，自动携带浏览器 Cookie；支持 SPA 页面渲染模式，等待 JS 渲染后提取页面内容 |

### 🌐 浏览器操作

| 能力               | 说明                                                                                                                                                                                                                                                                        |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **browser_list**   | 统一列出普通浏览器和托管浏览器，返回默认目标、类型以及 `connected` / `running_disconnected` / `stopped` 状态                                                                                                                                                                |
| **browser_launch** | 启动独立 Profile 的托管 Chrome，可选择 headless、持久化 Profile、复制指定域 Cookie 或登录 TDBank 测试账号                                                                                                                                                                   |
| **browser_close**  | 关闭指定托管浏览器；临时 Profile 自动删除，持久化 Profile 可按需保留或删除                                                                                                                                                                                                  |
| **tab_open**       | 打开新标签页并等待加载完成，支持前台/后台打开、可选 `emulation` 开 tab 即移动态                                                                                                                                                                                             |
| **tab_close**      | 关闭指定标签页                                                                                                                                                                                                                                                              |
| **tab_list**       | 列出当前窗口所有标签页（ID、URL、标题、激活状态）                                                                                                                                                                                                                           |
| **page_navigate**  | 在当前标签页内导航到新 URL、刷新页面或沿浏览历史后退/前进，等待完成后返回                                                                                                                                                                                                   |
| **page_snapshot**  | 获取页面无障碍树快照，支持完整树、当前视口、可交互控件或指定 CSS 子树，并返回 `@ref` 引用                                                                                                                                                                                   |
| **page_click**     | 点击页面元素并默认内置观察（等待页面稳定并返回高置信度信号或导航结果），按 `selector`（CSS 或 `@ref`）/ `text`（可见文本）/ `point`（视口坐标）三选一定位；`clickMode: "auto"` 在可见页按设备模拟状态派发可信 mouse/touch，隐藏页使用 DOM fallback，checkbox/radio 校验状态 |
| **page_type**      | 向输入框填写文本并默认内置观察，默认先清空再输入，兼容 React 受控组件                                                                                                                                                                                                       |
| **page_press**     | 按下键盘按键并默认内置观察（Enter / Tab / Escape / Space 等），支持 Ctrl / Shift / Alt / Meta 组合键                                                                                                                                                                        |
| **page_scroll**    | 滚动页面或指定容器并默认内置观察，支持 up / down / top / bottom 四个方向，可自定义滚动距离；容器支持 CSS selector 或 `@ref`                                                                                                                                                 |
| **page_wait**      | 等待指定毫秒数，或等待某个 CSS 选择器对应的元素出现（支持超时设置）                                                                                                                                                                                                         |
| **page_eval**      | 在页面上下文中执行任意 JavaScript 表达式，返回执行结果                                                                                                                                                                                                                      |
| **page_upload**    | 向 `<input type="file">` 元素上传本地文件并默认内置观察，支持单文件和多文件上传                                                                                                                                                                                             |

Agent 首次进入页面时使用 `page_snapshot` 建立基线，后续交互直接使用页面动作，它们默认内置观察，动作与异步同步在一次调用内完成。长列表回退时优先 `page_snapshot(mode: "viewport")`，已知区域时传 `rootSelector`。观察结果返回 `mode: "delta"` 时读取 `effects.notifications`、`effects.interactives` 和 `effects.focus`；可交互节点有 `node.ref` 时后续动作优先使用 ref，没有时使用 `node.selector`。通知中的 `change: "transient"` 表示 Toast/状态已消失。当它返回 `mode: "navigation"` 时，在新页面重建 snapshot；其他情况下根据 `fullSnapshotRecommended` 和 `snapshotReasons` 决定是否回退。滚动动作的 `moved` 只证明位置变化，下一步需要读取新视口内容时再按需获取 viewport 快照。传 `observe: false` 可关闭观察仅执行裸动作，适合排障。

### 环境模拟

| 能力                     | 说明                                                                                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **set_device_emulation** | 把目标 tab 切到移动端模拟（视口/UA/触摸），等价 DevTools 设备工具栏；内置 iPhone 15 Pro / iPhone SE / Pixel 8 / iPad Mini / Galaxy S23 预设，也支持自定义 width/height/UA |
| **set_timezone**         | 按目标 tab 覆盖页面时区，支持任意 IANA 时区；传空字符串恢复浏览器默认时区                                                                                                 |

## 全局命令

初始化时会自动注册全局命令 `mearl`，可在任意终端直接使用：

```bash
# 获取最近 5 条请求
mearl get_requests --payload '{"count": 5}'

# 获取页面截图
mearl page_screenshot --output ./screenshot.png

# 查看帮助
mearl --help
```

其他 skill 也可以直接通过 `mearl` 命令调用浏览器能力，无需关心脚本路径。
