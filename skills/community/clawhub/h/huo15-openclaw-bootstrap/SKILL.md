---
name: huo15-openclaw-bootstrap
displayName: 火一五你好世界技能
description: Use this skill when the user says "你好世界" / "你好世界初始化" / "初始化龙虾" / "龙虾初始化" / "初始化" / "bootstrap" / "hello world" / "onboarding" / "重新认识一下" / "重置我的偏好" / "更新画像", OR when the current working directory contains a BOOTSTRAP.md file. This skill guides users through a 4-step onboarding process to initialize their OpenClaw workspace by creating IDENTITY.md, USER.md, SOUL.md, TOOLS.md, and AGENTS.md files.
version: 2.1.0
homepage: https://github.com/zhaobod1/huo15-skills
metadata: { "openclaw": { "emoji": "🦞", "requires": { "bins": [] } } }
aliases:
  - 火一五你好世界技能
  - 火一五初始化技能
  - 你好世界
  - 龙虾你好世界
  - 龙虾初始化
  - 初始化龙虾
  - 首次设置
  - bootstrap
  - hello world
  - onboarding
  - welcome
  - 工作目录初始化
  - 填 SOUL.md
  - 填 IDENTITY.md
  - 填 USER.md
---

# 火一五你好世界技能 v2.1(huo15-openclaw-bootstrap)

> 一次 3 分钟(全默认 30 秒)的开机仪式。对齐 openclaw 2026.6.8 原生工作目录约定。
> 青岛火一五信息科技有限公司 · OpenClaw 生态标配

---

## 一、什么时候用

✅ **触发**:
- 当前 cwd 存在 `BOOTSTRAP.md`(原生 marker — openclaw seed 新 workspace 时自动创建)
- 用户说"你好"/"hello world"/"欢迎"/"初始化"/"bootstrap"/"onboarding"
- 用户说"重新认识一下"/"重置我的偏好"/"更新画像"
- 用户说"填一下 SOUL.md / IDENTITY.md / USER.md"

❌ **不触发**:
- BOOTSTRAP.md 不存在 + 5 件套(SOUL/IDENTITY/USER/TOOLS/AGENTS)都已填写 → **走增量更新模式**(§六)
- 用户问日常问题、与身份无关任务

---

## 二、与 openclaw 2026.6.8 原生约定对齐(必读)

> 依据:openclaw 2026.6.8 包内官方文档 `docs/concepts/agent-workspace.md`(随发布包分发,shasum 锚定)。

workspace 默认在 `~/.openclaw/workspace`(设了环境变量 `OPENCLAW_PROFILE` 且非 `default` 时为 `~/.openclaw/workspace-<profile>`)。OpenClaw **每次会话开始**把下列 workspace 文件加载进上下文;某个文件缺失则注入一个 "missing file" 占位并继续。

| 文件 | 视角 | 火一五填什么 |
|---|---|---|
| **AGENTS.md** | 操作规则,每会话加载 | 工作约定 / 自主度 / 隐私偏好 / 火一五品牌页脚 |
| **SOUL.md** | 人格语气,每会话加载 | 灵魂主辅权重 / 写作风格 / Communication 偏好 |
| **USER.md** | 用户是谁,每会话加载 | 昵称 / 称呼 / 时区 / 关注领域 |
| **IDENTITY.md** | Agent 名字/vibe/emoji,bootstrap 时建 | Name / Creature / Vibe / Emoji / Roles |
| **TOOLS.md** | 本机工具约定(仅指引,不控权限) | 项目目录 / 通知通道 / 设备别名 |
| **BOOTSTRAP.md** | 一次性开机仪式 marker(仅新 workspace) | **填完必须删** |
| HEARTBEAT.md | 心跳清单(可选,保持简短) | 本 skill 不填,保留原生 seed |
| BOOT.md | 网关重启启动清单(可选) | 本 skill 不填,保留原生 seed |
| MEMORY.md | 长期记忆索引(可选,**仅主会话**加载) | 不本 skill 管;明细放 `memory/YYYY-MM-DD.md` |

本 skill **只写 5 个**:`AGENTS.md` / `SOUL.md` / `USER.md` / `IDENTITY.md` / `TOOLS.md`。HEARTBEAT.md / BOOT.md / MEMORY.md 保留原生 seed,BOOTSTRAP.md 收尾删除。

⚠️ **写入限长**:bootstrap 文件注入时会截断 — 单文件上限 `agents.defaults.bootstrapMaxChars`(默认 20000 字符)、合计 `bootstrapTotalMaxChars`(默认 60000)。每个文件写精炼,别灌大段。

