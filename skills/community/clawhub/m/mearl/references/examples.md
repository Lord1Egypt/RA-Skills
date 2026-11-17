# Mearl 使用示例

## API 调试

```bash
# 获取最近请求（默认返回 mtop）
mearl get_requests --payload '{"count": 5}'

# 强制指定获取 mtop 请求
mearl get_requests --payload '{"count": 5, "source": "mtop"}'

# 强制指定获取普通 HTTP 请求（xhr/fetch，非 mtop）
mearl get_requests --payload '{"count": 10, "source": "requests"}'

# 获取 error 日志
mearl get_logs --payload '{"level": "error", "limit": 50}'

# 获取最近 20 条 RUM/aplus/ARMS 埋点事件
mearl get_events --payload '{"limit": 20}'

# 获取指定页面的埋点事件，无需打开 DevTools panel
mearl get_events --payload '{"tabId": 12345, "limit": 20}'

# 只看 aplus 埋点事件
mearl get_events --payload '{"source": "aplus", "limit": 20}'

# 按事件类型过滤（正则）
mearl get_events --payload '{"event_type": "CLK", "source": "aplus"}'

# 过滤特定 name/url（正则）
mearl get_events --payload '{"filter": "cart|order", "limit": 10}'

# 排查字段级问题时返回完整原始载荷和上下文
mearl get_events --payload '{"filter": "order", "limit": 1, "includeRaw": true}'

# 获取 API schema
mearl get_api_schema --payload '{"api": "mtop.fliggy.flyrs.render", "version": "1.0"}'

# 只获取 HSF 接口信息（服务名、方法、版本）
mearl get_api_schema --payload '{"api": "mtop.fliggy.flyrs.render", "fields": ["hsf"]}'

# 只获取请求参数 JSON Schema
mearl get_api_schema --payload '{"api": "mtop.fliggy.flyrs.render", "fields": ["schema"]}'
```

## Mock & 请求规则

```bash
# 按字段修改 API 响应（mock）
mearl set_mock --payload '{"apiName": "mtop.cart.query", "fields": [{"path": "data.total", "value": 150}], "enabled": true}'

# 查看所有 mock 配置
mearl get_mocks --payload '{}'

# 添加请求重定向规则（将 h5api.m.taobao.com 请求重定向到本地服务）
mearl set_rule --payload '{"actionType": "redirect", "filter": "^https://h5api\\.m\\.taobao\\.com/.*", "redirectUrl": "http://localhost:3000/$&", "description": "Redirect to local dev server"}'

# 添加请求头修改规则（给所有 mtop 请求添加自定义头）
mearl set_rule --payload '{"actionType": "modifyHeaders", "filter": "^https://h5api\\..*\\.taobao\\.com/", "requestHeaders": [{"header": "x-custom-token", "operation": "set", "value": "test-token-123"}]}'

# 添加请求拦截规则（阻止特定域名的请求）
mearl set_rule --payload '{"actionType": "block", "filter": "^https://ads\\.example\\.com/.*", "description": "Block ads"}'

# 查看当前存储的全部请求规则（含 Options 面板配置的）
mearl get_rules
```

## 网络请求代理

```bash
# 代理 GET 请求，自动携带 Cookie
mearl send_request --payload '{"url": "https://api.example.com/data", "method": "GET"}'

# 代理 POST 请求，自动携带 Cookie，发送 JSON body
mearl send_request --payload '{"url": "https://api.example.com/submit", "method": "POST", "body": {"key": "value"}, "withCookies": true}'

# 代理请求，指定自定义请求头
mearl send_request --payload '{"url": "https://api.example.com/data", "headers": {"X-Custom-Token": "abc123"}, "params": {"page": "1", "size": "20"}}'

# 发起 mtop GET 请求（自动签名、自动携带 token）
mearl send_mtop_request --payload '{"api": "mtop.trade.order.detail", "data": {"orderId": "12345"}}'

# 发起 mtop POST 请求，指定版本号
mearl send_mtop_request --payload '{"api": "mtop.trade.order.create", "data": {"itemId": "67890", "quantity": 1}, "method": "POST", "version": "2.0"}'

# 发起 mopen 请求（api 以 mopen. 开头，自动使用 mopen 签名算法）
mearl send_mtop_request --payload '{"api": "mopen.trade.order.query", "data": {"status": "paid"}}'

# 发起预发环境的 mtop 请求（h5api.wapa.taobao.com）
mearl send_mtop_request --payload '{"api": "mtop.trade.order.detail", "data": {"orderId": "12345"}, "env": "pre"}'

# 申请目标域名的访问权限（弹窗等待用户授权，granted=true 后再重试 send_request）
mearl request_domain_permission --payload '{"domain": "example.com"}'
```

