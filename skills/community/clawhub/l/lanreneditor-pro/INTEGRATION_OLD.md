# AI 平台通用集成指南

本文档面向所有支持以下任一能力的 AI 平台：

- 自定义 Skill / 插件 / Agent
- HTTP Tool / OpenAPI / API 调用
- 工作流节点编排
- Prompt 模板 + 外部接口

这意味着你可以把懒人编辑器安装到 OpenClaw、QClaw、WorkBuddy、扣子、Dify、FastGPT，以及任意自建 Agent 平台。

---

## 先看结论

| 平台类型 | 代表平台 | 推荐安装方式 | 是否支持一键式安装 |
|----------|----------|--------------|--------------------|
| Skill / 插件型 | OpenClaw、QClaw、WorkBuddy | 导入 `openclaw-skill` 技能包 | 支持 |
| Tool / API 型 | 扣子、Dify、FastGPT | 配置 HTTP 工具或 OpenAPI | 支持 |
| Prompt / Workflow 型 | 自建 Agent、Copilot 类平台 | 导入提示词模板 + 调用接口 | 支持 |

如果你的 AI 平台支持上传 ZIP、导入 Git 仓库、导入 OpenAPI、配置 HTTP Tool、复制工作流模板中的任意一种，就可以完成接入。

---

## 安装前准备

无论接入哪个平台，先准备下面 4 项：

### 1. 平台地址

```text
https://open.tyzxwl.cn
```

### 2. API Key

在懒人编辑器后台生成 API Key：

1. 登录平台
2. 进入「个人中心」或「设置」
3. 打开「API 管理」
4. 生成形如 `wemd_xxxxxxxxxxxx` 的密钥

### 3. 已授权公众号

至少先授权 1 个微信公众号，否则 AI 可以完成排版，但无法完成最终投递到草稿箱。

### 4. 至少 1 个模板

系统内置模板可直接使用；如果你想在 AI 平台里固定品牌风格，建议先在模板设计器中保存自己的模板。

---

## 平台兼容与推荐接入方式

| 平台 | 推荐方式 | 一键安装思路 | 说明 |
|------|----------|--------------|------|
| OpenClaw | Skill 包导入 | 上传 `openclaw-skill` 目录或 Git 同步 | 原生适配最佳 |
| QClaw | Skill 包导入 | 上传技能包 / ZIP / 仓库 | 与 OpenClaw 结构最接近 |
| WorkBuddy | Skill / 插件导入 | 导入目录、ZIP 或配置插件 | 适合团队内部机器人 |
| 扣子 Coze | HTTP Tool / 工作流 | 导入 OpenAPI 或创建 4 个工具 | 推荐工作流封装 |
| Dify | Tool / Workflow | 添加 HTTP 请求工具或 Agent Tool | 适合企业知识库场景 |
| FastGPT | 插件 / API 工具 | 配置自定义接口节点 | 适合 Bot 工作流接入 |
| 自建 Agent | Prompt + API | 复制提示词与接口清单 | 兼容性最强 |
| 其他平台 | 以上任一种 | 看平台是否支持 Tool / Workflow / Prompt | 原理完全一致 |

---

## 一键安装的 3 种标准方式

## 方式 A：直接导入 Skill 包

适合：OpenClaw、QClaw、WorkBuddy、支持插件目录的平台。

### 一键安装步骤

1. 下载或复制 `openclaw-skill` 目录
2. 在目标平台进入「技能 / 插件 / Skills」管理
3. 点击「导入」「上传 ZIP」「从目录安装」或「从 Git 安装」
4. 填入以下配置：

```yaml
apiBaseUrl: https://open.tyzxwl.cn
apiKey: wemd_xxxxxxxxxxxx
```

5. 保存并启用技能
6. 直接对 AI 说：

```text
帮我写一篇关于人工智能的文章，并发布到公众号
```

### 适合的平台

- OpenClaw
- QClaw
- WorkBuddy
- 其他支持本地 Skill / 插件目录的平台

---

## 方式 B：导入 HTTP Tool / OpenAPI

适合：扣子、Dify、FastGPT、支持 API 工具的平台。

### 一键安装思路

把懒人编辑器当成一个外部发布能力服务，向平台注册 4 个接口：

| 工具名 | 方法 | 地址 | 用途 |
|--------|------|------|------|
| get_templates | GET | `/api/skill/templates` | 获取模板列表 |
| get_accounts | GET | `/api/skill/accounts` | 获取公众号列表 |
| publish_article | POST | `/api/skill/publish` | 创建发布任务 |
| get_publish_status | GET | `/api/skill/publish/status` | 查询发布状态 |

统一配置：

```text
Base URL: https://open.tyzxwl.cn
Header: X-API-Key: wemd_xxxxxxxxxxxx
```

### 可直接复用的 OpenAPI 草案

