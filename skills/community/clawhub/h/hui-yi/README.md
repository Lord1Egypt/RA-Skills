# 回忆（Hui-Yi）

回忆（Hui-Yi ）是一个面向冷记忆的 skill。它的核心不是“时间到了就复习”，而是：

> **会话里反复出现、反复被激活的信息，优先强化；艾宾浩斯曲线负责安排强化节奏。**

也就是说，Hui-Yi 是一个把**冷记忆归档、历史唤回、重复强化**合在一起的系统，而不是普通的定时复习器。

---

## 第一层：定位与边界

### 一句话理解

适合 Hui-Yi 的内容：
- 30 天后仍然有价值的经验、决策、背景知识、排障结果
- “我们以前怎么做过这件事” 这类需要历史连续性的内容
- 在会话里反复出现、值得强化的低频知识

不适合 Hui-Yi 的内容：
- 当天临时记录：`memory/YYYY-MM-DD.md`
- 高频个人或项目事实：`MEMORY.md`
- 机器环境、路径、工具坑点：`TOOLS.md`
- 新鲜但还没验证的教训：`.learnings/`
- 密钥、口令、token、敏感凭据

### 与 OpenClaw 系统记忆的分工边界

为了避免重复存储、重复召回、重复维护，Hui-Yi 只管理 **冷记忆强化层**，不替代 OpenClaw 自带的系统记忆。

#### OpenClaw 系统记忆负责
- 当前会话上下文
- `memory/YYYY-MM-DD.md` 中的日常流水与最近连续性
- `MEMORY.md` 中的高频稳定事实、用户背景与长期偏好
- `TOOLS.md` 中的环境配置、路径、机器与工具注意事项
- `.learnings/` 中尚在验证期的经验、错误与改进建议

#### Hui-Yi 负责
- `memory/cold/` 下的低频、高价值、可复用历史知识
- 在真实会话里被反复提起、值得长期强化的经验、决策、背景与排障结论
- 对冷记忆进行 repetition-first 的强化、唤回、轻维护和归档质量控制

#### 选择规则
- **高频且稳定** → 进 OpenClaw 主记忆层，不进 Hui-Yi
- **低频但高价值** → 优先考虑 Hui-Yi
- **当天新鲜上下文** → 留在 daily memory，不急着冷却
- **工具/环境信息** → 固定进 `TOOLS.md`
- **还没验证的新教训** → 先进 `.learnings/`

一句话：

> **OpenClaw 负责“记住”，Hui-Yi 负责“强化那些值得长期巩固、但不应常驻主记忆的信息”。**

### 核心原则

- archive less, but archive better
- reinforce what keeps reappearing
- use time as pacing, not as the only trigger

### 核心模型

#### 1. 主触发：重复出现
优先强化这些内容：
- 当前会话里反复出现的
- 最近多个会话里重复出现的
- 被再次召回且证明有用的
- 用户持续追问或重复关注的

#### 2. 辅助触发：时间压力
艾宾浩斯曲线仍然保留，但它主要用来决定：
- 成功后间隔怎么拉长
- 失败后怎么快速回到短间隔
- 长期未强化的记忆如何保持“应复习”状态

而不是机械地说：
- 日期到了，无论有没有再次出现，都必须优先复习

### 优先级公式

当前实现更接近：

```text
Priority ≈
  0.40 * RepetitionSignal
+ 0.25 * CurrentRelevance
+ 0.15 * DuePressure
+ 0.10 * Importance
+ 0.10 * ReinforcementStrength
```

含义：
- `RepetitionSignal`：真实会话中的重复激活
- `CurrentRelevance`：当前上下文相关性
- `DuePressure`：相对 interval 的时间压力
- `Importance`：长期价值
- `ReinforcementStrength`：weak / normal / strong 记忆强度修正

---

## 第二层：快速开始与常用操作

## 运行方式

### 模式 A：当前仓库根目录直接运行

