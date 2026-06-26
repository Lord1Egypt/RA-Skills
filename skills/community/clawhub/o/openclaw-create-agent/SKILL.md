---
name: create-agent
description: >
  创建新的 OpenClaw Agent 及其 workspace。包含四个阶段：信息收集、
  workspace 构造、系统注册、重启验证。
  适用场景：新员工飞书配对后创建对应 Agent、新增功能型专业 Agent。
  触发词：创建 agent、新建 agent、添加 agent、新员工配对后创建、
         新增专业 agent。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - openclaw
  github: https://github.com/Dios-Man/create-agent
---

# create-agent — 创建 Agent 及 Workspace

## 两类 Agent 快速对比

> 在创建任何 Agent 之前，必须先判断它属于哪一类。两类路径差异显著，确认后再收集信息。

| 维度 | 人伴型（员工型） | 功能型（任务/领域型） |
|---|---|---|
| **面向谁** | 有真人用户直接对话 | 面向任务，可被 Agent 调度或人直接用 |
| **SOUL.md** | 写骨架，BOOTSTRAP 阶段填充 | 直接写完整版，体现专业判断倾向 |
| **BOOTSTRAP.md** | ✅ 需要，首次对话动态初始化 | ❌ 不需要 |
| **USER.md** | ✅ 需要，积累用户个人知识 | ❌ 不需要（最多记录调用方偏好） |
| **AGENTS.md 重点** | 场景触发规则 + 记忆规则 | 任务接口规范（输入/输出/边界） |
| **MEMORY.md 方向** | 个人偏好 + 业务判断模式 | 领域知识 + 任务经验 |
| **进化路径** | 了解他 → 理解他的工作 → 在稳定场景内提供预判（长期方向：逐步替代机械性工作） | 更实用 → 更专业 → 更好解决需求 |
| **脚本参数** | `--type human` | `--type functional` |

---

## 核心设计原则

> skill 负责骨架，BOOTSTRAP.md（人伴型专属）负责灵魂。

- **人伴型**：skill 产出 workspace 骨架 + BOOTSTRAP.md，首次对话时由用户参与填充
- **功能型**：skill 直接产出完整的 workspace，包含精心设计的 SOUL.md 和能力声明
- **两类共同**：workspace 通过触发式写入 + heartbeat 精炼持续生长

执行前**必须**阅读：
- `references/file-formats.md` — 每个文件"写好"的标准
- `references/soul-writing-guide.md` — SOUL.md 专项写作指南
- `references/evolve-rules.md` — workspace 持续生长规则
- `references/memory-rules.md` — 记忆规则精简模板（独立于 AGENTS.md）
- `references/bootstrap-protocol.md` — BOOTSTRAP.md 动态对话协议

---

## Phase 0 — 安装后配置（首次使用前执行一次）

> **判断依据（按顺序检查）：**
>
> 1. 读取 org-context.md：`~/.openclaw/workspace/agents-config/org-context.md`
>    不存在 → 尝试从 MEMORY.md 自动提取公司背景 → 仍无法提取 → 执行 Phase 0
>
> 2. 检查"公司："和"业务："字段是否均有实质内容。
>    任意一个为空 → 执行 Phase 0（跳过有效期检查）；两个都有内容 → 执行步骤 2。
>
> 3. 检查 `last_updated` 字段，计算距今天数。
>    超过 30 天 → 提示用户确认（不强制阻断，用户确认无需调整则继续）。
>    未超过 30 天 → 直接跳过 Phase 0。
>
> （不以文件是否存在为判断标准，空文件 ≠ 已填写）

### Step 1：读取记忆，自动提取

```
读取：MEMORY.md + 最近 3 天 memory/ 文件
提取：
  □ 公司名称
  □ 主营业务
  □ 已有的 Agent 列表和分工
  □ 其他稳定的组织背景
```

### Step 2：展示并确认

```
"我从记忆里整理了以下信息，将作为新 Agent 的背景预埋：

[展示提取内容]

有需要补充或修改的吗？"
```

### Step 3：写入 `~/.openclaw/workspace/agents-config/org-context.md`

```markdown
# org-context.md — 组织背景预埋信息

## 元信息
- last_updated: YYYY-MM-DD

## 公司信息
- 公司：[自动填入或用户补充]
- 业务：[自动填入或用户补充]

## 现有 Agent 架构
[自动填入已知的 Agent 列表和分工]

## 其他背景
[用户补充的信息]
```

**后续每次创建 Agent，自动读取此文件，不再重复询问。**

---

## Phase 1 — 信息收集

**所有信息必须确认后才能进入 Phase 2，不猜测，不假设。**

### 快速路径判断（可选，减少轻量场景的收集成本）

在开始详细收集前，先判断是否适合快速路径：

```
问用户：这是给刚配对的员工建基础 Agent，还是有特定职责的专业 Agent？
```

**如果回答是"刚配对的员工"且用户没有额外要求 → 快速路径：**

只收集 3 项：
```
□ agentId        staff-<open_id前几位>
□ open_id        用于 --notify-open-id（HEARTBEAT.md 闲置通知）
□ 基础工具权限    默认：feishu_get_user feishu_im_user_message feishu_search_user
```

