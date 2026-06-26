# 使用示例

## API 调试

```bash
# 获取最近请求（默认返回 panel 当前模式的数据）
mtop-devtools get_requests --payload '{"count": 5}'

# 强制指定获取 mtop 请求
mtop-devtools get_requests --payload '{"count": 5, "source": "mtop"}'

# 强制指定获取普通 HTTP 请求（xhr/fetch，非 mtop）
mtop-devtools get_requests --payload '{"count": 10, "source": "requests"}'

# 获取 error 日志
mtop-devtools get_logs --payload '{"level": "error", "limit": 50}'

# 获取最近 20 条 RUM/aplus 埋点事件
mtop-devtools get_events --payload '{"limit": 20}'

# 只看 aplus 埋点事件
mtop-devtools get_events --payload '{"source": "aplus", "limit": 20}'

# 按事件类型过滤（正则）
mtop-devtools get_events --payload '{"event_type": "CLK", "source": "aplus"}'

# 过滤特定 name/url（正则）
mtop-devtools get_events --payload '{"filter": "cart|order", "limit": 10}'

# 获取 API schema
mtop-devtools get_api_schema --payload '{"api": "mtop.fliggy.flyrs.render", "version": "1.0"}'

# 只获取 HSF 接口信息（服务名、方法、版本）
mtop-devtools get_api_schema --payload '{"api": "mtop.fliggy.flyrs.render", "fields": ["hsf"]}'

# 只获取请求参数 JSON Schema
mtop-devtools get_api_schema --payload '{"api": "mtop.fliggy.flyrs.render", "fields": ["schema"]}'
```

## Mock & 请求规则

```bash
# 按字段修改 API 响应（mock）
mtop-devtools set_mock --payload '{"apiName": "mtop.cart.query", "fields": [{"path": "data.total", "value": 150}], "enabled": true}'

# 查看所有 mock 配置
mtop-devtools get_mocks --payload '{}'

# 添加请求重定向规则（将 h5api.m.taobao.com 请求重定向到本地服务）
mtop-devtools add_rule --payload '{"actionType": "redirect", "filter": "^https://h5api\\.m\\.taobao\\.com/.*", "redirectUrl": "http://localhost:3000/$&", "description": "Redirect to local dev server"}'

# 添加请求头修改规则（给所有 mtop 请求添加自定义头）
mtop-devtools add_rule --payload '{"actionType": "modifyHeaders", "filter": "^https://h5api\\..*\\.taobao\\.com/", "requestHeaders": [{"header": "x-custom-token", "operation": "set", "value": "test-token-123"}]}'

# 添加请求拦截规则（阻止特定域名的请求）
mtop-devtools add_rule --payload '{"actionType": "block", "filter": "^https://ads\\.example\\.com/.*", "description": "Block ads"}'
```

## 网络请求代理

```bash
# 代理 GET 请求，自动携带 Cookie
mtop-devtools proxy_request --payload '{"url": "https://api.example.com/data", "method": "GET"}'

# 代理 POST 请求，自动携带 Cookie，发送 JSON body
mtop-devtools proxy_request --payload '{"url": "https://api.example.com/submit", "method": "POST", "body": {"key": "value"}, "withCookies": true}'

# 代理请求，指定自定义请求头
mtop-devtools proxy_request --payload '{"url": "https://api.example.com/data", "headers": {"X-Custom-Token": "abc123"}, "params": {"page": "1", "size": "20"}}'

# 发起 mtop GET 请求（自动签名、自动携带 token）
mtop-devtools send_mtop_request --payload '{"api": "mtop.trade.order.detail", "data": {"orderId": "12345"}}'

# 发起 mtop POST 请求，指定版本号
mtop-devtools send_mtop_request --payload '{"api": "mtop.trade.order.create", "data": {"itemId": "67890", "quantity": 1}, "method": "POST", "version": "2.0"}'

# 发起 mopen 请求（api 以 mopen. 开头，自动使用 mopen 签名算法）
mtop-devtools send_mtop_request --payload '{"api": "mopen.trade.order.query", "data": {"status": "paid"}}'

# 发起预发环境的 mtop 请求（h5api.wapa.taobao.com）
mtop-devtools send_mtop_request --payload '{"api": "mtop.trade.order.detail", "data": {"orderId": "12345"}, "env": "pre"}'

# 申请目标域名的访问权限（弹窗等待用户授权，granted=true 后再重试 proxy_request）
mtop-devtools request_domain_permission --payload '{"domain": "example.com"}'
```

## 浏览器操作