## 浏览器操作

```bash
# 打开新标签页（后台打开，等待加载完成后返回 tabId）
mearl tab_open --payload '{"url": "https://example.com"}'

# 打开新标签页并激活（前台显示）
mearl tab_open --payload '{"url": "https://example.com", "active": true}'

# 优先复用 URL 相同（忽略 query/hash）的标签页；找不到才新开
mearl tab_open --payload '{"url":"https://example.com/page?step=2","active":true,"reuse":"prefer","match":{"ignoreSearch":true,"ignoreHash":true}}'

# 只复用指定 URL glob 的标签页；找不到或匹配多个时明确报错
mearl tab_open --payload '{"url":"https://www.figma.com/design/file-key/File","reuse":"require","match":{"urlPattern":"https://www.figma.com/design/file-key/*","ignoreSearch":true}}'

# 临时激活新 Tab，关闭时恢复原活动标签页
mearl tab_open --payload '{"url":"https://example.com","active":true,"restoreFocusOnClose":true}'

# 开 tab 即以移动态打开 H5 页面（首屏即移动态，无需再单独切模拟 + reload）
mearl tab_open --payload '{"url": "https://m.example.com", "emulation": {"preset": "iphone-15-pro"}}'

# 列出当前窗口所有标签页
mearl tab_list --payload '{}'

# 关闭指定标签页
mearl tab_close --payload '{"tabId": 12345}'

# 首次进入页面时获取结构和 @ref 基线
mearl page_snapshot --payload '{"tabId": 12345}'

# 默认交互：按可见文本点击，并等待页面变化稳定（页面动作默认内置观察）
mearl page_click --payload '{"tabId":12345,"text":"提交"}'

# 文本多匹配时用 role 消歧
mearl page_click --payload '{"tabId":12345,"text":"退款明细","role":"button"}'

# 重复文本可限定在指定 CSS / @ref 子树内
mearl page_click --payload '{"tabId":12345,"text":"确定","scope":"@e12"}'

# CSS 选择器点击
mearl page_click --payload '{"tabId":12345,"selector":"button.submit"}'

# snapshot ref（先 page_snapshot 拿 @eN，再点击）
mearl page_click --payload '{"tabId":12345,"selector":"@e3"}'

# 默认 auto；仅在需要覆盖自动策略时显式强制 mouse / touch / dom
mearl page_click --payload '{"tabId":12345,"selector":".gesture-btn","clickMode":"touch"}'

# 按视口坐标点击（前两种都不适用的兜底）
mearl page_click --payload '{"tabId":12345,"point":{"x":336,"y":117}}'

# 向输入框填写文本（自动清空原有内容）
mearl page_type --payload '{"tabId":12345,"selector":"input[name=username]","text":"test_user"}'

# 向输入框追加文本（不清空原有内容）
mearl page_type --payload '{"tabId":12345,"selector":"textarea.comment","text":"追加内容","clearFirst":false}'

# 滚动到底部并观察懒加载内容
mearl page_scroll --payload '{"tabId":12345,"direction":"bottom"}'

# 向下滚动 800px
mearl page_scroll --payload '{"tabId":12345,"direction":"down","distance":800}'

# 滚动指定容器（也可使用 page_snapshot 返回的 @eN ref）
mearl page_scroll --payload '{"tabId":12345,"selector":".virtual-list","direction":"down","distance":800}'
mearl page_scroll --payload '{"tabId":12345,"selector":"@e8","direction":"bottom"}'

# ref 指向列表内子节点时，向上寻找最近可滚动容器
mearl page_scroll --payload '{"tabId":12345,"selector":"@e8","containerPolicy":"nearest","direction":"bottom"}'

# 悬停并观察下拉菜单
mearl page_hover --payload '{"tabId":12345,"selector":"#account-menu"}'

# 在页面上下文中执行 JavaScript
mearl page_eval --payload '{"expression": "document.title"}'

# 在指定 Tab 上执行 JavaScript
mearl page_eval --payload '{"tabId": 12345, "expression": "document.querySelectorAll(\"a\").length"}'

# 仅当表达式修改页面且需要观察变化时显式开启观察
mearl page_eval --payload '{"tabId":12345,"expression":"document.querySelector(\"#toggle\").click()","observe":{}}'

# 按 Enter 并观察提交结果
mearl page_press --payload '{"tabId":12345,"key":"Enter"}'

# 按 Ctrl+Space
mearl page_press --payload '{"tabId":12345,"key":"Space","modifiers":["ctrl"]}'

# 没有前置动作时，独立等待 2 秒
mearl page_wait --payload '{"tabId":12345,"time":2000}'

# 没有前置动作时，独立等待已知元素出现
mearl page_wait --payload '{"tabId":12345,"selector":".result-list","timeout":5000}'

# 没有前置动作时，轮询页面主上下文条件（支持 Promise，truthy 时结束）
mearl page_wait --payload '{"tabId":12345,"condition":"window.appReady === true","timeout":30000,"interval":250}'

# 在当前标签页导航
mearl page_navigate --payload '{"tabId":12345,"url":"https://example.com"}'
mearl page_navigate --payload '{"tabId":12345,"history":"back"}'

# 上传文件并观察上传状态
mearl page_upload --payload '{"tabId":12345,"selector":"input[type=file]","filePaths":["/Users/me/photo.jpg"]}'

# 无需观察结果或排障时，传 observe:false 只执行裸动作
mearl page_click --payload '{"tabId":12345,"selector":"#submit","observe":false}'
```

