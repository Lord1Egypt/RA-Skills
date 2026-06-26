# 微信公众号内容管线（排版与发布）

> 从素材收集到多平台分发的全链路 AI 内容管线，让 AI 帮你写文章、排版、生成封面、转换多平台文案并一键分发。

---

## 功能介绍

### 🔄 两条管线路径

| 路径 | 流程 | 适用场景 |
|------|------|----------|
| **Path A：素材→出稿** | 素材收集 → AI写稿 → 排版 → 封面 → 多平台文案 → 分发 | 日常内容积累、从零创作 |
| **Path B：微信文章→多平台** | 抓取文章 → 分析结构 → 多平台转换 → 封面 → 文案 → 分发 | 内容复用、跨平台分发 |

### ✨ 核心功能

- 📝 **素材管理**：收集零散灵感，按主题归类，AI 自动提取摘要
- 🤖 **AI 写稿**：六段式教程 + 四幕式深度两种框架，素材自动组织成文
- 🎨 **排版渲染**：自定义模板 + CSS 内联（微信兼容），100+ 主题可选
- 🖼️ **AI 封面图**：三种风格（渐变/品牌/极简），支持横版和竖版
- 📕 **小红书轮播图**：文章一键转 8-10 张小红书卡片
- 📱 **多平台文案**：小红书/即刻/朋友圈/播客，一键生成适配文案
- 🔗 **文章抓取**：微信文章链接 → 提取标题/正文/图片
- 📊 **文章分析**：解析结构、提取关键数据、推荐写作框架
- 📤 **一键发布**：直接发布到微信公众号草稿箱
- 📡 **多平台分发**：微信 L0 API 直推 + 多平台 CDP 分发
- 📊 **额度查询**：查看发布额度、公众号绑定、模板配额

> ⚠️ **重要提示**：本技能优先使用用户自定义模板进行排版。如果你尚未创建自定义模板，请先在平台创建。

---

## 配置参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `apiBaseUrl` | string | ✅ | SaaS 平台地址 | `https://open.tyzxwl.cn` |
| `apiKey` | secret | ✅ | API 密钥（从平台获取） | `wemd_xxxxxxxxxxxx` |

### 获取 API 密钥

1. 访问 https://open.tyzxwl.cn 并登录
2. 进入「个人中心」→「API Key」
3. 点击「生成新密钥」

### 绑定公众号

首次使用前需授权公众号：
1. 登录平台后点击「授权公众号」
2. 使用公众号管理员微信扫码授权

---

## API 接口

**Base URL**: `https://open.tyzxwl.cn`  
**鉴权方式**: Header `X-API-Key: {apiKey}`

---

### 1. 获取模板列表

```
GET /api/skill/templates
```

**Query 参数**（均可选）:
| 参数 | 说明 |
|------|------|
| `category` | 模板分类筛选 |
| `search` | 搜索关键词 |
| `page` | 页码，默认 1 |
| `limit` | 每页数量，默认 20 |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "list": [
      {
        "id": "tech-blue",
        "name": "科技蓝",
        "description": "渐变蓝色，适合技术/产品类文章",
        "category": "tech",
        "categoryName": "科技",
        "emoji": "💻",
        "isPremium": false,
        "isUserTemplate": false,
        "tags": ["科技", "产品", "技术"]
      }
    ],
    "userTemplatesCount": 2,
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 8,
      "totalPages": 1
    }
  }
}
```

**关于模板**: 优先使用用户自定义模板（`isUserTemplate: true`）。如果模板列表中没有用户模板（`userTemplatesCount: 0`），需要引导用户先创建模板。

---

### 2. 获取模板分类

```
GET /api/skill/templates/categories
```

---

### 3. 获取公众号列表

```
GET /api/skill/accounts
```

---

### 4. 查询发布额度

```
GET /api/skill/quota
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "planName": "专业版",
    "publish": { "used": 15, "total": 100, "remaining": 85 },
    "accounts": { "used": 2, "total": 5, "remaining": 3 }
  }
}
```

---

### 5. 发布文章

```
POST /api/skill/publish
Content-Type: application/json
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content` | string | ✅ | 文章内容（Markdown 格式） |
| `templateId` | string | ✅ | 模板 ID |
| `title` | string | ❌ | 文章标题（不填则从内容提取） |
| `accountId` | string | ❌ | 公众号 AppID |
| `author` | string | ❌ | 作者名 |
| `digest` | string | ❌ | 文章摘要 |
| `coverImage` | string | ❌ | 封面图 URL |
| `contentSourceUrl` | string | ❌ | 阅读原文链接 |
| `autoGenerateCover` | boolean | ❌ | 是否 AI 生成封面（默认 true） |

---

### 6. 查询发布状态

```
GET /api/skill/publish/status?taskId={taskId}
```

---

### 7. 素材管理（v2.0 新增）

**添加素材**:
```
POST /api/skill/materials
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content` | string | ✅ | 素材内容 |
| `type` | string | ❌ | 素材类型（manual/auto/hybrid，默认 manual） |
| `topic` | string | ❌ | 主题标签 |

**查看素材列表**:
```
GET /api/skill/materials
```

**清空素材**:
```
DELETE /api/skill/materials
```

---

### 8. AI 写稿（v2.0 新增）

```
POST /api/skill/draft
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `topic` | string | ✅ | 文章主题 |
| `framework` | string | ❌ | 写作框架（tutorial=六段式教程/deep=四幕式深度/auto=自动选择） |
| `templateId` | string | ❌ | 关联排版模板 ID |

