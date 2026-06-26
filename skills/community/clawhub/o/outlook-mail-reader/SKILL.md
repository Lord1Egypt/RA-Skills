---
name: outlook-mail-reader
description: 通过 MCP chrome-devtools 协议控制用户本地 Chrome 浏览器，查询 Outlook 邮件。支持按日期跳转、筛选、搜索邮件。使用前提：用户已在 Chrome 中开启远程调试（127.0.0.1:9222 或 18800），且 OpenClaw 已配置 chrome-devtools-mcp 或 browser 工具可用。触发场景：查看邮件、按日期查邮件、Outlook 收件情况、读邮件正文。
---

# M5Stack | Outlook 邮件查询 Skill（通过 Chrome MCP）

通过 MCP 协议控制用户本地 Chrome 浏览器，完成 Outlook 邮件查看、按日期跳转、筛选等操作。

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

## 二、工具选择策略（重要！）

### `chrome-devtools__*` 工具 vs `browser` 工具

两套工具都可以控制 Chrome，**优先按以下顺序尝试**：

1. **先用 `chrome-devtools__list_pages`** 确认连接状态
2. 如果返回 `"Could not find DevToolsActivePort"` → 用户未开启调试，引导用户开启
3. 如果返回 `"The browser is already running..."` 错误 → **切换到 `browser` 工具**，不要继续尝试 `chrome-devtools__*`

```
chrome-devtools__list_pages 失败（already running 错误）
  → 改用 browser(action="tabs") 列出标签页
  → 改用 browser(action="navigate", targetId=...) 导航
  → 改用 browser(action="snapshot") 读取页面
  → 改用 browser(action="act", request={kind:"click", ref:...}) 点击
```

**不要在同一次任务中反复切换工具**，确定哪套有效后全程使用那套。

---

## 三、MCP 工具说明

### chrome-devtools 系列

| 工具 | 用途 |
|------|------|
| `chrome-devtools__list_pages` | 列出所有标签页，返回 pageId 和 URL |
| `chrome-devtools__select_page(pageId)` | 切换到指定标签页 |
| `chrome-devtools__navigate_page(type, url)` | 在当前标签页导航到 URL |
| `chrome-devtools__take_snapshot()` | 获取页面 a11y 树，返回所有元素及 uid |
| `chrome-devtools__click(uid)` | 点击指定 uid 元素 |
| `chrome-devtools__fill(uid, value)` | 向输入框填入文本 |
| `chrome-devtools__wait_for(text)` | 等待页面出现指定文本 |

### browser 系列（chrome-devtools 不可用时的备用）

| 工具调用 | 用途 |
|----------|------|
| `browser(action="tabs")` | 列出所有标签页，返回 targetId 和 URL |
| `browser(action="navigate", targetId=..., url=...)` | 在指定标签页内导航 |
| `browser(action="snapshot", targetId=...)` | 获取页面 a11y 树，返回 ref 供点击 |
| `browser(action="act", request={kind:"click", ref:...}, targetId=...)` | 点击页面元素（用 ref 而非 uid）|
| `browser(action="act", request={kind:"fill", ref:..., text:...}, targetId=...)` | 填写输入框 |
| `browser(action="act", request={kind:"press", key:"Escape"}, targetId=...)` | 按键操作 |

---

## 四、Outlook 邮件查询完整流程

### 步骤 1：找到已登录的 Outlook 标签页

```
browser(action="tabs")
→ 查找 URL 含 "outlook.cloud.microsoft" 或 "outlook.office.com" 的标签页
→ 记录其 targetId
```

若不存在已登录标签：
```
browser(action="open", url="https://outlook.cloud.microsoft/mail/")
→ 提示用户手动登录，完成后告知 AI 继续
```

### 步骤 2：进入收件箱

```
browser(action="navigate", targetId=<已登录标签的targetId>, url="https://outlook.cloud.microsoft/mail/inbox")
browser(action="snapshot", targetId=...)
→ 读取邮件列表（按日期分组：本周/上周/上个月/各月）
```

### 步骤 3：按日期跳转（核心功能）

Outlook 邮件列表工具栏有一个 **"跳转到"按钮**，点击后弹出日期选择菜单。

**正确操作流程：**

```
1. snapshot → 在邮件列表工具栏找到 button "跳转到"（ref 或 uid）
   位置：邮件列表顶部，"选择"按钮右侧，"筛选器"按钮左侧

2. 点击"跳转到"按钮
   browser(action="act", request={kind:"click", ref:"跳转到按钮的ref"})

3. 弹出菜单包含：
   - menuitemradio "今天"
   - menuitemradio "昨天"
   - menuitemradio "上周"
   - menuitemradio "上个月"
   - menuitemradio "去年"
   - combobox（日期输入框，默认值为今天日期，格式 YYYY/M/D）
   - button "转到 YYYY/M/D"（确认跳转按钮）

4a. 快捷选项：直接点击对应 menuitemradio
    例如查看去年：点击 menuitemradio "去年"

4b. 指定日期：
    → fill combobox，输入目标日期（格式：YYYY/M/D，例如 "2025/1/1"）
    → 点击 button "转到 YYYY/M/D"（开始）

5. 邮件列表自动跳转到对应日期位置
   snapshot → 读取该时间段的邮件
```

> ⚠️ **注意事项**：
> - 日期格式必须是 `YYYY/M/D`（斜杠分隔，月日不补零）
> - 按 Escape 可关闭菜单
> - 跳转后邮件列表仍按日期分组，需继续向上/下滚动加载更多

### 步骤 4：读取邮件正文

```
snapshot → 找到目标邮件的 option 元素（包含发件人、主题、预览）
→ 点击该邮件
→ snapshot → 读取右侧阅读窗格的正文内容
```

### 步骤 5：搜索特定邮件（可选）

```
snapshot → 找到搜索框 combobox "搜索电子邮件、会议、文件等。"
→ fill 搜索框，输入关键词（发件人名/主题/日期关键词）
→ 等待搜索结果出现
→ snapshot → 读取结果列表
```

---

## 五、常见错误与正确做法

| 错误做法 | 正确做法 |
|---------|---------|
| 用 `chrome-devtools__*` 遇到 "already running" 后继续重试 | 立即切换到 `browser` 工具 |
| 导航到 `outlook.live.com`（会跳转到产品宣传页） | 使用 `outlook.cloud.microsoft/mail/` |
| 试图直接操作日历弹窗 UI（交互复杂） | 使用"跳转到"按钮的菜单选项或日期输入框 |
| 在日期输入框输入 `2025-01-01` | 使用 `2025/1/1` 格式 |
| 跳转日期后只读一屏内容 | 继续 snapshot + 滚动加载更多邮件 |
| 没有找到 Outlook 标签就直接 open 新页面 | 先用 tabs 检查是否已有登录标签 |

---

## 六、故障排查

| 问题 | 原因 | 解决方法 |
|------|------|---------| 
| `Could not find DevToolsActivePort` | Chrome 未开启调试 | 在 `chrome://inspect` 重新开启远程调试 |
| `The browser is already running...` | chrome-devtools MCP 冲突 | 切换到 `browser` 工具 |
| `Could not find Chrome Beta executable` | MCP 含 `--channel=beta` | 去掉该参数，重启网关 |
| Outlook 跳转到产品宣传页 | URL 错误或未登录 | 用 tabs 找 `outlook.cloud.microsoft` 标签并 navigate |
| 页面内容为空 | 页面尚未加载完成 | 等待 2-3 秒后再 snapshot |
| 点击"跳转到"后菜单未出现 | snapshot 可能过时 | 重新 snapshot 确认 ref |
