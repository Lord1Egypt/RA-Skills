# API 参数参考

## set_mock 参数说明

用于动态设置 API 接口的 Mock 数据，支持两种方式：
- **方式一（mockData）**：直接传入完整的 Mock 响应数据，完全替换真实接口返回
- **方式二（fields）**：基于真实响应修改指定字段，适合微调场景

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `apiName` | string | ✅ | API 名称或正则表达式。例如 `"mtop.cart.query"` 精确匹配，`".*\\.cart\\..*"` 匹配所有购物车接口 |
| `mockData` | object | — | **【方式一】** 完整的 Mock 响应数据（JSON 对象）。传入后该接口将完全返回此数据，不再请求真实服务端。与 `fields` 二选一，同时提供时优先使用 `fields` |
| `fields` | array | — | **【方式二】** 基于真实响应修改指定字段。数组元素包含 `path`（字段路径）和 `value`（新值）。会先获取原始响应，然后只修改指定字段 |
| `enabled` | boolean | — | 是否启用 Mock。`true`（默认）：启用 Mock；`false`：禁用 Mock 恢复真实数据 |
| `delay` | number | — | 模拟响应延迟（毫秒），用于测试加载状态、超时等场景 |

### fields 数组元素结构

| 属性 | 类型 | 说明 |
|------|------|------|
| `path` | string | 字段路径，支持点号和数组索引。例如 `"data.result.list"`、`"data.items[0].name"` |
| `value` | any | 要设置的值，可以是任意类型（字符串、数字、布尔、对象、数组等） |

### 使用示例

**方式一：完整 Mock 数据**
```json
{
  "apiName": "mtop.cart.query",
  "mockData": {
    "data": {
      "result": {
        "total": 150,
        "items": [
          {"id": 1, "name": "商品1", "price": 50}
        ]
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
    {"path": "data.result.total", "value": 150},
    {"path": "data.result.items[0].name", "value": "测试商品"}
  ]
}
```

**禁用 Mock**
```json
{
  "apiName": "mtop.cart.query",
  "enabled": false
}
```

### 注意事项

1. **mockData 和 fields 二选一**：如果同时提供，`fields` 优先级更高
2. **大 JSON 支持**：当 `mockData` 很大时，建议使用 `--payload-file` 参数从文件读取
3. **Chrome Native Messaging 限制**：单条消息最大 1MB，超过会失败

---

## send_mtop_request 参数说明

在当前浏览器页面上下文中发起 mtop API 请求，自动处理签名计算、token 提取等。需要当前页面已登录（有对应的 Cookie）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `api` | string | ✅ | mtop API 名称，例如 `"mtop.trade.order.detail"`。以 `"mopen."` 开头的会使用 mopen 签名算法 |
| `data` | object | — | 请求数据（JSON 对象），即 mtop 请求中的 data 参数。例如 `{"itemId": "12345"}` |
| `version` | string | — | API 版本号，默认 `"1.0"` |
| `method` | string | — | HTTP 方法，`"GET"`（默认）或 `"POST"`。POST 时 data 参数放在请求体中 |
| `appKey` | string | — | appKey，默认 `"12574478"` |
| `env` | string | — | 请求环境：`"online"`（默认，线上）/ `"pre"`（预发）。不同环境对应不同的 mtop 网关域名 |
| `timeout` | number | — | 请求超时时间（毫秒），默认 10000 |

### 环境与域名映射

| `env` 值 | 网关域名 |
|---|---|
| `online`（默认） | `h5api.m.taobao.com` |
| `pre` | `h5api.wapa.taobao.com` |

### 签名算法

- **mtop 接口**：`md5(token & timestamp & appKey & data)`，token 从 `_m_h5_tk` Cookie 中提取
- **mopen 接口**（api 以 `mopen.` 开头）：`md5(api & v & timestamp & appKey & token & md5(data))`，token 从 `m_tk` 或 `_tb_token_` Cookie 中提取

### 使用示例

```json
{
  "api": "mtop.trade.order.detail",
  "data": {"orderId": "12345"},
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
  "requestData": {"orderId": "12345"}
}
```

