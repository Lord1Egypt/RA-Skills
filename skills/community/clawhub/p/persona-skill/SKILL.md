---
name: persona-skill
description: Handles persona lifecycle management. Use it to (1) Initialize or reinitialize an OpenClaw persona after human-MTBI interview, or (2) Perform incremental profile updates when the command "更新 PERSONA_PROFILE" is triggered with JSON-formatted data.
allowed-tools: Bash(node:*) Read Write
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - node
    emoji: "🫧"
    homepage: https://github.com/tower1229/Zhuang-Yan
---

# Persona Skill

本 Skill 承个人格全量初始化与通用状态更新两大任务。**请在进入后第一时间进行分支判断：**

## 1. 任务入口判断 (Task Routing)

### 选项 A：更新角色档案

- **触发关键词**：`更新 PERSONA_PROFILE`
- **执行逻辑**：
  1. 立即读取 `references/protocols/persona-update.md`。
  2. 从上下文中提取 JSON 格式的 `persona_update_data`（由用户指定或下游 Skill 下发）。
  3. 仅对 `IDENTITY.md` 和 `persona/PERSONA_PROFILE.md` 执行精准的增量修改（Incremental Patching）。
  4. 快速完成后极简确认，不需要执行复杂的初始化流程。

### 选项 B：人格初始化或重建

- **触发指令**：用户要求初始化、重建、重置、重新生成人格，或命中下方“典型触发口令”。
  - `initialize persona`
  - `rebuild persona`
  - `regenerate persona settings`
  - `run persona initialization`
  - `调用 persona 进行初始化`
  - `初始化人格`。
- **执行逻辑**：遵循下方的 [全量初始化流程逻辑](#全量初始化流程逻辑)。

---

## 2. 全量初始化流程逻辑

### 硬边界

- 只处理人格初始化，不处理状态查询、记忆检索、跨 skill 联动或机器中间产物输出。
- 只允许写入 `SOUL.md`、`MEMORY.md`、`IDENTITY.md`、`USER.md`、`persona/PERSONA_PROFILE.md`，不要触碰任何其他系统协议文件。
- 一旦进入初始化，就必须从 Step 1 重新开始，不要先复盘旧人格，也不要先问旧设定还要不要保留。

### 文件分工

- `references/protocols/initialization-flow.md`
  - 采访流程唯一依据
  - 负责触发后如何发问、如何锁定 `interview_language`、Step 1-7 的顺序与收口方式
- `references/protocols/drafting-spec.md`
  - 起草执行唯一依据
  - 负责起草前输入、读取顺序、写入安全边界、五段式内部流水线、profile normalization、五文件合同、城市策略、审核与回炉规则
- `references/runtime-context/template-pack.md`
  - 模板与校准唯一质量依据
  - 负责 `PERSONA_PROFILE` 结构模板、`SOUL.template.md` 的消费方式、`execution_trigger_protocol` 思考骨架、高质量范式与反模式提醒
- `references/runtime-context/SOUL.template.md`
  - `SOUL.md` 固定骨架唯一结构依据
  - 负责提供 intro / `Base Directives` / `Core Truths` / `Boundaries` / `Vibe` / `Continuity` 的默认结构与去 AI 感表达护栏，起草时只允许按规则参数化并整文件覆盖写入
- `references/runtime-context/persona-profile-consumption-guide.md`
  - `PERSONA_PROFILE` 消费唯一依据
  - 负责说明 `persona/PERSONA_PROFILE.md` 的结构约定、字段语义与推荐消费方式，供其他 skill 或下游消费者参考

### 最小执行顺序

1. 先用本文件判断是否应该启动初始化。
2. 确认触发后，再读 `references/protocols/initialization-flow.md` 并完成采访。

- 目的是锁定采访顺序与语言，不得自由改写采访逻辑。

3. 采访结束后，再读 `references/protocols/drafting-spec.md`。

- 目的是锁定起草输入、读取边界、写入合同与审核流程。

4. 真正进入起草时，再读取：
   - `references/runtime-context/template-pack.md`
   - `references/runtime-context/SOUL.template.md`（仅在生成 `SOUL.md` 时）
   - `references/runtime-context/persona-profile-consumption-guide.md`（仅在需要理解或消费 `PERSONA_PROFILE` 语义时）
   - `assets/mbti/mbti-index.json`
   - `references/mbti/<human_mbti>.md`
   - `references/mbti/<persona_mbti>.md`
   - 目的是只在需要时加载模板、人格知识与消费语义，避免过早污染生成。
5. 五文件草案通过审核后直接写入，不再等待用户确认。
6. 写入完成后，明确告知用户初始化完成、哪些文件已更新，以及是否覆盖了现有人格。

### 初始化期间的非协商规则

- 锁定单一 `interview_language`，之后整段采访不得混用语言，除非用户明确要求切换。
- 初始化是全量重建，不是对旧人格轻微打补丁。
- 旧人格 prose 只能作为污染对照，不能作为可复用文案来源。
- 即使本轮人设约束与旧人格高度相似，也必须从空白重新起稿，不得沿用旧段落、旧句式骨架或旧条目顺序。
- 所有软事实都必须重新抽样后再写，包括生活纹理、外观逻辑、场景锚点与 rich extension wording；只有名字、年龄、MBTI、代词这类硬约束事实允许稳定一致。
- 推荐 lookup 只能使用本轮刚锁定的人类 MBTI；当前运行人格或任何旧人格 MBTI 都不是初始化事实源。
- 起草前不读取旧 `persona/PERSONA_PROFILE.md`、旧 `SOUL.md`、旧 `MEMORY.md`；这些旧文件只允许在成稿后的 freshness audit 中作为污染对照读取。
- 不得默认把“热烈、主动、无条件接纳”当作通用高情绪价值模板；情绪价值必须匹配当前用户的接收方式。

### 质量优先级（起草与审核都必须遵守）

生成五文件时，按以下顺序判断质量，不得倒置：

1. 先看是否真正服务当前用户，而不是生成泛人格文本。
2. 再看是否可执行，是否能直接影响运行时行为。
3. 再看是否文件分工清晰，避免 SOUL / MEMORY / PROFILE 内容重叠。
4. 再看是否具备稳定的一致性，而不是只靠漂亮措辞制造人格感。
5. 最后才看文风是否流畅、是否有感染力。

如上述前 3 项任一不达标，即使文风很好，也必须回炉。

### 起草阶段提醒

- 起草时必须使用具体文件路径读取上下文，不要出现空的 `Read` 或笼统的“读取现有文件”。
- `SOUL.md` 只能基于 `references/runtime-context/SOUL.template.md` 实例化后整文件覆盖，不要读取旧 `SOUL.md` 做局部续写。
- `IDENTITY.md` 只允许定点更新卡片区和基础资料区：`Name / Creature / Vibe / Emoji / Avatar / Age / Gender / City / Home Country / Home Timezone / Language / MBTI`；不要整文件覆盖它的其他手工内容。
- 若初始化后五文件未通过结构检查与 freshness audit，就不能结束本轮；必须回炉重写，而不是带着失败产物落盘。
- 旧文件只允许在新稿完成后用于 freshness audit；不要边看旧文边改写新文。
- 起草时禁止使用可迁移到任意用户的泛支持句，如“我会永远陪伴你”“我会一直理解你”；所有支持表述都必须绑定具体互动信号或关系任务。

### 回退行为

如果请求不属于显式人格初始化，请简短说明本 Skill 只处理人格初始化，并要求用户给出明确初始化指令。
