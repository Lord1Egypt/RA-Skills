---
name: loop-skill
description: >-
  面向任意 coding-agent CLI 的计划驱动、无人值守多 agent loop 编排。当用户一句话触发推进多个仓库、
  需要主控通读仓库生成推进计划、再自动派发 CLI、会话可恢复、后台常驻 loop 或打开看板时使用。
  触发语：「用 loop-skill 推进某目录下的项目」「后台常驻 loop」「自动推进计划」。
metadata:
  version: 0.1.0
  license: MIT
  homepage: https://github.com/handsomestWei/loop-skill
  repository: https://github.com/handsomestWei/loop-skill
---

# loop-skill

把书面**推进计划**变成无人值守的 agent loop。计划由**主控 agent 通读仓库**后写出，不绑定固定文档名；loop 负责派发、验收、会话持久化。

## 何时使用

- 用户一句话要推进一个或多个仓库，且希望**零人工**配置。
- 需要主控先**理解需求**再产出/更新推进计划，然后后台 loop 常驻。
- 需要 Claude 等 CLI 在业务仓执行，主控只编排。

## 五阶段循环

```
发现 → 规划 → 执行 → 验收 → 迭代
```

- 第一次触发时的「规划」= **planner 开环**（主控通读仓库 → 写 `docs/loop-plan.md`）。详见 `references/plan-generation.md`。
- 之后 loop **闭环**自动跑任务；**默认每轮各仓并行派发**（每仓最多 1 个 CLI），看板先启动再派发。

## 一句话启动（主控协议，禁止打扰用户）

用户示例：「用 loop-skill 推进 `D:/my-vibe-project`，Claude 执行，后台常驻。」

主控在**同一轮**按序执行，不得让用户手写 `loop.json`：

```bash
cd <loop-skill>
python -m core.cli doctor claude
python -m core.cli discover --root D:/my-vibe-project
python -m core.cli scan --root D:/my-vibe-project
```

然后对 **scan 返回的每个仓库**（主控用 Read/Glob，非单文件）：

1. 通读 `markdown_files` 列出的文档 + README + 关键目录结构
2. 综合理解后，在该仓**写入或更新** `docs/loop-plan.md`（推荐路径；内容吸收旧需求文档，不机械复制）
3. 表格 ID 用 `P1-01` 格式；推荐五列 `| ID | 任务 | 验收 | 角色 | 状态 |`（见 `references/plan-generation.md`、`references/role-guide.md`）
4. **角色须多样化**：每阶段混合 `architect` / `coder` / `verifier` / `reviewer`；**禁止**写 `worker`（会回落为 coder）

再执行（**先 ingest，再 up**；`up` 会先起看板、确认 HTTP 可访问后再启动 loop）：

```bash
python -m core.cli ingest
python -m core.cli up --interval 300
```

回报 `dashboard_url`。停止：`python -m core.cli down`。

**`up` 成功后禁止反问**是否执行某任务——loop 自动派发（**默认各仓同时各跑 1 个任务**）。

**禁止**主控对每个仓库执行 `python -m core.cli dispatch <repo>` 做「试跑」或「推进」——那会同步阻塞等 CLI，4 仓 ≈ 4 次长等待。**禁止**主控代替 CLI 在业务仓写实现代码（除非用户明确只要主控、不用 loop）。

`doctor`：至少一个 `[ok]` 即视为有可用的执行 CLI（看输出末尾「可用 provider」行）。Windows 上 npm 全局 CLI 多为 `.cmd` shim，已由运行时 PATH 解析。

若 `ingest` 后任务数为 0，`up` 会失败并提示先完成 planner 步骤——主控应回到写推进计划，勿问用户。

仅当 `scan` 显示已有充分任务表且与用户意图一致时，可跳过写计划，直接 `ingest` → `up`。

## 从工作区移除推进计划（不删开发仓库）

用户说「移除 clip-forge 的推进计划」「从 loop 删掉这个仓库的编排」时，主控须**二次确认**（对话里问一次 + 执行 confirm），且明确告知：

- **会删**：`workspace/state/`、`prompts/`、`results/`、`logs/` 下该仓数据，以及 `loop.json` 注册项
- **不会删**：磁盘上的开发仓库及其 `docs/loop-plan.md`

```bash
# 第一步：获取确认令牌（5 分钟有效）
python -m core.cli remove-plan clip-forge

# 用户明确确认后，第二步：
python -m core.cli remove-plan clip-forge --confirm <token>
```

看板卡片「移除」按钮同样两步确认。移除后若要重新纳入多仓，重新 `discover` → 写计划 → `ingest`。

## 核心原则

1. **计划由主控理解后写出**，不强制某文件名；`ingest` 从各仓**全部** Markdown 合并任务表（推进计划类文件优先）。
2. **多仓并行（默认）** — `up` / `loop --all` 每轮对**所有就绪仓库各派发 1 个** pending 任务（`fleet_parallel_max=0`）；看板**先于** loop 启动。限制并发：`--fleet-parallel-max N`；单仓轮询：`--serial --fleet-parallel-max 1`。
3. **政策消灭交互** — `references/decisions-guide.md`
4. **会话持久** — `references/state-schema.md`
5. **主控不改业务代码** — 只写推进计划与 `loop-skill/`；实现由 CLI worker 完成

## 关键参数：`verify_mode`

`dev-first` | `tests` | `strict` — 见 `loop.yaml` / 每仓覆盖。

## 命令索引

完整分类与示例见 **`references/cli-commands.md`**。常用子命令摘要：

| 命令 | 用途 |
|------|------|
| `discover` / `scan` / `ingest` | 多仓登记、文档清单、导入任务 |
| `up` / `down` | 启停后台看板 + loop |
| `remove-plan` | 从工作区移除编排（二次确认） |
| `status` / `dispatch` / `loop` | 调试 |

## 文件索引

| 路径 | 用途 |
|------|------|
| `references/cli-commands.md` | **CLI 指令分类表（调试 / 主控用）** |
| `references/plan-generation.md` | **主控 planner 协议（必读）** |
| `references/role-guide.md` | **任务角色分配（architect/coder/verifier/reviewer）** |
| `references/loop-engineering.md` | 五阶段 + 六原语 |
| `references/decisions-guide.md` | 政策引擎 |
| `references/worker-contract.md` | CLI worker 输出契约 |
| `docs/loop-plan.md` | 各业务仓内，主控写入的推进计划（推荐；兼容 `docs/推进计划.md`） |
