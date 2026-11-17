# 回忆（Hui-Yi）

回忆（Hui-Yi ）是一个面向冷记忆的 skill。它的核心不是“时间到了就复习”，而是：

> **会话里反复出现、反复被激活的信息，优先强化；艾宾浩斯曲线负责安排强化节奏。**

也就是说，Hui-Yi 是一个把**冷记忆归档、历史唤回、重复强化**合在一起的系统，而不是普通的定时复习器。

当前源码版本为 **1.2.13**，包含文件安全、OpenClaw 兼容性与自动召回改进，详见 [发行说明](references/release-1.2.13.md)。发布版本可在 [ClawHub](https://clawhub.ai/fuetsui/skills/hui-yi) 与 [GitHub Releases](https://github.com/FueTsui/hui-yi/releases) 核验；发布成功不等于外部安全审计通过。

本次升级接通原生自动记忆与回答前召回，用户不必提供主题列表或手动触发命令。高频个人信息由主记忆承接；Hui-Yi 仍作为最后的低频归档层。中文匹配、相关度优先、真实计数、失效记录过滤及重建去重证据同步修复。

自动接入的范围、后台运行时间、模型调用、运行时守卫和升级步骤见 [自动识别与召回](references/native-memory.md)。旧 signal hook 保留给自定义宿主，当前原生接入会停用它；不能以旧 hook 已启用来证明普通聊天已经自动检测。

---

## 第一层：定位与边界

### 一句话理解

适合 Hui-Yi 的内容：
- 30 天后仍然有价值的经验、决策、背景知识、排障结果
- 当前对话和主记忆仍不能满足、明确需要低频归档知识的历史连续性请求
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
- 回忆顺序：当前对话 → 近期 daily notes / 系统主记忆 → 相关工具记录 / learnings → 仍需低频历史资料时才查 cold memory
- “之前 / 以前 / 回忆一下 / 你记得吗”只是历史上下文线索，不能单凭措辞启用 skill、写回信号或归档
- 加载 skill 不代表授权安装 hook、启用后台采集、注册定时任务或执行 cooling；这些动作需要当前请求或已有明确维护授权
- 回复语言跟随用户；本文中文例子和 schedule 提示词仅为示例，可按使用者语言配置
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
- hook 模板在 `skills/hui-yi/templates/hook/`，安装目标为 `workspace/hooks/hui-yi-signal-hook/`

上述默认目录由 skill 的安装位置推导。显式 `--memory-root` 等路径参数由本地调用者选择；相对路径按运行时工作目录解析。自动写入受信任工作区前，应检查选中的 archive、heartbeat、schedule、hook 与 config 路径。

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
| `python scripts/scrub_metadata.py --dry-run` | 预览 legacy session 标识清洗；省略 dry-run 后应用 |
| `python core/openclaw_runtime_probe.py --stdin --channel local --scope-type user --scope-id demo --dry-run` | 从 stdin 读取模拟输入，在进程内预览 adapter |

说明：
- `review.py` 现在会同时考虑 **重复出现** 和 **时间压力**
- `scheduler.py --preview` 适合调试 repetition / relevance / due_pressure 的排序结果
- `search.py` 支持把 `memory_root` 作为第二个位置参数传入
- `cool.py scan` 会更新 heartbeat 扫描状态；`cool.py status` 才是只读状态查询
- `feedback` 会在本地 retrieval log 中保存所提供的 query/action；不要传入密钥、口令或不应持久化的敏感内容
- Python detector/pipeline 默认省略原始 query/session 和 overlap terms，但检索结果可含 note 标题、路径；只有显式 `--include-sensitive` 才包含原始 query/context 与匹配词。adapter/probe 不支持该敏感诊断开关

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

`decay.py` 的日期维护不自动降低 `Memory state`。它会依据 `Last verified` 的陈旧程度调整事实可靠度：超过 120 天的 `high` 可变为 `medium`，超过 180 天的 `medium` 可变为 `low`；这和记忆温度、实际复习失败是不同概念。先用 `--dry-run` 查看变化，再在已授权维护范围内应用。`--dry-run --rebuild` 仍不会重建索引；应用后用 `--rebuild` 或单独运行 `rebuild.py`。

### 4. 做定时轻提醒

只有在用户已授权定时复习时才配置外部调度。可复制 `templates/schedule.example.json` 为 `memory/cold/schedule.json`，审阅语言、时间和筛选条件后显式将顶层 `enabled` 设为 `true`，再手动检查：

```bash
python scripts/scheduler.py --schedule-id daily-evening-review
python scripts/scheduler.py --schedule-id daily-evening-review --preview --query "当前话题"
```

边界要明确：
- `scheduler.py` 负责选候选，不负责真正发消息
- 是否投递、何时投递、通过什么消息链路投递，应由外部 scheduler / runtime / agent 层决定
- 示例配置默认关闭；skill 不注册 cron。selector 使用进程本地时区，并只识别 cron 字段中的固定小时/分钟，不实现完整 cron 语义；准确调度和时区转换由外部系统负责
- `--preview` 会绕过部分筛选门槛，仅用于检查排序，不是允许投递的结果

### 5. 可选旧版 Hui-Yi hook（自定义宿主）

原生自动检测应优先按 [自动识别与召回](references/native-memory.md) 接入。只有自定义宿主需要旧协议时，才显式安装启用此 hook：

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

启用后的显式文本入口示例：`/hui-yi 数据库迁移复盘`，也接受 `/hui_yi 数据库迁移复盘`。必须位于宿主映射的`context.body` 开头；命令不区分大小写，用 ASCII 空格或 tab 分隔非空查询。前导空白、引用/嵌入文字、带其他前缀的命令、空查询以及仅出现在 `bodyForAgent` 的命令均不触发。命令前缀会先去除再检索。

OpenClaw 2026.9.5 的原生 `message:preprocessed` mapper 不提供 skill-selection metadata；因此不要期待普通聊天被自动选中。普通文本命令需要未经包装地出现在映射正文开头；部分渠道会包装正文，原生 slash-command 快速路径也可能先消费命令。遇到这些情况使用显式 CLI/adapter。当前验证包含隔离的 mapper 形状事件，不代表已通过各真实渠道端到端测试；自定义可信宿主的 selection 集成仍受支持。

安全边界：
- hook 是显式 opt-in；先用 `--dry-run` 审阅安装目标与 `templates/hook/`。启用后处理可信宿主的 Hui-Yi selection 或上述严格显式文本命令；没有依据普通消息措辞的 heuristic fallback。宿主不能把用户提供的字段直接映射成可信 skill-selection 或 workspace 元数据
- hook 不访问网络、不提取凭据。`install_hook.py --enable` 会读取并重写整个已有 `openclaw.json`，其中可能包含其他插件的敏感配置；不能把这一操作描述为“完全不接触凭据”。它只主动修改披露的两个 hook-enable 键，保留其他值，并拒绝新建缺失 config
- 文件访问拒绝符号链接、Windows junction/reparse point、硬链接和特殊文件，并复查目标身份。Python 在 Windows 上先把现有文件的 DACL 复制到空暂存文件，再写数据并原子替换；TS 对 POSIX 文件及 Windows 新文件使用暂存原子替换，对 Windows 已有文件则通过核验后的文件描述符原位更新以保留 DACL，失败时尽力回滚。后一分支不具备崩溃原子性。上述检查不是抵御同账户恶意进程并发替换目录的内核沙箱，工作区及父目录必须由可信 OS 用户控制
- session key 仅以截断 `sha256:` 指纹写入 metadata，用于去重。它不是加密或用户授权：同一 workspace 共用 archive，不提供多租户隔离；不同信任域应由宿主路由到独立工作区
- 普通日志与 `HUI_YI_HOOK_DEBUG=1` 均不保存消息正文、原始身份/事件 metadata、note 标题/路径或 overlap terms。debug 只增加生命周期和计数；日志仍保留 session hash 并在 256 KB 附近轮转
- Python detector/pipeline 的显式 `--include-sensitive` 可输出原始上下文和匹配词，但不会输出 raw session key。adapter/probe 始终只输出计数、状态、安全错误和 session hash。使用 `--stdin` 传入消息可避免消息正文出现在命令行参数中；scope 参数仍应使用适当的本地身份引用
- signal 写回会清洗旧版 history 中的 raw session key；也可先运行 `python scripts/scrub_metadata.py --dry-run`，再在授权范围内应用清洗
- `allowed-tools` 和 manifest 的权限/路径声明是操作披露，不是运行时 ACL。CLI 的显式路径覆盖属于调用者权限

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
python -X utf8 -B -m unittest discover -s tests
node --experimental-strip-types --test tests/hook_security.test.mjs
python scripts/smoke_test.py --memory-root <已准备的测试归档>
```

Python/Node 回归测试使用测试夹具检查文件边界、触发条件、隐私及相关主流程。`smoke_test.py` 是对指定归档的只读 strict validate、search、scheduler preview 检查，并不创建隔离归档或覆盖所有写入流程；它只启动固定 Python 子命令并使用环境变量白名单。测试通过不等同于已验证真实 OpenClaw 事件链路。

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
- `python scripts/scrub_metadata.py --dry-run`：仅预览旧版 `tags.json` 中 raw session key metadata 清洗；去掉 `--dry-run` 才写入
- `python core/signal_detect.py --query "..." --json`：把当前 query / 上下文转成高置信 activation candidates
- `python core/signal_pipeline.py --query "..." --session-key "..." --apply --json`：统一执行 detect + threshold + weak activation writeback
- `python core/openclaw_signal_hook.py --stdin --channel local --scope-type user --scope-id demo --dry-run`：从 stdin 读取模拟消息，预览 Python adapter；也可显式使用 `--query`
- `python core/openclaw_runtime_probe.py --stdin --channel local --scope-type user --scope-id demo --dry-run`：在进程内调用 adapter；不启动命令行子进程、不返回原始命令/输出，不证明真实 host hook 已启用

### Signal / Hook contract

当前建议的理解方式：
- `templates/hook/handler.ts` 是独立的 TypeScript inline 实现，不调用 Python adapter；两套文件边界和输出合约分别测试
- Python 脚本通过 `core/safe_fs.py` 共用文件边界；TS hook 使用 `templates/hook/safe-fs.ts`。发布/安装 hook 时必须与 `handler.ts` 一起包含 `safe-fs.ts`，不能只复制 handler
- `core/openclaw_signal_hook.py` 只负责 OpenClaw-facing 参数归一化
- `core/signal_*` 模块负责 detection / apply / pipeline
- Python session-key 形状和调用阈值由 `core/signal_contract.py` 维护；兼容 CLI 的 trigger-source 参数不是依据正文自动触发的授权。TS hook 支持可信 host 的 Hui-Yi selection 和映射正文开头的严格 `/hui-yi` / `/hui_yi` 文本命令；原生宿主兼容范围见上文