**铁律**:
- 不另起 `profile.md` 灶(v1.x 的设计被废弃)
- 不写 L1 龙虾 memory(原生 file→memory 链路自己工作)
- L2 enhance / L3 KB 是**可选**增强,不写也工作
- 完成信号 = **BOOTSTRAP.md 删除**(openclaw 据此判定 onboarding 完成)
- 用户若自管 workspace 文件,可配 `agents.defaults.skipBootstrap: true` 关原生 seed

---

## 三、快捷流程(4 步)

**每一步都是一条消息、一次性把所有相关问题列出来,等用户一次性回复**。禁止拆成多轮问。

### Step 0 · 检测 + 招呼

LLM 第一件事:`ls` 当前 cwd,看是否有 BOOTSTRAP.md / 5 件套。

```
🦞 我看到你的工作目录有 BOOTSTRAP.md 等着我做开机仪式。

接下来 4 步,每步一张填空表,你一次回我就行,30 秒搞定:
① 基本信息 → ② 人设(经典组合 6 选 1 或自定义) → ③ 关注领域 → ④ 偏好

先回 "开始" 或者直接答 Step 1 的填空。
```

### Step 1 · 基本信息(一次填 3 项)

```
🦞 第 1 步,3 件事一起回(留空走默认):

① 昵称:____           (留空 = 用 user_identity.name 或 "朋友")
② 英文名/称呼:____    (留空 = 自动从昵称拼音生成)
③ 时区(选数字):
   1) 上海/北京 UTC+8  ← 推荐
   2) 香港  3) 东京/首尔  4) 新加坡
   5) 伦敦  6) 柏林/巴黎  7) 旧金山  8) 纽约  9) 其他

格式随意:"Job / Job / 1" 或 "昵称=Job" 或 "我叫 Job" 或 "1"(全默认仅答时区)
```

**解析规则**:支持松散格式;任何项缺失走默认;全空白("随便"/"默认")→ 全默认进 Step 2。

### Step 2 · 人设 — 经典组合 or 自定义

```
🎭 第 2 步,选龙虾人设。两条路:

【A】套经典组合(推荐新手) — 回数字 1-6:
1) 独立开发者  | 硅谷导师 × 禅师      | 全栈+PM+Indie      | 前端/后端/AI/变现
2) 品牌设计师  | 苹果极简 × 京都匠人  | 品牌+UI 设计       | UI/品牌/摄影/哲学
3) 产品经理    | 德鲁克 × 硅谷 PM     | PM+数据分析         | 产品/数据/管理
4) 技术博主    | TED × B站up主        | 技术作者+自媒体    | 写作/Obsidian/AI
5) AI 研究员   | 严谨学者 × 纪录片    | AI/ML+学术          | LLM/Agent/论文
6) 创业者      | 稻盛和夫 × 硅谷导师  | 创业者+PM+销售     | 创业/产品/团队

【B】自定义 — 回 "7",我给你填空模板(灵魂/角色/权重)
【C】完全随便 — 回 "默认",用组合 1
```

选 1-6 → 直接套用 §五 经典组合的 `soul + roles + interests`,跳到 Step 4。

选 7(自定义)→ 发填空模板:

```
📝 自定义人设(留空走推荐默认):

主灵魂:____   (数字或名字;见 presets/souls.md;默认:硅谷导师)
辅灵魂:____   (可留空;默认:禅师,权重 70/30)
权重:____     (默认 70/30;可 60/40 / 50/50)

主角色:____   (数字或名字;见 presets/roles.md;默认:全栈工程师)
副角色:____   (可留空;最多 2 个;逗号分隔,如 "产品经理, 独立开发者")

想看灵魂/角色全表?回 "看灵魂" 或 "看角色"。
```

### Step 3 · 关注领域 — 套餐 or 多选

经典组合已预填 → 仅询问"要改吗?"。否则发:

```
🧲 第 3 步,关注哪些领域?(挖新闻/推荐/维护 KB 用)

【A】套餐(8 选 1,回数字):
1) 独立开发者  (前端/后端/LLM/indie-saas/公众号/SEO/生产力/笔记)
2) 独立设计师  (UI/品牌/插画/设计系统/小红书/写作/摄影/哲学)
3) AI 研究员   (LLM/Agent/Prompt/RAG/ML/微调/论文/多模态)
4) 自媒体博主  (写作/技术写作/公众号/小红书/B站/抖音/剪辑/SEO)
5) 创业者      (创业/indie-saas/管理/增长/品牌/投资/销售/成长)
6) 增长 PM     (产品/数据/增长/SEO/信息流广告/社群/心理学/笔记)
7) 电商操盘手  (国内电商/跨境/直播/广告/品牌/社群/小红书/抖音)
8) 终身学习者  (成长/GTD/笔记/阅读/英语/思维模型/学习法/哲学/历史/心理学)

【B】自选 — 回 "自选",给你 82 项完整菜单
【C】完全随便 — 回 "默认",用套餐 1
```

"自选" → 显示 [`presets/domains.md`](presets/domains.md) 10 大类,用户回类号或 slug 列表。

### Step 4 · 偏好与边界(一张表,一次改完)

```
⚙️ 第 4 步,默认偏好表。看一下要改的吗?没有就回 "确认":

| # | 项         | 默认         | 其他选项                    |
|---|-----------|-------------|----------------------------|
| 1 | 主要语言   | 中文        | 英文 / 中英双语 / 跟随       |
| 2 | 详细度     | 适中        | 精简 / 详尽                 |
| 3 | 语气温度   | 平衡        | 冷静 / 热情                 |
| 4 | Emoji      | 克制        | 禁用 / 丰富                 |
| 5 | 出错处理   | 先给备选    | 立刻认错 / 深挖根因          |
| 6 | 执行自主度 | 平衡        | 保守(每步问) / 激进(自跑)    |
| 7 | 主动建议   | 允许        | 只在被问时回答              |
| 8 | 记忆隐私   | 只记工作相关 | 记所有 / 不记个人细节        |
| 9 | 项目目录   | ~/workspace/projects/ | 自定义路径        |
|10 | 通知通道   | 企微        | 微信 / 邮件 / 仅本地         |

改法示例:"1: 英文, 6: 激进, 10: 微信";不改就回 "确认"。
```

---

## 四、收尾:写 5 件套 + 删 BOOTSTRAP.md + (可选)L3

4 步结束后,LLM 按以下顺序操作。**所有 Edit/Write 都针对当前 cwd**(用户的 workspace,不是本 skill 目录)。

### 4.1 渲染 5 个原生文件

读 `templates/IDENTITY.md.tmpl` / `USER.md.tmpl` / `SOUL.md.tmpl` / `TOOLS.md.tmpl` / `AGENTS.md.tmpl` 四件套(在本 skill 目录下),做 string replace 把占位符 `{{nickname}}` `{{soul.primary}}` 等换成 slot 值。

**关键**:写到 cwd 的文件名是大写 `SOUL.md` / `IDENTITY.md` / `USER.md` / `TOOLS.md` / `AGENTS.md`(原生 DEFAULT_*_FILENAME)。如果 cwd 已存在(原生 seed 过)→ **覆盖前先备份**(`cp SOUL.md SOUL.md.bak.<ts>`)。

各文件的字段映射:

**IDENTITY.md**(Agent 视角)
- Name = `{english_name}` 或 `{nickname}`
- Creature = "龙虾的小助手"(默认)/ 自定义
- Vibe = 由 `comm.warmth` 推导:cool="冷静专业" / balanced="平衡敏锐" / warm="温暖热情"
- Emoji = `comm.emoji` 推导:off=空 / sparse=🦞 / rich=🦞✨
- Avatar = 留空("workspace-relative path TBD")
- **Roles**(火一五增强段):列 `{roles}`,主角色加 ⭐

**USER.md**(User 视角)
- Name = `{nickname}`
- What to call them = `{english_name}` 或 `{nickname}`
- Pronouns = 留空(用户后填)
- Timezone = `{timezone}`(IANA 形式)
- Notes = 留空
- **Context**(火一五增强段):列 `{interests}` slug,分组 + 一句话说"在做什么"

**SOUL.md**(Agent 性格)
- 保留原生 "Core Truths" 段(原始模板 1933 字节内容)
- **新加 "Personal Style"** 段:主灵魂 `{soul.primary}` 权重 X% / 辅灵魂 `{soul.secondary}` 权重 Y% — 列 souls.md 中两个灵魂的特征摘要
- **新加 "Communication"** 段:语言 `{comm.language}` / 详细度 `{comm.verbosity}` / 温度 `{comm.warmth}` / Emoji `{comm.emoji}` / 出错 `{comm.on_error}`