### 注意事项

1. **需要登录态**：浏览器中需要有对应域名的 Cookie，包含 `_m_h5_tk`（mtop）或 `m_tk`/`_tb_token_`（mopen）
2. **DNR 方式执行**：与 `proxy_request` 一样，通过 Chrome DNR 规则注入 Cookie 后在 background 中直接 fetch，不依赖页面上下文
3. **与 proxy_request 的区别**：`proxy_request` 是通用 HTTP 代理；`send_mtop_request` 专门用于 mtop 协议，自动处理签名

---

## request_domain_permission 参数说明

用于在 `proxy_request` 因为目标域名未授权而失败时，弹窗向用户申请该域名的访问权限（host permission）。授权成功后，后续 `proxy_request` 才能携带该域名 Cookie 并访问其接口。

**典型触发场景**：`proxy_request` 返回 `Cookie access not authorized` / `Permission denied` / `Host permission missing` 等错误，错误信息中通常会直接提示 `Call request_domain_permission with domain="..." to request user authorization, then retry.`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `domain` | string | ✅ | 需要授权的**纯主机名**，例如 `"example.com"`、`"atatech.org"`。不要传 URL 或带协议的 origin（内部会自动归一化为 `https://<domain>/*`） |

**响应结构**：

```json
{
  "granted": true,
  "domain": "example.com",
  "origin": "https://example.com/*"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `granted` | boolean | 用户是否同意授权。`true` = 已授权且 `chrome.permissions.request` 成功；`false` = 用户拒绝、关闭弹窗或超时 |
| `domain` | string | 回显请求的 domain |
| `origin` | string | 仅 `granted=true` 时返回，已授权的标准 origin（形如 `https://example.com/*`） |

### 行为与限制

1. **同步等待用户决定**：调用后会弹出一个独立的小窗口（约 380×230），由用户点"允许/拒绝"，命令会**阻塞等待**用户操作完成。
2. **超时时间 90 秒**：用户超过 90 秒未操作，自动按"拒绝"返回 `granted: false`。
3. **关闭弹窗 = 拒绝**：用户直接关闭弹窗，等价于拒绝。
4. **需要用户手势**：底层依赖 `chrome.permissions.request`，必须由用户在弹窗中点击触发，agent 无法绕过。
5. **常见报错**：
   - `Invalid domain: domain must be a non-empty string` —— 没传 `domain` 或传了空串
   - `Invalid domain format: "xxx". Provide a plain hostname like "example.com".` —— 传了带协议、带路径或非法字符的字符串

### 推荐调用流程（与 `proxy_request` 配合）

```
1. 调 proxy_request → 报权限错误，错误信息包含 domain="xxx"
2. 调 request_domain_permission --payload '{"domain":"xxx"}'
3. 若返回 granted=true → 重试原 proxy_request
4. 若返回 granted=false → 提示用户手动到扩展 Options 页「Agent Service > Domain Permissions」添加授权后再试
```

---

## proxy_request 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 完整的目标 URL（含 http/https） |
| `method` | string | — | HTTP 方法，默认 `GET`，支持 GET/POST/PUT/DELETE/PATCH/HEAD |
| `headers` | object | — | 自定义请求头（键值对） |
| `params` | object | — | URL 查询参数，自动拼接到 URL |
| `body` | any | — | 请求体。传对象时自动 JSON 序列化并设置 Content-Type: application/json |
| `withCookies` | boolean | — | 是否自动附加浏览器 Cookie，默认 `true` |
| `cookieDomain` | string | — | 指定读取 Cookie 的域名，不填时自动从 url 中提取 |
| `responseType` | string | — | 响应格式：`auto`（默认，自动检测）/`json`/`text`。`auto` 时若 Content-Type 为图片/音视频/PDF/压缩包等二进制类型，body 以 base64 字符串返回，`bodyType` 为 `"base64"` |
| `timeout` | number | — | 超时毫秒数，默认 30000 |

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

| `source` 值 | 说明 |
|---|---|
| 不传 | 使用 panel 当前模式（推荐默认用法） |
| `"mtop"` | 强制只返回 mtop 接口 |
| `"requests"` | 强制只返回普通 xhr/fetch 请求（非 mtop） |

