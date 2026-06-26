# OpenClaw Skill: 微信公众号排版与发布

让 OpenClaw AI 助手直接帮你写文章、AI 生成封面图、排版并发布到微信公众号。

---

## 功能特性

- 🤖 **AI 写作**：直接在 OpenClaw 对话中生成文章内容
- 🎨 **AI 封面图**：自动根据文章主题生成匹配的封面图（5 层兜底策略）
- 🎭 **智能排版**：6 种内置 Skill 模板 + 36 种模板市场模板 + 用户自定义模板
- 📤 **一键发布**：无需切换平台，直接发布到微信草稿箱
- 📱 **多账号支持**：可选择发布到哪个公众号
- ⚡ **状态可追踪**：创建任务后可持续查询发布进度与最终结果
- 📊 **额度查询**：随时查看当前套餐的发布额度和公众号绑定情况
- 🔍 **文章预览**：发布前可先预览排版效果
- 🎨 **自定义模板**：支持 Fork 官方模板或上传自定义模板，Skill 优先展示

---

## 安装配置

### 1. 安装 Skill

将本 Skill 文件夹复制到 OpenClaw Gateway 的 skills 目录，并安装依赖：

```bash
cp -r openclaw-skill /path/to/openclaw/gateway/skills/
cd /path/to/openclaw/gateway/skills/openclaw-skill
npm install
```

### 2. 配置 Skill

在 OpenClaw 界面中配置：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| **SaaS 平台地址** | 你的排版平台地址 | `https://open.tyzxwl.cn` |
| **API 密钥** | 从排版平台获取的密钥 | `wemd_xxxxxxxxxxxx` |

获取 API 密钥：
1. 登录排版平台
2. 进入「设置」→「API 管理」
3. 生成新的 API Key

### 3. 配置服务器端（封面图生成）

在服务器的 `.env` 文件中配置：

```bash
# 默认封面图路径（相对于 server/data/）
DEFAULT_COVER_IMAGE=./data/assets/default-cover.jpg

# AI 封面图生成服务（openclaw / dalle / default）
COVER_IMAGE_GENERATOR=openclaw

# OpenClaw Gateway 地址（用于 AI 生成封面）
OPENCLAW_GATEWAY_URL=https://your-openclaw-gateway

# OpenAI API Key（用于 DALL-E 生成，可选）
OPENAI_API_KEY=sk-xxx
```

### 4. 放置默认封面图

将封面图文件放置到 `server/data/assets/default-cover.jpg`（支持 jpg/png）。

### 5. 绑定公众号

首次使用前，需要在排版平台绑定公众号：
1. 登录排版平台
2. 点击「授权公众号」
3. 扫码授权你的公众号

---

## 使用方式

### 方式一：自然语言

直接在 OpenClaw 对话中输入：

```
写一篇关于人工智能的文章，用科技蓝模板发布到公众号
```

```
帮我写个美食探店文案，发到微信公众号
```

```
生成一篇教育类的文章，用教育培训模板
```

### 方式二：命令

```
/publish 写一篇关于 ChatGPT 的科普文章
```

```
/publish content="Markdown 内容" template="tech-blue" title="文章标题"
```

```
/quota
```

```
/preview content="Markdown 内容" template="tech-blue"
```

---

## 交互流程示例

### 场景 1：完整流程（未指定模板）

**用户**：写一篇关于 AI 的文章发布到公众号

**OpenClaw**：
> 好的，我来为你写一篇关于「AI」的文章，并发布到公众号。
> 
> 文章已生成！请选择一个排版模板：
> 
> [📝 默认主题] [💻 科技蓝] [📖 优雅简约] [💼 商务专业] [🍜 美食探店] [🎓 教育培训]

**用户**：（点击「科技蓝」）

**OpenClaw**：
> 已选择模板：**科技蓝**
> 
> 请选择要发布的公众号：
> 
> [公众号 A] [公众号 B]

**用户**：（选择公众号）

**OpenClaw**：
> ⏳ 正在发布... (30%)
> 
> 🎨 应用模板样式

**OpenClaw**：
> ⏳ 正在发布... (60%)
> 
> 🖼️ 上传文章图片 (2/5)

**OpenClaw**：
> ✅ 文章已成功发布到 **公众号 A**！
> 
> [查看草稿] [再写一篇]

---

### 场景 2：快速发布（已指定模板）

**用户**：用美食模板写一篇探店文章发到公众号

**OpenClaw**：
> 好的，我来为你写一篇美食探店文章...
> 
> 已选择模板：**美食探店**
> 
> ⏳ 正在发布... (45%)

**OpenClaw**：
> ✅ 发布成功！
> 
> [查看草稿]

---

### 场景 3：仅排版已有内容

**用户**：把这段内容排版发布到公众号：
> Markdown 内容...

**OpenClaw**：
> 收到内容！请选择一个排版模板：
> 
> [模板列表...]

---

## 支持的模板

### Skill 内置模板（6 种）

通过 `/api/skill/templates` 接口直接获取，Skill 工作流中默认使用：