```bash
# 打开新标签页（后台打开，等待加载完成后返回 tabId）
mtop-devtools tab_open --payload '{"url": "https://example.com"}'

# 打开新标签页并激活（前台显示）
mtop-devtools tab_open --payload '{"url": "https://example.com", "active": true}'

# 列出当前窗口所有标签页
mtop-devtools tab_list --payload '{}'

# 关闭指定标签页
mtop-devtools tab_close --payload '{"tabId": 12345}'

# 按可见文本点击（推荐——一步到位，不需要先 snapshot）
mtop-devtools page_click --payload '{"text": "提交"}'

# 文本多匹配时用 role 消歧
mtop-devtools page_click --payload '{"text": "退款明细", "role": "button"}'

# CSS 选择器（默认 CDP 真实事件，移动端 H5 触摸组件也可靠）
mtop-devtools page_click --payload '{"selector": "button.submit"}'

# snapshot ref（先 page_snapshot 拿 @eN，再点击）
mtop-devtools page_click --payload '{"selector": "@e3"}'

# 显式回退到 el.click()（少数页面对真实事件反应异常时使用）
mtop-devtools page_click --payload '{"selector": ".legacy-btn", "clickType": "js"}'

# 按视口坐标点击（前两种都不适用的兜底）
mtop-devtools page_click --payload '{"point": {"x": 336, "y": 117}}'

# 在指定 Tab 上点击元素
mtop-devtools page_click --payload '{"tabId": 12345, "selector": "#login-btn"}'

# 向输入框填写文本（自动清空原有内容）
mtop-devtools page_type --payload '{"selector": "input[name=username]", "text": "test_user"}'

# 向输入框追加文本（不清空原有内容）
mtop-devtools page_type --payload '{"selector": "textarea.comment", "text": "追加内容", "clearFirst": false}'

# 滚动到页面底部
mtop-devtools page_scroll --payload '{"direction": "bottom"}'

# 向下滚动 800px
mtop-devtools page_scroll --payload '{"direction": "down", "distance": 800}'

# 滚动到页面顶部
mtop-devtools page_scroll --payload '{"direction": "top"}'

# 在页面上下文中执行 JavaScript
mtop-devtools page_eval --payload '{"expression": "document.title"}'

# 在指定 Tab 上执行 JavaScript
mtop-devtools page_eval --payload '{"tabId": 12345, "expression": "document.querySelectorAll(\"a\").length"}'

# 按 Enter 键
mtop-devtools page_press --payload '{"key": "Enter"}'

# 按 Ctrl+Space
mtop-devtools page_press --payload '{"key": "Space", "modifiers": ["ctrl"]}'

# 等待 2 秒
mtop-devtools page_wait --payload '{"time": 2000}'

# 等待元素出现
mtop-devtools page_wait --payload '{"selector": ".result-list", "timeout": 5000}'

# 在当前标签页导航
mtop-devtools page_navigate --payload '{"url": "https://example.com"}'

# 上传单个文件
mtop-devtools page_upload --payload '{"selector": "input[type=file]", "filePaths": ["/Users/me/photo.jpg"]}'

# 上传多个文件
mtop-devtools page_upload --payload '{"selector": "#file-input", "filePaths": ["/tmp/a.png", "/tmp/b.pdf"]}'

# 使用 @ref 引用上传（从 page_snapshot 获取）
mtop-devtools page_upload --payload '{"selector": "@e5", "filePaths": ["/Users/me/doc.pdf"]}'
```

## 页面感知

```bash
# 获取当前页面的无障碍树快照（感知页面结构，决定下一步操作）
mtop-devtools page_snapshot --payload '{}'

# 获取指定 Tab 的页面快照
mtop-devtools page_snapshot --payload '{"tabId": 12345}'

# 控制树深度（默认 15，复杂页面可调大）
mtop-devtools page_snapshot --payload '{"depth": 20}'

# 获取当前页面截图（PNG 格式）
mtop-devtools get_screenshot --payload '{"format": "png"}'

# 获取当前页面截图（JPEG 格式，质量 90）
mtop-devtools get_screenshot --payload '{"format": "jpeg", "quality": 90}'

# 保存截图到文件（推荐方式，无需手动处理 base64）
mtop-devtools get_screenshot --output ./screenshot.png

# 保存 JPEG 截图到文件
mtop-devtools get_screenshot --payload '{"format": "jpeg", "quality": 80}' --output ./screenshot.jpg

# 获取 Elements 面板当前选中元素的详细信息（含布局、样式、属性）
mtop-devtools get_selected_element --payload '{}'

# 不含 outerHTML（减少数据量，适合只看布局和样式）
mtop-devtools get_selected_element --payload '{"includeOuterHTML": false}'

# 获取选中元素信息 + 节点截图（自动滚动并按元素裁剪）
mtop-devtools get_selected_element --payload '{"includeScreenshot": true}'
```

## 移动端模拟