```text
hui-yi/
├── memory/
│   ├── cold/
│   └── heartbeat-state.json
├── scripts/
├── core/
├── templates/
├── templates/
├── references/
├── SKILL.md
└── manifest.yaml
```

### 模式 B：安装到 `skills/hui-yi/`

```text
<workspace>/
├── memory/
│   ├── cold/
│   └── heartbeat-state.json
└── skills/
    └── hui-yi/
```

从 `<workspace>` 根目录运行时，把：
- `scripts/...` 替换为 `skills/hui-yi/scripts/...`
- `hook-template/...` 视为 skill 内模板目录，安装目标仍为 `workspace/hooks/hui-yi-signal-hook/...`

---

## 快速开始

### 1. 准备目录

至少准备：

```text
memory/
├── cold/
│   ├── index.md
│   ├── tags.json
│   ├── retrieval-log.md
│   └── _template.md
└── heartbeat-state.json
```

最小内容：

`memory/cold/index.md`

```md
# Cold Memory Index
```

`memory/cold/tags.json`

```json
{ "_meta": { "version": 5 }, "notes": [] }
```

`memory/cold/retrieval-log.md`

```md
# Retrieval Log
```

`memory/heartbeat-state.json`

```json
{}
```

然后复制：
- `templates/note-template.md` -> `memory/cold/_template.md`

### 2. 新建第一条冷记忆

```bash
python scripts/create.py --title "主题" --type experience --importance high --tags "tag1,tag2"
```

创建后会自动：
- 生成 note
- 设置 `interval_days: 1`
- 设置 `next_review: tomorrow`
- 初始化 `Session signals`
- 触发一次 `rebuild.py`

### 3. 校验与搜索

```bash
python scripts/validate.py --strict
python scripts/search.py 主题
python scripts/search.py 主题 --full-text
```

### 4. 开始复习或唤回

```bash
python scripts/review.py due
python scripts/review.py session
python scripts/review.py resurface --query "当前话题"
python scripts/review.py resurface --query "当前话题" --session-key "feishu:user:ou_xxx:main" --write-signals
```

---

## 最常用命令

| 命令 | 用途 |
| --- | --- |
| `python scripts/create.py --title "主题"` | 新建一条冷记忆 |
| `python scripts/validate.py --strict` | 校验 note schema、字段和索引一致性 |
| `python scripts/search.py <keyword>` | 按 metadata 检索 |
| `python scripts/search.py <keyword> --full-text` | 检索 metadata + note 正文 |
| `python scripts/rebuild.py` | 重建 `index.md` 和 `tags.json` |
| `python scripts/review.py due` | 查看时间到期或重复激活的条目 |
| `python scripts/review.py session` | 进入交互式批量强化 |
| `python scripts/review.py resurface --query "..."` | 按当前话题找最值得强化的旧内容 |
| `python scripts/review.py resurface --query "..." --session-key "..." --write-signals` | 对高置信 resurfacing 命中写回 weak activation |
| `python scripts/review.py feedback <note> --useful yes|no --query "..." --session-key "..."` | 对单条 recall 写回反馈，并在 useful=yes 时写入强激活 |
| `python scripts/decay.py --dry-run --rebuild` | 预览轻量维护结果并同步索引 |
| `python scripts/cool.py status` | 查看 cold-memory heartbeat 状态 |
| `python scripts/cool.py scan` | 扫描 cooling 状态 |
| `python scripts/cool.py done <reviewed> <archived> <merged>` | 记录一次 cooling 完成情况 |
| `python scripts/scheduler.py --schedule-id <id>` | 运行指定 schedule 的筛选逻辑 |
| `python scripts/install_hook.py --dry-run` | 预览 Hui-Yi hook 模板安装结果 |

说明：
- `review.py` 现在会同时考虑 **重复出现** 和 **时间压力**
- `scheduler.py --preview` 适合调试 repetition / relevance / due_pressure 的排序结果
- `search.py` 支持把 `memory_root` 作为第二个位置参数传入

---

## 四个典型工作流

### 1. 找回以前处理过的问题

短上下文：