| 模板 | ID | 类别 | 付费 | 特点 |
|------|-----|------|------|------|
| 📝 默认主题 | `default` | 通用 | 免费 | 简洁优雅，适合各类文章 |
| 💻 科技蓝 | `tech-blue` | 科技 | 免费 | 渐变蓝色，适合技术/产品 |
| 📖 优雅简约 | `elegant-minimal` | 生活 | 高级 | 衬线字体，适合散文/阅读 |
| 💼 商务专业 | `business-pro` | 商务 | 高级 | 正式风格，适合报告/分析 |
| 🍜 美食探店 | `food-review` | 美食 | 高级 | 暖色调，适合美食/餐厅 |
| 🎓 教育培训 | `education` | 教育 | 免费 | 清新绿色，适合课程/知识 |

### 模板市场（36+ 种）

在 Web 端模板市场可浏览更多模板，涵盖新闻媒体、科技数码、商务服务、创意设计、生活美食、教育培训、情感生活、职场工作等分类。用户可以在模板市场 Fork 官方模板到私有模板库，然后在 Skill 中使用。

### 用户自定义模板

用户通过以下方式创建的自定义模板也会出现在 Skill 的模板列表中（排在内置模板之前）：

- 在 Web 端模板市场 Fork 官方模板
- 在模板设计器中自行创建
- 上传自定义 CSS 样式

---

## API 接口

本 Skill 调用 SaaS 平台的以下接口：

### 获取模板列表
```
GET /api/skill/templates?category=&search=&page=1&limit=20
Headers: X-API-Key: {apiKey}
```

返回内置模板与用户自定义模板（用户模板排在前面）。

### 获取模板分类
```
GET /api/skill/templates/categories
Headers: X-API-Key: {apiKey}
```

返回可用的模板分类列表（通用、科技、生活、商务、美食、教育等）。

### 获取公众号列表
```
GET /api/skill/accounts
Headers: X-API-Key: {apiKey}
```

响应字段包含 `appId`、`appName`、`appLogo`、`originalId`。

### 发布文章
```
POST /api/skill/publish
Headers: X-API-Key: {apiKey}
Body: {
  content: "文章内容（Markdown）",
  title: "标题",
  templateId: "模板ID",
  accountId: "公众号AppID（可选，默认第一个）",
  author: "作者（可选，默认使用公众号名称）",
  digest: "摘要（可选）",
  coverImage: "封面图URL（可选）",
  contentSourceUrl: "阅读原文链接（可选）",
  autoGenerateCover: true  // 是否AI自动生成封面（默认true）
}
```

### 查询发布状态
```
GET /api/skill/publish/status?taskId=xxx
Headers: X-API-Key: {apiKey}
```

### 查询额度
```
GET /api/skill/quota
Headers: X-API-Key: {apiKey}
```

返回当前套餐名称、发布额度使用情况、公众号绑定数量。

---

## 文件结构

```
openclaw-skill/
├── skill.yaml
├── handler.js
├── package.json
├── README.md
├── QUICKSTART.md
├── FAQ.md
├── INTEGRATION.md
├── APIKEY.md
├── MARKETING.md
├── examples/
└── templates/
```

---

## 更新日志

### v1.3.0
- ✅ 模板组件识别、容器注入、HTML 结构补全抽为共享 util，普通发布与 skill 发布统一使用同一模板渲染逻辑
- ✅ `generate_content` 的 `content` 与 `params` 双重携带 HTML 优先生成指令，兼容只读取文本的技能平台
- ✅ 服务端发布前新增 HTML 结构补全，降低 AI 漏掉组件包装时的样式失配概率

### v1.2.0
- ✅ 新增 `/quota` 命令和额度查询接口，随时查看发布额度和公众号绑定情况
- ✅ 新增 `/preview` 命令，发布前可预览排版效果
- ✅ Skill 模板列表支持展示用户自定义模板（优先显示在内置模板之前）
- ✅ 新增模板分类接口 `/api/skill/templates/categories`
- ✅ 触发器增加「懒人编辑器」唤起意图和额度查询意图
- ✅ 发布时支持 `autoGenerateCover`、`coverImage`、`contentSourceUrl` 等高级参数
- ✅ handler.js 新增 publishTasks / workflowSessions 内存上限管理，防止内存泄漏

### v1.1.3
- ✅ 多步交互增加显式 workflow session，模板选择与账号选择不再依赖隐式上下文续接
- ✅ 服务端 Markdown 渲染切换为 `marked`，表格、列表、代码块等复杂内容兼容性更稳定

### v1.1.2
- ✅ 技能侧模板选择明确展示系统模板与用户自定义模板
- ✅ 多公众号场景强制进入账号选择，不再静默落到默认账号
- ✅ 未显式填写作者时，默认使用所选公众号名称
- ✅ 修正 `skill.yaml` 中命令声明错误，补齐状态查询命令

### v1.1.1
- ✅ 补充 skill 独立安装所需的 `package.json`
- ✅ 修复多步交互发布流程中的模板/公众号选择续接
- ✅ 保留后端 4xx 业务错误，避免被 skill 侧错误泛化

### v1.1.0
- ✅ **AI 封面图生成**：自动根据文章主题生成匹配封面
- ✅ **默认封面图**：支持设置默认封面，生成失败时自动使用
- ✅ **5 层兜底策略**：用户指定 > AI 生成 > 文章首图 > 默认封面 > 占位图

### v1.0.0
- ✅ AI 写作与排版一体化
- ✅ 6 种精美模板
- ✅ 一键发布到微信草稿箱
- ✅ 多账号支持
- ✅ 实时进度展示

---

## 问题反馈

如有问题，请联系：
- 邮箱：lanren0405@163.com
- 微信：sugu717
