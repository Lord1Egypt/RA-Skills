---
name: m5stack-chrome-browser-control
description: M5Stack | 通过 MCP chrome-devtools 协议控制用户本地 Chrome 浏览器，实现自动打开网页、操作任意 Outlook 邮箱、搜索内容等任务。使用前提：用户已在 Chrome 中开启远程调试（127.0.0.1:9222），且 OpenClaw MCP 已配置 chrome-devtools-mcp。触发场景：打开浏览器、控制 Chrome、查看邮件、自动化网页操作、浏览器自动化。
---

# M5Stack | Chrome 浏览器控制 Skill

通过 MCP 协议远程控制用户本地 Chrome 浏览器，完成网页访问、Outlook 邮件查看、内容搜索等自动化任务。

---

## 一、用户需要做的准备工作

### 第一步：在 Chrome 中开启远程调试

1. 打开 Chrome 浏览器（**普通版 Chrome，不是 Chrome Beta**）
2. 在地址栏访问：`chrome://inspect/#devices`
3. 在页面顶部找到 **"Remote debugging"** 开关，点击开启
4. 确认页面显示：**"Server running at: 127.0.0.1:9222"**

> ⚠️ 每次重启 Chrome 后需要重新开启此开关。

### 第二步：配置 OpenClaw MCP

编辑 `~/.openclaw/openclaw.json`（Windows 下为 `C:\Users\<用户名>\.openclaw\openclaw.json`）。

**只在已有 JSON 对象中新增 `mcp` 字段，绝对不要修改或删除文件中其他已有字段**（如 plugins、gateway 等），否则 OpenClaw 将无法启动。

```json
{
  "（其他已有字段保持不变）": "...",
  "mcp": {
    "servers": {
      "chrome-devtools": {
        "command": "npx",
        "args": [
          "chrome-devtools-mcp@latest",
          "--autoConnect"
        ]
      }
    }
  }
}
```

> ⚠️ **严禁**：
> - 不能加 `--channel=beta`（会寻找 Chrome Beta 安装路径，必然失败）
> - 不能覆盖整个文件，只能新增 `mcp` 字段
> - 修改前建议备份原文件

配置完成后在终端运行 `openclaw gateway restart` 重启网关使配置生效。

---

## 二、MCP 工具说明

所有工具均来自 `chrome-devtools-mcp`，通过 `chrome-devtools__*` 前缀调用。

### `chrome-devtools__list_pages`
列出当前浏览器所有打开的标签页，返回每个页面的 `pageId` 和 URL。
- **用途**：确认 MCP 是否连接成功；查找已登录的目标标签页
- **成功标志**：返回页面列表
- **失败标志**：`Could not find DevToolsActivePort` → 用户未开启调试模式

### `chrome-devtools__select_page(pageId)`
切换到指定标签页，后续操作将作用于该页面。
- **用途**：当浏览器有多个标签时，切换到目标标签（如已登录的 Outlook 或 X）

### `chrome-devtools__new_page(url)`
新建标签页并导航到指定 URL。
- **用途**：打开一个全新页面

### `chrome-devtools__navigate_page(type, url)`
在当前选中标签页中导航到指定 URL。
- `type="url"` → 跳转到新地址
- `type="reload"` → 刷新当前页
- **用途**：在已登录的标签页内跳转到目标页面（避免登录状态丢失）

### `chrome-devtools__take_snapshot()`
获取当前页面的无障碍树（a11y tree），返回所有可见元素及其 `uid`。
- **用途**：读取页面内容（邮件列表、推文、正文等）；获取可交互元素的 `uid` 供后续点击/输入使用
- **注意**：页面加载中时需等待后再调用

### `chrome-devtools__click(uid)`
点击页面中指定 `uid` 的元素。
- **用途**：打开邮件、点击按钮、展开折叠内容

### `chrome-devtools__fill(uid, value)`
向指定 `uid` 的输入框填入文本。
- **用途**：填写搜索框、表单输入

### `chrome-devtools__wait_for(text)`
等待页面出现指定文本后再继续。
- **用途**：等待页面加载完成，避免在未加载时读取空内容

### `chrome-devtools__take_screenshot()`
截取当前页面截图（返回图片）。
- **用途**：当 snapshot 无法准确反映页面状态时，用截图辅助判断

---

## 三、常见任务流程

### 查看 Outlook 邮件（支持任意 Outlook 账号）

```
1. chrome-devtools__list_pages
   → 查找 URL 含 "outlook.cloud.microsoft" 的标签页

2. 若存在已登录标签：
   chrome-devtools__select_page(pageId=N)
   chrome-devtools__take_snapshot()
   → 读取收件箱邮件列表

3. 若不存在：
   chrome-devtools__new_page(url="https://outlook.cloud.microsoft/mail/")
   → 提示用户手动登录，完成后告知 AI 继续

4. 点击目标邮件：
   chrome-devtools__click(uid="邮件元素uid")
   chrome-devtools__take_snapshot()
   → 读取邮件正文
```

### 搜索 X（Twitter）内容

> ⚠️ **X 无法在未登录状态下访问**：必须依赖浏览器中已保存的登录 Cookie，不能从零打开登录页。

```
1. chrome-devtools__list_pages
   → 查找已登录 X 的标签页（URL 含 "x.com"）

2. 若存在：
   chrome-devtools__select_page(pageId=N)
   chrome-devtools__navigate_page(type="url", url="https://x.com/search?q=关键词&f=live")
   chrome-devtools__wait_for(text="推文关键词或用户名")
   chrome-devtools__take_snapshot()
   → 读取推文列表并总结

3. 若不存在：
   → 提示用户先在浏览器手动登录 X，完成后告知 AI 继续
```

---

## 四、故障排查

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| `Could not find DevToolsActivePort` | Chrome 未开启调试 | 重新在 `chrome://inspect` 开启远程调试 |
| `Could not find Chrome Beta executable` | MCP 含 `--channel=beta` | 去掉该参数，重启网关 |
| `gateway closed (1008): pairing required` | OpenClaw 网关配对失效 | 重启 OpenClaw 或重新配对 |
| Outlook 跳转到产品宣传页 | 浏览器未登录或标签错误 | 用 `list_pages` 找 `outlook.cloud.microsoft` 标签并 `select_page` |
| X 跳转到登录页 | 未登录或 Cookie 失效 | 用户手动在浏览器登录 X 后告知 AI |
| 页面内容为空 | 页面尚未加载完成 | 先调用 `wait_for` 等待关键文字出现 |