```bash
python scripts/review.py resurface --query "数据库迁移失败"
```

长上下文：

```bash
python scripts/review.py resurface --context-file context.txt
```

从标准输入传入：

```bash
Get-Content context.txt | python scripts/review.py resurface --stdin
```

建议做法：
- 只打开最相关的 1 到 3 条 note
- 输出总结，不要直接倾倒原始笔记
- 如果 recall 确实有帮助，补一条 `feedback`

### 2. 新增一条冷记忆

判断标准：
- 30 天后还会有价值
- 它是可复用的经验、决策或背景
- 它会明显提升未来回答质量

建议顺序：
1. 先搜有没有同主题 note
2. 没有再 `create.py`
3. 补齐 `TL;DR`、`Semantic context`、`Triggers`、`Use this when`
4. 运行 `validate.py`

### 3. 做一次强化维护

```bash
python scripts/review.py due
python scripts/review.py session
python scripts/decay.py --dry-run --rebuild
python scripts/cool.py status
```

维护时重点看：
- 是否有重复 note 可以合并
- 哪些 note 在会话里反复出现
- 哪些 recall 经常有用，哪些经常无用
- 高价值 note 的 `Importance`、`Session signals`、`Next review` 是否合理

### 4. 做定时轻提醒

先准备 `memory/cold/schedule.json`，再运行：

```bash
python scripts/scheduler.py --schedule-id daily-evening-review
python scripts/scheduler.py --schedule-id daily-evening-review --preview --query "当前话题"
```

边界要明确：
- `scheduler.py` 负责选候选，不负责真正发消息
- 是否投递、何时投递、通过什么消息链路投递，应由外部 scheduler / runtime / agent 层决定

### 5. 安装并启用 Hui-Yi hook

如果你希望在初始化 skill 时把 Hui-Yi 的 signal hook 一起装上并启用，可直接运行：

```bash
python scripts/install_hook.py --enable
```

常用形式：

```bash
python scripts/install_hook.py --dry-run --enable
python scripts/install_hook.py --force --enable
python scripts/install_hook.py --enable --config-path C:\path\to\openclaw.json
```

行为说明：
- 默认会把 `skills/hui-yi/templates/hook/` 下的模板文件安装到 `workspace/hooks/hui-yi-signal-hook/`
- 模板来源是 skill 包内的 `skills/hui-yi/templates/hook/`，不是 workspace 中旧的已安装文件
- `--enable` 会同时确保 `openclaw.json` 里的以下配置开启：
  - `hooks.internal.enabled = true`
  - `hooks.internal.entries.hui-yi-signal-hook.enabled = true`
- 如果文件已存在、配置已启用，安装器会直接报告状态，不会无意义重写；如需覆盖旧占位文件，请使用 `--force --enable`

安全边界：
- hook 是显式 opt-in；建议先运行 `--dry-run` 并审阅 `templates/hook/` 后再启用
- hook 不访问网络，不读取凭据目录，只在本地 `memory/cold/` 内读取 note 并写回 `tags.json` / note 的 `Session signals`
- note path 会被解析并强制限制在 `memory/cold/` 内；绝对路径和 `..` 父级跳转会被拒绝
- 为避免持久化原始聊天标识，session key 仅以短 `sha256:` fingerprint 形式写入 metadata，用于去重和重复激活判断
- v1.2.9 起，signal 写回会顺手清洗旧版 `signal_history` 中的 raw session key；老用户也可以运行 `python scripts/scrub_metadata.py` 一次性清洗 legacy metadata
- v1.2.10 起，OpenClaw signal hook 不再通过全局 `sys.argv` 串接 Python pipeline；TS hook 的 `signal_history` 迁移即使命中去重也会落盘，并收紧 heuristic fallback、日志截断和 session 连续计数语义；`scripts/cool.py --memory-root` 同时兼容 `memory/` 与 `memory/cold/` 两种路径。
- v1.2.11 起，hook 默认日志做了隐私最小化：不再记录任何消息正文预览和原始 user/chat 标识，`triggered`/`completed` 日志里 scope 身份只以 `sessionHash` 哈希出现，`alive`/`skipped` 调试日志默认关闭（需 `HUI_YI_HOOK_DEBUG=1` 显式开启）；heuristic fallback 里过宽的 `remember` 触发收紧为回忆性短语；`install_hook.py --enable` 会先打印将修改的配置项披露，且在 `openclaw.json` 不存在时拒绝凭空新建；`manifest.yaml` 补全了 hooks 目录与 `openclaw.json` 的可选路径声明和用户警告。本版本无功能变更。