```yaml
openapi: 3.0.1
info:
  title: Lazy Editor Publish API
  version: 1.0.0
servers:
  - url: https://open.tyzxwl.cn
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
security:
  - ApiKeyAuth: []
paths:
  /api/skill/templates:
    get:
      summary: 获取模板列表
      parameters:
        - in: query
          name: search
          schema:
            type: string
      responses:
        '200':
          description: ok
  /api/skill/accounts:
    get:
      summary: 获取已授权公众号
      responses:
        '200':
          description: ok
  /api/skill/publish:
    post:
      summary: 创建发布任务
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [content, templateId]
              properties:
                content:
                  type: string
                title:
                  type: string
                author:
                  type: string
                templateId:
                  type: string
                accountId:
                  type: string
                digest:
                  type: string
                coverImage:
                  type: string
                contentSourceUrl:
                  type: string
      responses:
        '200':
          description: ok
  /api/skill/publish/status:
    get:
      summary: 查询发布状态
      parameters:
        - in: query
          name: taskId
          required: true
          schema:
            type: string
      responses:
        '200':
          description: ok
```

---

## 方式 C：导入 Prompt + Workflow 模板

适合：任意支持系统提示词、工作流编排、工具调用的 AI 平台。

### 推荐系统提示词

```text
你是一个微信公众号排版与发布助手。

你的目标：
1. 帮用户生成或接收 Markdown 文章内容
2. 先调用模板接口获取模板列表
3. 如果用户未指定模板，让用户选择模板
4. 再调用公众号接口获取已授权账号
5. 如果用户有多个账号，让用户选择目标公众号
6. 调用发布接口创建任务
7. 轮询状态接口，直到任务完成或失败

规则：
- 如果未指定作者，默认使用公众号名称
- 如果平台支持交互式卡片，优先用卡片展示模板和公众号
- 如果平台只支持文本，展示编号列表让用户回复编号
- 任何错误都要原样展示服务端返回的 message
```

### 推荐工作流节点

1. 接收用户需求
2. 如果没有内容则让大模型生成内容
3. 调用 `get_templates`
4. 选择模板
5. 调用 `get_accounts`
6. 选择公众号
7. 调用 `publish_article`
8. 轮询 `get_publish_status`
9. 返回草稿链接

---

## OpenClaw 一键安装

### 方式 1：本地目录导入

```bash
cp -r openclaw-skill /path/to/openclaw/gateway/skills/wechat-md-publisher
cd /path/to/openclaw/gateway/skills/wechat-md-publisher
npm install
```

然后在 OpenClaw 后台启用该技能，填入：

```text
apiBaseUrl = https://open.tyzxwl.cn
apiKey = wemd_xxxxxxxxxxxx
```

### 方式 2：Git 仓库导入

```bash
cd /path/to/openclaw/gateway/skills
git clone <your-repo-url> wechat-md-publisher
```

### 方式 3：ZIP 一键上传

如果你的 OpenClaw 后台提供上传功能，直接把 `openclaw-skill` 打包成 ZIP 上传即可。

---

## QClaw 一键安装

QClaw 推荐与 OpenClaw 相同的 Skill 包模式。

### 安装步骤

1. 上传 `openclaw-skill` 目录或 ZIP
2. 在技能配置中填写 `apiBaseUrl` 和 `apiKey`
3. 启用技能
4. 直接通过对话触发：

```text
把这篇内容排版后发布到公众号
```

如果 QClaw 支持 Git 仓库同步，也可以直接绑定仓库实现一键安装和后续更新。

---

## WorkBuddy 一键安装

WorkBuddy 更适合团队内知识助手和运营机器人场景，建议两种方式：

### 方式 1：插件 / 技能导入

1. 进入 WorkBuddy 管理台
2. 创建新插件或机器人技能
3. 上传 `openclaw-skill` 或复制其中的接口定义
4. 填入：

```text
Base URL = https://open.tyzxwl.cn
X-API-Key = wemd_xxxxxxxxxxxx
```

### 方式 2：工作流封装

把发布过程拆成：模板获取、账号获取、创建任务、查询任务 4 个节点，然后封装成一个“公众号发布”工作流，供团队成员一键复用。

---

## 扣子（Coze）一键安装

扣子推荐使用 HTTP Tool 或工作流模式。

### 方式 1：HTTP Tool 一键配置

1. 新建 Bot
2. 进入插件或工具配置
3. 新增 4 个 HTTP 工具
4. 每个工具统一添加 Header：

```text
X-API-Key: wemd_xxxxxxxxxxxx
```

5. Base URL 填：

```text
https://open.tyzxwl.cn
```

### 方式 2：工作流一键搭建

推荐节点顺序：

1. LLM 生成文章
2. HTTP 获取模板
3. 选择模板
4. HTTP 获取公众号
5. 选择公众号
6. HTTP 创建发布任务
7. HTTP 查询任务状态