**TOOLS.md**(本机环境)
- 保留原生 "What Goes Here" / "Examples"
- **新加 "Environment"** 段:项目目录 `{ecosystem.project_dir}` / 通知通道 `{ecosystem.notify}`(企微/微信/邮件/仅本地)
- 留出 SSH/摄像头/设备昵称等空白行让用户后填

**AGENTS.md**(工作约定)
- 保留原生 "First Run" / "Session Startup"
- **新加 "Working Style"** 段:执行自主度 `{autonomy.exec}` / 主动建议 `{autonomy.proactive}` / 记忆隐私 `{autonomy.privacy}`
- **新加 "Brand Footer"**:火一五 LOGO + 公司 + QQ群 + 联系邮箱(见 `templates/AGENTS.md.tmpl` 页脚)

### 4.2 复制全局 MEMORY.md（可选，支持多 workspace 共享记忆）

**场景**：当钉钉插件配置为 `separateSessionByConversation=true` + `sharedMemoryAcrossConversations=false` 时，每个用户有独立的 workspace，但需要共享全局记忆（如公司组织架构、凭据等）。

**操作**：
1. 检查全局 MEMORY.md 是否存在：`~/.openclaw/workspace/MEMORY.md`
2. 如果存在且当前 workspace 的 MEMORY.md 不存在或为空，则复制全局 MEMORY.md 到当前 workspace
3. 如果当前 workspace 已有 MEMORY.md，则在文件末尾追加全局 MEMORY.md 的内容（避免覆盖用户个人记忆）

```bash
# 检查全局 MEMORY.md
GLOBAL_MEMORY=~/.openclaw/workspace/MEMORY.md
if [ -f "$GLOBAL_MEMORY" ]; then
  if [ ! -f MEMORY.md ]; then
    # 当前 workspace 没有 MEMORY.md，直接复制
    cp "$GLOBAL_MEMORY" MEMORY.md
  else
    # 当前 workspace 已有 MEMORY.md，追加全局内容
    echo "\n\n---\n\n## 全局共享记忆（来自 ~/.openclaw/workspace/MEMORY.md）\n" >> MEMORY.md
    cat "$GLOBAL_MEMORY" >> MEMORY.md
  fi
fi
```

**注意**：这一步是可选的，只在多 workspace 模式下需要。如果是单一 workspace 模式（`sharedMemoryAcrossConversations=true`），则跳过此步骤。

### 4.3 删 BOOTSTRAP.md(完成信号)

```bash
rm BOOTSTRAP.md  # 或 mv BOOTSTRAP.md BOOTSTRAP.md.completed.<ts>
```

**为什么必须删**:`src/agents/workspace.ts` 检测 BOOTSTRAP.md 存在 = "bootstrap pending" 状态;删除 = "bootstrap complete"。不删 → workspace 永远在 onboarding 模式。

### 4.4 可选 L3 KB 备份(跨设备/跨 workspace 副本)

写 `~/knowledge/huo15/profile/<nickname>-<workspace-name>.md`,用 `templates/L3-kb.md.tmpl` 渲染——内容 = 5 件套关键字段聚合 + frontmatter(便于 grep 历史画像)。

**这一步可跳**(如果用户说"不要 L3"或当前是个临时 workspace)。

### 4.5 回显摘要

```
🦞 搞定!欢迎 <昵称>。开机仪式 4 步完成:

身份:<昵称> / <英文名> / <时区>
灵魂:<主>(<weight>% 主) × <辅>(<weight>% 辅)
角色:<主角色> + <副角色若有>
领域:<N>个(<类列表>)
偏好:<语言>/<详细度>/<语气>/自主度<X>

✓ 已写入工作目录 5 件套:SOUL.md / IDENTITY.md / USER.md / TOOLS.md / AGENTS.md
✓ 已复制全局 MEMORY.md(如适用)
✓ 已删 BOOTSTRAP.md(workspace 状态:complete)
✓ 已备份 L3 KB:~/knowledge/huo15/profile/<昵称>.md

下一回 openclaw 进同一 workspace 会自动加载这 5 个文件到 system prompt。

第一件想让我帮你做什么?
```

---

## 五、6 个经典组合(Classic Combos)详表

### 🚀 1. 独立开发者 / Indie Hacker
- 灵魂:硅谷导师(主 70)× 禅师(辅 30)
- 角色:全栈工程师 + 产品经理 + 独立开发者
- 领域:`frontend` `backend` `llm-app` `indie-saas` `wechat-gzh` `seo-sem` `productivity-gtd` `note-taking`

