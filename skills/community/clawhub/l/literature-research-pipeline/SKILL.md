---
name: literature-research-pipeline
description: 端到端学术文献检索与下载全流程自动化。当用户请求检索文献、下载论文、查找学术资料、搜索论文，或提到"帮我找XX相关的文献"、"下载这篇论文"、"需要某篇文献"时触发本技能。完整流程：检索 → 推荐 → 多渠道下载 → 科研通常控监控 → 通知 → 进度追踪。
env:
  - name: LIT_DOWNLOAD_DIR
    required: true
    description: 论文下载保存目录
  - name: LIT_PROGRESS_FILE
    required: true
    description: 下载进度追踪文件路径
  - name: LIT_CDP_PORT
    required: false
    default: "9334"
    description: 浏览器远程调试端口
  - name: LIT_NOTIFY_CHANNEL
    required: false
    description: 通知渠道（如 wechat-access、telegram 等）
  - name: LIT_NOTIFY_USER
    required: false
    description: 通知目标用户 ID
  - name: SEMANTIC_SCHOLAR_API_KEY
    required: false
    description: Semantic Scholar API 密钥
  - name: LIT_UNPAYWALL_EMAIL
    required: false
    description: Unpaywall API 所需邮箱
permissions:
  - browser-cdp
  - filesystem-read
  - filesystem-write
  - cron
  - subprocess
---

# 文献检索与下载全流程

## 概述

端到端学术文献检索与下载自动化。接收用户的研究主题 → 检索文献 → 推荐高价值目标 → 多渠道下载 → 科研通常控监控 → 应助后自动下载 → 通知用户。

---

## 环境变量与配置

本技能依赖以下环境变量（需在首次使用前配置）：

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `LIT_DOWNLOAD_DIR` | 是 | 论文下载保存目录 | `~/Downloads` |
| `LIT_PROGRESS_FILE` | 是 | 下载进度追踪文件路径 | `memory/literature-progress.md` |
| `LIT_CDP_PORT` | 否 | 浏览器远程调试端口（默认 9334） | `9334` |
| `LIT_NOTIFY_CHANNEL` | 否 | 通知渠道（如 wechat-access、telegram 等） | `wechat-access` |
| `LIT_NOTIFY_USER` | 否 | 通知目标用户 ID | `your-user-id` |
| `SEMANTIC_SCHOLAR_API_KEY` | 否 | Semantic Scholar API 密钥 | `your-key` |
| `LIT_UNPAYWALL_EMAIL` | 否 | Unpaywall API 所需邮箱 | `your-email@example.com` |

**首次使用时**，AI 应检查以上变量是否已配置。若缺失，主动询问用户并引导配置。
若用户未配置通知渠道，跳过通知步骤，仅在对话中告知结果。

---

## 流程概览

```
1. 文献检索  →  2. 结果展示  →  3. 用户确认  →  4a. 直接下载成功
                                                   ↓ (失败)
                                               4b. 科研通求助
                                                   ↓
                                               5. 建立Cron监控
                                                   ↓
                                               6. 应助 → 自动下载 → 通知用户
                                                   ↓
                                               7. 告知用户 + 更新进度
```

---

## Step 1：文献检索

**必须先读取 academic-literature-search 技能**，路径通过以下方式定位：
1. 优先查找当前 workspace 下的 `skills/academic-literature-search/SKILL.md`
2. 其次查找 `~/.qclaw/skills/academic-literature-search/SKILL.md`
3. 若均不存在，提示用户先安装 academic-literature-search skill

使用其 `scripts/search.py` 执行检索：

```python
import subprocess, os

# 自动定位脚本路径
workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.qclaw/workspace"))
search_script = os.path.join(workspace, "skills/academic-literature-search/scripts/search.py")

result = subprocess.run([
    "python3", search_script,
    "--query", "用户的研究主题",
    "--databases", "semantic_scholar,crossref",
    "--max_results", "20",
    "--output_format", "json"
], capture_output=True, text=True)
```

**优先选择 Crossref 数据库**（DOI 数据最权威，可靠性高）。

