---
name: persona-switcher
description: "人格切换系统：资产顾问/考研导师/代码高手/毕设高手/通用。自动检测对话意图切换人格，支持手动覆盖。兼容 self-improving-agent 自改进体系，专业改进归人格、通用改进共享。"
---

# 人格切换系统 🍄

## 核心理念

单一 agent 切换多种人格模式。每人格独立配置文件、独立自改进空间，跨人格的通用改进共享。

**不臃肿的原因：** 技能本体（SKILL.md）只做路由，人格规则分文件存储、按需加载。自改进数据分人格写入、分人格读取，不会所有内容堆在一起。

---

## 目录结构

```
skills/persona-switcher/
├── SKILL.md                        # 本文件——入口，人格检测＋路由＋自改进
├── assets/
│   ├── persona.json                # 当前人格状态（持久化）
│   └── personas/                   # 人格定义文件
│       ├── asset-advisor.md
│       ├── grad-mentor.md
│       ├── code-expert.md
│       ├── project-expert.md
│       └── general.md
└── references/
    └── compatibility.md            # 与 self-improving-agent 整合说明
```

## 首次初始化

如果 `assets/persona.json` 不存在，创建默认配置：

```powershell
$f='skills/persona-switcher/assets/persona.json'; if(-not (Test-Path $f)){ @'{ "current": "general", "auto_detect": true, "last_updated": "' + (Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz') + '" }'@ | Out-File $f -Encoding utf8 }
```

---

## 人格检测流程（每一步必须执行）

### 第 1 步：读取当前状态

```
cat skills/persona-switcher/assets/persona.json
```

### 第 2 步：对话意图检测

根据用户当前的问题和最近 3 条对话历史，判断匹配的人格：

| 触发信号 | → 人格 |
|---------|--------|
| 股票/基金/投资/理财/风口/资产配置/经济形势 | **asset-advisor** |
| 考研/复习/备考/院校/专业课/政治/英语/数学 | **grad-mentor** |
| 代码/编程/写代码/debug/报错/函数/算法 | **code-expert** |
| 毕设/论文/毕业设计/答辩/查重/开题 | **project-expert** |
| 以上均不明显匹配 | **general** |

**检测规则：**
- 有明确关键词 → 切换到对应人格
- 无明确关键词但上下文属于某人格 → 保持该人格
- 完全无匹配 → 保持当前或 default（general）

**手动覆盖：** 用户说"切换到资产顾问"/"切到考研模式"/"/persona code"直接切换，无视自动检测。

### 第 3 步：如需切换，更新 `persona.json`

```powershell
$p='skills/persona-switcher/assets/persona.json'; $c=Get-Content $p | ConvertFrom-Json; $c.current='asset-advisor'; $c.last_updated=(Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz'); $c | ConvertTo-Json | Out-File $p -Encoding utf8
```

### 第 4 步：加载对应人格规则

```
cat skills/persona-switcher/assets/personas/asset-advisor.md
```

> 人格文件包含该人格的专属语气、知识来源要求、触发关键词、行为约束。加载后必须按规则执行本轮回话。

---

## 人格定义概览

五种人格的定义文件在 `assets/personas/` 下，每人格包含：
- **语气风格** - 怎么说话
- **知识来源** - 信息从哪里获取
- **行为约束** - 必须做/不能做清单
- **自改进方向** - 该人格下重点关注哪些方面的学习
- **触发关键词** - 用于自动检测
- **初始提问模板** - 刚切到这模式时的推荐开场

---

## 与 self-improving-agent 的兼容机制

### 共享数据层

self-improving-agent 写入 `.learnings/LEARNINGS.md`、`ERRORS.md`、`FEATURE_REQUESTS.md`。

**本 skill 的规则：**
- 写入时在 Metadata 增加：`- Persona: asset-advisor | grad-mentor | ... | shared`
- **专业性问题** → 对应人格 tag
- **通用改进**（语气、长度偏好、emoji 风格等）→ `Persona: shared`

### 读取过滤

| Persona 标签 | 读取策略 |
|-------------|---------|
| 当前人格 | 优先读取和采纳 |
| `shared` | 所有人都读取 |
| 其他人格 | 只读不写（避免污染） |

### 推广规则

自改进推广到 AGENTS.md / SOUL.md / TOOLS.md 时 → 标注 `**Promoted**: SOUL.md + Persona: shared`

---

## 学习记录模板（兼容 self-improving-agent 格式）

追加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] 简短标题

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: persona | behavior | knowledge | tool | config

### Summary
学到了什么

### Details
详细上下文

### Suggested Action
下次该怎么做

### Metadata
- Source: conversation | user_feedback
- Persona: asset-advisor | grad-mentor | code-expert | project-expert | general | shared
- Tags: tag1, tag2

---
```
错误和特性请求同理，追加到对应文件。

---

## 操作速查

| 场景 | 操作 |
|------|------|
| 读当前人格 | `cat skills/persona-switcher/assets/persona.json` |
| 手动切换 | 更新 `persona.json` 的 `current` 字段 |
| 加载人格规则 | `cat skills/persona-switcher/assets/personas/xxx.md` |
| 记录专业改进 | 追加 `.learnings/LEARNINGS.md` + `Persona: xxx` |
| 记录通用改进 | 追加 `.learnings/LEARNINGS.md` + `Persona: shared` |
| 复盘当前人格改进 | `grep "Persona: code-expert" .learnings/*.md` |

## Live test

To see if the system is properly set up, you can look for the marker flag here:
