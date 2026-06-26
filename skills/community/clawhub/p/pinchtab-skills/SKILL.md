---
name: pinchtab
description: 通过 PinchTab HTTP API 控制无头或有头 Chrome 浏览器，用于网页自动化、爬虫、表单填充、导航、截图和数据提取
metadata:
  short-description: 浏览器自动化 via PinchTab HTTP API
---

# PinchTab Skill

快速、轻量级的 AI 代理浏览器控制工具，通过 HTTP + 可访问性树实现。

## 安全说明

PinchTab 完全在本地运行，不联系外部服务、不发送遥测数据。但它控制真实的 Chrome 实例——如果指向包含已保存登录信息的配置文件，代理可以访问认证网站。

**最佳实践：**
- 始终使用专用的空配置文件
- 暴露 API 时设置 `BRIDGE_TOKEN`
- 不要将你的日常 Chrome 配置文件指向 PinchTab

## 快速开始

### 1. 启动 PinchTab

```bash
# 无头模式（默认）- 无可见窗口
pinchtab &

# 有头模式 - 可见 Chrome 窗口，便于调试
BRIDGE_HEADLESS=false pinchtab &

# 带认证令牌
BRIDGE_TOKEN="your-secret-token" pinchtab &

# 自定义端口
BRIDGE_PORT=8080 pinchtab &
```

默认：**端口 9867**，无需认证（本地）。设置 `BRIDGE_TOKEN` 用于远程访问。

### 2. 代理工作流（30 秒模式）

```bash
# 1. 启动 PinchTab（持续运行，本地 :9867）
pinchtab &

# 2. 在代理中遵循此循环：
#    a) 导航到 URL
#    b) 快照页面（获取 refs 如 e0, e5, e12）
#    c) 对 ref 执行操作（点击 e5，输入 e12 "搜索文本"）
#    d) 再次快照查看结果
#    e) 重复步骤 c-d 直到完成
```

**就这么简单。** Refs 是稳定的——每次操作前不需要重新快照，只在页面显著变化时快照。

## 核心工作流

典型的代理循环：

1. **导航** 到 URL
2. **快照** 可访问性树（获取 refs）
3. **执行** 操作（点击、输入、按键）
4. **再次快照** 查看结果

### CLI 示例

```bash
# 导航
pinchtab nav https://example.com

# 获取交互式元素（紧凑格式）
pinchtab snap -i -c

# 点击元素
pinchtab click e5

# 输入文本
pinchtab type e12 hello world

# 按键
pinchtab press Enter

# 提取文本（~1K tokens）
pinchtab text

# 截图
pinchtab ss -o page.jpg

# 执行 JavaScript
pinchtab eval "document.title"

# 导出 PDF
pinchtab pdf --tab TAB_ID -o page.pdf
```

## HTTP API 示例

### 导航

```bash
curl -X POST http://localhost:9867/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 获取快照

```bash
# 完整快照
curl http://localhost:9867/snapshot

# 仅交互式元素（按钮、链接、输入）
curl "http://localhost:9867/snapshot?filter=interactive"

# 紧凑格式（节省 56-64% tokens）
curl "http://localhost:9867/snapshot?format=compact"

# 仅变化部分（多步骤工作流）
curl "http://localhost:9867/snapshot?diff=true"
```

### 执行操作

```bash
# 点击
curl -X POST http://localhost:9867/action \
  -H "Content-Type: application/json" \
  -d '{"kind": "click", "ref": "e5"}'

# 输入
curl -X POST http://localhost:9867/action \
  -H "Content-Type: application/json" \
  -d '{"kind": "type", "ref": "e12", "text": "hello"}'

# 按键
curl -X POST http://localhost:9867/action \
  -H "Content-Type: application/json" \
  -d '{"kind": "press", "key": "Enter"}'
```

### 提取文本

```bash
# 可读文本（~800 tokens）
curl http://localhost:9867/text