### 🎨 2. 品牌设计师 / Brand Designer
- 灵魂:苹果极简(主 60)× 京都匠人(辅 40)
- 角色:品牌设计师 + UI 设计师
- 领域:`ui-visual` `brand-vi` `illustration` `design-systems` `xiaohongshu` `writing` `photography` `philosophy`

### 📊 3. 产品经理 / Product Manager
- 灵魂:德鲁克顾问(主 60)× 硅谷 PM(辅 40)
- 角色:产品经理 + 数据分析师
- 领域:`product-design` `data-analysis` `growth-hacking` `ui-visual` `psychology` `management-leadership` `note-taking` `writing`

### 🎓 4. 技术博主 / Tech Content Creator
- 灵魂:TED 演说(主 60)× B 站 up 主(辅 40)
- 角色:技术作者 + 自媒体作者 + 独立开发者
- 领域:`tech-writing` `note-taking` `writing` `wechat-gzh` `bilibili-youtube` `llm-app` `seo-sem` `frontend`

### 🧠 5. AI 研究员 / AI Researcher
- 灵魂:严谨学者(主 70)× 纪录片旁白(辅 30)
- 角色:AI/ML 研究员 + 学术研究员
- 领域:`llm-app` `agent-dev` `prompt-engineering` `rag-vectordb` `ml-dl` `llm-finetune` `academic-writing` `computer-vision`

### 💼 6. 创业者 / Founder
- 灵魂:稻盛和夫(主 50)× 硅谷导师(辅 50)
- 角色:创业者 + 产品经理 + 销售代表
- 领域:`entrepreneurship` `indie-saas` `management-leadership` `growth-hacking` `brand-marketing` `finance-investment` `sales-negotiation` `personal-growth`

(完整清单见 [`presets/souls.md`](presets/souls.md) / [`presets/roles.md`](presets/roles.md) / [`presets/domains.md`](presets/domains.md))

---

## 六、增量更新模式

`BOOTSTRAP.md` 已删除 + 5 件套都在 = workspace 已 onboarded → 走这一支。

```
🦞 你的工作目录已经初始化过了。要改哪个?

1) IDENTITY.md  — 我是谁(name / creature / vibe / emoji)
2) USER.md      — 你是谁(昵称 / 时区 / 关注领域)
3) SOUL.md      — 我的性格(灵魂权重 / Communication 偏好)
4) TOOLS.md     — 本机环境(项目目录 / 通知通道 / SSH 别名)
5) AGENTS.md    — 工作约定(自主度 / 隐私 / 团队规则)
6) 全部重置     — 重新跑 4 步仪式(会备份当前 5 件套到 .bak)

回数字 + 想改的具体字段,如:"3, 灵魂权重改 50/50"
```

改完后:在被改文件的"Update log"段 append 一行 `- <ISO date> 更新 <字段>: <旧> → <新>`。L3 KB 同步加 changelog 行。

---

## 七、硬红线

1. ❌ **不写自定义 profile.md** — v1.x 的产物已废弃,只用原生 5 件套
2. ❌ **不写 L1 龙虾 memory** — 原生 file→memory 链路自己工作,本 skill 不重复
3. ❌ **不要拆成 9 轮问** — 4 步极限,每步一张填空表
4. ❌ **不要擅自覆盖用户已有答案** — 默认值是建议,用户明确给的值优先
5. ❌ **覆盖原生 seed 文件前必备份**(`cp SOUL.md SOUL.md.bak.<ts>`)
6. ❌ **必须删 BOOTSTRAP.md** — 不删 = workspace 永远 onboarding 模式
7. ❌ **不要在流程中干别的活** — 4 步走完再说其它
8. ❌ **全默认路径不要追问** — 用户说"默认"就全默认到底,连确认都省

---

## 八、Slots / 变量命名

