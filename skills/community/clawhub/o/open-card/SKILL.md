---
name: open-card
description: 从本地 OpenClaw数据生成或迭代 OpenCard 个人名片。读取工作区身份信息、配置和会话统计；渲染 HTML 预览；导出 PNG。只读模式——不写入用户档案数据。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "bash", "node", "npm"] },
        "install":
          [
            {
              "id": "playwright-core",
              "kind": "node",
              "package": "playwright-core",
              "label": "Install playwright-core (npm)",
            },
          ],
      },
  }
---

# OpenCard

从本地 agent 状态生成可分享的 OpenClaw 个人名片。

优先读取已有的本地数据源，不凭空编造字段。本 skill 对用户档案数据严格只读：提取、汇总、排版、渲染。

## 核心流程

1. 从工作区读取身份/上下文文件。
2. 从 `~/.openclaw/` 读取运行时配置和会话状态。
3. 将字段归一化为稳定的名片 schema。
4. 先渲染 HTML/CSS 预览。
5. 与用户迭代布局和样式。
6. HTML 版本确认无误后再导出图片。

## 数据源

按优先级顺序使用以下数据源。

### 1. 工作区身份文件

读取路径：
- `~/.openclaw/workspace/USER.md`
- `~/.openclaw/workspace/IDENTITY.md`
- `~/.openclaw/workspace/MEMORY.md`

提取字段：
- `display_name`
- `role_title`
- `recent_focus`

规则：
- 优先使用文件中已有的显式字段。
- 除非用户明确要求，不创建新的档案字段。
- 多个文件冲突时，以更明确的文件为准（`IDENTITY.md` 用于 agent 身份，`USER.md` 用于人类身份）。

### 2. OpenClaw 配置/运行时

读取路径：
- `~/.openclaw/openclaw.json`
- `~/.openclaw/agents/main/sessions/*.jsonl`（会话记录）

提取字段：
- `default_model`：来自配置中的默认 agent 模型，而非当前对话切换的模型（除非用户要求当前会话状态）。
- `token_30d`：最近 30 天的会话 token 用量。
- `skills_count`：已安装的本地 skills 数量。
- `platforms`：会话中观察到的已连接平台。

规则：
- 模型显示优先使用简洁的展示值（如 `GPT-5.4`），而非原始 provider 路径。
- Token 统计使用用户要求的时间范围；未指定时询问或使用当前任务中最近达成共识的范围。
- 平台展示所有已连接/观察到的平台，而非仅展示使用最多的那个。

## 稳定字段 schema

渲染前归一化为以下 schema：

```json
{
  "display_name": "Trent",
  "role_title": "产品经理 · AI 博主",
  "born_label": "Born",
  "born_date": "2026.03.10",
  "default_model": "GPT-5.4",
  "token_30d": 26000000,
  "token_30d_display": "26M tokens",
  "skill_names": ["open-card", "prd", "translate"],
  "skills_count": 3,
  "platforms": ["CLI", "飞书", "Discord", "WEB"],
  "recent_focus": "最近在探索 always-on AI 硬件形态，希望让 AI 走出屏幕、进入物理世界。",
  "openclaw_review": "给 AI 取名、造人格、找载体——你不是在用工具，你在养一个数字生命。",
  "generated_at": "2026-03-14"
}
```

## 运行依赖

数据采集和 HTML 预览（`collect-data.py`、`render-background-card.py`）仅需 Python 3.10+。

PNG 导出（`export-background-card.sh`）额外需要：
- `node`（>= 18）和 `npm`
- `playwright-core` — 可通过 metadata 中声明的 npm 依赖安装，或手动执行 `npm i -g playwright-core`
- 本地安装的 Chrome 或 Chromium 浏览器（当前仅文档声明，不能由 skill 自动安装）

如果缺少导出依赖，脚本会给出明确的错误提示。HTML 预览和迭代无需这些依赖。

## 网络请求与数据流向

本 skill 涉及以下外部通信：

### 浏览器资源请求（渲染/导出阶段）
- **背景图片**：`https://pub-626ee41d8f1544638070799686c756bf.r2.dev/open-card-bg.png`（Cloudflare R2，通过 CSS 加载）。可用本地文件路径覆盖以避免请求。
- **Google Fonts**：`https://fonts.googleapis.com` / `https://fonts.gstatic.com`（Inter 字体，通过 HTML 模板中的 `<link>` 加载）。

