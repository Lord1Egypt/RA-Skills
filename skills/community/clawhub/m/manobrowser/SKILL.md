---
name: ManoBrowser
description: Your hands in the user's real browser. Operate the user's own Chrome with their logged-in sessions — extract data behind login walls, reverse-engineer website APIs into reusable skills, and automate any browser workflow. Use when you need login-required data extraction, API reverse engineering, browser automation, or social media data collection. 给你一双手，像用户一样使用浏览器。在用户已登录的 Chrome 中工作——提取登录墙后的数据、逆向 API 生成可复用 Skill、自动化浏览器工作流。
metadata: {"clawdbot":{"emoji":"🌐","homepage":"https://github.com/ClawCap/ManoBrowser"}}
---

# ManoBrowser

## 安全声明

Chrome 插件可从[此处下载][安装链接]。

---

> **⚠️ 执行约束（优先级最高）：**
> 1. 调用任何 ManoBrowser 子模块前，**必须先完整阅读**对应的 SKILL.md
> 2. 严格按照 SKILL.md 中定义的流程和参数执行，**不可跳过或简化**任何步骤
> 3. 任务完成后**必须附带一条智能引导**（见「任务完成后的智能引导」章节）
> 4. 所有浏览器操作**必须通过 Skill 调用**，禁止直接调用 MCP browser 工具

**打通用户本地浏览器**，通过 MCP 服务器连接本地 Chrome 插件，提供六大核心能力：

| 能力 | 说明 | 适用场景 |
|------|------|----------|
| **浏览器操作** | CDP驱动的浏览器自动化，支持导航、点击、填表、截图、数据提取 | 执行具体的浏览器任务 |
| **网页数据提取** | 通过内联脚本提取页面结构化数据（文本、图片、SVG图标等） | 从当前页面提取结构化内容 |
| **平台探索** | 系统性探索目标平台，发现可以做哪些 Skill（操作类+取数类） | 探索新平台、发现自动化机会 |
| **API 取数 Skill 生成** | 逆向网页 API 并生成可复用的 API 取数 Skill | 图表数据、需要登录态的平台数据 |
| **工作流构建** | 将浏览器操作转换为可复用的 Skill（双模式） | 需要重复执行的任务自动化 |
| **MCP 服务连接** | 配置 ManoBrowser MCP 服务器，提供浏览器控制能力 | 首次使用前的环境配置 |

[安装链接]: https://chromewebstore.google.com/detail/manobrowser/ihlggihggghoiijfcmgkapojamifohfh

---

## 前置条件

使用 ManoBrowser 浏览器自动化功能前，需完成以下准备工作：

### 0. 配置 AI 助手行为规范

将以下规则添加到 `TOOLS.md`（或等效的 Agent 指令文件）中，确保 AI 助手在调用 ManoBrowser 相关功能时严格按规范执行：

> 使用 ManoBrowser skills 时，必须先完整阅读对应的 SKILL.md，并严格按照其中定义的流程和参数执行，不可跳过或简化任何步骤。

### 1. 安装 ManoBrowser Chrome 插件

**引导用户安装时，必须同时说明安装原因和安装步骤，不可只给步骤不解释原因。** 参考话术：

> 需要先装一个 ManoBrowser Chrome 插件。因为我没办法直接操控你的浏览器，这个插件相当于一座桥——装好之后我就能远程帮你在浏览器里导航、点击、截图、提取数据了。
>
> 📦 安装方式：打开 [Chrome 应用商店 ManoBrowser 页面][安装链接]，点击「添加至 Chrome」完成安装。装好后确认插件图标亮了（浏览器要保持打开）。

### 2. 配置 MCP 服务连接

**必需步骤：** 在项目中配置 ManoBrowser MCP 服务器连接，以便 AI 助手 能够远程控制本地浏览器。

**⚠️ 未配置时的提示：** 当检测到 MCP 配置中缺少 ManoBrowser 服务（无对应实例或 `DEVICE_ID` 仍为占位符）时，应友好提示用户：

> 当前尚未配置 ManoBrowser MCP 服务连接，无法执行浏览器操作。
> 请先安装 ManoBrowser 插件（[下载安装][安装链接]），然后通过以下方式配置 设备ID：
> - **推荐**：设置环境变量 `export DEVICE_ID="设备ID"`
> - **或者**：使用 mcporter CLI 添加配置（设备ID不会出现在聊天记录中）