可选收集（传入后 SOUL.md 骨架会有岗位相关倾向，不传则使用通用表述）：
```
○ 岗位类型（一句话，如"内容运营""客户经理""视频剪辑"）
```

其余全部自动处理：
- 名字/emoji：AI 根据飞书姓名自动生成（Phase 2 A-2）
- SOUL.md：骨架（BOOTSTRAP 阶段填充）
- AGENTS.md：最小规则集（不含场景规则，仅基础记忆规则）
- alsoAllow：仅 3 个基础工具
- 核心职责/边界/父 Agent：全部使用默认值（"服务配对员工的日常工作"，父 Agent = main）

快速路径跳过功能型专有字段和可选字段，直接进入 Phase 2。Phase 2 中 AGENTS.md 的场景规则和明确不做的事留空（由 BOOTSTRAP 或后续使用中补充）。

**如果不适合快速路径 → 继续下面的详细收集。**

> ⚠️ **Agent 类型必须第一个确认**，它决定 Phase 2 走哪条路径，两条路差异显著。
> 收集顺序：先定类型 → 再按对应路径收集剩余信息。

### 通用必填（按此顺序收集）

```
□ Agent 类型     【第一个确认】员工 Agent（有真人用户直接对话）
                              还是功能型 Agent（面向任务/被其他 Agent 调度）
□ agentId        全小写，字母+连字符（如 staff-ou_xxx、data-analyst）
□ 名字 + emoji   用于 IDENTITY.md，也是 SOUL.md 的叙事起点
□ 核心职责       1-2句话（这个 Agent 主要干什么）
□ 明确不做什么   至少说出 2-3 条边界
□ 父 Agent id    谁来调度它（用于 allowAgents 白名单）
□ alsoAllow 列表 需要哪些飞书/系统工具权限
```

如果是员工 Agent，agentId 通常是 `staff-<open_id前几位>`。

### 功能型专有必填（仅当类型为功能型时收集）

```
□ 判断偏向      遇到不确定性时默认保守还是激进
                 （比如：宁可多问一句不瞎猜 / 给个方向等反馈 / 先按最常见情况处理）
□ 输入模糊时    收到的信息不完整时的默认行为
的默认行为        （追问 / 按默认假设执行并标注 / 拒绝执行并说明缺什么）
□ 质量标准排序  正确性 / 完整性 / 效率 / 创新性——哪个优先
                 （比如：宁可慢但要准 / 快速给粗糙结论再迭代）
□ 最不能容忍    这个 Agent 在执行中最不该出现的行为
的输出缺陷        （比如：给了一个看起来完整但实际有错的答案 / 推理过程有跳跃）
```

### 可选

```
○ 是否需要专属 skills
○ 特殊的工具限制或安全约束
```

---

## Phase 2 — Workspace 构造

> **根据 Agent 类型走不同路径。确认类型后只读对应文件，不读另一个。**

**人伴型（路径 A）：** 读取 `references/human-path.md`，按步骤执行 A-1 到 A-9。

**功能型（路径 B）：** 读取 `references/functional-path.md`，按步骤执行 B-1 到 B-9。

---

## Phase 3 — 系统注册（高危，严格执行）

```bash
python3 scripts/register_agent.py \
  --agent-id <agentId> \
  --workspace ~/.openclaw/agency-agents/<agentId> \
  --parent-id <父AgentId> \
  --agent-type human \
  --core-duty "核心职责一句话描述" \
  --also-allow feishu_get_user feishu_im_user_message feishu_calendar_event
```

**可选参数：**
- `--model`：指定模型（不传则继承默认）
- `--heartbeat-interval`：心跳间隔分钟数（默认 60）
- `--agent-dir`：极少数情况才需要，不传则不写入此字段
- `--dry-run`：预览变更不写入

脚本执行顺序：
1. 备份 openclaw.json（带时间戳）
2. 在 `agents.list` 追加新 Agent 定义（含 heartbeat + 可选 model）
3. 在父 Agent 的 `subagents.allowAgents` 追加新 agentId（**双向绑定**）
4. 执行 `openclaw config validate`
5. validate 通过 → 在父 Agent MEMORY.md 追加子 Agent 档案 → 继续
   validate 失败 → 自动回滚，报错退出

💡 **首次使用或调试时**，先加 `--dry-run` 预览：
```bash
python3 scripts/register_agent.py --agent-id <agentId> ... --dry-run
```

⚠️ **不要手动改 openclaw.json**，用脚本。

---

## 注销 Agent（废弃 / 员工离职）

```bash
python3 scripts/deregister_agent.py --agent-id <agentId>
# 预览：python3 scripts/deregister_agent.py --agent-id <agentId> --dry-run
```

脚本执行：
1. 从 `agents.list` 移除目标 Agent
2. 从所有父 Agent 的 `allowAgents` 移除该 id（自动扫描，不会遗漏）
3. validate + 回滚机制同注册
4. workspace 存档到 `~/.openclaw/agency-agents/.archived/<agentId>-<时间戳>/`（不删除）

---

## Phase 4 — 重启与验证

