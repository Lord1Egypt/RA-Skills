# Trigger Modes + Integration Patterns

这份文档专门解释 Hui-Yi **怎么被触发**、**谁来调用脚本**、以及它如何和 heartbeat / cron / 上层 agent 对接。

---

## 1. Trigger Modes

Hui-Yi 不是常驻守护进程，也不是安装后自动执行的后台服务。

它有三种触发模式：

### A. Semantic Trigger（语义触发）

当当前请求明显涉及以下意图时，优先考虑 Hui-Yi：

- 回忆旧上下文
- 询问“之前怎么处理的”
- 要求 archive / cool / 冷却 / 归档
- 需要低频但高价值的历史背景来补强当前回答

典型触发语句：
- do you remember
- how did we handle that
- archive this
- cool this down
- 回忆一下 / 之前 / 以前 / 你记得吗 / 有记录吗

**责任边界：**
- 上层 agent 决定是否命中 skill
- Hui-Yi 负责说明应该查哪里、怎么查、怎么写回
- 真正执行时，由 agent 显式运行脚本或读写文件

### B. Maintenance Trigger（维护触发）

当目标是定期维护 cold memory，而不是回答一个具体问题时，触发 Hui-Yi 的维护流程。

适合：
- cooling recent daily notes
- rebuild / validate / decay
- heartbeat 例行维护
- 发布前巡检

常见入口：
- `cool.py scan`
- `decay.py --dry-run`
- `rebuild.py`
- `validate.py --strict`
- `smoke_test.py`

**责任边界：**
- 外部 heartbeat / cron / 人工维护流程 触发
- Hui-Yi 只提供维护规则和脚本接口，不自己调度自己

### C. Debug Trigger（调试触发）

当你要检查 skill 是否健康、某个筛选是否正确、或者发布前回归时，进入调试模式。

适合：
- 冒烟测试
- schema 校验
- scheduler 预览
- 文档与实现对齐检查

常见入口：
- `python3 skills/hui-yi/scripts/smoke_test.py`
- `python3 skills/hui-yi/scripts/validate.py --strict`
- `python3 skills/hui-yi/scripts/scheduler.py --schedule-id <id> --preview --query "..."`

**责任边界：**
- 由开发者 / 维护者显式触发
- 不应被误当成正常用户工作流的一部分

---

## 2. Who actually starts the skill?

Hui-Yi 的启动链条通常是：

1. 上层 agent 发现当前意图和 Hui-Yi 匹配
2. agent 读取 `SKILL.md`
3. agent 决定是否读取 cold-memory 文件，或运行某个 helper script
4. helper script 执行具体动作

所以 Hui-Yi 的真正入口不是某个 daemon，而是：

- `SKILL.md` 的触发描述
- 上层 agent 的技能选择逻辑
- 外部维护流程（heartbeat / cron / manual run）

---

## 3. Integration Patterns

### Pattern 1: In-chat recall（对话内回忆）

适用：
- 用户问“之前有记录吗”
- 当前回答明显需要历史上下文补强

建议流程：
1. 先看当前对话和 warm memory
2. 再决定是否进入 cold memory
3. 如需查询，优先用 `search.py` / `review.py resurface`
4. 总结结果，不直接 dump 原始 note

建议脚本：
- `search.py <query>`
- `review.py resurface --query "..."`
- `review.py resurface --context-file <file>`

### Pattern 2: Heartbeat maintenance（心跳维护）

适用：
- 周期性扫描最近 daily notes
- 低打扰地做 cooling 维护

建议流程：
1. `cool.py scan`
2. 判断哪些 daily notes 值得进入 cold memory
3. 需要时更新 / 新建 cold note
4. `rebuild.py`
5. `cool.py done <reviewed> <archived> <merged>`

说明：
- heartbeat 负责“什么时候检查”
- Hui-Yi 负责“检查时怎么处理”
- 不建议 heartbeat 每次都大扫除

### Pattern 3: Cron-driven scheduled recall（外部定时回忆）

适用：
- 你已经有外部 cron / scheduler
- 想定时挑选一个值得提醒的旧 note

建议流程：
1. 外部 cron 定时运行 `scheduler.py`
2. `scheduler.py` 输出候选 note
3. 上层 agent / workflow 决定是否真的发给用户

重要：
- `scheduler.py` 是 **selector**，不是发消息守护进程
- 它负责选候选，不负责投递

常见命令：
- 正常模式：
  - `python3 skills/hui-yi/scripts/scheduler.py --schedule-id daily-evening-review`
- 调试预览：
  - `python3 skills/hui-yi/scripts/scheduler.py --schedule-id daily-evening-review --preview --query "..."`

### Pattern 4: Release / audit workflow（发布前巡检）

适用：
- 发 ClawHub / GitHub 之前
- 审计或大改之后

建议流程：
1. `smoke_test.py`
2. `validate.py --strict`
3. scheduler 正常 / preview 各跑一次
4. 对照 `references/publish-checklist.md`
5. 确认 manifest / docs / version 同步

---

## 4. Normal mode vs Preview mode

### `--schedule-id`
表示：
- 只运行某条 schedule 的筛选规则

不表示：
- 强制返回一个候选

所以如果该 schedule 本身要求：
- due
- high importance
- allowed_states
- cooldown

那它依然可能返回：
- `No scheduled recall candidates right now.`

### `--preview`
表示：
- 调试 / 预览模式
- 用于看候选排序
- 会绕过 due、importance、allowed_states、cooldown、require_relevance 等正式门槛

适合：
- 开发时检查配置
- 发布前验证 scheduler 没死
- 排查“为什么现在没候选”

---

## 5. Recommended boundaries

### Hui-Yi 应该负责
- 冷记忆的结构规则
- recall / archive / maintenance 的方法论
- helper scripts
- 候选选择与元数据维护

### Hui-Yi 不应该负责
- 自动发消息
- 自己注册 cron
- 自己决定何时打扰用户
- 代替上层 agent 做最终沟通判断

一句话：

**Hui-Yi 负责记忆策略和候选选择，上层系统负责调度与沟通。**

---

## 6. Practical recommendation

如果你想让这套系统长期稳定，建议默认这么接：

- 对话回忆 → `review.py resurface` / `search.py`
- 周期维护 → heartbeat + `cool.py` / `rebuild.py`
- 定时候选 → 外部 cron + `scheduler.py`
- 发布前检查 → `smoke_test.py` + `publish-checklist.md`

这样职责最清楚，也最不容易互相打架。
