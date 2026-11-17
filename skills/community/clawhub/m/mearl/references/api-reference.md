# Mearl API 参数参考

## browser_list / browser_launch / browser_close 参数说明

`browser_list` 统一返回普通浏览器和托管浏览器。顶层包含 `count`、`connectedCount`、`defaultBrowserId` 和 `browsers`；每个浏览器的公共字段包括 `browserId`、`name`、`type` 和 `status`：

- `type` 为 `regular` 或 `managed`。
- `status` 为 `connected`、`running_disconnected` 或 `stopped`；只有 `connected` 可作为浏览器操作目标。
- 托管浏览器额外返回 `headless`、`persistent`、`cdpPort`、`createdAt`，以及可用时的 `account` / `copiedCookies`。

`browser_launch` 启动一个独立 Chrome 实例。控制浏览器已经登录 TDBank 时，可通过 TDBank SSO 在新实例中登录指定测试账号，供 `taobao.com` 及其子域页面使用；SSO 地址只在本地内部传递。

| 参数                | 类型          | 必填 | 说明                                                                                   |
| ------------------- | ------------- | ---- | -------------------------------------------------------------------------------------- |
| `name`              | string        | ✅   | 实例名称，最多 64 个字符；名称大小写不敏感，返回的 browserId 为小写的 `managed:<name>` |
| `headless`          | boolean       | —    | 是否使用 `headless=new`，默认 `true`                                                   |
| `userAgentMode`     | string        | —    | `default` 使用 Chrome 默认 UA，`desktop` 使用匹配本机版本的桌面 UA，默认 `default`     |
| `persistent`        | boolean       | —    | 关闭后是否保留独立 Profile，默认 `false`                                               |
| `url`               | string        | —    | TDBank SSO 登录完成后打开的初始页面，通常为 `taobao.com` 系页面                        |
| `executablePath`    | string        | —    | Chrome 可执行文件路径；也可用 `MEARL_CHROME_PATH`                                      |
| `accountId`         | string/number | —    | TDBank 账号列表中的账号 ID                                                             |
| `havanaId`          | string/number | —    | 直接指定账号；必须同时传 `site`                                                        |
| `site`              | string/number | —    | havanaId 对应站点                                                                      |
| `query`             | string        | —    | 搜索、快速借用并登录匹配账号                                                           |
| `tabId`             | number        | —    | CDP 控制浏览器中用于读取 TDBank Cookie 的标签页                                        |
| `copyCookieDomains` | string[]      | —    | 从控制浏览器复制到新实例的 Cookie 域名；支持主机名或 URL，可传多个                     |

`accountId`、`havanaId + site`、`query` 互斥；三者均不传时只启动空白隔离浏览器。

Cookie 复制保留 HttpOnly、Secure、SameSite、过期时间和可用的分区属性；复制发生在 TDBank SSO 之前。扩展模式下，非内置域需要先通过 `request_domain_permission` 授权。响应只返回复制域和数量，不返回 Cookie 值。

`browser_close` 接受 `browser`（browserId 或名称）和可选的 `deleteProfile`。临时 Profile 始终删除；持久化 Profile 仅在 `deleteProfile: true` 时删除。

---

## set_mock 参数说明

用于动态设置 API 接口的 Mock 数据，支持两种响应构造方式：

- **方式一（mockData）**：直接传入完整的 Mock 响应数据，完全替换真实接口返回
- **方式二（fields）**：基于真实响应修改指定字段，适合微调场景

| 参数         | 类型    | 必填 | 说明                                                                                                                                                |
| ------------ | ------- | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `apiName`    | string  | ✅   | API 名称或正则表达式。例如 `"mtop.cart.query"` 精确匹配，`".*\\.cart\\..*"` 匹配所有购物车接口                                                      |
| `mockData`   | object  | —    | **【方式一】** 完整的 Mock 响应数据（JSON 对象）。传入后该接口将完全返回此数据，不再请求真实服务端。与 `fields` 二选一，同时提供时优先使用 `fields` |
| `fields`     | array   | —    | **【方式二】** 基于真实响应修改指定字段。数组元素包含 `path`（字段路径）和 `value`（新值）。会先获取原始响应，然后只修改指定字段                    |
| `enabled`    | boolean | —    | 是否启用 Mock。省略即默认 `true`（启用）；仅 `false` 才禁用 Mock 恢复真实数据                                                                       |
| `duration`   | number  | —    | 完整响应时长（毫秒）：mock 的总耗时，绕过真实服务器精确控制，用于测试加载状态、超时等场景                                                           |
| `conditions` | object  | —    | 请求 query/body 字段的**子集匹配**规则；保留字段 `$index` 从 0 开始指定同一场景的调用顺序，不参与请求字段匹配                                       |

### fields 数组元素结构

| 属性    | 类型   | 说明                                                                            |
| ------- | ------ | ------------------------------------------------------------------------------- |
| `path`  | string | 字段路径，支持点号和数组索引。例如 `"data.result.list"`、`"data.items[0].name"` |
| `value` | any    | 要设置的值，可以是任意类型（字符串、数字、布尔、对象、数组等）                  |

### 使用示例

**方式一：完整 Mock 数据**

```json
{
  "apiName": "mtop.cart.query",
  "mockData": {
    "data": {
      "result": {
        "total": 150,
        "items": [{ "id": 1, "name": "商品1", "price": 50 }]
      }
    },
    "ret": ["SUCCESS::调用成功"]
  }
}
```

**方式二：基于真实响应修改字段**

```json
{
  "apiName": "mtop.cart.query",
  "fields": [
    { "path": "data.result.total", "value": 150 },
    { "path": "data.result.items[0].name", "value": "测试商品" }
  ]
}
```

**按入参条件生效（同一接口多条 mock）**

```json
{
  "apiName": "mtop.item.detail",
  "mockData": { "ret": ["SUCCESS::调用成功"], "data": { "title": "缺货商品" } },
  "conditions": { "itemId": "12345" }
}
```

> 仅当请求 query/body 中 `itemId === "12345"` 时返回该 mock；对同一 `apiName` 再设置一条 `conditions: { "itemId": "67890" }` 的 mock，二者可共存、互不覆盖。

**按调用顺序返回**

```json
{
  "apiName": "mtop.order.query",
  "conditions": { "orderId": "12345", "$index": 0 },
  "mockData": { "data": { "state": "processing" } },
  "duration": 10
}
```

再次调用 `set_mock` 并保持相同业务条件、改为 `$index: 1`，即可设置下一次调用的响应。`$index` 只控制调用顺序，不参与请求字段匹配；需要一次安装多条时可使用 `run_actions` 批量执行。

**禁用 Mock**

```json
{
  "apiName": "mtop.cart.query",
  "enabled": false
}
```

### 注意事项