# 原始 HTML
curl "http://localhost:9867/text?mode=raw"
```

### 截图

```bash
curl -X POST http://localhost:9867/screenshot \
  -H "Content-Type: application/json" \
  -d '{"format": "jpeg", "quality": 80}' \
  --output page.jpg
```

### 多标签页管理

```bash
# 创建新标签页
curl -X POST http://localhost:9867/tabs \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# 切换标签页
curl -X POST http://localhost:9867/tabs/switch \
  -H "Content-Type: application/json" \
  -d '{"tabId": "TAB_123"}'

# 关闭标签页
curl -X DELETE http://localhost:9867/tabs/TAB_123
```

## 快照示例

调用 `/snapshot` 后，获得页面的可访问性树 JSON：

```json
{
  "refs": [
    {"id": "e0", "role": "link", "text": "Sign In", "selector": "a[href='/login']"},
    {"id": "e1", "role": "textbox", "label": "Email", "selector": "input[name='email']"},
    {"id": "e2", "role": "button", "text": "Submit", "selector": "button[type='submit']"}
  ],
  "text": "... 页面的可读文本版本 ...",
  "title": "Login Page"
}
```

然后对 refs 执行操作：`click e0`，`type e1 "user@example.com"`，`press e2 Enter`。

## Token 成本指南

| 方法 | 典型 tokens | 使用场景 |
|---|---|---|
| `/text` | ~800 | 阅读页面内容 |
| `/snapshot?filter=interactive` | ~3,600 | 查找要点击的按钮/链接 |
| `/snapshot?diff=true` | 变化量 | 多步骤工作流（仅变化） |
| `/snapshot?format=compact` | 减少 56-64% | 每行一个节点，最佳效率 |
| `/snapshot` | ~10,500 | 完整页面理解 |
| `/screenshot` | ~2K (vision) | 视觉验证 |
| `/tabs/{id}/pdf` | 0 (二进制) | 导出 PDF（无 token 成本） |

**策略**：从 `?filter=interactive&format=compact` 开始。后续快照使用 `?diff=true`。仅需要可读内容时使用 `/text`。仅在需要时使用完整 `/snapshot`。

## 代理优化

**2026 年 2 月验证**：测试发现关键模式，实现可靠、节省 token 的爬虫。

### 3 秒模式

导航后等待 3 秒再快照：

```bash
curl -X POST http://localhost:9867/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' && \
sleep 3 && \
curl http://localhost:9867/snapshot | jq
```

**Token 节省**：93% 减少（3,842 → 272 tokens）。

## 提示

- **多标签页时始终显式传递 `tabId`**
- Refs 在快照和操作之间稳定——点击前无需重新快照
- 导航或页面重大变化后，获取新快照获取新鲜 refs
- PinchTab 持久化会话——标签页在重启后存活（用 `BRIDGE_NO_RESTORE=true` 禁用）
- Chrome 配置文件持久化——cookies/登录信息在运行间保留
- 阅读密集型任务使用 `BRIDGE_BLOCK_IMAGES=true` 或 `"blockImages": true`
- **导航后等待 3+ 秒再快照**——Chrome 需要时间渲染 2000+ 可访问性树节点

## 环境变量

```bash
# 绑定地址（默认 127.0.0.1）
BRIDGE_BIND=127.0.0.1

# 认证令牌（默认无）
BRIDGE_TOKEN="your-secret-token"

# 端口（默认 9867）
BRIDGE_PORT=9867

# 无头模式（默认 true）
BRIDGE_HEADLESS=false

# 配置文件路径
BRIDGE_PROFILE=~/.pinchtab/automation-profile

# 阻止图片（节省带宽）
BRIDGE_BLOCK_IMAGES=true

# 禁用会话恢复
BRIDGE_NO_RESTORE=true
```

## 完整文档

- [API 参考](references/api.md) - 完整 HTTP API
- [配置文件](references/profiles.md) - 配置文件管理
- [环境变量](references/env.md) - 所有配置选项