### 扣子里建议给 Bot 的描述词

```text
你是微信公众号排版助手。你负责生成文章、让用户选模板、让用户选公众号，并调用外部接口完成发布。
```

---

## Dify 一键安装

推荐使用 Dify 的 Tool + Workflow 组合。

### 安装步骤

1. 新建应用或 Agent
2. 添加自定义工具
3. 导入 OpenAPI，或手动创建 4 个 HTTP 请求工具
4. 绑定 `X-API-Key`
5. 在工作流里串起来

### 推荐组合

- Chatflow：适合一步一步引导用户选模板和账号
- Agent：适合直接自然语言触发
- Workflow：适合企业内部固定流程发布

---

## FastGPT 一键安装

FastGPT 推荐把懒人编辑器作为一个外部 API 插件使用。

### 安装步骤

1. 创建插件或 API 工具
2. 配置 4 个接口
3. 增加系统提示词，要求 AI 在发布前先获取模板和公众号
4. 在节点编排中增加状态轮询

### 最简可用模式

如果你不做完整工作流，至少配置下面两个接口也能跑通：

- `GET /api/skill/templates`
- `POST /api/skill/publish`

但更推荐完整接入 4 个接口，这样用户可以在 AI 内完成模板与账号选择。

---

## 通用自建 Agent / Copilot / Chat SDK 一键安装

如果你用的是任意自建 AI 平台，只要支持发 HTTP 请求，就可以集成。

### 最小接入方案

1. 给 Agent 一个系统提示词
2. 注册 4 个外部工具
3. 调用流程按下面的顺序串起来：

```text
生成内容 → 获取模板 → 选择模板 → 获取公众号 → 选择公众号 → 发布 → 查询状态
```

### 通用工具清单

```text
GET  https://open.tyzxwl.cn/api/skill/templates
GET  https://open.tyzxwl.cn/api/skill/accounts
POST https://open.tyzxwl.cn/api/skill/publish
GET  https://open.tyzxwl.cn/api/skill/publish/status
```

统一请求头：

```text
X-API-Key: wemd_xxxxxxxxxxxx
Content-Type: application/json
```

---

## 为什么说它支持任何 AI 平台

因为本质上它只依赖 4 件事：

1. 平台能让 AI 读取用户输入
2. 平台能调用 HTTP 接口
3. 平台能把接口结果回传给大模型
4. 平台允许多轮对话继续执行

具备这 4 条中的前 3 条，至少能完成半自动发布；4 条都具备，就能完成完整的一键式交互发布。

---

## 返回结果说明

### 发布成功

会返回：

- taskId
- 草稿链接 draftUrl
- 公众号名称 accountName
- 模板名称 templateName

### 发布中

会返回：

- 当前进度 progress
- 当前步骤 step
- 日志 logs

### 发布失败

会返回：

- error
- 业务错误码 code
- 可能的升级链接 upgradeUrl
- 管理入口 manageUrl

---

## 测试方式

### 先测模板接口

```bash
curl -H "X-API-Key: wemd_test_key" \
  https://open.tyzxwl.cn/api/skill/templates
```

### 再测账号接口

```bash
curl -H "X-API-Key: wemd_test_key" \
  https://open.tyzxwl.cn/api/skill/accounts
```

### 最后测发布接口

```bash
curl -X POST \
  -H "X-API-Key: wemd_test_key" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 测试文章\n\n这是内容",
    "title": "测试标题",
    "templateId": "default"
  }' \
  https://open.tyzxwl.cn/api/skill/publish
```

---

## 常见问题

### 1. 为什么平台里没有真正的“安装按钮”？

不同 AI 平台术语不同，有的叫技能，有的叫插件，有的叫工作流，有的叫工具。你只需要找到它的导入入口，本质上都是把同一套 API 能力接进去。

### 2. 哪个平台接入成本最低？

OpenClaw、QClaw、WorkBuddy 这类支持 Skill 包的平台最低，因为可以直接导入整个技能包。

### 3. 哪个平台最通用？

扣子、Dify、FastGPT 这类支持 HTTP Tool / Workflow 的平台最通用，因为几乎不依赖特定 Skill 格式。

### 4. 如果平台不支持卡片交互怎么办？

直接把模板和账号列成编号列表，让用户回复编号即可。

---

## 推荐对外文案

如果你要对外展示这项能力，可以直接使用下面这段：

```text
懒人编辑器支持安装到任意 AI 平台。无论你使用的是扣子、WorkBuddy、QClaw、OpenClaw、Dify、FastGPT，还是自建 Agent，只要平台支持技能、工作流、HTTP Tool 或 Prompt 配置，就可以让 AI 直接帮你生成文章、选择模板、选择公众号并一键发布到微信草稿箱。
```