1. **mockData 和 fields 二选一**：如果同时提供，`fields` 优先级更高
2. **大 JSON 用文件引用**：当 `mockData` 很大时，用 `"@/abs/resp.json"` 文件引用（见下方「文件引用」），或用 `--payload-file` 从文件读取整个 payload
3. **Chrome Native Messaging 限制**：单条消息最大 1MB，超过会失败（文件引用解析后仍走同一通道，超限同样失败）
4. **enabled 默认启用**：省略 `enabled` 等价于 `true`；只有显式传 `false` 才会清除该接口的 mock
5. **conditions 子集匹配**：条件按字段子集比对请求的 query 与 body（含 `data` 内层兼容）；同接口多条无条件 mock 会互相覆盖，需多条共存时请给每条都设置 `conditions`

---

## 文件引用：payload 字段从文件读取（通用）

任意 action 的 payload 中，**顶层字段**若是以 `@` 开头的字符串，`@` 之后即为文件路径，发送前会被替换为该文件内容。用于把大体积字段（mock 响应体、`send_request` 的 body、`page_eval` 的 script 等）放到文件里，避免把整段内容塞进调用方上下文。

| 写法                | 说明                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------- |
| `"@/abs/resp.json"` | 读取文件，**默认按 JSON 解析**；解析失败则按原始文本注入（脚本 / HTML / 纯文本 body 等） |

**示例（mock 响应体放文件）**

```json
{
  "apiName": "mtop.cart.query",
  "mockData": "@/abs/path/cart-resp.json"
}
```

```bash
mearl set_mock --payload '{"apiName":"mtop.cart.query","mockData":"@/abs/path/cart-resp.json"}'
```

说明：

- 解析在 client 层统一完成，对 CLI / MCP / SDK 与所有 action 生效。
- **仅作用于顶层字段，不递归嵌套**。
- 路径按运行进程 cwd 解析，**建议用绝对路径**。
- **找不到 / 读不到文件时原样保留该字符串**（不报错），因此 `@xxx` 这类非文件路径的普通值不会被误伤。
- 与 `--payload-file`（整包从文件）正交，可组合使用。

---

## send_mtop_request 参数说明

在当前浏览器页面上下文中发起 mtop API 请求，自动处理签名计算、token 提取等。需要当前页面已登录（有对应的 Cookie）。

| 参数      | 类型   | 必填 | 说明                                                                                       |
| --------- | ------ | ---- | ------------------------------------------------------------------------------------------ |
| `api`     | string | ✅   | mtop API 名称，例如 `"mtop.trade.order.detail"`。以 `"mopen."` 开头的会使用 mopen 签名算法 |
| `data`    | object | —    | 请求数据（JSON 对象），即 mtop 请求中的 data 参数。例如 `{"itemId": "12345"}`              |
| `version` | string | —    | API 版本号，默认 `"1.0"`                                                                   |
| `method`  | string | —    | HTTP 方法，`"GET"`（默认）或 `"POST"`。POST 时 data 参数放在请求体中                       |
| `appKey`  | string | —    | appKey，默认 `"12574478"`                                                                  |
| `env`     | string | —    | 请求环境：`"online"`（默认，线上）/ `"pre"`（预发）。不同环境对应不同的 mtop 网关域名      |
| `timeout` | number | —    | 请求超时时间（毫秒），默认 10000                                                           |

### 环境与域名映射

| `env` 值         | 网关域名                |
| ---------------- | ----------------------- |
| `online`（默认） | `h5api.m.taobao.com`    |
| `pre`            | `h5api.wapa.taobao.com` |

### 签名算法

- **mtop 接口**：`md5(token & timestamp & appKey & data)`，token 从 `_m_h5_tk` Cookie 中提取
- **mopen 接口**（api 以 `mopen.` 开头）：`md5(api & v & timestamp & appKey & token & md5(data))`，token 从 `m_tk` 或 `_tb_token_` Cookie 中提取

### 使用示例

```json
{
  "api": "mtop.trade.order.detail",
  "data": { "orderId": "12345" },
  "version": "1.0",
  "method": "GET"
}
```

**响应结构**：

```json
{
  "success": true,
  "response": {
    "api": "mtop.trade.order.detail",
    "data": { "...": "..." },
    "ret": ["SUCCESS::调用成功"],
    "v": "1.0"
  },
  "requestData": { "orderId": "12345" }
}
```

### 注意事项

1. **需要登录态**：浏览器中需要有对应域名的 Cookie，包含 `_m_h5_tk`（mtop）或 `m_tk`/`_tb_token_`（mopen）
2. **DNR 方式执行**：与 `send_request` 一样，通过 Chrome DNR 规则注入 Cookie 后在 background 中直接 fetch，不依赖页面上下文
3. **与 send_request 的区别**：`send_request` 是通用 HTTP 代理；`send_mtop_request` 专门用于 mtop 协议，自动处理签名

---

## request_domain_permission 参数说明

用于在 `send_request` 因为目标域名未授权而失败时，弹窗向用户申请该域名的访问权限（host permission）。授权成功后，后续 `send_request` 才能携带该域名 Cookie 并访问其接口。

**典型触发场景**：`send_request` 返回 `Cookie access not authorized` / `Permission denied` / `Host permission missing` 等错误，错误信息中通常会直接提示 `Call request_domain_permission with domain="..." to request user authorization, then retry.`

| 参数     | 类型   | 必填 | 说明                                                                                                                                   |
| -------- | ------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `domain` | string | ✅   | 需要授权的**纯主机名**，例如 `"example.com"`、`"atatech.org"`。不要传 URL 或带协议的 origin（内部会自动归一化为 `https://<domain>/*`） |

**响应结构**：

```json
{
  "granted": true,
  "domain": "example.com",
  "origin": "https://example.com/*"
}
```

| 字段      | 类型    | 说明                                                                                                      |
| --------- | ------- | --------------------------------------------------------------------------------------------------------- |
| `granted` | boolean | 用户是否同意授权。`true` = 已授权且 `chrome.permissions.request` 成功；`false` = 用户拒绝、关闭弹窗或超时 |
| `domain`  | string  | 回显请求的 domain                                                                                         |
| `origin`  | string  | 仅 `granted=true` 时返回，已授权的标准 origin（形如 `https://example.com/*`）                             |

### 行为与限制

1. **同步等待用户决定**：调用后会弹出一个独立的小窗口（约 380×230），由用户点"允许/拒绝"，命令会**阻塞等待**用户操作完成。
2. **超时时间 90 秒**：用户超过 90 秒未操作，自动按"拒绝"返回 `granted: false`。
3. **关闭弹窗 = 拒绝**：用户直接关闭弹窗，等价于拒绝。
4. **需要用户手势**：底层依赖 `chrome.permissions.request`，必须由用户在弹窗中点击触发，agent 无法绕过。
5. **常见报错**：
   - `Invalid domain: domain must be a non-empty string` —— 没传 `domain` 或传了空串
   - `Invalid domain format: "xxx". Provide a plain hostname like "example.com".` —— 传了带协议、带路径或非法字符的字符串

### 推荐调用流程（与 `send_request` 配合）