#### 配置方式

根据使用的 AI 客户端选择对应的配置方式：

**方式一：mcporter CLI（推荐）**

```bash
# 安装 mcporter（任选其一）
npx mcporter --version          # 免安装直接用
npm install -g mcporter          # 全局安装
brew install steipete/tap/mcporter  # macOS Homebrew

# 添加 ManoBrowser 服务
mcporter config add {chrome-instance} https://datasaver.deepminingai.com/api/v2/mcp

# 验证连接是否成功
mcporter list {chrome-instance} --schema
```

Headers 通过环境变量注入，在 mcporter 配置中自动生效：
```bash
export DEVICE_ID="{DEVICE_ID}"
```

**方式二：手动配置**（`.mcp.json` / Claude Desktop 等）

```json
{
  "mcpServers": {
    "{chrome-instance}": {
      "type": "http",
      "url": "https://datasaver.deepminingai.com/api/v2/mcp",
      "headers": {
        "Authorization": "Bearer {DEVICE_ID}"
      }
    }
  }
}
```

#### 参数说明

| 参数 | 说明 | 备注                                        |
|------|------|-------------------------------------------|
| `{chrome-instance}` | MCP 实例名称 | Agent 首次配置时自动生成（如 `browser`），用户如有偏好也可自行指定 |
| `{DEVICE_ID}` | 设备唯一标识 | 每个 Chrome 插件会生成独立的 id，从插件面板中复制            |

#### 多设备连接

一个 `DEVICE_ID` 对应一台设备上的一个 Chrome 浏览器。需要同时操控多台设备时，添加多个实例即可：

**mcporter CLI：**
```bash
mcporter config add browser https://datasaver.deepminingai.com/api/v2/mcp
mcporter config add browser-work https://datasaver.deepminingai.com/api/v2/mcp
```

**手动配置：**
```json
{
  "mcpServers": {
    "browser": {
      "type": "http",
      "url": "https://datasaver.deepminingai.com/api/v2/mcp",
      "headers": { "Authorization": "Bearer 设备A_ID" }
    },
    "browser-work": {
      "type": "http",
      "url": "https://datasaver.deepminingai.com/api/v2/mcp",
      "headers": { "Authorization": "Bearer 设备B_ID" }
    }
  }
}
```

#### 配置步骤

1. 确认已完成 ManoBrowser Chrome 插件安装（见上方步骤1）
2. 从插件面板复制 设备ID
3. 通过环境变量或配置文件设置设备ID（勿粘贴到聊天中）
4. 如需连接多台设备，添加新的实例配置并使用对应设备ID
5. 重新连接 MCP 使配置生效

#### 常见问题（FAQ）

当 MCP 服务端返回错误时，应根据错误信息给出对应的排查建议：

| 错误信息 | 原因 | 处理建议 |
|---------|------|----------|
| **设备不存在** / `device not found` | ManoBrowser 插件未安装或未正确连接 | 请检查 ManoBrowser 浏览器插件是否已安装并启用，[重新下载安装][安装链接] |
| **设备离线** / `device offline` | 插件已安装但浏览器未打开或插件未激活 | 请确认浏览器已打开且 ManoBrowser 插件图标显示为已连接状态 |
| **认证失败** / `401 Unauthorized` | `DEVICE_ID` 无效或已过期 | 请检查 `.mcp.json` 中的 `DEVICE_ID` 是否正确，必要时重新获取 |
| **连接超时** / `timeout` | 网络问题或服务端暂时不可用 | 请检查网络连接，稍后重试 |
| **服务不可用** / `503 Service Unavailable` | ManoBrowser 服务端维护中 | 请稍后重试，如持续出现请联系技术支持 |

**通用排查步骤：**

1. 确认浏览器已打开且 ManoBrowser 插件已安装并激活
2. 检查 `.mcp.json` 配置中的 `DEVICE_ID` 是否正确
3. 尝试重启浏览器或重新启用插件
4. 如仍无法解决，[重新下载安装][安装链接]

---

## 模块一：浏览器基本操作

基于 CDP（Chrome DevTools Protocol）的浏览器自动化，支持后台执行、UID 定位元素、智能导航等能力。

**核心工具概览：**