---

## Scheduler

`scheduler.py` 负责：
- 读取 `schedule.json`
- 根据 repetition、due pressure、importance、allowed_states、context、cooldown 选择候选
- 输出人类可读结果或 JSON

---

## 常见问题

### 1. 运行后提示 `memory root not found`

原因通常有两个：
- 还没初始化 `memory/cold`
- 你当前不在预期的 workspace 根目录

处理方式：
- 先按“快速开始”创建最小目录
- 或显式传入 `--memory-root`

### 2. `index.md` / `tags.json` 缺失或损坏

直接运行：

```bash
python scripts/rebuild.py
```

### 3. `resurface` 没有返回结果

优先检查：
- `tags.json` 是否为空
- query 是否太短或太噪
- note 的 `Triggers`、`Semantic context` 是否写得太弱
- note 是否缺少足够的 `Session signals`
- schedule 是否开了过严的 `min_relevance`、`min_priority`、`min_repetition`

调试时可先用：

```bash
python scripts/scheduler.py --schedule-id <id> --preview --query "当前话题"
```

### 4. 为什么有些 note 没到日期也会进入 review 池

因为 Hui-Yi 现在的核心是：
- **重复出现优先强化**

如果一条记忆在当前会话或近期会话里反复被激活，它可以在没到 `Next review` 时提前进入候选池。

### 5. 如何确认改动没有破坏主流程

运行：

```bash
python scripts/smoke_test.py
```

它会在 skill 目录下创建隔离的临时工作区，串行验证：
- create
- validate
- search
- review/resurface
- feedback
- decay
- cool
- scheduler

---

## 第三层：延伸文档与实现细节

这一层不放在 `SKILL.md`，只在需要时再展开。

### references/
- `references/cold-memory-schema.md`：note / index / tags 结构说明
- `references/examples.md`：示例 note
- `references/heartbeat-cooling-playbook.md`：cooling 流程
- `references/integration-patterns.md`：scheduler 与外部系统的对接边界
- `references/real-session-signals-design.md`：真实会话信号如何自动累积到 `Session signals`

### 补充脚本与模块
- `python scripts/install_hook.py --dry-run`：预览 Hui-Yi hook 文件安装
- `python scripts/install_hook.py`：将 Hui-Yi hook 模板显式安装到 `hooks/hui-yi-signal-hook/`
- `python scripts/scrub_metadata.py --dry-run`：预览并清洗旧版 `tags.json` 中 raw session key metadata
- `python core/signal_detect.py --query "..." --json`：把当前 query / 上下文转成高置信 activation candidates
- `python core/signal_pipeline.py --query "..." --session-key "..." --apply --json`：统一执行 detect + threshold + weak activation writeback
- `python core/openclaw_signal_hook.py --query "..." --channel feishu --scope-type user --scope-id "..." --dry-run`：模拟 OpenClaw 上层在 skill-hit 场景中的最小 hook 调用
- `python core/openclaw_runtime_probe.py --query "..." --channel feishu --scope-type user --scope-id "..." --dry-run`：workspace 侧上层接入原型 runner，不直接修改 OpenClaw runtime

### Signal / Hook contract

当前建议的理解方式：
- hook 只负责监听事件和调用 adapter
- `core/openclaw_signal_hook.py` 只负责 OpenClaw-facing 参数归一化
- `core/signal_*` 模块负责 detection / apply / pipeline
- session key 形状和 trigger-source 默认值由 `core/signal_contract.py` 统一维护