## 页面感知

```bash
# 首次进入页面时获取无障碍树快照，建立结构基线
mearl page_snapshot --payload '{}'

# 页面动作观察建议回退时优先获取当前视口，避免长列表整页输出
mearl page_snapshot --payload '{"tabId":12345,"mode":"viewport"}'

# 已知弹层或区域时只获取该 AX 子树
mearl page_snapshot --payload '{"tabId":12345,"rootSelector":"[role=dialog]"}'

# 已有 ref 时获取其局部子树；ancestorDepth 可向上补充容器上下文
mearl page_snapshot --payload '{"tabId":12345,"rootRef":"@e8","ancestorDepth":1}'

# 在服务端按 accessibility name / role 裁剪，只返回命中节点及祖先路径
mearl page_snapshot --payload '{"tabId":12345,"query":{"text":"保存","role":"button"}}'

# 只保留表单、按钮、链接等可交互节点
mearl page_snapshot --payload '{"tabId":12345,"mode":"interactive"}'

# 限制输出节点数；截断时会同时保留首尾
mearl page_snapshot --payload '{"tabId":12345,"maxNodes":200}'

# 控制树深度（默认 15，复杂页面可调大）
mearl page_snapshot --payload '{"depth": 20}'

# 任务需要视觉判断或增量观察不可用时获取截图
mearl page_screenshot --payload '{"format": "png"}'

# 获取当前页面截图（JPEG 格式，质量 90）
mearl page_screenshot --payload '{"format": "jpeg", "quality": 90}'

# 保存截图到文件（推荐方式，无需手动处理 base64）
mearl page_screenshot --output ./screenshot.png

# 保存 JPEG 截图到文件
mearl page_screenshot --payload '{"format": "jpeg", "quality": 80}' --output ./screenshot.jpg

# 获取 Elements 面板当前选中元素的详细信息（含布局、样式、属性）
mearl page_selected_element --payload '{}'

# 不含 outerHTML（减少数据量，适合只看布局和样式）
mearl page_selected_element --payload '{"includeOuterHTML": false}'

# 获取选中元素信息 + 节点截图（自动滚动并按元素裁剪）
mearl page_selected_element --payload '{"includeScreenshot": true}'
```

## 移动端模拟