```bash
# 一键切到 iPhone 15 Pro 调试 H5 移动页面（自动 reload 让页面以移动模式重新初始化）
mtop-devtools set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro"}'

# 切到 Pixel 8
mtop-devtools set_device_emulation --payload '{"enabled":true,"preset":"pixel-8"}'

# 横屏调试
mtop-devtools set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro","orientation":"landscape"}'

# 仅改 viewport 不重载（保留当前页面状态，只看 CSS 响应式）
mtop-devtools set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro","reload":false}'

# 自定义 viewport + UA（无 preset 时 width/height/userAgent 必填）
mtop-devtools set_device_emulation --payload '{"enabled":true,"width":360,"height":640,"deviceScaleFactor":3,"userAgent":"Mozilla/5.0 (Linux; Android 14; CustomDevice) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"}'

# 清除移动模拟，回到桌面态
mtop-devtools set_device_emulation --payload '{"enabled":false}'

# 典型工作流：开新 tab → 切移动模拟 → 截图查看
mtop-devtools tab_open --payload '{"url":"https://m.example.com"}'
mtop-devtools set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro"}'
mtop-devtools get_screenshot --output ./mobile.png
```

## 组合调用

```bash
# 滚动到底部后截图（两步合一）
mtop-devtools run_actions --payload '{"actions":[{"action":"page_scroll","data":{"direction":"bottom"}},{"action":"get_screenshot"}]}' --output ./bottom.png

# 点击按钮 → 等待列表出现 → 截图
mtop-devtools run_actions --payload '{"actions":[{"action":"page_click","data":{"text":"加载更多"}},{"action":"page_wait","data":{"selector":".list-item","timeout":5000}},{"action":"get_screenshot"}]}' --output ./loaded.png

# 在指定 Tab 上执行组合操作（tabId 自动注入每一步）
mtop-devtools run_actions --payload '{"tabId":12345,"actions":[{"action":"page_scroll","data":{"direction":"down","distance":800}},{"action":"page_wait","data":{"time":500}},{"action":"page_click","data":{"selector":"#load-more"}},{"action":"page_wait","data":{"selector":".new-content","timeout":5000}},{"action":"get_screenshot"}]}'

# 导航 → 等待加载 → 快照（获取页面结构）
mtop-devtools run_actions --payload '{"actions":[{"action":"page_navigate","data":{"url":"https://example.com/page"}},{"action":"page_wait","data":{"time":2000}},{"action":"page_snapshot"}]}'

# 输入搜索 → 按回车 → 等待结果 → 截图
mtop-devtools run_actions --payload '{"actions":[{"action":"page_type","data":{"selector":"input[name=q]","text":"test query"}},{"action":"page_press","data":{"key":"Enter"}},{"action":"page_wait","data":{"selector":".search-results","timeout":5000}},{"action":"get_screenshot"}]}' --output ./search.png
```

## 用户信息

```bash
# 获取用户工号
mtop-devtools get_user_info
# 返回: {"userId": "179605"}

# 获取完整用户信息（姓名、花名、部门、BU 等）
mtop-devtools get_user_info --payload '{"detail": true}'
# 返回:
# {
#   "userId": "179605",
#   "detail": {
#     "empId": "179605",
#     "bucUserId": "1203402",
#     "name": "柴茂源",
#     "displayName": "柴茂源(徒言)",
#     "nickName": "徒言",
#     "deptId": "N5513",
#     "deptDesc": "飞猪-飞猪-CTO线-用户技术-交通线前端-机票出行服务&全球化前端",
#     "buName": "CTO线",
#     "buNo": "72609",
#     "empType": "R",
#     "admin": false,
#     "photoPath": "TFS_TO_OSS/dKpPFvtHkqxUbpCT1761627405988",
#     "lang": "zh-CN",
#     "cid": "K6033"
#   }
# }
```

## TDBank 账号

```bash
# 获取当前 TDBank 账号
mtop-devtools tdbank_account --payload '{"operation":"current"}'

# 获取账号列表
mtop-devtools tdbank_account --payload '{"operation":"list","refresh":true}'

# 切换到列表中的账号
mtop-devtools tdbank_account --payload '{"operation":"switch","accountId":12345}'

# 快速借用账号并切换
mtop-devtools tdbank_account --payload '{"operation":"borrow","query":"test_account"}'
```

## 从文件读取参数（--payload-file）

当 JSON 参数很大（如完整的 mock 响应数据），使用 `--payload-file` 从文件读取：

```bash
# 使用文件中的 JSON 作为参数
mtop-devtools set_mock --payload-file ./mock-data.json

# 大体积 mock 数据推荐用法
mtop-devtools set_mock --payload-file /path/to/large-mock.json
```

`mock-data.json` 示例：
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
  },
  "enabled": true
}
```
