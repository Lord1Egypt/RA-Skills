# Playwright CLI 使用示例

## 目录

1. [表单提交](#表单提交)
2. [多标签页工作流](#多标签页工作流)
3. [DevTools 调试](#devtools-调试)
4. [网络拦截](#网络拦截)
5. [视频录制](#视频录制)
6. [追踪调试](#追踪调试)
7. [状态持久化](#状态持久化)
8. [交互式标注](#交互式标注)
9. [自定义代码执行](#自定义代码执行)

---

## 表单提交

基本的表单填写和提交流程：

```bash
# 打开浏览器并导航到表单页面
playwright-cli open https://example.com/form

# 获取快照查看元素
playwright-cli snapshot

# 填充表单字段
playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli fill e3 "John Doe"

# 选择下拉选项
playwright-cli select e4 "option-value"

# 勾选复选框
playwright-cli check e5

# 提交表单
playwright-cli click e6

# 等待并验证结果
playwright-cli snapshot
playwright-cli eval "document.querySelector('.success-message')?.textContent"

# 关闭
playwright-cli close
```

使用 `--submit` 参数简化：

```bash
playwright-cli fill e5 "user@example.com" --submit  # 填充后自动按 Enter
```

---

## 多标签页工作流

在多个标签页之间切换：

```bash
# 打开主页
playwright-cli open https://example.com

# 创建新标签页
playwright-cli tab-new https://example.com/page1
playwright-cli tab-new https://example.com/page2

# 列出所有标签页
playwright-cli tab-list

# 切换标签页
playwright-cli tab-select 0    # 第一个
playwright-cli tab-select 1    # 第二个

# 在当前标签页操作
playwright-cli snapshot
playwright-cli click e5

# 关闭特定标签页
playwright-cli tab-close 2

# 关闭当前标签页
playwright-cli tab-close

# 完成
playwright-cli close
```

---

## DevTools 调试

### 控制台日志和请求

```bash
playwright-cli open https://example.com

# 执行一些操作
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli press Enter

# 查看控制台输出
playwright-cli console
playwright-cli console warning    # 仅警告

# 查看网络请求
playwright-cli requests
playwright-cli request 5          # 第 5 个请求详情

playwright-cli close
```

### 执行自定义 JavaScript

```bash
# 获取页面信息
playwright-cli eval "document.title"
playwright-cli eval "location.href"

# 获取元素属性
playwright-cli eval "el => el.id" e5
playwright-cli eval "el => el.className" e5
playwright-cli eval "el => el.getAttribute('data-testid')" e5

# 复杂查询
playwright-cli eval "JSON.stringify([...document.querySelectorAll('a')].map(a => ({text: a.textContent, href: a.href})))"
```

---

## 网络拦截

### 模拟 API 响应

```bash
playwright-cli open https://example.com

# 拦截图片请求，返回 404
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "**/*.png" --status=404

# 模拟 API 响应
playwright-cli route "https://api.example.com/users" --body='{"users": [{"id": 1, "name": "Test User"}]}'

# 查看已设置的路由
playwright-cli route-list

# 执行操作（会使用模拟数据）
playwright-cli snapshot
playwright-cli click e5

# 移除路由
playwright-cli unroute "**/*.jpg"
playwright-cli unroute    # 移除所有

playwright-cli close
```

### 测试离线状态

```bash
# 模拟所有 API 请求失败
playwright-cli route "https://api.example.com/**" --status=500

# 测试应用的错误处理
playwright-cli snapshot
```

---

## 视频录制

录制操作视频用于演示或调试：

```bash
playwright-cli open https://example.com

# 开始录制
playwright-cli video-start demo.webm

# 执行操作
playwright-cli goto https://example.com/products
playwright-cli click e5
playwright-cli fill e7 "search term"
playwright-cli press Enter

# 添加章节标记
playwright-cli video-chapter "Search" --description="User searches for product" --duration=2000

# 继续操作
playwright-cli click e10
playwright-cli video-chapter "Add to Cart" --description="User adds item" --duration=2000

# 为每个操作添加标注
playwright-cli video-show-actions --duration=600 --position=top-right

playwright-cli click e15
playwright-cli fill e16 "1"

# 隐藏操作标注
playwright-cli video-hide-actions

# 停止录制
playwright-cli video-stop

playwright-cli close
```

---

## 追踪调试

使用 Playwright 追踪捕获详细调试信息：

```bash
playwright-cli open https://example.com

# 开始追踪
playwright-cli tracing-start

# 执行操作
playwright-cli click e4
playwright-cli fill e7 "test data"
playwright-cli press Enter
playwright-cli snapshot

# 停止追踪（生成 trace.zip）
playwright-cli tracing-stop

playwright-cli close

# 查看追踪（在浏览器中打开 trace viewer）
# npx playwright show-trace trace.zip
```

---

## 状态持久化

### 保存和恢复登录状态

```bash
# 第一次：登录并保存状态
playwright-cli open https://example.com/login
playwright-cli fill e1 "username"
playwright-cli fill e2 "password"
playwright-cli click e3
playwright-cli snapshot

# 保存认证状态
playwright-cli state-save auth.json

# 保存 cookies
playwright-cli cookie-list
playwright-cli cookie-get session_id

playwright-cli close

# 第二次：恢复状态（无需重新登录）
playwright-cli open https://example.com
playwright-cli state-load auth.json
playwright-cli reload
playwright-cli snapshot    # 应该已登录
```

### 操作 LocalStorage

```bash
playwright-cli open https://example.com

# 设置主题
playwright-cli localstorage-set theme dark
playwright-cli localstorage-set language zh-CN

# 查看
playwright-cli localstorage-list

# 获取
playwright-cli localstorage-get theme

# 清除
playwright-cli localstorage-delete theme
playwright-cli localstorage-clear

playwright-cli close
```

---

## 交互式标注

让用户在页面上画框、写注释，用于 UI 审查或设计反馈：

```bash
playwright-cli open https://example.com/dashboard

# 启动交互式标注模式
playwright-cli show --annotate

# 用户在页面上：
# - 用鼠标画框标记区域
# - 输入文字注释
# - 提交反馈

# 你收到：
# - 带标注的截图
# - 标记区域的快照
# - 用户的文字注释

playwright-cli close
```

---

## 自定义代码执行

运行任意 Playwright 代码：

```bash
playwright-cli open https://example.com

# 授予地理位置权限
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"

# 设置地理位置
playwright-cli run-code "async page => await page.context().setGeolocation({ latitude: 37.7749, longitude: -122.4194 })"

# 从文件运行脚本
playwright-cli run-code --filename=custom-script.js

playwright-cli close
```

脚本文件示例 (`custom-script.js`)：

```javascript
async page => {
  // 等待特定元素
  await page.waitForSelector('.loaded');
  
  // 滚动到底部
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  
  // 截图
  await page.screenshot({ path: 'full-page.png', fullPage: true });
}
```

---

## 会话管理示例

### 多会话并行

```bash
# 创建两个独立会话
playwright-cli -s=session1 open https://example.com --persistent
playwright-cli -s=session2 open https://other-site.com --persistent

# 分别操作
playwright-cli -s=session1 click e5
playwright-cli -s=session2 fill e3 "test"

# 查看会话列表
playwright-cli list

# 分别关闭
playwright-cli -s=session1 close
playwright-cli -s=session2 close

# 或一次关闭所有
playwright-cli close-all
```

### 连接已运行的浏览器

```bash
# 连接到已打开的 Chrome
playwright-cli attach --cdp=chrome

# 或连接到特定 CDP 端点
playwright-cli attach --cdp=http://localhost:9222

# 操作
playwright-cli snapshot
playwright-cli click e5

# 分离（不关闭浏览器）
playwright-cli detach
```

---

## Raw 输出管道示例

```bash
# 提取所有链接
playwright-cli --raw eval "JSON.stringify([...document.querySelectorAll('a')].map(a => a.href))" > links.json

# 计算页面加载时间
playwright-cli --raw eval "JSON.stringify(performance.timing)" | jq '.loadEventEnd - .navigationStart'

# 获取 token
TOKEN=$(playwright-cli --raw cookie-get auth_token)
echo "Token: $TOKEN"

# 快照对比
playwright-cli --raw snapshot > before.yml
playwright-cli click e5
playwright-cli --raw snapshot > after.yml
diff before.yml after.yml

# JSON 输出
playwright-cli list --json | jq '.sessions'
```
