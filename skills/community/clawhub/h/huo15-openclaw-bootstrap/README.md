# 火一五你好世界技能 · huo15-openclaw-bootstrap

---

<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

<h3>打破信息孤岛，用一套系统驱动企业增长</h3>
<h3>加速企业用户向全场景人工智能机器人转变</h3>

</div>

<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>

---

<div align="center">

![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.6.8-orange)
![ClawHub](https://img.shields.io/badge/ClawHub-published-ff6b6b)

</div>

---

## 这是什么

**`huo15-openclaw-bootstrap` v2.1.0** 是龙虾(OpenClaw)/ Claude Code 工作目录的**开机仪式**技能。3 分钟(全默认 30 秒)4 步填空,自动写满 openclaw 原生约定的 5 件套(`SOUL.md` / `IDENTITY.md` / `USER.md` / `TOOLS.md` / `AGENTS.md`),并删掉 `BOOTSTRAP.md` 让 workspace 状态转 `complete`。

**v2.0.0 关键升级**:对齐 openclaw 2026.5+ `src/agents/system-prompt.ts` `CONTEXT_FILE_ORDER` 自动加载约定,**不再产 v1.x 的 `profile.md`**(违反"不复制龙虾原生功能"红线),改写**原生 5 件套**让 system-prompt loader 自己工作。

---

## 它解决什么

新装 OpenClaw / Claude Code 进一个新 workspace,看到一堆 `BOOTSTRAP.md` / `IDENTITY.md` / `USER.md` 空模板,通常会:

1. **手填**:每个文件挨个开,看原生模板里 6-8 个空格,逐项写 — 累且枯燥
2. **跳过**:不填,但 system-prompt 加载空模板 = AI 不知道你是谁,AI 也不知道自己是谁

本 skill 把"填 5 件套"这件事打包成 **4 步对话**(每步一张填空表),并提供 6 经典人设组合**一键套用**。30 秒走完,5 文件全填好,BOOTSTRAP.md 自删。

---

## 与 openclaw 原生约定对齐

openclaw 2026.6.8 **每次会话开始**加载 workspace 文件到上下文(依据包内官方文档 `docs/concepts/agent-workspace.md`)。本 skill 写其中 5 个,其余保留原生 seed:

| 文件 | 视角 | 本 skill |
|---|---|---|
| **AGENTS.md** | 操作规则,每会话加载 | ✅ 写 |
| **SOUL.md** | 人格语气,每会话加载 | ✅ 写 |
| **USER.md** | 用户是谁,每会话加载 | ✅ 写 |
| **IDENTITY.md** | 名字/vibe/emoji | ✅ 写 |
| **TOOLS.md** | 本机工具约定 | ✅ 写 |
| **BOOTSTRAP.md** | 一次性开机 marker | 🗑️ 填完删 |
| HEARTBEAT.md / BOOT.md | 心跳清单 / 网关重启启动清单(可选) | 保留原生 seed |
| MEMORY.md | 长期记忆索引(仅主会话加载) | 不本 skill 管 |

> 注:bootstrap 文件注入有长度上限(`bootstrapMaxChars` 默认 20000 / `bootstrapTotalMaxChars` 默认 60000),写精炼。

---

## 怎么触发

✅ **触发**:
- 当前 cwd 存在 `BOOTSTRAP.md`(原生 marker)
- 用户说"你好"/"hello world"/"欢迎"/"初始化"/"bootstrap"/"onboarding"
- 用户说"重新认识一下"/"重置我的偏好"/"更新画像"
- 用户说"填一下 SOUL.md / IDENTITY.md / USER.md"

❌ **不触发**:
- BOOTSTRAP.md 不存在 + 5 件套都已填写 → **走增量更新模式**
- 用户问日常问题、与身份无关任务

---

## 4 步流程概览

### Step 1 · 基本信息(一次填 3 项)

```
① 昵称 / ② 英文名 / ③ 时区(9 选 1)
```

支持松散格式 ("Job / Job / 1"、"我叫 Job"、"默认")。

### Step 2 · 人设 — 经典组合 6 选 1 或自定义

| # | 组合 | 灵魂 | 角色 | 领域 |
|---|---|---|---|---|
| 1 | 独立开发者 | 硅谷导师 × 禅师 | 全栈+PM+Indie | 前端/后端/AI/变现 |
| 2 | 品牌设计师 | 苹果极简 × 京都匠人 | 品牌+UI 设计 | UI/品牌/摄影/哲学 |
| 3 | 产品经理 | 德鲁克 × 硅谷 PM | PM+数据分析 | 产品/数据/管理 |
| 4 | 技术博主 | TED × B站up主 | 技术作者+自媒体 | 写作/Obsidian/AI |
| 5 | AI 研究员 | 严谨学者 × 纪录片 | AI/ML+学术 | LLM/Agent/论文 |
| 6 | 创业者 | 稻盛和夫 × 硅谷导师 | 创业者+PM+销售 | 创业/产品/团队 |

选 1-6 一键套用;选 7 进自定义模板(主辅灵魂 + 权重 + 1-3 角色)。

### Step 3 · 关注领域

8 个套餐 or 82 项 [`presets/domains.md`](presets/domains.md) 自选。

### Step 4 · 偏好与边界(10 项一表)

语言 / 详细度 / 语气温度 / Emoji / 出错处理 / 执行自主度 / 主动建议 / 记忆隐私 / 项目目录 / 通知通道 — 一次回 "1: 英文, 6: 激进, 10: 微信" 或 "确认"。

---

## Slot → 5 件套字段映射

| 收集到的字段 | 写到原生 |
|---|---|
| nickname / english_name / timezone | `USER.md` |
| interests(领域) | `USER.md` Context 段 |
| soul.primary/secondary/weight + comm.* | `SOUL.md` Personal Style + Communication 段 |
| roles(1-3) | `IDENTITY.md` Roles 段 |
| autonomy.exec/proactive/privacy | `AGENTS.md` Working Style 段 |
| ecosystem.project_dir/notify | `TOOLS.md` Environment 段 |
| 火一五品牌(LOGO / QQ群 / 公司) | `AGENTS.md` 页脚 |

---

## L3 KB 备份(可选 · 火一五独有价值)

写到 `~/knowledge/huo15/profile/<昵称>-<workspace>.md`,用 [`templates/L3-kb.md.tmpl`](templates/L3-kb.md.tmpl) 渲染——frontmatter **23 个字段**(nickname / soul / roles / interests / comm / autonomy / ecosystem / meta)便于 grep 历史画像。

**为什么有这一层**:openclaw 原生 5 件套只在**单 workspace 内**生效。L3 KB 是跨 workspace / 跨设备的副本,翻历史画像 / 同步新 workspace / 跨账号迁移用。

---

## 文件结构

```
huo15-openclaw-bootstrap/
├── SKILL.md                  # ClawHub 嵌入源(< 25KB)
├── README.md                 # 本文件
├── _meta.json                # ownerId / slug / version
├── LICENSE                   # MIT
├── presets/
│   ├── souls.md              # 37 款灵魂全表
│   ├── roles.md              # 49 款角色全表
│   ├── domains.md            # 82 项领域全表
│   └── timezones.md          # 9 个常用时区
└── templates/                # v2.0.0 重构:5 件套 + 火一五增强
    ├── IDENTITY.md.tmpl
    ├── USER.md.tmpl
    ├── SOUL.md.tmpl
    ├── TOOLS.md.tmpl
    ├── AGENTS.md.tmpl
    ├── BOOTSTRAP.md.tmpl     # 火一五版首次对话引导(可选替换原生 seed)
    └── L3-kb.md.tmpl         # ~/knowledge/huo15/profile/ 备份
```

---

## 安装

### 从 ClawHub 安装(推荐)

```bash
clawhub install huo15-openclaw-bootstrap --dir ~/.openclaw/workspace/skills
```

### 从源码安装

```bash
git clone git@github.com:zhaobod1/huo15-skills.git
cp -r huo15-skills/huo15-openclaw-bootstrap/ ~/.openclaw/workspace/skills/
```

重启 OpenClaw / Claude Code 即可识别。

---

## 使用

进入一个新 workspace(或当前 workspace 还有 `BOOTSTRAP.md` 没删)→ 跟 AI 说**任意一种**:

- "你好"
- "hello world"
- "初始化龙虾"
- "bootstrap"
- "走开机仪式"
- "填一下 SOUL.md / IDENTITY.md / USER.md"

AI 自动按 SKILL.md 流程走完 4 步,写好 5 件套,删 BOOTSTRAP.md,告诉你下一回 openclaw 进同一 workspace 会自动加载这 5 个文件到 system prompt。

---

## 增量更新

`BOOTSTRAP.md` 已删 + 5 件套都在 = 已 onboarded → 跟 AI 说"重新认识一下"或"改我的偏好"等,AI 进增量模式问改哪个文件:

```
1) IDENTITY.md  — 我是谁(name / creature / vibe / emoji)
2) USER.md      — 你是谁(昵称 / 时区 / 关注领域)
3) SOUL.md      — 我的性格(灵魂权重 / Communication)
4) TOOLS.md     — 本机环境(项目目录 / 通知通道 / SSH 别名)
5) AGENTS.md    — 工作约定(自主度 / 隐私 / 团队规则)
6) 全部重置     — 重新跑 4 步仪式(会备份当前 5 件套到 .bak)
```

改完后:被改文件的 "Update log" 段 append 一行 `- <ISO date> 更新 <字段>: <旧> → <新>`;L3 KB 同步加 changelog。

---

## 与火一五其他 skill 协作

| 场景 | 配套 skill |
|---|---|
| 仪式后写第一份复盘 / 客户提案 PDF | [`huo15-markdown-export`](../huo15-markdown-export/)(11 主题排版发布) |
| 仪式后做品牌设计 / UI 原型 | [`huo15-openclaw-frontend-design`](../huo15-openclaw-frontend-design/) |
| 仪式后写公文 / 合同 / PRD | [`huo15-openclaw-office-doc`](../huo15-openclaw-office-doc/) |
| 仪式后整理记忆 | [`huo15-openclaw-memory-curator`](../huo15-openclaw-memory-curator/) |
| 仪式后挖小红书 | [`huo15-xiaohongshu`](../huo15-xiaohongshu/) |

---

## License

[MIT](LICENSE) — 自由商用 / 修改 / 再发布。需保留版权声明 `Copyright (c) 2026 青岛火一五信息科技有限公司` + MIT License 全文。

---

## 版本

- **v2.1.0**(2026-06-20) — 对齐 openclaw 2026.6.8(依据包内官方文档 `docs/concepts/agent-workspace.md`):workspace 文件表补 HEARTBEAT.md / BOOT.md,去掉不精确的 CONTEXT_FILE_ORDER 说法,新增 bootstrapMaxChars 写入限长提示;仍只写 5 件套、完成信号仍是删 BOOTSTRAP.md
- **v2.0.0**(2026-05-07) — 对齐 openclaw 2026.5+ 原生工作目录约定:不再产 profile.md,改产原生 5 件套,完成信号 = 删 BOOTSTRAP.md
- **v1.1.0**(2026-04-25) — 4 步极简流程 + 6 经典组合 + 全默认 30 秒
- **v1.0.0**(2026-04-24) — 初始 9 步流程

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>
