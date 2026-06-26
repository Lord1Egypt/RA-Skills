# GSwitch - GStack for OpenClaw

## 什麼是 GSwitch？

GSwitch is a multi-agent coordination system for OpenClaw, inspired by Garry Tan's GStack. It turns OpenClaw into a virtual engineering team with 7 specialized roles working together through shared memory.

GSwitch 是一個 OpenClaw 多智能體協調系統，受 Garry Tan 的 GStack 啟發。它將 OpenClaw 變成一個虛擬工程團隊，由 7 個專業角色通過共享內存共同工作。

---

## The 7 Roles | 7 個角色

| Role | ID | Description |
|------|-----|-------------|
| CEO | (Main Agent) | Rethinks problems, sets direction |
| Engineering Manager | `{username}-em` | Architecture, technical decisions |
| Designer | `{username}-designer` | UI/UX, content, visuals |
| Code Reviewer | `{username}-reviewer` | Code review, bug finding |
| QA Lead | `{username}-qa` | Testing, final gate |
| Security Officer | `{username}-security` | Security audits |
| Release Engineer | `{username}-release` | Deployment |

---

## Core Principle | 核心原則

**Each agent ONLY does their own job. NEVER do others' work.**

每個代理只做自己的工作。永遠不要做他人的工作。

When finding issues, send to the right agent:
發現問題時，發送到正確的代理：

| Issue Type | Send To |
|------------|---------|
| Code/Technical | → EM |
| Design/UI/UX | → Designer |
| Security | → Security |
| Multiple types | → All relevant |

---

## Workflow | 工作流程

```
User → CEO → EM → Designer → Reviewer → QA → Release
                         ↓           ↓
                       EM       QA (if issues found)
                         ↓           ↓
                       EM fixes    Designer/Security/EM
```

**QA is the FINAL gate. Nothing deploys without QA approval.**
QA 是最後的把關。未經 QA 批准，任何東西都不能部署。

---

## Installation | 安裝指南

### Prerequisites | 前提條件

- OpenClaw installed
- OpenClaw 已安裝

### Step 1: Copy GSwitch Folder | 步驟 1：複製 GSwitch 文件夾

Copy the entire `GSwitch` folder to your OpenClaw workspace:
將整個 `GSwitch` 文件夾複製到您的 OpenClaw 工作區：

```
/path/to/your/workspace/GSwitch/
```

### Step 2: Replace {username} | 步驟 2：替換 {username}

Replace ALL occurrences of `{username}` with your own username.

Example | 例如：
- `{username}-em` → `john-em`
- `{username}-designer` → `john-designer`

Do this for all 6 agents:
對所有 6 個代理執行此操作：
- `{username}-em`
- `{username}-designer`
- `{username}-reviewer`
- `{username}-qa`
- `{username}-security`
- `{username}-release`

### Step 3: Create Subagents | 步驟 3：創建子代理

Create 6 subagents in OpenClaw with the following IDs:

| ID | Role |
|----|------|
| `{yourname}-em` | Engineering Manager |
| `{yourname}-designer` | Designer |
| `{yourname}-reviewer` | Code Reviewer |
| `{yourname}-qa` | QA Lead |
| `{yourname}-security` | Security Officer |
| `{yourname}-release` | Release Engineer |

### Step 4: Configure OpenClaw | 步驟 4：配置 OpenClaw

Add to your OpenClaw config:
添加到您的 OpenClaw 配置：

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 5,
        "runTimeoutSeconds": 0
      }
    }
  }
}
```

### Step 5: Create Shared Memory Folder | 步驟 5：創建共享內存文件夾

Create your shared memory folder:
創建您的共享內存文件夾：

```
/path/to/GSwitch/shared-memory/{username}/
```

---

## Shared Memory | 共享內存

All agents append to the same daily log.
所有代理追加到相同的日誌中。

**Format | 格式：**
```markdown
### {username}-role | HH:MM
- 任務：[Task description]
- 結果：[Success/Failure]
- 發現：[Issues if any]
- 檔案位置：[File path]
- 下一步：[Next step]
---
```

**Rule: APPEND ONLY, NEVER OVERWRITE.**
規則：僅追加，永遠不要覆蓋。

---

## Coordination | 協調

Each agent completes their work → notifies {username}-ceo → spawns next agent.

每個代理完成工作 → 通知 {username}-ceo → 生成下一個代理。

{username}-ceo receives all notifications → summarizes for User.
{username}-ceo 接收所有通知 → 為用戶總結。

---

## Example Session | 示例對話

```
User: Build a chatbot for my website.

{username}-ceo (CEO): Office Hours - understands the problem

Designer: Creates UI/UX design

EM: Implements with Claude Code

Reviewer: Code review - finds issues

EM: Fixes issues

QA: E2E testing - passes

Release: Deploys to production

{username}-ceo: Notifies User - "Chatbot complete!"
```

---

## Files Structure | 文件結構

```
GSwitch/
├── SKILL.md              # Main entry
├── README.md             # This file
├── config/
│   └── recommended-settings.json
├── roles/
│   ├── ceo.md           # CEO role
│   ├── em.md            # Engineering Manager
│   ├── designer.md       # Designer
│   ├── reviewer.md      # Code Reviewer
│   ├── qa.md           # QA Lead
│   ├── security.md      # Security Officer
│   └── release.md     # Release Engineer
└── shared-memory/
    └── TEMPLATE.md     # Memory template
```

---

## Credits | 鳴謝

- **Inspired by:** Garry Tan's GStack
- **Concept:** GStack for Claude Code
- **Created by:** Bozzai & Gary

---

*Build fast. Ship confidently. Learn continuously.*
*快速構建。自信交付。持續學習。*