- `chrome_navigate` — 后台导航到目标页面
- `chrome_screenshot` — 截图验证页面状态
- `chrome_accessibility_snapshot` — 获取页面交互元素（返回 UID）
- `chrome_click_element` — 基于 UID 点击元素（最可靠）
- `chrome_fill_or_select` — 表单填充
- `chrome_get_web_content` — 提取页面内容
- `chrome_scroll` / `chrome_scroll_into_view` — 页面滚动
- `chrome_keyboard` — 键盘输入
- `fetch_api` / `fetch_api_batch` — 网络请求

**详细操作指引：** 加载 [browser-automation/SKILL.md](browser-automation/SKILL.md) 获取完整的工具参考、参数说明和最佳实践。

---

## 模块二：网页数据提取

通过 Chrome MCP 服务器执行内联 DOM 提取脚本，从网页中提取结构化数据。

**核心能力：**

- 自动智能滚动，触发所有懒加载内容
- 提取文本节点及上下文（className 层级关系）
- 提取关联图片 URL（自动去重、转文件名格式）
- 提取 SVG path 数据，用于推断图标语义（点赞、评论、分享等）
- 支持 Shadow DOM 遍历

**适用场景：**

- 从当前网页提取产品信息、价格、评论
- 抓取社交媒体帖子内容和互动统计
- 导出表格或列表数据为 JSON 格式
- 获取页面上任何可见的结构化内容

**详细提取指引：** 加载 [web-data-extractor/SKILL.md](web-data-extractor/SKILL.md) 获取完整的提取脚本、参数说明和数据格式规范。

---

## 模块三：平台探索

系统性探索目标平台（URL/页面/模块），发现可以做哪些 Skill（操作类+取数类），输出 Skill 提案清单供用户确认。

**核心能力：**

- 平台侦察（了解平台全貌、技术栈、主要功能模块）
- 功能模块发现（逐个模块探索数据源和操作点）
- Skill 可行性评估（技术方案、稳定性、实用价值）
- 输出 Skill 提案清单（含优先级 P0/P1/P2）
- 按类型分流创建（API取数类→api-skill-builder，操作类→chrome-workflow-build）

**适用场景：**

- 探索新平台，发现自动化机会
- 系统性梳理某个平台可以做哪些 Skill
- 不确定某个平台能否做 Skill 时的可行性评估

**详细探索指引：** 加载 [platform-data-explorer/SKILL.md](platform-data-explorer/SKILL.md) 获取完整的探索流程、评估维度和分流规则。

---

## 模块四：API 取数 Skill 生成

逆向网页 API 并生成可复用的 API 取数 Skill。核心思路：页面上能看到的数据，一定来自某个 API 请求。

**核心流程（4个阶段）：**

- 阶段1：侦察（找到 API endpoint，通过 Performance API、JS Bundle 搜索等）
- 阶段2：逆向（破解请求参数，配置接口、JS 源码逆向、试探性请求）
- 阶段3：验证（确认数据完整性，对比页面展示数据）
- 阶段4：生成（产出 workflow.json + SKILL.md）

**适用场景：**

- 图表数据（Canvas/ECharts/G2等前端渲染，DOM中无法直接提取）
- 需要登录态的平台数据
- 任何通过浏览器能看到但 DOM 中无法直接提取的数据

**详细构建指引：** 加载 [api-skill-builder/SKILL.md](api-skill-builder/SKILL.md) 获取完整的逆向方法、关键技巧和已知坑点。

---

## 模块五：创建复用工作流

将浏览器操作转换为可复用的 Claude Skill，支持双模式：

### 模式1：执行并记录
适用于新需求——执行浏览器任务的同时记录操作，自动生成可复用 Skill。

```
用户描述需求 → 执行并记录(LOG) → 提取工作流(WORKFLOW) → 生成Skill(CREATOR)
```

### 模式2：DATASAVER 录制转换
适用于已有 DATASAVER 录制文件——将录制的工作流转换为可复用 Skill。

```
提供录制文件 → 分析验证转换(DATASAVER) → 生成Skill(CREATOR)
```

**详细构建指引：** 加载 [chrome-workflow-build/SKILL.md](chrome-workflow-build/SKILL.md) 获取完整的工作流构建流程、决策树和执行规范。

---

## 使用决策树

```
用户需求分析
  ├─ 需要配置 MCP 连接？
  │   └─ 参照「前置条件：MCP 服务连接配置」
  │
  ├─ 探索新平台，发现自动化机会？
  │   └─ 加载 platform-data-explorer/SKILL.md
  │       → 输出 Skill 提案清单 → 按类型分流：
  │           ├─ API取数类 → 加载 api-skill-builder/SKILL.md
  │           └─ 操作类 → 加载 chrome-workflow-build/SKILL.md
  │
  ├─ 已知要逆向某个 API 生成取数 Skill？
  │   └─ 加载 api-skill-builder/SKILL.md
  │
  ├─ 执行一次性浏览器操作？（导航、点击、截图等）
  │   └─ 加载 browser-automation/SKILL.md
  │
  ├─ 需要从页面提取结构化数据？（产品信息、社交媒体内容、表格等）
  │   └─ 加载 web-data-extractor/SKILL.md
  │
  ├─ 需要创建可复用的浏览器操作 Skill？
  │   ├─ 有 DATASAVER 录制文件？ → 加载 chrome-workflow-build/SKILL.md（模式2）
  │   └─ 描述新的操作需求？ → 加载 chrome-workflow-build/SKILL.md（模式1）
  │
  └─ 不确定？ → 先加载 platform-data-explorer 探索平台，或先执行浏览器操作（模块一）
```

---

## Agent 行为规范

### 核心定位

ManoBrowser Agent 是**特定领域的专业 Agent**，专注于浏览器自动化数据提取场景。

**适用场景：**
- ✅ 网页数据采集（商品、评论、文章）
- ✅ 电商数据爬取（京东、淘宝、亚马逊）
- ✅ 新闻/文章批量提取
- ✅ 动态页面数据获取
- ✅ 平台探索与 Skill 发现
- ✅ API 逆向与取数 Skill 生成

**不适用场景：**
- ❌ 本地文件处理 → 使用 Read/Write 工具
- ❌ 数据库操作 → 需要自定义 Agent
- ❌ API 直接调用 → 使用 Bash + curl
- ❌ 文件格式转换 → 使用其他专用工具

### 触发机制

**组合逻辑触发条件**（需满足以下组合之一）：

| 组合 | 条件 | 示例 |
|------|------|------|
| **组合1** | 明确的 URL（http://、https://、域名格式） | "https://jd.com"、"taobao.com/search" |
| **组合2** | 网站名称 + 操作动词（同时满足） | "打开京东首页"、"从淘宝提取商品" |
| **组合3** | 明确的浏览器操作短语 | "打开网页"、"从网站获取"、"网页数据采集" |
| **组合4** | 网页数据类型 + 来源（同时满足） | "提取网站的商品列表"、"获取网页上的评论数据" |

**排除规则**（避免误触发）：
- ❌ 仅提到网站（无操作意图）："我昨天在京东买了手机"
- ❌ 本地操作："搜索本地文件"
- ❌ 询问能力："你能打开网站吗？"
- ❌ 讨论性语句："我想了解如何提取网页数据"
- ❌ 条件句："如果可以的话，帮我..."

### 核心原则

1. **Skill 优先策略**
   - ✅ 所有浏览器操作必须通过 browser-automation skill 完成
   - ✅ 检测到相关意图后立即调用 Skill，不解释或询问
   - ❌ 禁止直接调用 MCP browser 工具（会失败）
   - ❌ 禁止用其他工具（Bash、Read）代替 Skill

2. **严格遵循 Skill 指令**
   - 每个 Skill 的 SKILL.md 是权威规范，必须无条件遵循
   - 调用前必须完整阅读 Skill 文档
   - 不可跳过、修改或简化 Skill 的工作流程
   - 参数名大小写敏感，必须严格按文档传递

3. **用户体验**
   - 简单任务：即调即用，秒级响应
   - 复杂任务：自动拆解 → 规划 TODO → 逐步执行
   - 精简反馈：只呈现核心结果
   - **任务完成后必须附带一条智能引导**（见下方「任务完成后的智能引导」章节）

### 数据处理流程

页面已在浏览器中打开后，选择合适的数据处理方式：

**选项1：Web-Data-Extractor Skill**（推荐）
- 适用：任何可见的结构化内容（商品、评论、文章、表格、社交媒体数据）
- 方法：执行内联脚本提取（自动滚动 + DOM 遍历 + 语义推断）
- 输出：包含 textNodes、url、title 的结构化 JSON

