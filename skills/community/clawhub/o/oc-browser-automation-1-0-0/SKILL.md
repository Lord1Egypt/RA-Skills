---
name: bb-browser
description: 浏览器控制工具 - 封装 OpenClaw browser 工具，支持网页自动化、截图、点击输入等操作
triggers:
  - bb-browser
  - 浏览器
  - 浏览网页
  - 截图
  - browser
---

# bb-browser 浏览器控制工具

这是 OpenClaw browser 工具的封装，提供强大的浏览器自动化能力。

## 核心功能

| 功能 | 说明 |
|------|------|
| **打开网页** | 导航到指定 URL |
| **截图** | 页面截图或全页截图 |
| **快照** | 获取页面 DOM 快照（AI 快照或 ARIA 快照） |
| **点击** | 点击页面元素 |
| **输入** | 在输入框中输入文本 |
| **滚动** | 滚动页面 |
| **等待** | 等待元素/文本/URL 加载 |
| **标签页管理** | 打开/切换/关闭标签页 |
| **文件上传** | 上传文件到网页 |
| **下载** | 从网页下载文件 |

## 使用方式

### 1. 查看浏览器状态

```
browser action=status
```

### 2. 启动浏览器

```
browser action=start
```

### 3. 打开网页

```
browser action=open url="https://example.com"
```

### 4. 截图

```javascript
// 普通截图
browser action=screenshot

// 全页截图
browser action=screenshot fullPage=true

// 带标签的截图（显示元素编号）
browser action=snapshot labels=true
```

### 5. 获取页面快照

```javascript
// AI 快照（带数字编号，适合点击操作）
browser action=snapshot

// 交互式快照（推荐，更稳定）
browser action=snapshot interactive=true

// 紧凑模式
browser action=snapshot compact=true
```

### 6. 点击元素

```javascript
// 使用快照返回的数字 ref
browser action=act kind=click ref="12"

// 使用 role ref
browser action=act kind=click ref="e12"
```

### 7. 输入文本

```javascript
// 输入文本并提交
browser action=act kind=type ref="23" text="hello" submit=true

// 输入后按回车
browser action=act kind=press key="Enter"
```

### 8. 等待元素

```javascript
// 等待文本出现
browser action=wait text="完成"

// 等待 URL 变化
browser action=wait url="**/dashboard"

// 等待加载状态
browser action=wait load=networkidle

// 组合等待
browser action=wait selector="#main" url="**/dash" load=networkidle
```

### 9. 标签页操作

```javascript
// 打开新标签页
browser action=open url="https://example.com"

// 列出标签页
browser action=tabs

// 切换到指定标签页
browser action=focus targetId="abcd1234"

// 关闭标签页
browser action=close targetId="abcd1234"
```

### 10. 文件上传

```javascript
// 上传文件
browser action=upload filePath="/tmp/openclaw/uploads/file.pdf"
```

### 11. 滚动页面

```javascript
// 滚动到元素可见
browser action=act kind=scrollIntoView ref="e12"

// 滚动到顶部/底部
browser action=act kind=evaluate fn="window.scrollTo(0, document.body.scrollHeight)"
```

### 12. 设置浏览器状态

```javascript
// 设置离线模式
browser action=set offline=true

// 设置自定义 Headers
browser action=set headers="{\"X-Debug\":\"1\"}"

// 设置地理位置
browser action=set geo="37.7749,-122.4194"

// 设置 User Agent / 设备
browser action=set device="iPhone 14"
```

## 快照引用 (Refs) 详解

### AI 快照 (默认)
- 返回带数字编号的快照 (1, 2, 3...)
- 点击时使用 `ref="12"` 这样的数字

### Role 快照 (推荐)
- 使用 `--interactive` 或 `--compact` 参数
- 返回 `[ref=e12]` 格式的角色引用
- 更稳定，不依赖 DOM 结构变化

### 重要提示
- **Refs 在页面导航后会失效**，每次操作前建议重新获取快照
- 使用 `highlight` 可以高亮显示目标元素，验证点击位置

## 常见工作流

### 登录网页示例
1. `browser action=open url="https://example.com/login"`
2. `browser action=snapshot` → 获取快照
3. `browser action=act kind=type ref="5" text="username"` → 输入用户名
4. `browser action=act kind=type ref="6" text="password"` → 输入密码
5. `browser action=act kind=click ref="7"` → 点击登录按钮
6. `browser action=wait url="**/dashboard"` → 等待跳转

### 填写表单示例
1. 打开页面
2. `browser action=snapshot interactive=true`
3. 使用 `fill` 批量填充多个字段：
   ```javascript
   browser action=act kind=fill fields='[{"ref":"1","type":"text","value":"张三"},{"ref":"2","type":"text","value":"25"}]'
   ```

### 下载文件示例
1. 点击下载链接
2. `browser action=waitfordownload filename="report.pdf"`
3. 文件保存到 `/tmp/openclaw/downloads/`

## 调试技巧

### 查看控制台错误
```javascript
browser action=console level="error"
```

### 查看网络请求
```javascript
browser action=requests filter="api"
```

### 录制 Trace
```javascript
browser action=trace_start
// 执行操作
browser action=trace_stop
```

### 高亮元素
```javascript
browser action=highlight ref="e12"
```

## 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| action | string | 操作类型：status, start, stop, tabs, open, focus, close, snapshot, screenshot, act, navigate, wait, upload 等 |
| url | string | 目标 URL |
| profile | string | 浏览器配置：openclaw (默认) / chrome (使用你的 Chrome) |
| target | string | 浏览器目标：sandbox / host / node |
| ref | string | 元素引用编号 |
| text | string | 输入的文本 |
| fullPage | boolean | 是否截取完整页面 |
| interactive | boolean | 是否使用交互式快照 |
| compact | boolean | 是否使用紧凑模式 |
| kind | string | 操作类型：click, type, press, hover, scroll, select, drag, fill, evaluate |

## 注意事项

1. **安全**：浏览器可能包含登录会话，请勿分享浏览器状态
2. **Refs**：每次页面变化后需要重新获取快照
3. **等待**：网络慢的页面记得增加等待时间
4. **调试**：先用 snapshot 查看页面结构，再进行操作