**写作框架说明**:
- **tutorial（六段式教程）**：引言→概念→步骤→案例→常见问题→总结，适合技术教程、实操指南
- **deep（四幕式深度）**：现象→分析→洞察→展望，适合深度分析、行业观点
- **auto**：根据主题自动选择最合适的框架

---

### 9. 排版渲染（v2.0 新增）

```
POST /api/skill/render
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content` | string | ✅ | 文章内容（Markdown 或 HTML） |
| `templateId` | string | ✅ | 模板 ID |

返回**内联 CSS 的 HTML**，可直接粘贴到微信公众号编辑器。

---

### 10. 封面生成（v2.0 新增）

```
POST /api/skill/cover
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文章标题 |
| `style` | string | ❌ | 封面风格（gradient/brand/minimal，默认 gradient） |
| `size` | string | ❌ | 封面尺寸（900x383=横版/1080x1440=竖版，默认 900x383） |

---

### 11. 小红书轮播图（v2.0 新增）

```
POST /api/skill/xiaohongshu
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文章标题 |
| `content` | string | ❌ | 文章内容 |

返回 8-10 张小红书轮播卡片的 HTML。

---

### 12. 多平台文案（v2.0 新增）

```
POST /api/skill/social-copy
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文章标题 |
| `content` | string | ❌ | 文章内容 |
| `platforms` | string | ❌ | 目标平台（逗号分隔：xiaohongshu,jike,moments,podcast） |

返回适配各平台的文案版本。

---

### 13. 文章抓取（v2.0 新增）

```
POST /api/skill/fetch
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 微信文章链接 |

返回标题、作者、正文 HTML、纯文本内容。

---

### 14. 文章分析（v2.0 新增）

```
POST /api/skill/analyze
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ❌ | 文章链接 |
| `content` | string | ❌ | 文章内容（url 和 content 二选一） |

返回文章结构、关键数据、推荐写作框架。

---

### 15. 多平台分发（v2.0 新增）

```
POST /api/skill/distribute
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `manifest` | object | ✅ | 分发内容清单（含各平台内容） |
| `platforms` | array | ❌ | 目标平台列表 |

微信 L0 API 直推，其他平台需 CDP 集成。

---

### 16. 管线编排（v2.0 新增）

一步完成全链路操作：

```
POST /api/skill/pipeline
Content-Type: application/json
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `steps` | array | ❌ | 执行步骤（默认全部：material,draft,render,cover,socialCopy） |
| `material` | object | ❌ | 素材参数（content, topic） |
| `draft` | object | ❌ | 写稿参数（framework, templateId） |
| `render` | object | ❌ | 排版参数（templateId） |
| `cover` | object | ❌ | 封面参数（style, size） |
| `socialCopy` | object | ❌ | 文案参数（platforms） |

**请求示例**:
```json
{
  "steps": ["material", "draft", "render", "cover", "socialCopy"],
  "material": { "content": "AI 正在改变内容创作方式...", "topic": "AI内容创作" },
  "draft": { "framework": "tutorial" },
  "render": { "templateId": "tech-blue" },
  "cover": { "style": "gradient" },
  "socialCopy": { "platforms": ["xiaohongshu", "jike"] }
}
```

返回 `jobId`，轮询 `GET /api/skill/pipeline/:jobId` 获取进度。

---

## 系统提示词

将以下内容添加到 Bot 的系统提示词中：

```
你是一个微信公众号内容管线助手。你支持从素材收集到多平台分发的全链路操作。
你必须严格按照以下步骤执行，不允许跳过或合并任何步骤。

## 🔄 两条管线路径

### Path A：素材→出稿（日常积累场景）
素材收集 → AI写稿 → 排版 → 封面 → 多平台文案 → 分发

### Path B：微信文章→多平台（内容复用场景）
抓取文章 → 分析结构 → 多平台转换 → 封面 → 文案 → 分发

## ⚠️ 强制工作流程

### 全链路管线（推荐）

当用户说"出稿"、"一键出稿"、"全链路"时：
1. 检查素材：GET /api/skill/materials
2. AI 写稿：POST /api/skill/draft（需指定 topic 和 templateId）
3. 排版渲染：POST /api/skill/render（content + templateId）
4. 生成封面：POST /api/skill/cover（title）
5. 多平台文案：POST /api/skill/social-copy（title + content）
6. 或使用一键编排：POST /api/skill/pipeline

### 单步操作

**素材收集**：
- 添加素材：POST /api/skill/materials（content 必填）
- 查看素材：GET /api/skill/materials
- 清空素材：DELETE /api/skill/materials

**AI 写稿**：
- POST /api/skill/draft（topic 必填，framework 可选：tutorial/deep/auto）