---

## get_events 参数说明

用于查询面板"埋点验证"（RUM/aplus）模块缓存的上报事件。**需要先在 DevTools 中切换到埋点验证视图以启用采集。**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source` | string | — | 数据来源：`"rum"`（阿里云 RUM）/ `"aplus"`（aplus 埋点）/ `"all"`（默认） |
| `event_type` | string | — | 按事件类型过滤，支持正则，如 `"CLK"` `"PV"` `"resource"` |
| `filter` | string | — | 按 `name` 或 `url` 字段过滤，支持正则 |
| `since` | number | — | 只返回最近 N 秒内的事件 |
| `limit` | number | — | 返回条数，默认 20 |

**响应结构**：
```json
{
  "meta": { "count": 5, "totalMatched": 12, "totalInBuffer": 80, "source": "all" },
  "events": [
    {
      "id": "aplus-1-1700000000000",
      "source": "aplus",
      "event_type": "CLK",
      "name": "181.xxx.c.d",
      "url": "https://...",
      "timestamp": 1700000000000,
      "batchTimestampMs": 1700000000000,
      "validation": { "level": "success", "issues": [], "checks": ["..."] },
      "_raw": { "gmkey": "CLK", "gokey_params": {} },
      "_context": { "view": { "spm-url": "..." } }
    }
  ]
}
```

---

## get_selected_element 参数说明

用于读取 DevTools Elements 面板当前选中元素的信息，可选返回节点截图。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `includeOuterHTML` | boolean | — | 是否返回 `outerHTML`（最多 3000 字符），默认 `true` |
| `includeScreenshot` | boolean | — | 是否附带选中元素截图，默认 `false`。开启后会自动滚动到元素并按元素范围裁剪 |

**CLI 选项**：

| 选项 | 说明 |
|------|------|
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

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |

**响应结构**：
```json
{
  "frames": [
    { "frameId": "A1B2C3", "url": "https://example.com", "name": "", "isMainFrame": true },
    { "frameId": "D4E5F6", "url": "https://example.com/iframe-content", "name": "preview", "isMainFrame": false }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `frameId` | CDP frame ID，可用于其他 CDP 操作 |
| `url` | 该 frame 的 URL |
| `name` | frame 名称（`<iframe name="...">` 属性），无则为空字符串 |
| `isMainFrame` | 是否为主 frame |

**示例**
```bash
mtop-devtools page_frames
mtop-devtools page_frames --payload '{"tabId": 12345}'
```

---

## page_snapshot 参数说明

用于获取当前页面的无障碍树快照，感知页面结构以决定下一步操作。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `depth` | number | — | 树深度，默认 15，复杂页面可调大 |

**响应结构**：
```json
{
  "url": "https://example.com",
  "title": "Example Page",
  "snapshot": "@e1 [WebArea \"Example Page\"]\n  @e2 [navigation]\n    @e3 [link \"Home\"]\n    @e4 [link \"About\"]\n  @e5 [heading \"Welcome\"] (level=1)\n  @e6 [textbox \"Search\"] (focused)\n  @e7 [button \"Submit\"]",
  "elementCount": 7
}
```

**@ref 机制**：snapshot 输出中每个元素会带有 `@ref`（如 `@e1`、`@e2`），可以直接用于 `page_click` 和 `page_type` 的 `selector` 参数。

---

## page_click 参数说明

定位方式 **三选一**（`selector` / `text` / `point` 必须恰好提供一个），默认走 CDP 真实 mouse/touch 事件，对依赖 `touchend`、`pointerdown` 的移动端 H5 组件可靠。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `selector` | string | △ | CSS 选择器或 `@eN` snapshot ref（从 page_snapshot 获取，必须带 `@` 前缀）。不支持 :has-text/:visible 等 Playwright 私有伪类 |
| `text` | string | △ | 按可见文本（accessibility name）定位。匹配到多个会报错并列出候选——可配合 `role` / `exact` 收敛，或用 `@ref` |
| `point` | `{x, y}` | △ | 按视口坐标点击（CSS 像素，左上角为原点）。其他方式都不适用的兜底 |
| `role` | string | — | 配合 `text` 使用，按 AX role 过滤消歧（如 `button`、`link`、`heading`、`StaticText`） |
| `exact` | boolean | — | 配合 `text` 使用，默认 `true` 精确匹配；`false` 时按子串匹配 |
| `clickType` | string | — | 点击方式：`cdp`（默认，真实 mouse/touch 事件）/ `js`（el.click() 兜底，仅对 selector/@ref 生效；`text` 和 `point` 始终走 cdp） |

**多匹配处理**：`text` 命中 ≥2 个元素时不会乱点，会报错并列出前 5 个候选 `role + name`，例如：
```
page_click: text "退款明细" matched 3 elements. Refine with "role" or "exact: true", or run page_snapshot and use an "@eN" ref:
  1. StaticText "退款明细"
  2. button "退款明细 >"
  3. heading "退款明细"
```

**移动端 H5 行为变更**：旧版本走 `el.click()`，对挂在 `touchend` 上的 vue/rax 组件不触发；新版本默认派发真实 touch 事件（在 device emulation 触屏模式下自动检测）。如遇极少数页面对真实事件反应异常，可显式 `clickType: "js"` 回退。

---

## page_type 参数说明

用于向输入框填写文本。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `selector` | string | ✅ | 元素选择器，支持 CSS 选择器或 `@ref` 格式（从 page_snapshot 获取） |
| `text` | string | ✅ | 要填写的文本 |
| `clearFirst` | boolean | — | 是否先清空原有内容，默认 `true`。设为 `false` 时追加文本 |

---

## page_press 参数说明

用于在页面中按下键盘按键。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `key` | string | ✅ | 按键名称，支持 Enter/Tab/Escape/Backspace/Delete/ArrowUp/ArrowDown/ArrowLeft/ArrowRight/Home/End/PageUp/PageDown/Space |
| `modifiers` | string[] | — | 修饰键数组，支持 ctrl/alt/shift/meta/cmd |

---

## page_wait 参数说明

用于等待指定时间或等待某个元素出现。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `time` | number | — | 等待毫秒数，与 `selector` 二选一 |
| `selector` | string | — | CSS 选择器，等待元素出现，与 `time` 二选一 |
| `timeout` | number | — | 等待超时时间（毫秒），默认 10000 |

---

## page_navigate 参数说明

用于在当前标签页内导航到新 URL。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `url` | string | ✅ | 要导航到的 URL |

---

## page_upload 参数说明

用于向页面上的 `<input type="file">` 元素上传文件。通过 CDP `DOM.setFileInputFiles` 实现。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `selector` | string | ✅ | 元素选择器，支持 CSS 选择器或 `@ref` 格式（从 page_snapshot 获取），必须指向 `<input type="file">` 元素 |
| `filePaths` | string[] | ✅ | 本地文件路径数组，如 `["/Users/me/photo.jpg"]`。支持多文件上传 |

---

## get_screenshot 参数说明

获取当前页面截图，支持全页截图或指定元素截图（类似 DevTools "Capture node screenshot"）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `selector` | string | — | CSS 选择器。提供后只截取该元素区域（会自动滚动元素到可见区域），不提供则截取整个页面 |
| `format` | string | — | 图片格式：`"png"`（默认）或 `"jpeg"` |
| `quality` | number | — | JPEG 压缩质量（0-100），仅 format 为 `"jpeg"` 时生效，默认 80 |

**CLI 选项**：

| 选项 | 说明 |
|------|------|
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
mtop-devtools get_screenshot
```

**示例：保存截图到文件**
```bash
mtop-devtools get_screenshot --output ./screenshot.png
```

**示例：截取指定元素**
```bash
mtop-devtools get_screenshot --payload '{"selector": ".product-card:first-child"}'
```

**示例：保存指定元素截图到文件**
```bash
mtop-devtools get_screenshot --payload '{"selector": ".product-card:first-child"}' --output ./product-card.png
```

---

## set_device_emulation 参数说明

把目标标签页切换为移动端模拟态：视口尺寸 / DPR / UA / 触摸事件全部按指定设备生效。底层是 CDP `Emulation.*` 指令，等价于 Chrome DevTools 设备工具栏，作用域仅限该 tab，会话结束（detach 或关闭 tab）自动还原。

适用场景：
- 调试 H5 移动页面，让服务端按移动 UA 返回数据
- 让 `page_click` 在 swiper / better-scroll / fastclick 等只听 `touchstart` 的页面上正确触发交互
- 截图、布局排查时使用真机视口

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tabId` | number | — | 目标标签页 ID，不填时使用当前激活标签页 |
| `enabled` | boolean | ✅ | `true` = 启用模拟，`false` = 清除模拟回到桌面态 |
| `preset` | string | — | 内置预设：`iphone-15-pro` / `iphone-se` / `pixel-8` / `ipad-mini` / `galaxy-s23`，一键提供 viewport/DPR/UA |
| `width` | number | — | 视口宽度（覆盖 preset）。无 preset 时与 `height` 必须成对提供 |
| `height` | number | — | 视口高度（覆盖 preset） |
| `deviceScaleFactor` | number | — | devicePixelRatio（覆盖 preset） |
| `mobile` | boolean | — | 是否启用移动渲染模式，影响 `hover/pointer` media query 与 viewport meta 行为。默认从 preset 推断，无 preset 默认 `true` |
| `userAgent` | string | — | 自定义 UA（覆盖 preset）。无 preset 时必填 |
| `orientation` | "portrait" \| "landscape" | — | 横竖屏。`landscape` 会对调 width/height。默认 `portrait` |
| `touch` | boolean | — | 是否启用触摸事件并把鼠标事件转成 touch。默认 `mobile === true` |
| `reload` | boolean | — | 启用模拟后是否重载页面，让 JS 读到新的 `navigator.userAgent` / `window.innerWidth`。默认 `true` |

**内置预设尺寸**：

| preset | width × height | DPR | mobile | UA 类型 |
|---|---|---|---|---|
| `iphone-15-pro` | 393 × 852 | 3 | true | iPhone Safari 17 |
| `iphone-se` | 375 × 667 | 2 | true | iPhone Safari 16 |
| `pixel-8` | 412 × 915 | 2.625 | true | Android Chrome Mobile |
| `ipad-mini` | 768 × 1024 | 2 | false | iPadOS desktop Safari |
| `galaxy-s23` | 360 × 780 | 3 | true | Android Chrome Mobile |

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
mtop-devtools set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro"}'
```

**示例：Pixel 8 横屏**
```bash
mtop-devtools set_device_emulation --payload '{"enabled":true,"preset":"pixel-8","orientation":"landscape"}'
```

**示例：自定义 viewport + UA**
```bash
mtop-devtools set_device_emulation --payload '{"enabled":true,"width":360,"height":640,"deviceScaleFactor":3,"userAgent":"Mozilla/5.0 (Linux; Android 14; CustomPhone) AppleWebKit/537.36 ..."}'
```

**示例：清除模拟**
```bash
mtop-devtools set_device_emulation --payload '{"enabled":false}'
```

---

## run_actions 参数说明

批量顺序执行多个 action，一次调用完成「滚动→等待→点击→截图」等组合流程。遇到第一个失败的步骤立即停止，返回已完成步骤的结果。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `actions` | array | ✅ | 要依次执行的 action 列表，每项包含 `action`（名称）和 `data`（参数） |
| `tabId` | number | — | 所有步骤共享的目标标签页 ID。步骤自身 data 中指定的 `tabId` 优先级更高 |

### actions 数组元素结构

| 属性 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | ✅ | action 名称（与单独调用时相同），如 `page_scroll`、`page_click`、`get_screenshot`、`page_wait` 等 |
| `data` | object | — | 该 action 的参数（与单独调用时的参数完全一致） |

### 限制

- 最多 50 个步骤
- 不允许嵌套 `run_actions`
- 遇到第一个失败步骤立即停止（stop-on-error）

### 响应结构

```json
{
  "results": [
    { "step": 0, "action": "page_scroll", "success": true, "data": { "scrollY": 600, "scrollHeight": 3000 } },
    { "step": 1, "action": "page_wait", "success": true, "data": { "waited": true, "elapsed": 500 } },
    { "step": 2, "action": "get_screenshot", "success": true, "data": { "meta": { "format": "png", "width": 1280, "height": 720 }, "data": "iVBORw0..." } }
  ],
  "completedSteps": 3,
  "totalSteps": 3
}
```

**失败时的响应**：
```json
{
  "results": [
    { "step": 0, "action": "page_scroll", "success": true, "data": { "scrollY": 600 } },
    { "step": 1, "action": "page_click", "success": false, "error": "Element not found: #nonexistent" }
  ],
  "completedSteps": 1,
  "totalSteps": 3,
  "error": "Element not found: #nonexistent",
  "failedStep": 1
}
```

---

## get_user_info 参数说明

获取当前登录用户的信息。默认只返回工号，设置 `detail` 为 `true` 时返回完整的用户信息。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `detail` | boolean | — | 是否获取完整用户信息。默认 `false`（只返回工号）；设置为 `true` 时返回姓名、花名、部门、BU 等详细信息 |

**响应结构（detail=false）**：
```json
{
  "userId": "123456"
}
```

**响应结构（detail=true）**：
```json
{
  "userId": "123456",
  "detail": {
    "empId": "123456",
    "bucUserId": "789012",
    "name": "张三",
    "displayName": "张三(花名)",
    "nickName": "花名",
    "deptId": "A1234",
    "deptDesc": "某某事业部-某某技术部",
    "buName": "某某事业部",
    "buNo": "12345",
    "empType": "P",
    "admin": false,
    "photoPath": "TFS_TO_OSS/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "lang": "zh-CN",
    "cid": "C1234"
  }
}
```

**字段说明**：

| 字段 | 说明 |
|------|------|
| `userId` / `empId` | 工号 |
| `bucUserId` | BUC 用户 ID |
| `name` | 姓名 |
| `displayName` | 显示名称（姓名+花名） |
| `nickName` | 花名 |
| `deptId` | 部门 ID |
| `deptDesc` | 部门完整路径 |
| `buName` | BU 名称 |
| `buNo` | BU 编号 |
| `empType` | 员工类型 |
| `admin` | 是否管理员 |
| `photoPath` | 头像路径 |
| `lang` | 语言偏好 |
| `cid` | CID |

**示例：获取工号**
```bash
mtop-devtools get_user_info
```

**示例：获取完整用户信息**
```bash
mtop-devtools get_user_info --payload '{"detail": true}'
```

---

## tdbank_account 参数说明

TDBank 账号操作入口。支持获取当前账号、账号列表、切换账号、快速借用并切换账号。需要浏览器已登录 `tdbank.alibaba-inc.com`。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `operation` | `"current" \| "list" \| "switch" \| "borrow"` | — | 操作类型，默认 `list` |
| `refresh` | boolean | — | `list` 时是否强制刷新账号列表，默认 `false` |
| `pageIndex` | number | — | `list` 时的页码，默认 `1` |
| `accountId` | string/number | 条件必填 | `switch` 时使用账号列表中的 `id` |
| `havanaId` | string/number | 条件必填 | `switch` 时可直接指定账号 Havana ID；需同时传 `site` |
| `site` | string/number | 条件必填 | 直接指定 `havanaId` 时必填 |
| `query` | string | 条件必填 | `borrow` 时输入要借用的账号 loginId 或关键词 |
| `tabId` | number | — | CDP 模式下可指定用于读取 Cookie 的标签页 ID |

**示例：获取当前账号**
```bash
mtop-devtools tdbank_account --payload '{"operation":"current"}'
```

**示例：刷新账号列表**
```bash
mtop-devtools tdbank_account --payload '{"operation":"list","refresh":true}'
```

**示例：切换账号**
```bash
mtop-devtools tdbank_account --payload '{"operation":"switch","accountId":12345}'
```

**示例：快速借用并切换**
```bash
mtop-devtools tdbank_account --payload '{"operation":"borrow","query":"test_account"}'
```