```yaml
nickname: string              # Step 1 → USER.md.Name + IDENTITY.md fallback
english_name: string          # Step 1 → IDENTITY.md.Name
timezone: string (IANA)       # Step 1 → USER.md.Timezone
soul:
  primary: string (slug)      # → SOUL.md "Personal Style" 主
  secondary: string|null      # → SOUL.md "Personal Style" 辅
  weight: string              # "70/30" etc.
roles: [{slug, primary}]      # → IDENTITY.md "Roles" 段
interests: [string]           # → USER.md "Context" 段
comm:
  language: string            # → SOUL.md "Communication" 段
  verbosity: "concise"|"balanced"|"thorough"
  warmth: "cool"|"balanced"|"warm"   # → IDENTITY.md.Vibe 推导
  emoji: "off"|"sparse"|"rich"        # → IDENTITY.md.Emoji 推导
  on_error: "admit"|"alt-then-fix"|"rca"
autonomy:
  exec: "conservative"|"balanced"|"aggressive"   # → AGENTS.md "Working Style"
  proactive: bool
  privacy: "work-only"|"all"|"minimal"
ecosystem:
  project_dir: string         # → TOOLS.md "Environment"
  notify: "wecom"|"wechat"|"email"|"local"
  kb_targets: [string]        # 可选,L3 KB 写到哪
meta:
  bootstrapped_at: ISO date
  version: "2.1.0"
  combo_id: "1".."6"|null     # null = 自定义
  workspace_dir: string       # cwd 绝对路径
```

---

## 九、文件清单

```
huo15-openclaw-bootstrap/
├── SKILL.md                  # 你正在看的这个
├── _meta.json                # ClawHub meta
├── LICENSE
├── presets/
│   ├── souls.md              # 灵魂全表(用作 §三 Step 2 自定义参考)
│   ├── roles.md              # 角色全表
│   ├── domains.md            # 领域全表(82 项)
│   └── timezones.md          # 时区参考
└── templates/                # v2.0 重构:5 件套原生模板 + 火一五增强段
    ├── IDENTITY.md.tmpl
    ├── USER.md.tmpl
    ├── SOUL.md.tmpl
    ├── TOOLS.md.tmpl
    ├── AGENTS.md.tmpl
    ├── BOOTSTRAP.md.tmpl     # 火一五版首次对话引导(可选,装本 skill 时把它替换原生 seed)
    └── L3-kb.md.tmpl         # ~/knowledge/huo15/profile/ 备份
```

---

## 十、版本

- **v2.1.0(2026-06-20)**:**对齐 openclaw 2026.6.8(依据包内官方文档 `docs/concepts/agent-workspace.md`,shasum 锚定)**
  - §二 workspace 文件表按官方文档校正:补 `HEARTBEAT.md`(可选心跳清单)/ `BOOT.md`(可选,网关重启启动清单)
  - 去掉不精确的 `src/agents/system-prompt.ts CONTEXT_FILE_ORDER` 说法,改用官方表述「每次会话开始加载」
  - 新增写入限长提示:`bootstrapMaxChars`(默认 20000)/ `bootstrapTotalMaxChars`(默认 60000),文件过大会被截断
  - 补 workspace 默认路径(`~/.openclaw/workspace` / `OPENCLAW_PROFILE` 变体)与 `skipBootstrap` 开关
  - 仍只写 5 件套(AGENTS/SOUL/USER/IDENTITY/TOOLS),完成信号仍是删 `BOOTSTRAP.md`(经官方文档确认未变)
- **v2.0.0(2026-05-07)**:**对齐 openclaw 2026.5+ 原生约定的重构**
  - 不再产 `profile.md`,改产原生 5 件套 `SOUL.md` / `IDENTITY.md` / `USER.md` / `TOOLS.md` / `AGENTS.md`(由 `src/agents/system-prompt.ts` `CONTEXT_FILE_ORDER` 自动加载到 system prompt)
  - 删 L1 龙虾 memory 写盘逻辑(原生 file→memory 链路自己管,§11.4 红线 §1 不复制)
  - 完成信号改为**删 `BOOTSTRAP.md`**(让 openclaw workspace state 转 complete)
  - L3 KB 备份保留为可选(跨设备/跨 workspace 副本,火一五独有)
  - 增量更新模式按 5 件套拆分(改哪个文件就改哪个)
  - 触发器优先检测 BOOTSTRAP.md 存在(原生 marker)
  - 新增 `templates/{IDENTITY,USER,SOUL,TOOLS,AGENTS,BOOTSTRAP,L3-kb}.md.tmpl`,删 `templates/profile.md`
  - 字段映射规范化:nickname/timezone → USER.md;soul/comm → SOUL.md;roles → IDENTITY.md;autonomy → AGENTS.md;ecosystem → TOOLS.md
- **v1.1.0**(2026-04-25):4 步极简流程 + 6 经典组合 + 全默认 30 秒(已废弃 — 用 v2.0)
- **v1.0.0**(2026-04-24):首发 9 步硬流程

---

**公司:** 青岛火一五信息科技有限公司 · postmaster@huo15.com · QQ群 1093992108