**检索完成后立即检查每篇文献的 `is_open_access` 字段**：
- `open_access = true` → 标记为可尝试 Unpaywall 直接下载
- `open_access = false` → 直接规划科研通求助路线，避免在无效渠道浪费时间

---

## Step 2：结果展示

呈现检索结果时使用以下格式（Markdown）：

```
## 📚 文献检索结果（共 N 篇）

| # | 标题 | 作者 | 年份 | 期刊/会议 | DOI | 引用 | 开放获取 |
|---|------|------|------|-----------|-----|------|----------|
| 1 | ... | ... | 2023 | ... | 10.xxxx/xxx | 45 | ✅ |

### 🎯 高价值推荐

1. **[论文标题1]**（推荐理由）
   - DOI：`10.xxxx/xxx`
   - 亮点：...
2. **[论文标题2]**（推荐理由）
   - DOI：`10.xxxx/xxx`
```

**推荐标准**：高引用数 / 最新年份 / 开源可获取 / 直接相关用户主题

---

## Step 3：确认用户需求

展示结果后，**询问用户**：「请告诉我想下载哪些论文（序号或标题），或者让我推荐？」

等待用户回复后，对每篇目标论文记录：
- DOI、标题、发表年份
- 是否开放获取
- 目标下载优先级

---

## Step 4a：多渠道直接下载

按以下优先级逐个尝试：

### 渠道 1：Unpaywall（最快）
```
GET https://api.unpaywall.org/v2/{DOI}?email={LIT_UNPAYWALL_EMAIL}
```
- 响应中取 `best_oa_location.landing_page` 或 `best_oa_location.url_for_pdf`
- 注意：Unpaywall 有频率限制，每小时 ≤ 5000 请求

### 渠道 2：DOI.org 重定向
```
GET https://doi.org/{DOI}
（跟随重定向，查找 Content-Type: application/pdf 的最终 URL）
```
- 若重定向至 Springer/IEEE/Elsevier → 返回 418 或需登录 → 放弃此渠道

### 渠道 3：Semantic Scholar PDF
```
GET https://api.semanticscholar.org/graph/v1/paper/{DOI}/PDF
（需设置 API Key：SEMANTIC_SCHOLAR_API_KEY）
```

### 渠道 4：Crossref PDF 链接
```
GET https://api.crossref.org/works/{DOI}
（从响应中取 `link` 字段）
```

**成功标准**：文件以 `%PDF` 开头（Magic Bytes），大小 > 50 KB
**失败处理**：记录失败原因（418 / 403 / 404 / 无 OA 版本），转向 Step 4b

---

## Step 4b：科研通常控求助

### 前置条件
- 用户已登录浏览器，开启了远程调试端口（默认 `LIT_CDP_PORT`，通常为 9334）
- 参考命令（Mac）：`"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --remote-debugging-port=9334 "--remote-allow-origins=*"`
- 参考命令（Linux）：`google-chrome --remote-debugging-port=9334 --remote-allow-origins=*`

### 步骤 4b-1：发布求助帖

通过 CDP 连接浏览器，在 `https://www.ablesci.com/assist/create` 发布求助：

**关键参数获取**（每次操作前必须从页面重新获取）：
1. **CSRF Token**：从页面 `<meta name="csrf-token">` 提取
2. **Cookie**：通过 `Network.getAllCookies` 获取所有 ablesci.com 域名下的 cookie
3. **标签页**：每次操作前重新 `list_tabs()` 并 attach，不要缓存 tab ID

**发布 API**：
```
POST https://www.ablesci.com/assist/create
Content-Type: application/x-www-form-urlencoded

_csrf={token}&title={标题}&content={内容}&tag_id={分类ID}
```

**求助帖标题建议格式**：`【求助全文】【期刊名+年份】论文标题`
**求助帖内容建议**：包含 DOI、论文标题、作者、发表信息

### 步骤 4b-2：记录求助状态

每篇论文发布后，更新**下载进度追踪表**（路径：`LIT_PROGRESS_FILE`）：

