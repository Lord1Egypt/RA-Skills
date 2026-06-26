# 自动创建 Agent - 完整流程

## 触发条件

当用户说以下任意一句时触发：
- "配置小说agent"
- "创建小说agent"
- "初始化小说工作流"
- "设置小说创作环境"

## 配置步骤（每步需用户确认）

### 步骤 1: 定位 Skill 目录

自动检测当前 skill 的位置：
- 从 `SKILL.md` 路径推导
- 模板路径：`assets/agent-templates/`

### 步骤 2: 用户配置

**必须用户输入或确认**，不能自动决定：

```
1. 工作区位置 [<默认路径>]: 
   → 用户输入路径或回车使用默认

2. 写作风格:
   [1] 通用风格（默认）
       - 段落≤5行，句子≤20字
       - 节奏明快，去AI味
   [2] 番茄小说风格
       - 段落≤4行，句子≤18字
       - 情绪按摩，发疯文学，短快爽
   → 用户选择

3. 要创建的 agent:
   [x] writer（写作）
   [x] checker（审稿）
   [x] planner（规划）
   [x] manager（统筹）
   → 用户勾选或回车全选

4. 模型选择:
   [1] xiaomi/mimo-v2-omni（默认）
   [2] moonshot/kimi-k2.5
   → 用户选择

5. 确认配置:
   工作区: <用户输入的路径>
   风格: 通用/番茄
   Agent: writer, checker, planner, manager
   模型: <用户选择的模型>
   [确认] [取消]
   → 用户确认后才执行
```

### 步骤 3: 创建 Agent 配置目录

在 `~/.openclaw/agents/` 下创建：
```
~/.openclaw/agents/
├── writer/agent/
│   ├── models.json          ← 从模板复制
│   └── auth-profiles.json   ← 从模板复制
├── checker/agent/
│   ├── models.json
│   └── auth-profiles.json
├── planner/agent/
│   ├── models.json
│   └── auth-profiles.json
└── manager/agent/
    ├── models.json
    └── auth-profiles.json
```

### 步骤 4: 创建工作区目录并迁移引用文件

#### 4.1 创建基础目录结构

```
<工作区>/
├── agent/
│   ├── writer/
│   │   ├── chapters/        ← 创建空目录
│   │   ├── docs/            ← 创建空目录
│   │   ├── references/      ← 创建空目录（存放引用的参考文件）
│   │   ├── AGENTS.md        ← 从模板复制
│   │   ├── SOUL.md          ← 从模板复制
│   │   ├── USER.md          ← 从模板复制
│   │   ├── TOOLS.md         ← 从模板复制
│   │   ├── HEARTBEAT.md     ← 从模板复制
│   │   └── IDENTITY.md      ← 从模板复制
│   ├── checker/             ← 同上
│   ├── planner/             ← 同上
│   └── manager/             ← 同上
```

#### 4.2 检测并迁移引用的 references 文件

对于每个 agent，执行以下步骤：

1. **扫描引用**：读取 agent 的 AGENTS.md，查找 `references/XXX.md` 引用
2. **复制文件**：将引用的文件从 skill 复制到 agent 工作区
   ```
   skill/references/XXX.md → <工作区>/agent/<agent>/references/XXX.md
   ```
3. **更新路径**：修改 agent/AGENTS.md 中的引用路径
   - 原：`见 references/XXX.md`
   - 改为：`见 references/XXX.md`（指向工作区副本）

**各 agent 默认引用**：
- **writer**: `references/chapter-format.md`
- **checker**: `references/review-template.md`, `references/quality-standards.md`
- **planner**: `references/workflow-diagrams.md`
- **manager**: `references/handoffs.md`, `references/routing.md`

#### 4.3 风格处理

- **通用风格**：直接复制模板
- **番茄风格**：复制模板后，将 `references/platform-tomato.md` 内容合并到 writer/AGENTS.md 的创作原则部分

### 步骤 5: 更新 openclaw.json

读取现有配置，添加 agent 定义：

```json
{
  "agents": {
    "list": [
      {
        "id": "writer",
        "workspace": "<工作区>\\agent\\writer",
        "agentDir": "<用户主目录>\\.openclaw\\agents\\writer\\agent",
        "model": "<用户选择的模型>"
      },
      {
        "id": "checker", 
        "workspace": "<工作区>\\agent\\checker",
        "agentDir": "<用户主目录>\\.openclaw\\agents\\checker\\agent",
        "model": "<用户选择的模型>"
      },
      {
        "id": "planner",
        "workspace": "<工作区>\\agent\\planner", 
        "agentDir": "<用户主目录>\\.openclaw\\agents\\planner\\agent",
        "model": "<用户选择的模型>"
      },
      {
        "id": "manager",
        "workspace": "<工作区>\\agent\\manager",
        "agentDir": "<用户主目录>\\.openclaw\\agents\\manager\\agent",
        "skillsDir": "<工作区>\\skills",
        "model": "<用户选择的模型>"
      }
    ]
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "writer", "checker", "planner", "manager"]
    }
  }
}
```

### 步骤 6: 验证配置

检查：
- [ ] Agent 配置目录存在
- [ ] 工作区目录存在
- [ ] openclaw.json 格式正确
- [ ] 无重复 agent ID

### 步骤 7: 提示重启

```
✅ 小说 agent 配置完成！

已创建:
- writer: <工作区>\agent\writer
- checker: <工作区>\agent\checker  
- planner: <工作区>\agent\planner
- manager: <工作区>\agent\manager

请重启 OpenClaw Gateway 使配置生效:
  openclaw gateway stop
  openclaw gateway start

重启后即可使用:
- "写第X章" → writer
- "审第X章" → checker
- "规划大纲" → planner
- "统筹流程" → manager
```

## 手动命令参考

如需手动执行，使用以下命令：

```powershell
# 1. 创建 agent 配置目录
$agents = @("writer", "checker", "planner", "manager")
foreach ($agent in $agents) {
    New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.openclaw\agents\$agent\agent"
}

# 2. 复制配置文件（$skillDir 为 skill 所在目录）
foreach ($agent in $agents) {
    Copy-Item "$skillDir\assets\agent-templates\models.json" "$env:USERPROFILE\.openclaw\agents\$agent\agent\"
    Copy-Item "$skillDir\assets\agent-templates\auth-profiles.json" "$env:USERPROFILE\.openclaw\agents\$agent\agent\"
}

# 3. 创建工作区（$workspace 为用户指定的工作区）
foreach ($agent in $agents) {
    New-Item -ItemType Directory -Force -Path "$workspace\agent\$agent\chapters"
    New-Item -ItemType Directory -Force -Path "$workspace\agent\$agent\docs"
    Copy-Item "$skillDir\assets\agent-templates\$agent\*" "$workspace\agent\$agent\" -Recurse
}

# 4. 更新 openclaw.json（手动编辑）
# 5. 重启 Gateway
openclaw gateway stop
openclaw gateway start
```
