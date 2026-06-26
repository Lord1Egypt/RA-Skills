# create-agent

> 基于 [OpenClaw](https://github.com/openclaw/openclaw) 的 AgentSkill

**让每一个 Agent，从第一天起就值得信赖。**

---

## 为什么需要它

在 OpenClaw 里，注册一个 Agent 只需要几行配置。
但注册一个**真正好用的 Agent**，是另一回事。

好用的 Agent 不只是"能回答问题"——
它知道你不喜欢废话，习惯把方案写成结论优先；
它记得你负责的客户类型，不用每次都解释背景；
它有明确的边界，不会越界做不该做的事。

**这些不是配置出来的，是设计出来的。**

没有标准流程时，创建 Agent 容易踩这些坑：

- workspace 文件繁多，漏写哪个都可能悄悄影响行为
- SOUL.md 写成"我是一个专业高效的 AI 助手"——没有性格，就等于没有灵魂
- 人伴型和功能型 Agent 结构完全不同，混用就是在起点埋雷
- 直接修改 openclaw.json 出错，一堆 Agent 跟着挂
- heartbeat 没注册，进化机制从未真正运行

你花两天创建了一个 Agent，用了一周发现它没有"灵魂"——重来。

---

## 它是什么

**一套从零到一的 Agent 创建标准流程。**

把"创建一个好 Agent"这件复杂的事，拆成四个清晰的 Phase。
能自动化的自动化，必须人工判断的有明确引导。

走完四个 Phase，你得到的不是一个空壳：

- ✅ workspace 结构正确，所有必须文件齐全且有实质内容
- ✅ SOUL.md 有具体性格，不是套了名字的通用模板
- ✅ 系统注册安全完成，配置有备份，validate 失败自动回滚
- ✅ heartbeat 自动配置，进化机制从创建第一天起就在运转
- ✅ 父 Agent MEMORY.md 自动预埋子 Agent 档案，调度关系清晰
- ✅ 人伴型 Agent 携带 BOOTSTRAP 初始化协议——
  准备好通过第一次真实对话，建立只属于这个人的专属关系

---

## 核心设计理念

> **skill 负责骨架，BOOTSTRAP.md 负责灵魂。**

创建时产出的是可运行的结构。
真正的性格，来自 Agent 与用户第一次对话时的动态初始化——
不是填表，是一段由浅入深的自然对话，
把用户的习惯、厌恶、工作方式，转化成叙事、规则、记忆。

**workspace 不靠创建时决定好坏，靠使用过程中的持续积累决定。**
从第一次对话起，它就在变成更懂你的那个版本。

---

## 功能

### 四 Phase 创建流程

- **Phase 0** — 安装后配置（一次性，写入组织背景到 `~/.openclaw/workspace/agents-config/org-context.md`，含 30 天有效期提醒）
- **Phase 1** — 信息收集（Agent 类型【第一确认】/ agentId / 工具权限 / 父 Agent）
- **Phase 2** — Workspace 构造（按类型走不同路径，脚本自动生成带模板的骨架文件）
- **Phase 3** — 系统注册（安全修改 openclaw.json，备份 + 双向绑定 + validate + 回滚 + 父 MEMORY 预埋）
- **Phase 4** — 重启验证（两层检查 + 首次激活自检）

### 两类 Agent

| 维度 | 人伴型（员工型） | 功能型（任务/领域型） |
|---|---|---|
| **面向谁** | 有真人用户直接对话 | 面向任务，可被 Agent 调度或人直接用 |
| **SOUL.md** | 写骨架，BOOTSTRAP 阶段填充 | 直接写完整版，体现专业判断倾向 |
| **BOOTSTRAP.md** | ✅ 需要，支持断点续接 | ❌ 不需要 |
| **USER.md** | ✅ 需要 | ❌ 不需要 |
| **脚本参数** | `--type human` | `--type functional` |

### 脚本能力

| 脚本 | 功能 |
|---|---|
| `create_workspace.sh` | 创建目录 + 生成带模板的骨架文件（含 HEARTBEAT 闲置检查逻辑） |
| `register_agent.py` | 注册到 openclaw.json（备份/双向绑定/validate/回滚/heartbeat/父MEMORY预埋） |
| `deregister_agent.py` | 注销 Agent（反向操作，workspace 存档不删除） |
| `verify_workspace.sh` | 两层验证：存在性+行数 / 内容特征（名字/边界/占位符/公司信息） |

### 持续进化机制

workspace 不是静态配置，是会生长的知识库：

- **触发式写入**：对话中感知到偏好、判断、术语习惯，立刻写入对应文件
- **业务判断过滤**：判断类信息先写日记，满足重要性条件才提炼进 MEMORY.md（防止膨胀）
- **Heartbeat 精炼**：每 3 天扫描日记，提炼稳定知识，清理过时内容
- **闲置感知**：14 天无调用自动通知调度者（或写入闲置提醒）

---

## 文件结构

```
create-agent/
├── SKILL.md                          # 触发条件 + 四 Phase 执行流程
├── config/
│   └── org-context.md               # 组织背景预埋（Phase 0 生成，含 last_updated 有效期）
├── references/
│   ├── file-formats.md               # 每个 workspace 文件"写好"的标准
│   ├── soul-writing-guide.md         # SOUL.md 写作指南（人伴型 + 功能型专节）
│   ├── evolve-rules.md               # workspace 持续生长规则（含重要性过滤）
│   └── bootstrap-protocol.md        # BOOTSTRAP.md 动态对话协议（含断点续接 + 默认值处理）
└── scripts/
    ├── create_workspace.sh           # 创建骨架文件（--type human|functional，--notify-open-id）
    ├── register_agent.py             # 安全注册（--model / --heartbeat-interval / --dry-run）
    ├── deregister_agent.py           # 安全注销（存档 workspace，--dry-run）
    └── verify_workspace.sh           # 两层验证（存在性 + 内容特征）
```

---

## 安装

需要先安装 [OpenClaw](https://github.com/openclaw/openclaw)。

```bash
clawhub install openclaw-create-agent
```

或手动克隆到 `~/.openclaw/skills/create-agent/`。

---

## 触发

在 OpenClaw 对话中说：

- "创建 agent"
- "新建 agent"
- "新员工配对后创建 agent"
- "新增专业 agent"

---

## 典型用法

### 创建人伴型 Agent（新员工）

```bash
# Phase 2：生成 workspace 骨架
bash scripts/create_workspace.sh staff-ou_xxx \
  --type human \
  --notify-open-id ou_manager123   # 闲置时通知的管理者

# Phase 3：注册（AI 执行，自动备份+validate+预埋父MEMORY）
python3 scripts/register_agent.py \
  --agent-id staff-ou_xxx \
  --workspace ~/.openclaw/agency-agents/staff-ou_xxx \
  --parent-id main \
  --agent-type human \
  --core-duty "负责3个餐饮客户的抖音文案撰写" \
  --also-allow feishu_get_user feishu_im_user_message \
  --heartbeat-interval 60

# Phase 4：验证
bash scripts/verify_workspace.sh staff-ou_xxx --type human
```

### 注销废弃 Agent

```bash
python3 scripts/deregister_agent.py --agent-id staff-ou_xxx --dry-run  # 先预览
python3 scripts/deregister_agent.py --agent-id staff-ou_xxx            # 确认执行
```

---

## 依赖

- OpenClaw >= 2026.3.0
- `openclaw` CLI（用于 config validate）
- `systemctl --user`（用于 Gateway 重启）
- Python 3.10+（deregister_agent.py 使用 `Path | None` 类型注解）