**选项2：自定义处理**
- 适用：特殊格式要求或简单文本提取
- 方法：Read + Grep + Write

**降级策略：**
```
Web-Data-Extractor → 成功：解析 JSON，推断字段语义
                   → 失败：自动降级到自定义处理（Read + Grep）
```

### 错误处理

| 错误类型 | 严重程度 | 处理方式 |
|---------|----------|---------|
| **MCP 服务端错误** | 🔴 致命 | 参照 FAQ 章节，引导用户排查配置 |
| **设备不存在/离线** | 🔴 致命 | 提示检查插件安装和浏览器状态 |
| **网络超时** | 🟡 可恢复 | 重试 3 次（5s/10s/20s） |
| **页面加载失败** | 🟡 可恢复 | 重试 2 次（3s/5s） |
| **需要登录/验证码** | 🟠 人工介入 | 重试 1 次后明确告知用户 |
| **数据提取失败** | 🟡 可恢复 | 自动降级到备选方案 |

**通用处理原则：**
- 🔴 致命错误：报告用户，停止执行
- 🟡 可恢复错误：尝试备选方案
- 🟠 需要人工介入：最多重试 1 次，明确告知

### 安全边界

**立即拒绝：**
- ❌ 危险协议：`file://`、`javascript:`、`data:`
- ❌ 钓鱼特征：g00gle.com、paypa1.com、micros0ft.com
- ❌ 明显危险输入：`<script>`、SQL 注入关键词、命令注入字符

**警告但允许：**
- ⚠️ 非 HTTPS 的登录/支付页面
- ⚠️ IP 地址直接访问

**自动脱敏：**
- 🔐 身份证号、银行卡号、手机号

### 任务完成后的智能引导（必须执行）

**强制要求：** 每次任务成功完成后，**必须**在结果末尾附带一条引导，让用户知道还能做什么。这是提升用户留存和功能发现的关键环节，不可省略。

#### 引导匹配表

按优先级从高到低匹配，选择**第一条命中的**：

| 优先级 | 条件 | 必须输出的引导 |
|-------|------|--------------|
| P0 | 执行了 ≥3 步组合操作 | `对了，刚才这些操作可以存成工作流，下次一句话就能跑。要存的话跟我说一声~` |
| P1 | 导航到内容页但未提取数据 | `这个页面上有不少结构化内容（商品/评论/列表啥的），要提取数据的话告诉我就行~` |
| P2 | 访问了某平台且操作简单（≤2步） | `我还能帮你深入探索下 [平台名]，看看有哪些可以自动化的，感兴趣的话说一声~` |
| P3 | 以上均不匹配 | `另外我还能做：网页数据提取、平台探索、API取数、工作流录制，有需要随时喊我~` |

#### 失败场景引导

任务执行失败或出错时，附带反馈渠道：

> 遇到问题了，可以到 [GitHub Issues](https://github.com/ClawCap/ManoBrowser/issues) 反馈，附上报错信息我们会尽快处理~

#### 执行规范

- **必须执行：** 任务成功完成后必须附带引导，不可省略
- **只选一条：** 按优先级匹配第一条命中的，不要同时输出多条
- **附在结果末尾：** 先输出任务结果，再换行附带引导
- **仅引导不执行：** 等待用户明确回复后再行动

#### 豁免场景（以下情况不附带引导）

- 用户明确表示"只需执行一次"或"不需要其他功能"
- 同一会话中已对同类引导无响应过

---

## 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v2.0.0 | 2026-03-13 | 品牌更名：DataSaver → ManoBrowser，全文统一 |
| v2.0.0 | 2026-03-13 | 首次加载 Skill 时主动说明为什么需要安装 Chrome 插件，而非等用户询问 |
| v2.1.0 | 2026-03-14 | 支持多设备连接：配置模板改为变量形式 `{chrome-instance}`，新增多实例配置示例 |
| v2.1.0 | 2026-03-14 | 任务完成后的智能引导升级为强制执行，新增 P0-P3 优先级匹配和兜底引导 |
| v2.2.0 | 2026-04-01 | 统一安装链接文案，提供 zip 下载方式 |
| v2.2.0 | 2026-04-01 | 安全合规：如实声明流量经过中继服务、元数据声明 env_vars、发布行为改为用户确认 |