以上为浏览器渲染时发起的纯资源 GET 请求，不携带用户数据，但会暴露客户端 IP 和 HTTP 元数据。

### LLM 上下文传递（文案生成阶段）
`collect-data.py` 提取的 `copy_inputs` 包含本地文件摘录（USER.md / IDENTITY.md / MEMORY.md 的前 1000–2000 字符、记忆要点、统计摘要），这些内容会作为 LLM 上下文用于生成 `recent_focus`、`openclaw_review` 等文案字段。

- **如果 agent 使用云端模型**：摘录内容会发送至模型提供者的 API 端点。这是 agent 平台层面的行为，本 skill 不额外发起网络请求，但用户应知晓此数据流向。
- **如果 agent 使用本地模型**：所有处理均在本地完成，无数据外传。
- 本 skill 的脚本本身不直接调用任何外部 API，LLM 调用由 agent 运行时负责。

## LLM 生成字段

`recent_focus` 和 `openclaw_review` 必须由 AI agent 生成，而非 Python 脚本。脚本仅将结构化事实、备选文案和记忆要点提取到 `copy_inputs` 中；agent 必须在渲染前撰写并写入这两个字段。

### 生成流程

运行 `collect-data.py` 后，输出 JSON 中的 `copy_inputs` 包含所有生成所需的素材。agent 直接基于 `copy_inputs` 生成，不需要再去读原始文件。

`copy_inputs` 素材说明：

| 字段 | 内容 | 用途 |
|------|------|------|
| `user_md_excerpt` | USER.md 前 2000 字符 | 身份、角色、笔记、深度背景 |
| `identity_md_excerpt` | IDENTITY.md 前 1000 字符 | Agent 名称和人设，影响评论语气 |
| `memory_md_excerpt` | MEMORY.md 前 2000 字符 | 用户近期活动的完整上下文 |
| `memory_bullets` | 清洗后的记忆要点（≤12 条） | 精炼版近期行为 |
| `stats_summary` | token/平台/skills 统计 | 仅作辅助佐证，不作为文案主线 |

生成步骤：
1. 读取 `copy_inputs` 中的全部素材。
2. 生成 `recent_focus` 和 `openclaw_review`。
3. 将两个字段写入数据 JSON 后传给渲染器。

### `born_label` / `born_date` — 部署时间

右下角字段默认展示 OpenClaw 的部署时间，而不是时区城市。

- `born_label` 固定为 `Born`。
- `born_date` 使用 OpenClaw 首次开始运行的日期，默认格式为 `YYYY.MM.DD`。
- 时间来源优先取 `~/.openclaw/agents/main/sessions` 下最早的会话产物时间（包含当前会话、reset/deleted 历史文件和 `sessions.json` 索引文件）。
- 如果无法可靠读取，允许留空或使用中性占位，不要伪造日期。

### `platforms` — 展示层平台归一化

`platforms` 应展示用户可理解的接入平台，而不是内部 session source 原样输出。

默认归一化规则：
- 所有 `tui-*`、terminal、console 类来源 → `CLI`
- 所有 web / dashboard / browser / `webchat` 类来源 → `WEB`
- 消息平台保留平台名（如 `Discord`、`飞书`、`Telegram`、`Slack`）
- `cron` 等系统内部来源不展示
- 最终结果去重后输出

### `recent_focus` — 用户近况（卡片视觉主角）

**位置**：左侧大字区域，字号 38-56px，是整张卡片最醒目的文字。

写一个短句，概括用户近期在探索或推进的方向。

- 从 `memory_bullets` 和 `user_md_excerpt` 中提炼核心关键词。
- 要像一个标题/slogan，不是完整句子。可以省略主语。
- 具体、有画面感，不编造。
- 用用户的语言。
- **8–15 个中文字**（或 15–35 英文字符）。太短没有信息量，太长在大字号下会折行过多。
- 好的例子：`探索 always-on AI 硬件形态`、`让 agent 走进物理世界`
- 差的例子：`最近在研究一些关于 AI 的东西`（太泛）、`探索 always-on AI 硬件形态，希望让 AI 走出屏幕，进入物理世界并改变人们的日常生活方式`（太长）

### `openclaw_review` — OpenClaw 点评（左侧中间）

**位置**：左侧引用区域，字号 15-19px，带左侧竖线装饰。功能是**洞察**——让看到卡片的人停下来想"这话说得有意思"。

写一句犀利的判断，揭示用户自己可能都没注意到的行为模式。