```
1. 调 send_request → 报权限错误，错误信息包含 domain="xxx"
2. 调 request_domain_permission --payload '{"domain":"xxx"}'
3. 若返回 granted=true → 重试原 send_request
4. 若返回 granted=false → 提示用户手动到扩展 Options 页「Agent Service > Domain Permissions」添加授权后再试
```

---

## send_request 参数说明

| 参数           | 类型    | 必填 | 说明                                                                                                                                                                 |
| -------------- | ------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`          | string  | ✅   | 完整的目标 URL（含 http/https）                                                                                                                                      |
| `method`       | string  | —    | HTTP 方法，默认 `GET`，支持 GET/POST/PUT/DELETE/PATCH/HEAD                                                                                                           |
| `headers`      | object  | —    | 自定义请求头（键值对）                                                                                                                                               |
| `params`       | object  | —    | URL 查询参数，自动拼接到 URL                                                                                                                                         |
| `body`         | any     | —    | 请求体。传对象时自动 JSON 序列化并设置 Content-Type: application/json                                                                                                |
| `withCookies`  | boolean | —    | 是否自动附加浏览器 Cookie，默认 `true`                                                                                                                               |
| `cookieDomain` | string  | —    | 指定读取 Cookie 的域名，不填时自动从 url 中提取                                                                                                                      |
| `responseType` | string  | —    | 响应格式：`auto`（默认，自动检测）/`json`/`text`。`auto` 时若 Content-Type 为图片/音视频/PDF/压缩包等二进制类型，body 以 base64 字符串返回，`bodyType` 为 `"base64"` |
| `timeout`      | number  | —    | 超时毫秒数，默认 30000                                                                                                                                               |

**响应结构**：

```json
{
  "status": 200,
  "statusText": "OK",
  "headers": { "content-type": "application/json" },
  "body": { "data": "..." },
  "bodyType": "json",
  "attachedCookieCount": 12
}
```

- `bodyType`：`"json"` | `"text"` | `"base64"`
- **二进制响应（图片/PDF/压缩包等）**：`bodyType` 为 `"base64"`，`body` 为 base64 编码字符串。如需保存文件，可将其 decode 后写入磁盘。

---

## get_requests `source` 参数说明

| `source` 值  | 说明                                     |
| ------------ | ---------------------------------------- |
| 不传         | 默认返回 mtop 请求                       |
| `"mtop"`     | 强制只返回 mtop 接口                     |
| `"requests"` | 强制只返回普通 xhr/fetch 请求（非 mtop） |

---

## get_events 参数说明

用于查询目标 tab 后台缓存的 RUM/aplus/ARMS 上报事件，无需打开 DevTools panel。`tab_open` 新开的页面会从首屏开始采集；既有页面首次查询时才启用采集，需要刷新或再次触发埋点后查询。

| 参数         | 类型    | 必填 | 说明                                                       |
| ------------ | ------- | ---- | ---------------------------------------------------------- |
| `tabId`      | number  | —    | 目标标签页 ID，从 `tab_list` 获取；不传时使用当前激活 tab  |
| `source`     | string  | —    | 数据来源：`"rum"` / `"aplus"` / `"arms"` / `"all"`（默认） |
| `event_type` | string  | —    | 按事件类型过滤，支持正则，如 `"CLK"` `"PV"` `"resource"`   |
| `filter`     | string  | —    | 按 `name` 或 `url` 字段过滤，支持正则                      |
| `since`      | number  | —    | 只返回最近 N 秒内的事件                                    |
| `limit`      | number  | —    | 返回条数，默认 20                                          |
| `includeRaw` | boolean | —    | 返回完整 URL、`_raw` 和 `_context`；默认 `false`           |

**响应结构**：

```json
{
  "meta": {
    "count": 5,
    "totalMatched": 12,
    "totalInBuffer": 80,
    "source": "all",
    "captureStatus": "active",
    "captureSource": "background_collector",
    "includeRaw": false
  },
  "events": [
    {
      "id": "aplus-1-1700000000000",
      "source": "aplus",
      "event_type": "CLK",
      "name": "181.xxx.c.d",
      "url": "https://gm.mmstat.com/aplus.clk",
      "timestamp": 1700000000000,
      "batchTimestampMs": 1700000000000,
      "validation": { "level": "success", "issues": [], "checks": ["..."] }
    }
  ]
}
```

默认响应只保留解析后的事件字段，并移除 tracking URL 的 query。排查原始上报字段时传
`"includeRaw": true`，响应会额外保留完整 URL、`_raw` 和 `_context`。

`captureStatus` 为 `"armed"`（采集已启用但尚无历史）、`"active"`（已有采集历史）或
`"inactive"`（扩展后台未能启用采集）。`captureSource` 为
`"background_collector"`、`"panel"`、`"cdp"` 或 `"none"`；空结果附带 `hint` 时应按提示
刷新页面或重新触发埋点。

---

## page_selected_element 参数说明

用于读取 DevTools Elements 面板当前选中元素的信息，可选返回节点截图。

| 参数                | 类型    | 必填 | 说明                                                                       |
| ------------------- | ------- | ---- | -------------------------------------------------------------------------- |
| `tabId`             | number  | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                              |
| `includeOuterHTML`  | boolean | —    | 是否返回 `outerHTML`（最多 3000 字符），默认 `true`                        |
| `includeScreenshot` | boolean | —    | 是否附带选中元素截图，默认 `false`。开启后会自动滚动到元素并按元素范围裁剪 |

**CLI 选项**：

| 选项              | 说明                                                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `--output <path>` | 将截图保存到本地文件，自动注入 `includeScreenshot: true`，无需手动传 payload。未指定时，命令在 stdout 返回包含 base64 `data` 字段的 JSON。 |

**响应结构（不带截图）**：

```json
{
  "tagName": "div",
  "selector": "body > div.app > main.content",
  "xpath": "/html/body/div/main",
  "rect": { "x": 120, "y": 240, "width": 320, "height": 80 },
  "computedStyle": { "display": "block", "position": "relative" },
  "attributes": { "class": "content" }
}
```

**响应结构（带截图）**：

```json
{
  "tagName": "div",
  "selector": "body > div.app > main.content",
  "rect": { "x": 120, "y": 240, "width": 320, "height": 80 },
  "screenshot": {
    "meta": {
      "format": "png",
      "width": 336,
      "height": 96,
      "size": 18244,
      "url": "https://example.com/page",
      "title": "Example"
    },
    "data": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

---

## page_frames 参数说明

获取当前页面的 frame 树，列出主 frame 和所有 iframe。适用于分析包含 iframe 的页面（如 Storybook、嵌入式组件文档）。

| 参数    | 类型   | 必填 | 说明                                          |
| ------- | ------ | ---- | --------------------------------------------- |
| `tabId` | number | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取） |

**响应结构**：

```json
{
  "frames": [
    { "frameId": "A1B2C3", "url": "https://example.com", "name": "", "isMainFrame": true },
    {
      "frameId": "D4E5F6",
      "url": "https://example.com/iframe-content",
      "name": "preview",
      "isMainFrame": false
    }
  ]
}
```

| 字段          | 说明                                                     |
| ------------- | -------------------------------------------------------- |
| `frameId`     | CDP frame ID，可用于其他 CDP 操作                        |
| `url`         | 该 frame 的 URL                                          |
| `name`        | frame 名称（`<iframe name="...">` 属性），无则为空字符串 |
| `isMainFrame` | 是否为主 frame                                           |

**示例**

```bash
mearl page_frames
mearl page_frames --payload '{"tabId": 12345}'
```

---

## page_snapshot 参数说明

用于首次进入页面、导航完成或增量观察建议回退时获取无障碍树，建立页面结构和 `@ref` 基线。默认获取完整树；长列表、弹层和表单应使用范围参数减少上下文。后续常规交互依赖页面动作内置的观察结果，不要在每次动作后重复获取快照。

| 参数            | 类型    | 必填 | 说明                                                                              |
| --------------- | ------- | ---- | --------------------------------------------------------------------------------- |
| `tabId`         | number  | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                                     |
| `depth`         | number  | —    | 树深度，默认 15，复杂页面可调大                                                   |
| `mode`          | string  | —    | `full`（默认）/ `interactive`（当前视口内的语义控件）/ `viewport`（当前可视区域） |
| `rootSelector`  | string  | —    | 只获取指定 CSS 根元素的 AX 子树，可与 `mode` 组合；与 `rootRef` 互斥              |
| `rootRef`       | string  | —    | 以已有 `@eN` ref 为根获取局部 AX 子树；与 `rootSelector` 互斥                     |
| `ancestorDepth` | number  | —    | `rootRef` 向上扩展的 DOM 祖先层数，默认 0，范围 0–20                              |
| `query`         | object  | —    | 按 `text` / `role` 服务端裁剪 AX 树，只保留命中节点和祖先路径；至少提供一个字段   |
| `query.text`    | string  | —    | 匹配 accessibility name                                                           |
| `query.role`    | string  | —    | 匹配 AX role                                                                      |
| `query.exact`   | boolean | —    | `text` 默认精确匹配；`false` 时按子串匹配                                         |
| `maxNodes`      | number  | —    | 最大输出节点数，超出时保留首尾；`0` 表示不限制                                    |
| `maxChars`      | number  | —    | 最大输出字符数，默认 60000，超出时保留首尾；`0` 表示不限制                        |

**响应结构**：

```json
{
  "url": "https://example.com",
  "title": "Example Page",
  "snapshot": "@e1 [WebArea \"Example Page\"]\n  @e2 [navigation]\n    @e3 [link \"Home\"]\n    @e4 [link \"About\"]\n  @e5 [heading \"Welcome\"] (level=1)\n  @e6 [textbox \"Search\"] (focused)\n  @e7 [button \"Submit\"]",
  "elementCount": 7,
  "outputNodeCount": 7,
  "mode": "full"
}
```

长列表优先调用 `mode: "viewport"`；已知 CSS 根节点时传 `rootSelector`，已有区域 ref 时传 `rootRef`，需要容器上下文时配合 `ancestorDepth`；只查找特定目标时使用 `query`；只需要当前视口内的控件时使用 `mode: "interactive"`。视口内没有暴露 AX 控件语义时，`interactive` 会在同一次调用内回退到 viewport，并返回 `fallbackMode: "viewport"`。发生截断时，输出会同时保留开头和结尾，`truncated` 为 `true`。传 `query` 时响应额外包含结构化 `matches` 和完整的 `matchCount`；为控制传输体积，`matches` 最多返回 100 项，发生裁剪时 `matchesTruncated` 为 `true`。

**@ref 机制**：snapshot 输出中每个元素会带有 `@ref`（如 `@e1`、`@e2`），可直接用作 `page_click`、`page_type`、`page_scroll` 等动作的 `selector` 参数。每次 snapshot 会刷新当前有效 ref 集合，因此局部快照后继续使用该次响应中的新 ref。

---

## page_scroll 参数说明

滚动整个页面或指定的滚动容器。未提供 `selector` 时滚动页面；提供 CSS selector 或 `@ref` 时滚动对应容器。

| 参数              | 类型            | 必填 | 说明                                                               |
| ----------------- | --------------- | ---- | ------------------------------------------------------------------ |
| `tabId`           | number          | ✅   | 目标标签页 ID                                                      |
| `direction`       | string          | ✅   | `up` / `down` / `top` / `bottom`                                   |
| `distance`        | number          | —    | `up` / `down` 的滚动距离，默认 600px                               |
| `selector`        | string          | —    | 目标容器的原生 CSS 选择器或 snapshot `@ref`；不传时滚动整个页面    |
| `containerPolicy` | string          | —    | `self`（默认）要求目标自身可滚动；`nearest` 会使用最近的可滚动祖先 |
| `observe`         | object \| false | —    | 观察选项；传 `false` 仅执行裸滚动                                  |

响应同时返回 `scrollYBefore` / `scrollYAfter`、`moved`、`atTop` / `atBottom`、`maxScrollY`、`resolvedContainer` 和 `ancestorDistance`，可直接判断是否实际滚动、是否到达边界以及最终使用了哪个容器。`scrollY` 保留为 `scrollYAfter` 的兼容别名。

```bash
# 滚动页面
mearl page_scroll --payload '{"tabId":12345,"direction":"down","distance":800}'

# 通过 CSS 选择器滚动容器
mearl page_scroll --payload '{"tabId":12345,"selector":".virtual-list","direction":"bottom"}'

# 通过 snapshot ref 滚动容器
mearl page_scroll --payload '{"tabId":12345,"selector":"@e8","direction":"down"}'

# ref 指向子节点时使用最近的可滚动祖先
mearl page_scroll --payload '{"tabId":12345,"selector":"@e8","containerPolicy":"nearest","direction":"bottom"}'
```

---

## 页面动作的内置观察（observe）

`page_click`、`page_type`、`page_hover`、`page_scroll`、`page_press` 和 `page_upload` 默认内置观察：同一次调用内执行动作、等待异步稳定并返回少量高置信度页面信号，响应结构为 `{ action, observation }`。它不替代 `page_snapshot` 的完整页面结构。传 `observe: false` 可关闭观察，仅执行裸动作并直接返回其结果（适合排障或无需观察的场景）。`page_eval` 默认裸执行，只有显式传入 `observe: {}` 或具体观察选项时才启用同一观察链路。

增量 DOM 信号覆盖主文档，并在 `mode: "delta"` 时返回 `scope: "main-document"`。iframe、Shadow DOM、Canvas 或纯视觉变化需要重新获取局部 snapshot；跨域 iframe 和视觉任务使用 screenshot。

`observe` 字段（对六个页面动作通用，直接放在 payload 顶层）：

| 参数                           | 类型            | 必填 | 说明                                                                                                     |
| ------------------------------ | --------------- | ---- | -------------------------------------------------------------------------------------------------------- |
| `observe`                      | object \| false | —    | 不传使用默认观察；传 `false` 关闭观察，仅执行裸动作                                                      |
| `observe.quietMs`              | number          | —    | 最后一次相关 DOM 变化后的稳定窗口，默认 100ms                                                            |
| `observe.firstChangeTimeoutMs` | number          | —    | 动作后没有 DOM 变化时最多观察多久，默认 500ms                                                            |
| `observe.timeoutMs`            | number          | —    | 整个观察阶段的最大时间，默认 3000ms                                                                      |
| `observe.navigationGraceMs`    | number          | —    | 低信息量点击或按键后等待导航开始的基础宽限，默认 1000ms；仍有网络活动时自动延长，有明确 effects 时不等待 |
| `observe.navigationTimeoutMs`  | number          | —    | 导航开始后等待页面就绪的最大时间，默认 15000ms                                                           |
| `observe.networkIdleMs`        | number          | —    | 文档完成且相关 XHR/Fetch/MTop 请求归零后继续静默的时间，默认 500ms，用于跳过业务骨架屏                   |
| `observe.contentReadyAfterMs`  | number          | —    | 动作开始后启用结构稳定兜底的保护期，默认 5000ms，并自动限制在导航超时之前                                |

**点击示例**：

```bash
mearl page_click --payload '{"tabId":12345,"selector":"@e3"}'
```

**输入示例（自定义观察窗口）**：

```bash
mearl page_type --payload '{"tabId":12345,"selector":"input[name=q]","text":"test query","observe":{"quietMs":150,"timeoutMs":5000}}'
```

**响应结构**：

```json
{
  "action": {
    "name": "page_click",
    "success": true,
    "data": {
      "clicked": true,
      "text": "提交",
      "requestedTarget": { "kind": "ref", "selector": "@e3", "role": "button", "name": "提交" },
      "resolvedTarget": {
        "tag": "button",
        "text": "提交订单",
        "strategy": "actionable-ancestor",
        "distance": 1
      },
      "dispatchTarget": { "tag": "button", "text": "提交订单" }
    }
  },
  "observation": {
    "mode": "delta",
    "scope": "main-document",
    "checkpoint": 2,
    "version": 4,
    "elapsed": 236.5,
    "settledBy": "quiet",
    "url": "https://example.com/results",
    "title": "Search results",
    "changed": true,
    "effects": {
      "notifications": [
        {
          "change": "transient",
          "node": {
            "selector": "#save-toast",
            "tag": "div",
            "role": "status",
            "name": "保存成功"
          },
          "appearedAt": 12.4,
          "disappearedAt": 1512.8,
          "duration": 1500.4
        }
      ],
      "interactives": [
        {
          "change": "appeared",
          "node": {
            "ref": "@e8",
            "selector": "#next-page",
            "tag": "button",
            "role": "button",
            "name": "下一页"
          }
        }
      ]
    },
    "mutationCount": 3,
    "overflow": false,
    "fullSnapshotRecommended": false,
    "snapshotReasons": []
  }
}
```

先检查 `action.success`，再使用 `observation` 决定下一步。`action.success` 只表示动作成功派发；点击结果中的 `requestedTarget` 是请求的 ref/CSS/文本/坐标目标，`resolvedTarget` 是实际解析结果：`strategy` 为 `self`、`actionable-ancestor` 或 `single-child-descendant`，`distance` 是解析层数。`dispatchTarget` 保留实际节点的简要信息：

- `effects.notifications`：只包含 `role=alert/status`、`aria-live`、Toast/Snackbar 等高置信度通知；`change` 为 `appeared` / `updated` / `disappeared` / `transient`。transient 节点已经消失，只读取文案，不要继续点击。
- `effects.interactives`：本次新增、显隐或状态变化的原生/ARIA 可交互控件。节点会尽量返回真实 backend `node.ref`，后续动作优先使用 ref；解析不到 ref 时使用 `node.selector`。
- `effects.focus`：动作后新获得焦点的可交互元素；焦点未变化时省略，同样可能携带可直接操作的 `node.ref`。同一节点不会再重复出现在 `effects.interactives`。
- `changed: true` 但 effects 为空：页面发生了变化，但没有高置信度通知、控件或焦点信号；class 动画等纯表现变化不会因此要求完整快照。
- `fullSnapshotRecommended: true`：根据 `snapshotReasons` 决定是否调用 `page_snapshot`。可能原因包括 `navigation`、`observer-unavailable`、`observation-timeout`、`observation-overflow`、`unclassified-structure` 和 `network-pending`。已经返回 notifications/interactives 时，未分类结构变化仍可能包含未覆盖的页面内容，应按最小范围补充快照。Canvas、跨域 iframe 或视觉任务改用 `page_screenshot`。
- `mode: "unavailable"`：导航或执行上下文重建导致观察器不可用，重新建立页面快照。
- `mode: "navigation"`：动作触发了导航，响应包含 `urlBefore` / `urlAfter` / `title` / `loaded` / `ready` / `settledBy` / `pendingRequests`。`loaded` 表示文档加载完成；`settledBy: "network-idle"` 表示相关请求已静默；长连接持续存在时，`settledBy: "content-stable"` 表示页面已有足量结构化内容、无可见 skeleton/busy 标记且 Mutation 已静默。只有 `ready: true` 时才直接在新页面重建快照。
- `mode: "delta"`：URL 或标题与动作前相同时会省略，发生同页 history/title 变化时仍返回新值。动作触发同页请求时，响应额外包含 `network.ready` / `network.settledBy` / `network.pendingRequests` / `network.elapsed`。网络静默后会重新汇总从动作前 checkpoint 开始的信号。
- `settledBy: "quiet"`：DOM 变化已进入稳定窗口；`no-change` 表示观察期内没有可见变化，不会自动要求 snapshot；`timeout` 会通过 `snapshotReasons` 建议回退。

---

## page_click 参数说明

点击页面元素的动作接口，默认内置观察（见上方「页面动作的内置观察」），传 `observe: false` 仅执行裸点击。定位方式 **三选一**（`selector` / `text` / `point` 必须恰好提供一个）。

| 参数        | 类型            | 必填 | 说明                                                                                                                                      |
| ----------- | --------------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `tabId`     | number          | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                                                                                             |
| `selector`  | string          | △    | CSS 选择器或 `@eN` ref（从 page_snapshot 或页面动作 observation 获取，必须带 `@` 前缀）。不支持 :has-text/:visible 等 Playwright 私有伪类 |
| `text`      | string          | △    | 按可见文本（accessibility name）定位。匹配到多个会报错并列出候选——可配合 `role` / `exact` / `scope` 收敛，或用 `@ref`                     |
| `point`     | `{x, y}`        | △    | 按视口坐标点击（CSS 像素，左上角为原点）。其他方式都不适用的兜底                                                                          |
| `role`      | string          | —    | 配合 `text` 使用，按 AX role 过滤消歧（如 `button`、`link`、`heading`、`StaticText`）                                                     |
| `exact`     | boolean         | —    | 配合 `text` 使用，默认 `true` 精确匹配；`false` 时按子串匹配                                                                              |
| `scope`     | string          | —    | 配合 `text` 使用，把 AX 匹配限制在指定 CSS 元素或 `@eN` ref 子树内                                                                        |
| `clickMode` | string          | —    | `auto`（默认）/ `dom` / `mouse` / `touch`；auto 在可见页按设备模拟状态选择可信输入，在隐藏页使用 DOM fallback                             |
| `observe`   | object \| false | —    | 观察选项；传 `false` 关闭内置观察                                                                                                         |

**多匹配处理**：`text` 命中 ≥2 个元素时不会乱点，会报错并列出前 5 个候选 `role + name`，例如：

```
page_click: text "退款明细" matched 3 elements. Refine with "role" or "exact: true", or run page_snapshot and use an "@eN" ref:
  1. StaticText "退款明细"
  2. button "退款明细 >"
  3. heading "退款明细"
```

**移动端 H5**：`auto` 根据该 tab 的设备模拟配置选择输入方式：桌面页派发完整的可信 mouse 序列，移动模拟页派发可信 touch。未由 Mearl 建立模拟状态时，会结合移动 UA 与 touch 能力识别。checkbox/radio 会返回 `controlState.checkedBefore / checkedAfter`；只有明确需要覆盖默认策略时才传 `clickMode`。

**隐藏页**：Chrome 不可靠地确认隐藏页的 CDP Input。页面因后台标签或最小化窗口而隐藏时，`auto` 会使用 DOM fallback，不切换标签或还原窗口，并返回 `dispatchMode: "dom"`、`fallbackReason: "page-hidden"`。显式 `mouse` / `touch` 会强制尝试可信输入且仍不改变窗口焦点；若浏览器未确认输入，每个 Input 命令的超时上限为 10 秒。确实依赖可信手势时，让目标页可见最可靠。

**返回值**：`dispatchMode` 表示实际使用 `trusted-input` 还是 `dom`；可信输入同时返回 `pointerType: "mouse" | "touch"`。`resolvedTarget` 说明最终命中的 DOM 节点。

---

## page_eval 参数说明

在页面上下文执行 JavaScript 表达式。默认只返回 `{ result }`，不安装页面观察器；结构化快照、文本定位和滚动容器解析无法表达需求时再使用。

| 参数           | 类型    | 必填 | 说明                                                                 |
| -------------- | ------- | ---- | -------------------------------------------------------------------- |
| `tabId`        | number  | ✅   | 目标标签页 ID                                                        |
| `expression`   | string  | ✅   | JavaScript 表达式，支持返回 Promise                                  |
| `frameId`      | string  | —    | 目标 frame ID；不传在主 frame 执行                                   |
| `awaitPromise` | boolean | —    | 是否等待 Promise，默认 `true`                                        |
| `observe`      | object  | —    | 仅当表达式会修改页面且需要变化信号时显式传入，字段与页面动作观察一致 |

```bash
# 读取数据：保持默认裸执行
mearl page_eval --payload '{"tabId":12345,"expression":"document.title"}'

# 修改页面且需要观察结果：显式开启
mearl page_eval --payload '{"tabId":12345,"expression":"document.querySelector(\"#toggle\").click()","observe":{}}'
```

---

## page_type 参数说明

输入内容到页面输入框，默认内置观察（见上方「页面动作的内置观察」），传 `observe: false` 仅执行裸输入。

| 参数         | 类型            | 必填 | 说明                                                                                      |
| ------------ | --------------- | ---- | ----------------------------------------------------------------------------------------- |
| `tabId`      | number          | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                                             |
| `selector`   | string          | ✅   | 元素选择器，支持 CSS 选择器或 `@ref` 格式（从 page_snapshot 或页面动作 observation 获取） |
| `text`       | string          | ✅   | 要填写的文本                                                                              |
| `clearFirst` | boolean         | —    | 是否先清空原有内容，默认 `true`。设为 `false` 时追加文本                                  |
| `observe`    | object \| false | —    | 观察选项；传 `false` 关闭内置观察                                                         |

---

## page_press 参数说明

在页面中按下键盘按键，默认内置观察（见上方「页面动作的内置观察」），传 `observe: false` 仅执行裸按键。

| 参数        | 类型            | 必填 | 说明                                                                                                                   |
| ----------- | --------------- | ---- | ---------------------------------------------------------------------------------------------------------------------- |
| `tabId`     | number          | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                                                                          |
| `key`       | string          | ✅   | 按键名称，支持 Enter/Tab/Escape/Backspace/Delete/ArrowUp/ArrowDown/ArrowLeft/ArrowRight/Home/End/PageUp/PageDown/Space |
| `modifiers` | string[]        | —    | 修饰键数组，支持 ctrl/alt/shift/meta/cmd                                                                               |
| `observe`   | object \| false | —    | 观察选项；传 `false` 关闭内置观察                                                                                      |

---

## page_wait 参数说明

用于没有前置动作的独立等待：等待指定时间、已知元素出现或页面状态成立。动作后的异步稳定判断由页面动作内置的观察完成，不要固定在页面动作后追加等待。

`time`、`selector`、`condition` 必须且只能提供一个。扩展模式与直连 CDP 模式使用相同的参数和响应结构。

| 参数        | 类型   | 必填   | 说明                                                                         |
| ----------- | ------ | ------ | ---------------------------------------------------------------------------- |
| `tabId`     | number | 条件   | `selector` / `condition` 模式的目标标签页 ID；不传时使用当前活动页           |
| `time`      | number | 三选一 | 固定等待毫秒数，范围 0–60000                                                 |
| `selector`  | string | 三选一 | 原生 CSS 选择器，元素出现时结束                                              |
| `condition` | string | 三选一 | 在页面主上下文轮询的 JavaScript 表达式；返回 truthy 时结束，支持返回 Promise |
| `timeout`   | number | —      | `selector` / `condition` 的总超时毫秒数，默认 10000，范围 1–300000           |
| `interval`  | number | —      | 轮询间隔毫秒数，默认 200，范围 50–5000                                       |

成功响应包含 `success: true`、`waited: true`、`elapsed` 和 `mode`；`selector` / `condition` 还会返回命中的 `value`。条件表达式与 `page_eval` 使用相同的域名授权规则。

```bash
mearl page_wait --payload '{"tabId":12345,"condition":"window.appReady === true","timeout":30000,"interval":250}'
```

---

## page_navigate 参数说明

用于在当前标签页内导航到新 URL、刷新当前页面，或沿浏览历史后退/前进。

| 参数      | 类型                  | 必填 | 说明                                                        |
| --------- | --------------------- | ---- | ----------------------------------------------------------- |
| `tabId`   | number                | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）               |
| `url`     | string                | —    | 要导航到的 URL；与 `refresh` / `history` 互斥               |
| `refresh` | boolean               | —    | 为 `true` 时直接重新加载当前页面；与 `url` / `history` 互斥 |
| `history` | `"back" \| "forward"` | —    | 沿当前标签页浏览历史后退或前进；与 `url` / `refresh` 互斥   |

---

## page_upload 参数说明

向 `<input type="file">` 上传文件，默认内置观察（见上方「页面动作的内置观察」），传 `observe: false` 仅执行裸上传。底层通过 CDP `DOM.setFileInputFiles` 实现。

| 参数        | 类型            | 必填 | 说明                                                                                                                           |
| ----------- | --------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------ |
| `tabId`     | number          | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                                                                                  |
| `selector`  | string          | ✅   | 元素选择器，支持 CSS 选择器或 `@ref` 格式（从 page_snapshot 或页面动作 observation 获取），必须指向 `<input type="file">` 元素 |
| `filePaths` | string[]        | ✅   | 本地文件路径数组，如 `["/Users/me/photo.jpg"]`。支持多文件上传                                                                 |
| `observe`   | object \| false | —    | 观察选项；传 `false` 关闭内置观察                                                                                              |

---

## page_screenshot 参数说明

获取当前页面的视觉截图，支持全页截图或指定元素截图（类似 DevTools "Capture node screenshot"）。用于视觉判断、Canvas、跨域 iframe、UI 排查或页面动作观察建议回退的场景，不作为每次动作后的固定步骤。

| 参数       | 类型   | 必填 | 说明                                                                                 |
| ---------- | ------ | ---- | ------------------------------------------------------------------------------------ |
| `tabId`    | number | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                                        |
| `selector` | string | —    | CSS 选择器。提供后只截取该元素区域（会自动滚动元素到可见区域），不提供则截取整个页面 |
| `format`   | string | —    | 图片格式：`"png"`（默认）或 `"jpeg"`                                                 |
| `quality`  | number | —    | JPEG 压缩质量（0-100），仅 format 为 `"jpeg"` 时生效，默认 80                        |

**CLI 选项**：

| 选项              | 说明                                                                                                     |
| ----------------- | -------------------------------------------------------------------------------------------------------- |
| `--output <path>` | 将截图保存到本地文件（推荐用于图片查看）。未指定时，命令会在 stdout 返回包含 base64 `data` 字段的 JSON。 |

**响应结构**：

```json
{
  "meta": {
    "format": "png",
    "width": 320,
    "height": 180,
    "size": 12345,
    "url": "https://example.com",
    "title": "页面标题"
  },
  "data": "<base64 encoded image>"
}
```

> `width`/`height` 为物理像素尺寸（CSS 像素 × devicePixelRatio），与图像实际分辨率一致。

**示例：截取整个页面**

```bash
mearl page_screenshot
```

**示例：保存截图到文件**

```bash
mearl page_screenshot --output ./screenshot.png
```

**示例：截取指定元素**

```bash
mearl page_screenshot --payload '{"selector": ".product-card:first-child"}'
```

**示例：保存指定元素截图到文件**

```bash
mearl page_screenshot --payload '{"selector": ".product-card:first-child"}' --output ./product-card.png
```

---

## tab_open 参数说明

打开或复用标签页。默认行为仍是新建并等待加载完成；需要复用时直接通过 `reuse` 和 `match` 交给 `tab_open` 完成，无需组合出额外的 acquire/release action。

| 参数                  | 类型    | 必填 | 说明                                                                                                                                                                                                                                                                                                    |
| --------------------- | ------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`                 | string  | ✅   | 要打开或匹配的页面 URL                                                                                                                                                                                                                                                                                  |
| `active`              | boolean | —    | 是否激活（前台显示）目标标签页。默认 `false`                                                                                                                                                                                                                                                            |
| `reuse`               | string  | —    | `"never"`（默认）始终新建；`"prefer"` 匹配到则复用、否则新建；`"require"` 只允许复用，找不到时报错                                                                                                                                                                                                      |
| `match`               | object  | —    | 复用匹配规则：`urlPattern` 为支持 `*` 的完整 URL glob；`ignoreSearch` / `ignoreHash` 可忽略查询串或锚点；多匹配默认报错，`onMultiple: "first"` 可显式取第一个                                                                                                                                           |
| `restoreFocusOnClose` | boolean | —    | 新建 active Tab 时记录原活动页，随后用 `tab_close` 关闭该 Tab 后恢复原焦点。默认 `false`；扩展模式显式恢复，直连 CDP 模式依赖浏览器关闭前台 Tab 的原生回退行为                                                                                                                                          |
| `closeExisting`       | boolean | —    | 打开前先关闭 Agent 受控的已有标签页。默认 `false`；不能与复用组合                                                                                                                                                                                                                                       |
| `group`               | string  | —    | 把目标标签页加入指定标题的标签页分组（同窗口同名分组存在则加入，否则新建）。仅扩展模式支持，直连 CDP 模式忽略                                                                                                                                                                                           |
| `emulation`           | object  | —    | 开 tab 即进入移动端模拟态。字段规则与 `set_device_emulation` 完全一致，但**不含 `enabled`**（开 tab 即启用），常用 `{"preset":"iphone-15-pro"}`。只适用于新建 Tab，不能应用到复用 Tab。可用字段：`preset` / `width` / `height` / `deviceScaleFactor` / `mobile` / `userAgent` / `orientation` / `touch` |

**响应结构**（`opened` / `reused` 可用于决定是否应在流程结束时关闭；带 emulation 时额外返回其生效配置）：

```json
{
  "tabId": 12345,
  "url": "https://m.example.com/",
  "title": "示例",
  "opened": true,
  "reused": false,
  "emulation": {
    "preset": "iphone-15-pro",
    "viewport": { "width": 393, "height": 852, "deviceScaleFactor": 3 },
    "userAgent": "Mozilla/5.0 (iPhone; ...) Safari/604.1",
    "mobile": true,
    "touch": true,
    "orientation": "portrait"
  }
}
```

**示例：同一设计文件忽略节点 query，优先复用已打开的 Figma Tab**

```bash
mearl tab_open --payload '{"url":"https://www.figma.com/design/file-key/File?node-id=1-2","active":true,"reuse":"prefer","match":{"urlPattern":"https://www.figma.com/design/file-key/*","ignoreSearch":true,"ignoreHash":true}}'
```

若响应是 `reused: true`，调用方不应把用户原有 Tab 当作临时资源关闭；若是 `opened: true`，可在流程结束后调用 `tab_close`。因此生命周期仍由现有两个 action 覆盖。

**示例：开 tab 即以 iPhone 15 Pro 打开 H5 页面（首屏即移动态）**

```bash
mearl tab_open --payload '{"url":"https://m.example.com","emulation":{"preset":"iphone-15-pro"}}'
```

> 已经打开的 tab 想再切设备，或想清除模拟，用 `set_device_emulation`；开 tab 时就确定用移动态，优先用这里的 `emulation` 参数，省一次 reload。

---

## set_device_emulation 参数说明

把目标标签页切换为移动端模拟态：视口尺寸 / DPR / UA / 触摸事件全部按指定设备生效。底层是 CDP `Emulation.*` 指令，等价于 Chrome DevTools 设备工具栏，作用域仅限该 tab，会话结束（detach 或关闭 tab）自动还原。

适用场景：

- 调试 H5 移动页面，让服务端按移动 UA 返回数据
- 让 `page_click` 在 swiper / better-scroll / fastclick 等只听 `touchstart` 的页面上正确触发交互
- 截图、布局排查时使用真机视口

| 参数                | 类型                      | 必填 | 说明                                                                                                                    |
| ------------------- | ------------------------- | ---- | ----------------------------------------------------------------------------------------------------------------------- |
| `tabId`             | number                    | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                                                                           |
| `enabled`           | boolean                   | ✅   | `true` = 启用模拟，`false` = 清除模拟回到桌面态                                                                         |
| `preset`            | string                    | —    | 内置预设：`iphone-15-pro` / `iphone-se` / `pixel-8` / `ipad-mini` / `galaxy-s23`，一键提供 viewport/DPR/UA              |
| `width`             | number                    | —    | 视口宽度（覆盖 preset）。无 preset 时与 `height` 必须成对提供                                                           |
| `height`            | number                    | —    | 视口高度（覆盖 preset）                                                                                                 |
| `deviceScaleFactor` | number                    | —    | devicePixelRatio（覆盖 preset）                                                                                         |
| `mobile`            | boolean                   | —    | 是否启用移动渲染模式，影响 `hover/pointer` media query 与 viewport meta 行为。默认从 preset 推断，无 preset 默认 `true` |
| `userAgent`         | string                    | —    | 自定义 UA（覆盖 preset）。无 preset 时必填                                                                              |
| `orientation`       | "portrait" \| "landscape" | —    | 横竖屏。`landscape` 会对调 width/height。默认 `portrait`                                                                |
| `touch`             | boolean                   | —    | 是否启用触摸事件并把鼠标事件转成 touch。默认 `mobile === true`                                                          |
| `reload`            | boolean                   | —    | 启用模拟后是否重载页面，让 JS 读到新的 `navigator.userAgent` / `window.innerWidth`。默认 `true`                         |

**内置预设尺寸**：

| preset          | width × height | DPR   | mobile | UA 类型               |
| --------------- | -------------- | ----- | ------ | --------------------- |
| `iphone-15-pro` | 393 × 852      | 3     | true   | iPhone Safari 17      |
| `iphone-se`     | 375 × 667      | 2     | true   | iPhone Safari 16      |
| `pixel-8`       | 412 × 915      | 2.625 | true   | Android Chrome Mobile |
| `ipad-mini`     | 768 × 1024     | 2     | false  | iPadOS desktop Safari |
| `galaxy-s23`    | 360 × 780      | 3     | true   | Android Chrome Mobile |

**响应结构**：

```json
{
  "enabled": true,
  "preset": "iphone-15-pro",
  "viewport": { "width": 393, "height": 852, "deviceScaleFactor": 3 },
  "userAgent": "Mozilla/5.0 (iPhone; ...) Safari/604.1",
  "mobile": true,
  "touch": true,
  "orientation": "portrait",
  "reloaded": true
}
```

`enabled: false` 时只返回 `{ "enabled": false, "reloaded": false }`。

**示例：切到 iPhone 15 Pro**

```bash
mearl set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro"}'
```

**示例：Pixel 8 横屏**

```bash
mearl set_device_emulation --payload '{"enabled":true,"preset":"pixel-8","orientation":"landscape"}'
```

**示例：自定义 viewport + UA**

```bash
mearl set_device_emulation --payload '{"enabled":true,"width":360,"height":640,"deviceScaleFactor":3,"userAgent":"Mozilla/5.0 (Linux; Android 14; CustomPhone) AppleWebKit/537.36 ..."}'
```

**示例：清除模拟**

```bash
mearl set_device_emulation --payload '{"enabled":false}'
```

---

## set_timezone 参数说明

按目标标签页覆盖页面时区。底层使用 CDP `Emulation.setTimezoneOverride`，会立即影响 `Date`、`Intl.DateTimeFormat` 等页面 API，不需要刷新页面。

| 参数       | 类型   | 必填 | 说明                                                                        |
| ---------- | ------ | ---- | --------------------------------------------------------------------------- |
| `tabId`    | number | ✅   | 目标标签页 ID（从 tab_open 或 tab_list 获取）                               |
| `timezone` | string | ✅   | IANA 时区标识，例如 `Asia/Shanghai`、`America/New_York`；传空字符串清除覆盖 |

启用后返回 `{ "enabled": true, "timezone": "America/New_York" }`；清除后返回 `{ "enabled": false, "timezone": null }`。无效时区会直接返回 CDP 校验错误。

```bash
mearl set_timezone --payload '{"tabId":12345,"timezone":"America/New_York"}'
mearl set_timezone --payload '{"tabId":12345,"timezone":""}'
```

---

## run_actions 参数说明

批量顺序执行多个不需要中间判断的原子 action，适合 hover 后立即 click 等紧密连续操作。步骤内的页面动作不带内置观察；遇到第一个失败的步骤立即停止。`actions` 中不能嵌套 `run_actions`；若下一步需要根据页面变化决定，逐步使用带观察的页面动作，不要用本接口固化「点击→等待→截图」循环。

| 参数      | 类型   | 必填 | 说明                                                                   |
| --------- | ------ | ---- | ---------------------------------------------------------------------- |
| `actions` | array  | ✅   | 要依次执行的 action 列表，每项包含 `action`（名称）和 `data`（参数）   |
| `tabId`   | number | ✅   | 所有步骤共享的目标标签页 ID。步骤自身 data 中指定的 `tabId` 优先级更高 |

### actions 数组元素结构

| 属性     | 类型   | 必填 | 说明                                                              |
| -------- | ------ | ---- | ----------------------------------------------------------------- |
| `action` | string | ✅   | action 名称（与单独调用时相同），如 `page_hover`、`page_click` 等 |
| `data`   | object | —    | 该 action 的参数（与单独调用时的参数完全一致）                    |

### 限制

- 最多 50 个步骤
- 不允许嵌套 `run_actions`
- 遇到第一个失败步骤立即停止（stop-on-error）

### 响应结构

```json
{
  "results": [
    { "step": 0, "action": "page_hover", "success": true, "data": { "hovered": true } },
    { "step": 1, "action": "page_click", "success": true, "data": { "clicked": true } }
  ],
  "completedSteps": 2,
  "totalSteps": 2
}
```

**失败时的响应**：

```json
{
  "results": [
    { "step": 0, "action": "page_scroll", "success": true, "data": { "scrollY": 600 } },
    {
      "step": 1,
      "action": "page_click",
      "success": false,
      "error": "Element not found: #nonexistent"
    }
  ],
  "completedSteps": 1,
  "totalSteps": 3,
  "error": "Element not found: #nonexistent",
  "failedStep": 1
}
```