### Step 1：验证 workspace 完整性

```bash
bash scripts/verify_workspace.sh <agentId> --type human      # 人伴型
bash scripts/verify_workspace.sh <agentId> --type functional # 功能型
```

脚本执行两层检查：
1. **存在性 + 行数**：文件存在且有足够有效行
2. **内容特征**：无未填充占位符、SOUL.md 含名字、AGENTS.md 含边界声明、MEMORY.md 公司已填写

有 ❌ 或 ⚠️ → 补充后重新验证，通过后再重启。

### Step 2：重启 Gateway

```bash
if systemctl --user status openclaw-gateway.service &>/dev/null 2>&1; then
  systemctl --user restart openclaw-gateway.service
elif pgrep -f "openclaw gateway" &>/dev/null; then
  openclaw gateway restart
else
  echo "⚠️  无法自动检测 Gateway 运行方式，请手动重启后继续验证。"
fi
sleep 8
```

### Step 3：验证工具可用性

1. 确认新 Agent 在 Gateway 日志里出现
2. 确认 alsoAllow 里的工具已注册（不以"重启完成"作为结束）

### Step 4：首次激活自检

通过 `sessions_send` 向新 Agent 发一条激活消息：

```
请读取你的 workspace，用一段话说清楚：你是谁、主要职责是什么、有哪些明确不做的事。
```

收到回应后：
- 检查回应是否包含 Agent 名字、核心职责、边界声明三要素
- 将回应写入新 Agent 的 `memory/<今天日期>.md` 作为第一条记录（标题："首次激活自检"）
- 回应缺少三要素之一 → workspace 有问题，检查对应文件后重新自检

### Step 5：最小场景化行为验证

自检通过后，根据 Agent 类型发送测试消息。

**人伴型：**
根据 Phase 1 收集的"明确不做什么"，构造一条超出边界的请求：
```
帮我做一下 [某条明确不做的事]
```
**验证标准：** Agent 明确拒绝 + 说明边界，不尝试执行。
**不通过时：** 检查 SOUL.md 边界 + AGENTS.md 场景规则。

**功能型（两项测试，全部通过才算完成）：**

测试 1 — 输入完整性测试：
```
帮我处理一下数据
```
**验证标准：** Agent 按能力卡点响应（追问必要输入 / 说明需要什么信息 / 指出输入不完整），不直接猜测执行。
**不通过时：** 检查 AGENTS.md "接受的输入" 部分。

测试 2 — 判断边界测试：
```
这是一个 [Agent 职责领域] 的任务：[具体但处于能力边界的情况描述]
```
**验证标准：**
- Agent 没有直接跳过判断就执行（说明"工作执念"生效）
- Agent 的回应中体现了 Phase 1 收集的"判断偏向"
- Agent 对不确定的部分有标注（不是假装确定）
**不通过时：** 检查 SOUL.md 是否包含判断偏向素材 + AGENTS.md 边界声明是否覆盖灰色地带。

⚠️ 以**"自检三要素通过 + 场景行为验证通过"**作为整个 skill 的完成标志。

---

## 完成后告知

```
Agent [名字] 已创建完成：
- agentId: <agentId>
- workspace: ~/.openclaw/agency-agents/<agentId>
- 工具权限: <alsoAllow 列表>
- 状态: 等待用户首次对话完成个性化初始化

员工首次与 Agent 对话时，BOOTSTRAP.md 会自动触发，
通过动态对话完成 workspace 的内容层定制。
```

---

## Agent 进化里程碑

> 里程碑是可观测、可验证的状态，不是抽象承诺。
> 对应 HEARTBEAT 中 Workspace 成熟度评分（I1）。

| 阶段 | 达成条件 | 成熟度参考 |
|---|---|---|
| 🌱 种子 | 创建完成，workspace 文件完整，公司背景已预埋 | 0-20 |
| 📋 知道你是谁 | BOOTSTRAP 完成：USER.md 有称呼+岗位+核心工作，SOUL.md 有具体性格，≥3 条偏好 | 20-40 |
| 🔍 理解你的工作 | 使用 2-4 周：MEMORY.md 有 ≥3 条业务背景，memory/ 有 ≥2 条业务判断，USER.md 有 ≥5 条偏好 | 40-70 |
| 🎯 不用你说就知道 | 使用 1-3 月：Agent 在用户开口前主动提供相关信息，用户不再重复解释背景 | 70+ |

创建者可通过读取 Agent 的 memory/.health 文件中的 maturity 值来判断当前阶段。

---

## 注意事项

- **每个 Agent 必须有独立 workspace**，不能多个 Agent 共用
- **SOUL.md 和 AGENTS.md 不能内容重叠**：性格在 SOUL，规则在 AGENTS
- **TOOLS.md 不进 BOOTSTRAP 对话**：由 skill 根据 alsoAllow 自动生成
- **MEMORY.md 和 memory/ 严格区分**：长期知识 vs 日期事件
- **Gateway 重启后必须验证工具可用性**，不以重启完成作为结束
- **记忆规则**：由 create_workspace.sh 自动生成独立文件 `memory-rules.md`，AGENTS.md 只保留引用