```bash
# 一键切到 iPhone 15 Pro 调试 H5 移动页面（自动 reload 让页面以移动模式重新初始化）
mearl set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro"}'

# 切到 Pixel 8
mearl set_device_emulation --payload '{"enabled":true,"preset":"pixel-8"}'

# 横屏调试
mearl set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro","orientation":"landscape"}'

# 仅改 viewport 不重载（保留当前页面状态，只看 CSS 响应式）
mearl set_device_emulation --payload '{"enabled":true,"preset":"iphone-15-pro","reload":false}'

# 自定义 viewport + UA（无 preset 时 width/height/userAgent 必填）
mearl set_device_emulation --payload '{"enabled":true,"width":360,"height":640,"deviceScaleFactor":3,"userAgent":"Mozilla/5.0 (Linux; Android 14; CustomDevice) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"}'

# 清除移动模拟，回到桌面态
mearl set_device_emulation --payload '{"enabled":false}'

# 典型工作流：开新 tab（直接移动态）→ 截图查看
# 推荐用 tab_open 的 emulation 参数，一步到位、首屏即移动态，省一次 reload
mearl tab_open --payload '{"url":"https://m.example.com","emulation":{"preset":"iphone-15-pro"}}'
mearl page_screenshot --output ./mobile.png
```

## 时区模拟

```bash
# 切换到纽约时区
mearl set_timezone --payload '{"tabId":12345,"timezone":"America/New_York"}'

# 恢复浏览器默认时区
mearl set_timezone --payload '{"tabId":12345,"timezone":""}'
```

## 组合调用

```bash
# hover 后必须立即点击、无需中间判断时使用 run_actions
mearl run_actions --payload '{"tabId":12345,"actions":[{"action":"page_hover","data":{"selector":"#account-menu"}},{"action":"page_click","data":{"selector":"#logout"}}]}'

# 任务明确需要视觉结果时，滚动到底部后截图
mearl run_actions --payload '{"actions":[{"action":"page_scroll","data":{"direction":"bottom"}},{"action":"page_screenshot"}]}' --output ./bottom.png

# 下一步依赖页面变化时逐步调用带观察的页面动作，不把点击→等待→截图固化为 run_actions
mearl page_click --payload '{"tabId":12345,"text":"加载更多"}'

# observation.fullSnapshotRecommended=true 时获取最小必要范围；滚动后需读取新视口时按需获取 viewport；视觉任务再截图
mearl page_snapshot --payload '{"tabId":12345,"mode":"viewport"}'

# 导航完成后建立新的页面基线
mearl run_actions --payload '{"tabId":12345,"actions":[{"action":"page_navigate","data":{"url":"https://example.com/page"}},{"action":"page_snapshot"}]}'

# 输入搜索并按回车，每一步都返回增量结果
mearl page_type --payload '{"tabId":12345,"selector":"input[name=q]","text":"test query"}'
mearl page_press --payload '{"tabId":12345,"key":"Enter"}'
```

## 用户信息

```bash
# 获取用户工号
mearl get_user_info
# 返回: {"userId": "179605"}

# 获取完整用户信息（姓名、花名、部门、BU 等）
mearl get_user_info --payload '{"detail": true}'
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

## 托管浏览器

```bash
# 当前控制浏览器需已登录 TDBank；通过 SSO 登录测试账号，供 taobao.com 系页面使用
# 新实例默认 headless、临时 Profile
mearl browser_launch --payload '{"name":"account-a","accountId":12345}'

# 搜索并快速借用账号，在另一个独立实例中登录
mearl browser_launch --payload '{"name":"account-b","query":"test_account","url":"https://www.taobao.com"}'

# 复制指定域 Cookie，可同时传多个域
mearl browser_launch --payload '{"name":"cookie-copy","copyCookieDomains":["example.com","sub.example.org"],"url":"https://example.com"}'

# 查看实例，并定向操作
mearl browser_list
mearl tab_open --browser managed:account-a --payload '{"url":"https://example.com"}'

# 关闭；临时 Profile 自动清理
mearl browser_close --payload '{"browser":"managed:account-a"}'

# 持久化 Profile 关闭时默认保留，显式传 deleteProfile 才删除
mearl browser_close --payload '{"browser":"managed:account-b","deleteProfile":true}'
```

## 从文件读取参数（--payload-file）

当 JSON 参数很大（如完整的 mock 响应数据），使用 `--payload-file` 从文件读取：

```bash
# 使用文件中的 JSON 作为参数
mearl set_mock --payload-file ./mock-data.json

# 大体积 mock 数据推荐用法
mearl set_mock --payload-file /path/to/large-mock.json
```

`mock-data.json` 示例：

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
  },
  "enabled": true
}
```