**文章抓取**：
- POST /api/skill/fetch（url 必填，仅微信链接）

**排版渲染**：
- POST /api/skill/render（content + templateId）
- 返回内联CSS的HTML，可直接粘贴到公众号编辑器

**封面生成**：
- POST /api/skill/cover（title 必填）
- 支持 gradient/brand/minimal 三种风格

**小红书轮播图**：
- POST /api/skill/xiaohongshu（title + content）

**多平台文案**：
- POST /api/skill/social-copy（title + content）

**文章分析**：
- POST /api/skill/analyze（url 或 content）

**多平台分发**：
- POST /api/skill/distribute（manifest + platforms）

### 一键发布流程（保留 v1.x 兼容）

当用户说"发布到公众号"时：
1. GET /api/skill/templates → 选择模板
2. GET /api/skill/accounts → 选择公众号
3. POST /api/skill/publish → 一键发布
4. GET /api/skill/publish/status → 查询状态

## 排版输出规则（生成内容时必须遵守）
- 目标不是只生成"语义正确的 Markdown"，而是生成"能让模板 CSS 真正命中的内容结构"。
- 当模板依赖自定义 className 样式时，优先输出带 class 的 HTML 结构。
- 如果平台给出了 ::: className 容器语法，必须使用它或等价 HTML。
- 核心原则：使用 HTML 结构确保 CSS 样式显示。

## 模板选择规则
- 优先使用用户自定义模板（isUserTemplate: true）
- 用户无自定义模板时，引导到模板设计器创建
- 访问 https://open.tyzxwl.cn/website/template-designer.html

## 🚫 禁止事项
1. 禁止跳过模板选择
2. 禁止在用户未确认前调用发布接口
3. 禁止自动选择公众号（必须让用户确认）
4. 如果发布失败，展示完整的错误信息
```

---

## 使用示例

### 管线操作

```
帮我出一篇关于 AI 内容创作的文章，全链路
```

```
添加素材：AI 正在改变内容创作方式，从写作到排版到分发全流程自动化
```

```
AI写稿，主题：产品经理的 AI 工具箱
```

```
把这篇文章转成小红书轮播图
```

### 一键发布

```
写一篇关于人工智能的文章，发布到公众号
```

```
帮我写个美食探店文案，发到微信公众号
```

### 查询

```
查询我的发布额度
```

```
/pipeline-status jobId=pipeline_abc123
```

---

## 计费说明

| 操作 | 消耗配额 |
|------|----------|
| 素材管理（增删查）| 免费 |
| 排版渲染 | 免费 |
| 多平台文案生成 | 免费 |
| AI 写稿 | 1 次 |
| 封面生成 | 1 次 |
| 小红书轮播图 | 1 次 |
| 多平台分发 | 1 次 |
| 一键发布 | 1 次 |

---

## 错误码说明

| HTTP 状态码 | 错误信息 | 解决方案 |
|-------------|----------|----------|
| 400 | 缺少文章内容/主题 | 检查必填参数 |
| 401 | 未授权 | 检查 API Key 是否正确 |
| 403 | 发布配额已用完 | 升级套餐或等待下月重置 |
| 404 | 模板/任务不存在 | 检查 ID 是否正确 |
| 429 | 请求频率超限 | 降低调用频率（默认 100 次/小时） |

---

## 常见问题

**Q: 为什么发布后样式没生效？**  
A: 微信公众号不支持 `<style>` 标签，系统已自动将 CSS 转为内联样式。如仍有问题请检查模板 CSS 是否正确。

**Q: 封面图比例不对怎么办？**  
A: 系统会自动裁剪封面图到 2.35:1 比例（900×383），也可设置 `autoGenerateCover: true` 让 AI 生成封面。

**Q: 看不到我的自定义模板？**  
A: 确保 API Key 对应的用户已在 Web 端创建了自定义模板。可访问 https://open.tyzxwl.cn/website/template-designer.html 创建。

**Q: 管线任务进度怎么查？**  
A: 调用 `GET /api/skill/pipeline/:jobId` 轮询，每 2 秒一次，直到 status 为 completed 或 failed。

**Q: AI 写稿的两种框架怎么选？**  
A: `tutorial` 适合教程/实操类，`deep` 适合分析/观点类，`auto` 自动判断。默认 `auto`。

---

## 联系方式

- 平台地址：https://open.tyzxwl.cn
- 邮箱：lanren0405@163.com
- 微信：sugu717

---

## 版本信息

**当前版本**: v2.0.0

### 更新日志

- v2.0.0: Content Pipeline 全链路管线 — 新增素材管理、AI 写稿、排版渲染、封面生成、小红书轮播图、多平台文案、文章抓取/分析、多平台分发、管线编排共 14 个 API 端点
- v1.3.0: 模板组件识别、容器注入、HTML 结构补全，统一渲染链路
- v1.2.0: 新增额度查询、文章预览、自定义模板支持
- v1.1.0: 新增 AI 封面图生成、5 层兜底策略
- v1.0.0: 基础发布功能、6 种内置模板