写作方向（任选其一）：
1. **反差**：「多数人 X，你 Y」
2. **锐评**：把行为模式翻译成一句有态度的判断
3. **定性**：给一个意外但准确的标签
4. **洞察**：提出一个用户没意识到的模式

规则：
- 必须有观点。读起来像"用户简介"就是失败的。
- 至少引用一个来自 `memory_bullets` 或 `user_md_excerpt` 的具体细节作为论据。
- 语气：见过很多用户的老手，真诚认可但不夸张。
- 用用户的语言。
- **20–40 个中文字**（或 40–80 英文字符）。这个区域字号小、有竖线引用框，适合稍长的完整句。
- 好的例子：`给 AI 取名、造人格、找载体——你不是在用工具，你在养一个数字生命。`
- 差的例子：`你是一位很有想法的 AI 探索者。`（空话，无论据）

## 渲染指南

始终使用背景图合成模式（`render-background-card.py` + `background-template.html`）。

推荐流程：
1. 用 `scripts/collect-data.py` 生成数据 JSON，输出到 skill 目录之外的临时文件。
2. 阅读上下文来源，生成 `recent_focus` 和 `openclaw_review`（参见上方 LLM 生成字段）。
3. 将生成的字段更新到数据 JSON 中。
4. 用 `scripts/render-background-card.py` 和 `references/background-template.html` 渲染 HTML，输出到 skill 目录之外的临时预览文件。
5. 在浏览器中打开 HTML。
6. 视觉迭代。
7. 用 `scripts/export-background-card.sh` 导出最终图片。
8. 不要在 skill 打包目录中留下临时预览/数据文件。

## 设计指南

当用户要求调整样式时，将结构和样式分开处理。

典型顺序：
1. 确认要展示的字段。
2. 确认层级：什么应该视觉上突出。
3. 确认构图：居中、分栏、数据侧栏等。
4. 确认视觉体系：渐变、材质、字体排版、标签、边框。
5. 渲染并迭代。

高端展示卡的原则：
- 让主身份 + 近期关注承载情感分量。
- 让数据统计承载证明/展示分量。
- 避免让卡片看起来像后台仪表盘。
- 一个有力的构图优于多个嵌套的小卡片。

## 安全边界

- 不编造用户档案信息。
- 除非用户明确要求，不持久化新的用户档案设置。
- 不暴露本地文件中超出约定名片字段的敏感信息。
- 如果某个字段无法可靠读取，省略它或使用中性的备选值。
- 如果用户要求制作面向公众的卡片，优先使用更简洁的标签，减少原始技术字符串。

### 凭证与模型访问

本 skill 的脚本不读取、存储或要求任何 API 密钥或环境变量。但文案生成阶段隐含依赖 agent 平台已配置的模型访问能力——即 agent 运行时的模型凭证。这不由本 skill 管理，而是 agent 平台的基础设施责任。

### 会话数据隐私

会话记录文件（`*.jsonl`）可能包含敏感消息内容。数据采集脚本采用严格的字段级提取：
- 从会话记录中：仅读取 `type`、`timestamp` 和 `usage.totalTokens` 字段；不提取或存储任何消息正文内容。
- 从 `sessions.json` 中：仅读取 session key 结构和 `deliveryContext`/`origin` 元数据用于平台检测；不访问任何消息内容。
- 归一化后的 JSON 输出仅包含上述稳定 schema 中定义的字段，不包含任何原始会话内容。
- `copy_inputs` 中包含的本地文件摘录（USER.md / IDENTITY.md / MEMORY.md 片段）会作为 LLM 上下文使用，使用云端模型时这些摘录将发送至模型提供者。用户应根据自身隐私需求选择本地或云端模型。
- 临时数据/预览文件应视为半敏感文件，使用后及时清理。

## 资源

### scripts/
- `collect-data.py`：读取本地 OpenClaw/用户文件，归一化为渲染用 JSON。
- `render-background-card.py`：使用归一化数据和背景图渲染 OpenCard，生成 HTML 预览。
- `export-background-card.sh`：通过 Playwright + Chrome 将 HTML 预览导出为最终 PNG 图片。

### references/
- `field-schema.md`：字段定义和提取规则，供后续迭代参考。
- `design-notes.md`：本项目已确定的视觉约束和样式方向。
- `background-template.html`：背景图合成模板，用于海报风格的 OpenCard 输出。

### 默认背景图
- URL：`https://pub-626ee41d8f1544638070799686c756bf.r2.dev/open-card-bg.png`