```markdown
## 📥 文献下载进度

| 论文 | DOI | 状态 | 来源 | 备注 |
|------|-----|------|------|------|
| 论文标题1 | 10.xxxx/xxx | ✅ 已下载 | ablesci 应助 | 保存路径 |
| 论文标题2 | 10.xxxx/xxx | ⏳ 求助中 | 科研通 | ID: xxx |
```

---

## Step 5：建立 Cron 监控任务

### 读取 qclaw-cron-skill 获取正确的 cron 配置语法
路径：`~/Library/Application Support/QClaw/openclaw/config/skills/qclaw-cron-skill/SKILL.md`

### 监控任务配置

每 **30 分钟**检查一次科研通常控状态：

**Schedule**：
```json
{"kind": "every", "everyMs": 1800000}
```

**Payload（isolated session）**：
```json
{
  "kind": "agentTurn",
  "message": "检查科研通常控求助帖状态...\n\n1. 读取进度文件（LIT_PROGRESS_FILE）获取当前进度\n2. 通过 CDP 连接浏览器（http://127.0.0.1:{LIT_CDP_PORT}）\n3. 逐个访问求助帖详情页（URL格式：https://www.ablesci.com/assist/detail?id={帖子ID}）\n4. 检查每篇论文的状态：\n   - 求助中 → 无操作\n   - 待确认（有人上传）→ 自动下载（见下方下载流程）\n   - 已完成 → 无操作\n5. 如有新应助（状态：待确认）：\n   a. 提取下载页面链接\n   b. 通过浏览器触发下载\n   c. 更新进度文件\n   d. 通知用户（若已配置通知渠道）\n6. 如全部论文已下载完成，通知用户并删除 cron 监控任务"
}
```

**Delivery**（仅在配置了通知渠道时设置）：
```json
{
  "mode": "announce",
  "channel": "{LIT_NOTIFY_CHANNEL}",
  "to": "{LIT_NOTIFY_USER}"
}
```

**注意**：`sessionTarget = "isolated"`（必须），`payload.kind = "agentTurn"`

### 通知模板

```
📥 论文下载完成！

论文：{标题}
来源：{来源}
保存位置：{LIT_DOWNLOAD_DIR}/{文件名}
状态：{进度表更新}
```

---

## Step 6 & 7：自动下载与进度更新

当 cron 任务检测到新应助时：

1. **提取下载 ID**：从详情页 HTML 中解析下载链接
2. **触发下载**：
   - 新建标签页打开下载链接
   - 执行 `Page.setDownloadBehavior(behavior=allow, downloadPath={LIT_DOWNLOAD_DIR})`
   - 等待文件从 `.crdownload` 变为 `.pdf`（通常 5-30 秒）
3. **重命名文件**：去掉 `(科研通-ablesci.com)` 等后缀，保留年份信息
4. **验证 PDF**：文件头为 `%PDF`，大小 > 50 KB
5. **更新进度表**：`LIT_PROGRESS_FILE`
6. **通知用户**（若已配置通知渠道）

---

## 关键坑点记录（来自实战经验）

### CDP 操作时序问题
- `accessibility tree ref` 和 `backendDOMNodeId` 在跨调用后会失效
- **解决**：每次操作前重新获取 ref，不跨步缓存
- 优先使用 `DOM.querySelectorAll` + `DOM.resolveNode` 获取 `objectId`，再发送 `Input.dispatchMouseEvent`

### 科研通常控下载特殊机制
- API `file/request-download-token` 返回 code=0 但 **不返回 URL**
- 实际下载通过浏览器 XHR 流式传输，触发后等待浏览器自动下载
- **file_server=2** 对应普通线路，`file_server=3` 对应高速线路

### 常见下载失败原因
- IEEE/Elsevier 等商业出版社：返回 418（IP/地区限制）或 403（需登录）
- 无开放获取版本：Unpaywall 查不到 → 直接转向科研通

---

## 依赖技能

| 技能 | 用途 | 安装方式 |
|------|------|----------|
| academic-literature-search | Crossref/Semantic Scholar 文献检索 | `skillhub install academic-literature-search` |
| browser-cdp | CDP 浏览器自动化 | 内置或 `skillhub install browser-cdp` |
| qclaw-cron-skill | 定时任务管理 | 内置 |
