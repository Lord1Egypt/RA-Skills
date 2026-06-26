---
name: 赢得目标
description: 在目标平台（goal_web）发布高质量内容的完整技能流程设计。用于：读取任务json与goal_prompt，拆解任务、执行任务引擎、开发与自检、结果回写与评分回写。触发词：修改目标、赢得目标、触发目标实现、触发{网站名称}任务实现。
---

# {goal_web} 内容发布 Skill（仅流程文档，无脚本）

> **变量说明**：`{goal_web}` 是全局目标平台变量，每次运行时从 `references/core_goal.json` 的 `goal_web` 字段读取，读取后注入本文档所有出现 `{goal_web}` 的位置。当前值由 core_goal.json 决定，本文档不硬编码任何平台名称。

## 目录结构（约定）
- `references/core_goal.json`：固定核心目标，每次启动 Step 1 时必须从此文件读取 `core_goal` / `core_flow` / `goal_web`，未经用户明确修改不得更改
- ~~`references/goal_prompt.md`~~：**已迁移至 `references/prompts/goal_prompt.md`，旧路径废弃**
- `references/prompts/`：**Prompt 专属目录**，所有 Prompt 文件统一存放于此
  - `references/prompts/prompt_registry.md`：**Prompt 注册表**，Step 1 / Step 6 必须先查此表确定读取路径
  - `references/prompts/meta_prompt.md`：**Lyra meta-Prompt**，生产任何新 Prompt 时必须先用此 Prompt 驱动生成，再用 authoring_guide 校验字段
  - `references/prompts/prompt_authoring_guide.md`：**Prompt 撰写规范**，新建任何 Prompt 前必读，定义输入/输出字段硬性约束
  - `references/prompts/goal_prompt.md`：通用任务拆解 Prompt（fallback）
  - `references/prompts/retro_prompt.md`：通用复盘 Prompt（fallback）
- `references/technical-decision-reference.md`：开发方案决策参考，Step 3.1 必须读取
- `references/external-publishing-design-reference.md`：外部平台发布设计参考，涉及发布任务时必须读取
- `references/logging.md`：日志记录规范，每次执行必须遵循
- `references/script_registry.json`：脚本索引表（注册表），必须存在，允许写入脚本记录
- `references/step5_example.md`：Step 5 结果评分示例（参考用）
- `run/{date}/{batch_seq}/compressed_log.json`：**结构化压缩日志**（V2.0 新增），Step 4 每次执行后必须生成；Step 6 的 `{past_3_runs_logs}` 变量改读此文件，降低 Token 消耗
- `references/cron-design-reference.md`：**Cron 脚本设计规范，开发任何 cron 脚本前必须先读取本文件**
- `references/hook_config.json`：**Event-driven 自动运行配置表**，Step 0 启动时读取，控制一次触发自动跑几个 batch
- `tasks/`：**分平台任务 JSON 统一存放目录**（详见下方「任务文件命名规范」）
- `run/{date}/{batch_seq}/`：批次运行日志、retro_output 存放目录（仍保留，供日志归档）

---

## 任务文件命名规范（必须遵循）

所有任务 JSON 和复盘 JSON **统一存放在 `tasks/` 目录**，按以下规则命名：

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| 任务拆解 JSON | `{goal_web}_tasks_{batch_seq}.json` | `微博_tasks_001.json` |
| 复盘输出 JSON | `{goal_web}_retro_{batch_seq}.json` | `微博_retro_001.json` |

**说明**：
- `{goal_web}` = `core_goal.json` 中 `goal_web` 字段的实际值（如 `微博`、`脉脉`、`知乎`）
- `{batch_seq}` = 三位数字序号（如 `001`、`002`）
- 同一平台的任务和脚本隔离，不同平台之间绝对不互相读取
- 脚本注册表（`script_registry.json`）已含 `target_web` 字段，检索时**必须先过滤 `target_web == goal_web`**，只使用本平台的脚本

---

> 硬性约束
> - **开发 cron 定时脚本前，必须先读取 `references/cron-design-reference.md`**，按其规范开发，完成后在规范文件的「已有脚本清单」中追加记录
> - 若任务需要开发新脚本，必须先撰写"技术方案"
> - 必须基于"技术方案"进行开发
> - 允许并要求开发脚本以落地任务
> - 脚本索引表允许写入脚本记录，**禁止**清空
> - 禁止模拟数据：所有任务结果必须来自真实执行与真实平台反馈
> - 禁止询问人工帮助，即使失败了也会记录为失败数据，对下一轮仍有极大帮助
> - 所有涉及 `{goal_web}` 平台的浏览器操作，必须通过 attach 谷歌浏览器实例进行（Browser Relay），不得自行启动新浏览器
> - **【核心约束·最高优先级】必须自动化完成全流程，严禁向用户要求任何形式的人工介入（包括但不限于：请你打开页面、请你点击、请你 attach Tab、请你确认、请提供数据等）。若因环境缺失（Tab 未 attach、权限不足、网络异常等）导致任务无法完成，必须将该任务回写为 `task_state: "failed"`，`task_result` 中写明失败原因，继续执行后续任务，不得中断流程，不得等待人工处理。**

---

## 输入/输出规范

### 输入 JSON — 首批次（batch_seq = 001）
首次运行包含以下基础字段：
- `goal_web`：目标平台（从 core_goal.json 读取）
- `core_goal`：今日核心目标
- `core_flow`：（可为空/null）核心过程约束，与 `core_goal` 同级别。**非空时**描述任务必须遵循的执行流程或操作顺序；**为空/null 时**不影响任何流程，按正常逻辑执行
- `date`：今日日期（每次运行时读取）
- `batch_seq`：从 `001` 开始

### 输入 JSON — 续批次（batch_seq ≥ 002）
从第二批次起，上游 JSON 是 Step 6 复盘输出，额外包含以下字段，**Step 1 读取后必须透传给 Step 2 使用**：
- `workflow_status`：`continue_to_next_batch` 或 `goal_achieved`
- `retrospective_context`：上一批次的复盘摘要
- `next_batch_guidance`：对下一轮拆解和开发的约束指导（含 `blacklist`）
- `carry_over_tasks`：未完成或低分任务的结转列表
- `core_flow`：（可为空/null）同首批次，从上一批次 retro 或 core_goal.json 继承透传

> 若 `workflow_status = goal_achieved`，终止工作流，输出完成报告。

### Prompt 文件（通过注册表查找）
- Step 1 / Step 6 均使用 **Prompt 注册表查找机制**（详见下方「Prompt 查找规则」）
- 注册表路径：`references/prompts/prompt_registry.md`
- 通用 fallback：`references/prompts/goal_prompt.md`（任务拆解）/ `references/prompts/retro_prompt.md`（复盘）

### 输出 JSON（任务拆解结果）
在输入字段基础上新增：
- `task_id`：按优先级排序，从 1 开始
- `task`：任务名
- `task_description`：任务描述
- `task_reason`：为什么有利于实现 `core_goal`
- `depends_on`：**（V2.0 新增）** 前置任务 ID 列表，空数组 `[]` 表示无依赖，可立即执行；非空时必须等所有前置任务 `task_state = done` 才能执行
- `task_state`：`done | pending | failed | blocked`
  - `pending`：尚未执行（含「就绪待调度」）
  - `done`：任务目标达成
  - `failed`：任务目标未达成（含脚本报错、外部拦截、超时等一切失败情形，回写原因后立即进入 Step 5）
  - `blocked`：**（V2.0 新增）** 前置任务 failed，本任务自动标记为 blocked，跳过执行，直接交由 Step 6 复盘处理
- `task_result`：初始为 `null`
- `source`：**（V2.0 新增）** 脚本来源标记，`registry`（从注册表召回）或 `new`（本批次新开发），Step 5 OB 老化降级依赖此字段

---

## 主任务文件 vs 分支任务文件

| 概念 | 文件 | 职责 |
|------|------|------|
| **主任务文件** | `tasks/master_task.json` | 每次运行的上下文快照：runtime_goal_web、runtime_core_goal、触发来源、从分支任务合并的上下文 |
| **分支任务文件** | `tasks/{goal_web}_tasks_{batch_seq}.json` | 某平台某批次的任务拆解与执行结果（历史档案） |
| **分支复盘文件** | `tasks/{goal_web}_retro_{batch_seq}.json` | 某平台某批次的复盘输出，供下一批次 Step 1 读取 |

**合并优先级**（高优先级覆盖低优先级）：
```
用户输入（当次触发）> core_goal.json > 分支任务历史数据（retro）
```

---

## 执行总流程（必须严格遵循）

### 日志记录规范（必须遵循）
- 读取并遵循 `references/logging.md`
- 每次完整执行必须生成主日志文件，命名：`运行日志_{date}_{batch_seq}.md`

---

### 0) 触发解析（每次 Skill 启动的第一步）

**目标**：从用户输入中解析出意图类型（**Prompt 生产** 或 **批次任务执行**），分别进入对应流程。

#### 意图识别（最优先判断）

```
用户触发 Skill
    ↓
Step 0.0：识别意图类型
    ├── 意图 = Prompt 生产
    │       触发词：「撰写/生成/写/创建 + Prompt + 平台名」
    │       或：「帮我写 {goal_web} 的复盘Prompt / 任务拆解Prompt」
    │       → 跳转至「Prompt 生产流程」（见下方独立章节），不进入批次任务流程
    │
    └── 意图 = 批次任务执行（默认）
            → 继续 Step 0.1：解析 goal_web 和 core_goal（原有逻辑不变）
```

---

#### 解析流程（批次任务执行，原有逻辑不变）

```
用户触发 Skill
    ↓
Step 0.1：解析用户输入，尝试识别 goal_web 和 core_goal
    ├── 情况一：仅解析出 goal_web（无 core_goal）
    │       → 从 tasks/{goal_web}_retro_* 读取最新 core_goal
    │       → 分支任务提供全部上下文（retro/blacklist/carry_over 等）
    │
    ├── 情况二：同时解析出 goal_web + core_goal
    │       → runtime_core_goal = 用户输入值（覆盖 core_goal.json 和历史 retro）
    │       → 分支任务仅提供历史上下文（batch_seq/retro/blacklist/carry_over），不提供 core_goal
    │
    └── 情况三：解析不出 goal_web
            → 检查 tasks/ 目录下有几个平台的历史文件
            │   ├── 仅一个平台 → 提示用户：「检测到只有 {X} 的任务记录，是否触发 {X} 任务？」
            │   └── 多个平台 / 无历史 → 询问用户：「请问要对哪个平台执行任务？」
            → 等待用户确认后，重新走情况一或情况二
```

#### goal_web 识别规则

优先按以下顺序识别：
1. 用户明确提到平台名（微博、脉脉、知乎、Producthunt、Twitter 等）
2. 用户消息含 `goal_web=xxx` 或 `web=xxx` 等参数格式
3. `core_goal.json` 中的 `goal_web` 值（作为兜底默认值，非强制）

#### core_goal 识别规则

1. 用户明确说「目标是…」「core_goal=…」「goal=…」→ 使用用户值
2. 用户未提供 → 从 `tasks/{goal_web}_retro_*` 最新文件读取
3. 无历史 retro → 从 `core_goal.json` 读取

#### core_flow 识别规则

1. 用户明确说「流程是…」「core_flow=…」「必须按…流程」→ 使用用户值
2. 用户未提供 → 从 `tasks/{goal_web}_retro_*` 最新文件的 `core_flow` 字段读取（若有）
3. 无历史 retro 或字段为空 → 从 `core_goal.json`（或分支 `core_goal_{goal_web}.json`）读取 `core_flow` 字段
4. 以上来源均为空/null → `runtime_core_flow = null`，跳过所有 core_flow 相关流程约束，无任何影响

#### Step 0.2：读取 hook_config.json，初始化 auto_run

在生成 `master_task.json` 之前，**必须**读取 `references/hook_config.json`：

```
读取 hook_config.json
  → 查找 platforms[goal_web].auto_runs
  → 未找到则使用 default_auto_runs（默认 1）
  → 将 auto_runs 写入 master_task.json 的 auto_run 字段
```

**仅用户首次触发时初始化**（`trigger_source = user_message` 或 `cron`）。
自动触发下一批次时（`trigger_source = auto_hook`），`auto_run.remaining` 直接从上一个 master_task.json 继承并递减，**不重新读取 hook_config**（避免重置计数器）。

**（V2.1 新增）`meta_optimization` 初始化规则**：
- 用户首次触发时：检查上一个 master_task.json 是否已有 `branch_context.meta_optimization` 字段
  - 有 → 直接继承（`batches_since_last_opt` 和 `prompt_iteration_seq` 均继承，不重置）
  - 无（全新平台）→ 初始化为 `{"prompt_iteration_seq": "000", "batches_since_last_opt": 0}`
- 跨平台切换时（goal_web 变更）：`meta_optimization` 随 goal_web 独立维护，不互相干扰

#### 输出：master_task.json

每次触发后，将解析结果写入 `tasks/master_task.json`：

```json
{
  "trigger_time": "2026-03-17T18:53:00",
  "trigger_source": "user_message",
  "runtime_goal_web": "Producthunt",
  "runtime_core_goal": "获取Producthunt每日和近一周的核心AI产品，并介绍产品价值，输出报告。",
  "context_source": {
    "goal_web_from": "user_input",
    "core_goal_from": "branch_retro",
    "branch_retro_file": "tasks/Producthunt_retro_001.json"
  },
  "branch_context": {
    "last_batch_seq": "001",
    "next_batch_seq": "002",
    "next_batch_guidance": {},
    "carry_over_tasks": [],
    "blacklist": [],
    "meta_optimization": {
      "prompt_iteration_seq": "000",
      "batches_since_last_opt": 0
    }
  },
  "auto_run": {
    "total": 1,
    "remaining": 1,
    "current_run": 1
  }
}
```

> **字段说明**
> - `runtime_core_flow`：（可为空/null）过程约束字段，从 core_goal.json 或上一批次 retro 读取后注入。**非空时**：Step 2 必须将其作为硬性过程约束注入任务拆解（每个 task 须注明 `flow_step` 对应哪一环节）；Step 4 执行后校验每个 task 是否遵从流程（写入 `flow_compliant: true/false`）；Step 6 复盘输出中必须新增 `flow_violations` 字段记录违反情况及归因。**为空/null 时**：跳过上述所有检查，不影响正常流程。
> - `trigger_source`：`user_message` / `cron` / `auto_hook`（自动连续运行时）
> - `context_source`：记录每个字段的来源，便于调试
> - `branch_context`：从分支复盘文件提取的历史上下文，传递给 Step 1
> - `auto_run.total`：本次触发的总批次数（从 hook_config 读取）
> - `auto_run.remaining`：剩余还需运行的批次数（每完成一个 batch 减 1）
> - `auto_run.current_run`：当前是第几次自动运行（从 1 开始）
> - `branch_context.meta_optimization`：**（V2.1 新增）元学习进化计时器**，每个 goal_web 平台独立维护
>   - `prompt_iteration_seq`：当前使用的 Prompt 版本号（`000` = 原始版，`001` = 第一次进化后，依此类推）
>   - `batches_since_last_opt`：上次进化后完成的批次数，每次 Step 6 末尾 +1；达到 10 时触发 Step 6.5 元学习进化流并清零

---

### 1) 读取输入

> Step 0 已完成触发解析并写入 `tasks/master_task.json`，Step 1 直接从该文件读取运行时上下文。

1. 读取 `tasks/master_task.json`，获取：
   - `runtime_goal_web` → 本批次 `goal_web`（全局变量，注入所有后续步骤）
   - `runtime_core_goal` → 本批次 `core_goal`
   - `runtime_core_flow` → 本批次 `core_flow`（可为空/null；非空时作为硬性过程约束贯穿后续全部步骤）
   - `branch_context` → 历史上下文（`next_batch_seq` / `next_batch_guidance` / `carry_over_tasks` / `blacklist`）
   - **合并优先级再次确认**：master_task.json 已按「用户输入 > core_goal.json > 分支历史」合并，Step 1 直接使用，不再重新读取 core_goal.json
2. 从 `branch_context.next_batch_seq` 确定本批次序号：
   - 有值 → 使用该值
   - 无值（首批次）→ 强制 `001`，严禁继承其他平台序号
3. **读取 goal_prompt（通过注册表查找）**：
   ```
   读取 references/prompts/prompt_registry.md
     → 查找 type=任务拆解 AND web={goal_web} 的记录
     → 找到 → 读取该记录 path 指向的 Prompt 文件
     → 未找到 → fallback：读取 references/prompts/goal_prompt.md
   ```
4. **若 `branch_context` 含 `next_batch_guidance`**：提取约束条件和 `blacklist`，暂存备用（Step 2 和 Step 3 使用）
5. **若 `branch_context.workflow_status = goal_achieved`**：终止，输出完成报告，不再继续

---

### 2) 任务拆解（基于 goal_prompt）
1. **若上游 JSON 含 `carry_over_tasks`**：优先将结转任务纳入本批次拆解（保留原 task_id，补充调整策略）
2. **若上游 JSON 含 `next_batch_guidance`**：拆解前先读取其中 `task_breakdown_advice` 和 `development_constraints`，将其作为硬性约束应用于本批次任务设计
3. **【core_flow 约束注入（非空时必须执行）】**：
   - 若 `runtime_core_flow` 非空：将 `core_flow` 描述的流程步骤作为**硬性过程约束**注入任务拆解：
     - 每个 task 必须对应 `core_flow` 中的某个流程环节，在 task 字段中新增 `"flow_step": "对应的流程环节名称"`
     - 拆解出的任务顺序、依赖关系必须与 `core_flow` 描述的流程顺序严格一致，不得跳步或乱序
     - 若某个 `core_flow` 流程环节在本批次无法执行，需显式拆解为一个 `task_state: "blocked"` 的占位任务，写明原因
   - 若 `runtime_core_flow` 为空/null：跳过此步骤，按正常 `core_goal` 拆解逻辑执行
4. 使用上一步查找到的 `goal_prompt`（专属版或 fallback 通用版）对 `core_goal` 进行拆解，输出新的任务 JSON
5. 保持：`goal_web / core_goal / core_flow / date / batch_seq` 与上游一致
6. 任务描述中涉及平台操作时，用实际 `goal_web` 值替换 `{goal_web}`
7. **（V2.0 新增）DAG 依赖图谱**：为每个任务输出 `depends_on` 字段：
   - 无前置依赖的任务：`"depends_on": []`
   - 有前置依赖的任务：`"depends_on": [task_id_1, task_id_2]`
   - 示例：数据采集任务（task_id=1）无依赖；报告生成任务（task_id=2）依赖采集任务 → `"depends_on": [1]`
   - 拆解时优先设计「可并发执行的任务对」，相互无依赖的任务 `depends_on` 均为 `[]`
7. **任务 JSON 保存路径**：`tasks/{goal_web}_tasks_{batch_seq}.json`（例：`tasks/微博_tasks_002.json`）

---

### 3) 任务执行引擎
1. 从任务 JSON 中按顺序找到第一个 `task_state = pending` 的任务
2. 从 `task` 与 `task_description` 中提炼搜索 query（query 中用 `goal_web` 实际值）
3. 在脚本注册表中检索 `script_description`（仅限 `score >= 0.8`）
   - **平台过滤（首要条件）**：只检索 `target_web == goal_web` 的记录，其他平台的脚本一律忽略
   - **安全校验（黑名单过滤）**：若上游 JSON 的 `next_batch_guidance.blacklist` 不为空，必须排除其中的脚本路径，即使 score >= 0.8 也不得使用
   - 检索结果为空或 score < 0.8 → 进入 OB 召回
4. OB 召回：
   - 进入 OB 召回流程，召回文档时优先检索与 `{goal_web}` 平台相关的文档
   - 阅读文档并进行置信度评分（0-1）
   - 置信度 >= 0.8：可作为开发参考
   - 否则：进入开发流程
5. 若无任何参考文档：直接进入开发流程

---

### 3.2) 沙盒预检（静态检查 + 局部自愈）【V2.0 新增，在 3.1 之后、Step 4 之前执行】

> **目标**：拦截低级代码错误，避免浪费真实执行环境和复盘周期。

**触发条件**：Step 3.1 新开发的脚本写入路径后，进入本步骤。从注册表直接召回的脚本（`source = registry`）跳过本步骤（已验证过）。

**执行流程**：

```
Step 3.1 新脚本写入
    ↓
Step 3.2：静态语法检查
    ├── Python 脚本 → exec: python3 -m py_compile <script_path>
    │   返回码 = 0 → 通过，写入 task_script，进入 Step 4
    │   返回码 ≠ 0 → 截获 stderr，进入局部自愈循环
    │
    └── Shell 脚本 → exec: bash -n <script_path>
        返回码 = 0 → 通过
        返回码 ≠ 0 → 进入局部自愈循环
```

**局部自愈循环**（最多重试 3 次，超限则标记任务 failed）：
1. 将原脚本内容 + stderr 报错信息 提交给 LLM（当前 AI 上下文）进行修复
2. 重新写入脚本文件
3. 再次执行静态检查
4. 通过 → 写入 task_script，进入 Step 4
5. 第 3 次仍失败 → 将任务 `task_state = failed`，`task_result` 写入「沙盒预检失败，3 次自愈均未通过，报错：{stderr}」，进入 Step 5 评分

**放行条件**：只有通过静态检查的脚本路径，才允许写入任务 JSON 的 `task_script` 字段，进入 Step 4 真实执行。

---

### 3.1) 开发流程（技术方案 → 脚本）
1. 进入开发前**必须读取**：`references/technical-decision-reference.md`
2. 若任务涉及"发布/外部平台发布"，额外**必须读取**：`references/external-publishing-design-reference.md`
3. 若上游含 `next_batch_guidance.development_constraints`，**必须**将其作为约束条件纳入技术方案
4. 基于任务与参考内容，撰写技术方案：
   - 命名：`技术方案_v{版本号}_{date}.md`
   - 包含：业务目标 / 技术目标 / 约束（含 `{goal_web}` 平台特性）/ 三方案（A快 / B平衡 / C理想）/ 决策与取舍
   - **平台约束**：`{goal_web}` 平台操作必须通过 attach 谷歌浏览器实例（Browser Relay），脚本中使用 `get_relay_ws_url()` 获取连接
5. 按技术方案进行开发，生成可执行脚本（Python/Bash 等）
6. 自检：确认脚本逻辑与技术方案一致
7. 将脚本写入脚本注册表，**必须包含以下全部字段**：`name`、`path`、`script_description`、`score`、`score_reason`、`target_web`（填写当前 `goal_web` 实际值，不得留空）
8. 更新任务 JSON，在对应任务下新增字段：
   - `task_script_seq`：脚本序号（数组）
   - `task_script`：脚本路径（数组，与 seq 一一对应）

---

### 4) 记录执行结果（V2.0：并发调度 + 双轨日志）

#### 4.1 并发调度（DAG 执行器）

```
扫描任务 JSON，建立就绪队列：
  就绪条件：task_state = "pending" AND（depends_on = [] OR 所有前置任务 task_state = "done"）
    ↓
将就绪队列中的任务并发执行（同一批扫描周期内同时拉起）
    ↓
某任务执行完毕（done/failed）→ 立即回写 task_state 和 task_result
    ↓
重新扫描就绪队列（前置任务 done 后，其后继任务解锁为就绪态）
    ↓
重复，直到无 pending 任务
```

**blocked 标记规则**：若某任务的前置任务 `task_state = failed`，则该任务 `task_state → blocked`，`task_result = "前置任务 {task_id} 失败，本任务跳过执行"`，不进入执行队列，直接进入 Step 5 评分。

#### 4.2 执行与回写

1. 读取任务 JSON，按并发调度逻辑执行
2. 无论执行结果如何，立即将结果回写至 `tasks/{goal_web}_tasks_{batch_seq}.json` 的 `task_result`，**不得留空、不得等待外部条件**
2.5. **【core_flow 合规校验（非空时必须执行）】**：若 `runtime_core_flow` 非空，每个 task 执行完毕后，额外回写字段：
   - `flow_compliant: true`：该任务的执行路径符合 `core_flow` 中对应流程环节的要求
   - `flow_compliant: false`：执行路径偏离了 `core_flow` 约束（需在 `task_result` 中写明具体偏离点）
   - `flow_compliant: null`：`runtime_core_flow` 为空，跳过校验
3. 根据执行结果更新 `task_state`（**非此即彼，无中间态**）：
   - 任务目标达成 → `done`
   - 任务目标未达成（无论何种原因）→ `failed`，`task_result` 中写明失败现象与原因
   - 前置任务 failed → `blocked`

#### 4.3 双轨日志生成（V2.0 新增）

每次 batch 所有任务执行完毕后，**必须同时生成两份产物**：

**轨道 A：完整 Markdown 日志**（人类审计/归档用，原有逻辑不变）
- 路径：`run/{date}/{batch_seq}/运行日志_{date}_{batch_seq}.md`

**轨道 B：结构化压缩日志**（Step 6 复盘专用，V2.0 新增）
- 路径：`run/{date}/{batch_seq}/compressed_log.json`
- 内容结构：

```json
{
  "batch_seq": "008",
  "goal_web": "Producthunt",
  "date": "2026-03-21",
  "task_summary": [
    {
      "task_id": 1,
      "task": "任务名称",
      "task_state": "done",
      "source": "registry",
      "script_score": 0.95,
      "action_sequence": ["读取配置", "调用 API", "生成报告", "推送飞书"],
      "error_trace": null
    },
    {
      "task_id": 2,
      "task": "任务名称",
      "task_state": "failed",
      "source": "new",
      "script_score": 0.4,
      "action_sequence": ["读取配置", "调用 API"],
      "error_trace": "TypeError: NoneType has no attribute 'get' at line 42"
    }
  ],
  "batch_outcome": "partial_success",
  "top_error": "TypeError: NoneType has no attribute 'get'"
}
```

- **提取规则**：
  - `action_sequence`：从完整日志中提取关键动作序列（3-8 个动作词，如「打开网页 → 定位输入框 → 点击按钮」）
  - `error_trace`：只保留最底层 Exception 类型 + 报错所在行，过滤掉环境变量打印等无关输出
  - `batch_outcome`：`all_done`（全部成功）/ `partial_success`（部分成功）/ `all_failed`

> **流程铁律**
> - 失败即回写：脚本执行产生任何结果（含报错、超时、页面拦截），立即回写 `task_result = failed`，**不降级、不重试、不等待**
> - 单任务 failed 不阻断流程：`task_state = failed` 后直接进入 Step 5 评分
> - 失败原因交由 Step 6 复盘处理，由下一批次的 `carry_over_tasks` 承接重试策略
> - **compressed_log.json 必须在所有 task 回写完成后才生成**，不得提前

#### on_batch_complete 钩子（Step 4 所有 task 回写完成后触发）

```
所有 task task_state 均已回写（done/failed/blocked）
    ↓
【不再因 failed 停止】失败状态已在 Step 4 执行时回写至 task_result（含失败原因+操作路径），
Step 6 复盘将统一读取所有任务状态（包含 failed）进行归因分析，生成 carry_over_tasks 和 blacklist。
    ↓
直接读取 master_task.json 的 auto_run.remaining：
    remaining <= 0？
        → 终止，向用户输出完成摘要（含本批次 failed 任务列表）
    remaining > 0？
        → remaining -= 1，current_run += 1，写回 master_task.json
        → 自动执行 Step 5（评分）→ Step 6（复盘），生成 retro 文件
        → 更新 master_task.json：
              trigger_source = "auto_hook"
              batch_seq 递增（如 007 → 008）
        → 自动跳回 Step 1，开始下一个 batch
        → 不等待用户确认
```

> **设计原则**：失败是数据，不是中断信号。任何 task 失败只会在 task_result 中留下记录（失败原因、操作路径、错误信息），流程继续向前推进至 Step 6 复盘。复盘负责归因、生成修正指导，下一批次基于此重试。**严禁因单个 task 失败而停止整个工作流。**

**静默运行原则**：自动连续 batch 期间，每完成一个 batch 发送一条简短通知（含已完成/失败任务数量），不等待用户回复，直接开始下一个 batch。

**强制停止**：用户任意时刻说「停止」→ 将 `master_task.json` 的 `auto_run.remaining` 设为 0，当前 batch 完成后不再继续。

---

### 5) 结果评分 + 核心目标校验（V2.0：新增 OB 老化降级）
1. 读取任务 JSON，遍历所有任务：
   - `task_state = blocked`：跳过，不参与评分
   - `task_state = failed`：**不跳过，直接记录评分结果**，`script_score = 0`，`score_reason` 写入失败原因摘要（从 `task_result` 提取），交由 Step 6 复盘处理；**不因 failed 中止 Step 5 流程**
   - `task_state = done` 且 `task_result` 非空：正常评分
2. 对 `done` 任务打分（`script_score` 0~1，0.8 及格）并记录 `score_reason`
   - **绝对红线**：`task_result` 含 `Error/Exception/Traceback` → score 上限 0.5
   - **绝对红线**：`task_result` 为空或关键字段缺失 → score 上限 0.7
3. **注册表回写机制**：若 `script_score < 0.8`，必须同步将该评分回写至脚本注册表，强制覆盖或降低全局 score，防止该失败脚本下一轮被误选；**回写时同样必须确保 `target_web` 字段已填写（填写当前 `goal_web` 实际值）**
4. **（V2.0 新增）OB 脚本老化降级机制**：
   - 触发条件：该任务的 `source = registry`（从注册表召回）且 `script_score < 0.8`
   - 触发后执行以下两步：
     1. **降低权重**：在 `script_registry.json` 中找到对应记录，将 `score` 强制下调（基准：旧 score × 0.7，最低降至 0.3），`score_reason` 追加 `「[{date}] 召回执行失败，权重自动降级，需人工审查」`
     2. **追加老化标签**：在该记录中新增 `"tags": ["needs_update", "deprecated_by_{date}"]` 字段（若已有 tags 则追加，不覆盖）
   - 效果：下一轮 Step 3 检索时，该脚本因 score < 0.8 而被过滤，强制进入重新开发（Step 3.1）流程
   - 不触发条件：`source = new`（本批次新开发的脚本失败，只做常规注册表 score 回写，不走老化流程）
5. 核心目标校验：
   - 评估已完成任务集合是否足以达成 `core_goal`
   - 若不足：列出欠缺任务清单，追加回任务列表（`task_state = pending`，`task_result = null`），回到 Step 2

> 示例见：`references/step5_example.md`

---

### 6) 全局复盘与下一批次输入生成
> **必须通过 Prompt 注册表查找**复盘 Prompt，禁止自行简化或替换。

1. **读取 retro_prompt（通过注册表查找）**：
   ```
   读取 references/prompts/prompt_registry.md
     → 查找 type=复盘 AND web={goal_web} 的记录
     → 找到 → 读取该记录 path 指向的 Prompt 文件
     → 未找到 → fallback：读取 references/prompts/retro_prompt.md
   ```
2. 填充三个输入变量：
   - `{current_task_json}`：当前批次最终任务 JSON（含 `task_state` / `task_result` / `script_score` / `score_reason`）
   - `{current_run_log}`：当前批次完整运行日志（读取 `run/{date}/{batch_seq}/运行日志_*.md`）
   - `{past_3_runs_logs}`：**（V2.0 变更）** 不再读取原生 .md 日志，改读过去 3 个批次的 `compressed_log.json`（路径：`run/*/*/compressed_log.json`，按 batch_seq 倒序取最近 3 个）；若 compressed_log.json 不存在则 fallback 到原生 .md 日志
3. 执行复盘 Prompt（已通过注册表加载），按 Prompt 模板规则分析：
   - 现状评估：提取失败任务，定位根本原因
   - 历史模式识别：检查死循环，若命中则强制要求下一轮改变技术路线
   - 构建下一批次输入：步进 `batch_seq`，继承/细化 `core_goal`，生成 `blacklist` 与 `next_batch_guidance`，打包结转任务
4. 输出严格合法的 JSON，字段必须包含：
   - `batch_seq` / `goal_web` / `core_goal` / `workflow_status`
   - `core_flow`：**必须透传**，与上游保持一致（null 时写 null，非空时原样透传，不得丢失）
   - `retrospective_context`（`failed_tasks_summary` / `historical_patterns` / `lessons_learned`）
   - `next_batch_guidance`（`task_breakdown_advice` / `development_constraints` / `avoid_pitfalls` / **`blacklist`**）
   - `carry_over_tasks`
   - `flow_violations`：**【core_flow 非空时必须输出，为空/null 时省略】** 记录本批次中 `flow_compliant = false` 的任务列表，格式：
     ```json
     "flow_violations": [
       {
         "task_id": 2,
         "task": "任务名",
         "expected_flow_step": "core_flow 中要求的流程环节",
         "actual_behavior": "实际执行时偏离的具体描述",
         "root_cause": "偏离原因分析",
         "fix_suggestion": "下一批次如何修正"
       }
     ]
     ```
     若本批次无违反（所有 `flow_compliant = true`）：写 `"flow_violations": []`
   - `user_feedback`（详见下方规范，**若本批次有用户反馈则必须写入，无则省略该字段**）
   - **禁止输出任何 JSON 以外的文字或 Markdown**

#### user_feedback 字段规范

**触发条件**：用户说「把以下反馈写入 {goal_web}」/ 「加入反馈」/ 「写入用户反馈」等。

**写入目标**：当前批次的 retro 文件（`tasks/{goal_web}_retro_{batch_seq}.json`），**只写当期，不累积**。

**字段格式**：
```json
"user_feedback": {
  "priority": "HIGH",
  "date": "YYYY-MM-DD",
  "feedback": [
    "用户反馈内容1",
    "用户反馈内容2"
  ]
}
```

**字段说明**：
- `priority`：固定为 `HIGH`，无论内容如何，用户反馈永远最高优先级
- `date`：写入日期（当天）
- `feedback`：用户反馈条目数组，逐条写入，不合并、不改写原意

**下一批次读取机制**：
Step 1 读取 `branch_context` 时，若上一批次 retro 文件含 `user_feedback` 字段，**必须**：
1. 提取 `user_feedback.feedback` 数组
2. 在 Step 2 任务拆解时，将每一条 feedback 转化为显式约束或 task，优先级高于 `next_batch_guidance`
3. 在 master_task.json 的 `branch_context` 中透传 `user_feedback`，直到该批次任务全部完成为止
5. **复盘 JSON 保存路径**：
   - 主路径（Step 1 读取上游用）：`tasks/{goal_web}_retro_{batch_seq}.json`（例：`tasks/微博_retro_001.json`）
   - 归档路径（日志用）：`run/{date}/{batch_seq}/retro_output.json`（同时写入，保持日志完整性）
6. **（V2.1 新增）元学习计数器更新**：retro JSON 写入完成后，立即更新 `tasks/master_task.json` 的 `branch_context.meta_optimization`：
   - `batches_since_last_opt += 1`
   - 若 `batches_since_last_opt < 10`：继续正常流程，进入 Step 7 → 下一 Batch
   - 若 `batches_since_last_opt == 10`：**冻结引擎**，不进入下一 Batch，切入 **Step 6.5 元学习进化流**
7. 将输出 JSON 直接作为下一批次 **Step 1 读取输入** 的上游 JSON，自动触发下一轮工作流

---

### 6.5) 元学习进化流（Meta-Learning Evolution）【V2.1 新增，triggered when batches_since_last_opt == 10】

> **目标**：在完成 10 个批次后，自动审视失败模式，重写底层拆解/复盘 Prompt，实现系统方法论的版本迭代。
> **事件驱动**：由 Step 6 末尾的计数器检查触发，非 Cron，无竞态冲突风险。

#### 6.5.1 提取诊断上下文（防 Token 膨胀）

向上追溯，读取过去 **5 个批次**的 retro 文件（`tasks/{goal_web}_retro_*.json`，取最近 5 个）：

只提取以下两个字段：
- `retrospective_context.historical_patterns`
- `retrospective_context.lessons_learned`

将提取结果合并，生成一段《平台演进与系统瓶颈诊断报告》，格式：

```
【{goal_web} 平台近5批次诊断报告】
历史死循环模式：
- [来自各批次 historical_patterns 的去重合并]

核心教训：
- [来自各批次 lessons_learned 的去重合并]

高频失败根因：
- [出现 ≥ 2 次的失败类型，按频率排序]
```

#### 6.5.2 确定当前 Prompt 版本

从 `tasks/master_task.json` 读取 `branch_context.meta_optimization.prompt_iteration_seq`（如 `000`）。

从 `references/prompts/prompt_registry.md` 查找当前 `goal_web` 平台使用的 Prompt 文件路径：
- `type=任务拆解` → 当前 goal_prompt 路径
- `type=复盘` → 当前 retro_prompt 路径

读取这两个文件的完整内容，作为「待升级的当前 Prompt」。

#### 6.5.3 调用 meta_prompt 重写 Prompt（认知升级）

读取 `references/prompts/meta_prompt.md`，以其为角色框架，组装以下输入：

```
输入一：《平台演进与系统瓶颈诊断报告》（6.5.1 生成）
输入二：当前 goal_prompt 全文
输入三：当前 retro_prompt 全文
输入四：references/prompts/prompt_authoring_guide.md 中的字段规范（Schema 约束）

系统指令：
你是一个高级 Prompt 架构师，专为 {goal_web} 平台服务。
请审视这 5 轮的失败教训和死循环模式，找出当前拆解 Prompt 和复盘 Prompt 的思维盲区。
重写这两个 Prompt，强制加入针对上述失败模式的约束条款，提升对该平台规则变动和反爬机制的适应力。
输出格式必须完全遵循 prompt_authoring_guide.md 的字段规范，不得引入新字段或删除必填字段。
```

生成两份新 Prompt 全文：`new_goal_prompt` 和 `new_retro_prompt`。

#### 6.5.4 版本控制：另存为新版本（禁止覆盖）

计算新版本号：`new_seq = prompt_iteration_seq + 1`（格式三位数字，如 `001`）

**写入两个新文件**（不覆盖旧文件）：
- `references/prompts/goal_prompt_{goal_web}_v{new_seq}.md` ← 新 goal_prompt 内容
- `references/prompts/retro_prompt_{goal_web}_v{new_seq}.md` ← 新 retro_prompt 内容

**更新注册表** `references/prompts/prompt_registry.md`：
- 找到 `type=任务拆解 AND web={goal_web}` 的行 → 将 `path` 更新为新文件路径，在描述末尾追加 `[v{new_seq} auto-evolved {date}]`
- 找到 `type=复盘 AND web={goal_web}` 的行 → 同上

若注册表中无该平台记录（首次为该平台生成专属 Prompt）→ 追加新行。

#### 6.5.5 重置计数器 + 进化完成通知

更新 `tasks/master_task.json`：
```json
"meta_optimization": {
  "prompt_iteration_seq": "{new_seq}",
  "batches_since_last_opt": 0
}
```

向用户发送一条进化完成通知（不中断后续流程）：
```
🧬 {goal_web} Prompt 进化完成！
版本：v{old_seq} → v{new_seq}
核心改进：[用1-2句话总结本次重写的主要变更点]
旧版本保留在 references/prompts/ 可随时回滚
```

进化完成后，自动进入 Step 7（成功经验入库），然后继续正常的下一 Batch 流程。

#### 6.5.6 回滚机制

若下一批次执行后发现 Prompt 进化导致任务 JSON 解析严重失败（连续 2 个批次全部 failed），在 retro 的 `next_batch_guidance.development_constraints` 中加入：

```
Prompt 回滚指令：将 prompt_registry.md 中 {goal_web} 的 path 指针从 v{new_seq} 改回 v{old_seq}，
并将 master_task.json 的 prompt_iteration_seq 回滚为 {old_seq}。
```

---

### 7) 成功经验入库（Knowledge Ingestion）【V2.0 新增，在 Step 6 之后执行】

> **目标**：将高分成功路径固化为标准知识写入脚本注册表，充实知识飞轮，避免未来重复开发同类脚本。

**触发条件**：Step 6 复盘完成后，自动进入 Step 7（不需要用户触发）。

#### 7.1 筛选候选任务

从当前批次任务 JSON 中筛出满足以下全部条件的任务：
- `task_state = done`
- `script_score >= 0.8`
- `source = new`（本批次全新开发，非从注册表召回）

若无满足条件的任务 → Step 7 静默跳过，不写任何文件。

#### 7.2 长期价值评估

对每个候选任务，用以下微型 Prompt 判断其通用价值：

```
该任务路径是否满足以下条件（Yes/No/Partial）：
1. 解法不依赖特定日期/特定数据，未来同类任务可复用？
2. 核心逻辑对同平台（{goal_web}）其他批次有参考价值？
3. 与注册表已有脚本无高度重叠（相似度 < 80%）？

全部 Yes → 入库
任一 No → 跳过（记录原因）
```

#### 7.3 写入脚本注册表

满足条件的脚本，更新 `references/script_registry.json` 中对应记录，补充以下字段：
- `ingested_at`：入库日期（`YYYY-MM-DD`）
- `ingestion_reason`：入库理由（1句话，为什么认为可复用）
- `tags`：追加 `["verified", "batch_{batch_seq}"]`

> **约束**：Step 7 不产生任何新文件，只更新 `script_registry.json` 已有记录或追加新记录（若该脚本尚未注册）。注册表是唯一写入目标。

#### 7.4 Step 7 完成日志

在当前批次的 `compressed_log.json` 中追加字段：
```json
"step7_ingestion": {
  "candidates": 2,
  "ingested": 1,
  "skipped": 1,
  "skip_reason": "与已有脚本 auto_ph.py 重叠度 > 80%"
}
```

---

## Prompt 生产流程（独立章节，不干扰批次任务流程）

> 触发条件：Step 0.0 识别到意图 = Prompt 生产

### P1）确认生产参数

从用户输入提取：
- `prompt_type`：`任务拆解` 或 `复盘`
- `goal_web`：目标平台（如 `同花顺`、`东方财富`）

若任一字段缺失，询问用户后继续，不擅自猜测。

---

### P2）读取上下文（欠缺2修复）

自动收集生产所需的上下文，**不需要用户手动提供**：

```
读取 references/prompts/prompt_authoring_guide.md
  → 提取对应 prompt_type 的输入字段规范 + 输出字段规范（作为硬性 Schema）

读取 references/core_goal.json
  → 提取 goal_web 对应的 core_goal（作为业务背景）

读取最近 3 个 tasks/{goal_web}_retro_*.json
  → 提取 lessons_learned / historical_patterns / 平台特有约束
  → 作为「平台专属 Prompt 约束」注入 Lyra 的 USER INPUT
```

---

### P3）调用 meta_prompt 生产 Prompt 正文

以 `references/prompts/meta_prompt.md` 作为 Lyra 角色，组装以下三段输入：

```
1. User Requirement and Goal：
   「生产一个用于 {goal_web} 平台的 {prompt_type} Prompt。
    平台特有约束：[来自 P2 步骤提取的 retro 约束]
    核心目标：[来自 core_goal]」

2. Input JSON Schema Specification：
   [来自 prompt_authoring_guide.md 的输入字段规范]

3. Output JSON Schema Specification：
   [来自 prompt_authoring_guide.md 的输出字段规范]
```

以 DETAIL MODE 执行 Lyra 4-D 方法论（DECONSTRUCT → DIAGNOSE → DEVELOP → DELIVER），输出最终 Prompt 正文。

---

### P4）字段校验

对照 `prompt_authoring_guide.md` 校验生产出的 Prompt：
- 输入字段名 / 类型 / 默认值是否与规范一致？
- 输出 JSON 字段名 / 层级是否与规范一致？
- 若有不一致 → 自动修正后继续，不需要用户介入

---

### P5）命名 + 写入文件

命名规则：
- 任务拆解：`goal_prompt_{goal_web}.md`
- 复盘：`retro_prompt_{goal_web}.md`

写入路径：`references/prompts/{文件名}`

---

### P6）自动写入 prompt_registry.md（欠缺3修复）

在 `prompt_registry.md` 的注册表中追加一行：

```markdown
| {文件名（不含.md）} | {prompt_type} | {goal_web} | {一句话描述，含平台专属约束关键词} | `references/prompts/{文件名}` | {通用版名称} |
```

---

### P7）完成通知

向用户输出：
```
✅ Prompt 生产完成
文件：references/prompts/{文件名}
注册：prompt_registry.md 已追加记录
下次触发 {goal_web} 批次时，Step 1/Step 6 将自动调用此 Prompt
```

---

> **隔离原则**：Prompt 生产流程完全独立，不写入 master_task.json，不影响任何批次任务的 batch_seq / retro / task 文件。

---

## 输出检查清单（V2.0 已更新）
- [ ] **Step 0**：`tasks/master_task.json` 是否已生成，含 `runtime_goal_web` / `runtime_core_goal` / `runtime_core_flow` / `trigger_source` / `branch_context`
- [ ] **core_flow 读取**：是否按优先级（用户输入 > retro > core_goal.json）读取 `core_flow`，为空/null 时写 null 而非省略字段
- [ ] **Step 0**：`goal_web` 来源是否记录在 `context_source.goal_web_from`（user_input / core_goal_json / prompted）
- [ ] **Step 0**：若情况三（解析不出 web），是否已向用户询问并等待确认，而非擅自猜测
- [ ] **Step 0**：`references/hook_config.json` 是否已读取，`master_task.json` 中 `auto_run` 字段是否已初始化（`total` / `remaining` / `current_run`）
- [ ] **Step 1**：是否先读取 `references/prompts/prompt_registry.md`，按 `type=任务拆解 + web={goal_web}` 查找，未找到才 fallback 到通用 `goal_prompt.md`
- [ ] **Step 1（core_flow）**：`runtime_core_flow` 是否已从 master_task.json 读取并准备注入 Step 2
- [ ] **Step 6**：是否先读取 `references/prompts/prompt_registry.md`，按 `type=复盘 + web={goal_web}` 查找，未找到才 fallback 到通用 `retro_prompt.md`
- [ ] **Prompt 注册表**：新增平台专属 Prompt 时，是否已同步更新 `references/prompts/prompt_registry.md`
- [ ] **Prompt 生产流程**：Step 0.0 是否优先识别「Prompt 生产」意图，识别到后是否跳转至 Prompt 生产流程而非批次任务流程
- [ ] **Prompt 生产 P2**：是否自动读取 authoring_guide（Schema）+ core_goal.json（业务背景）+ 最近3个 retro（平台约束），无需用户手动提供
- [ ] **Prompt 生产 P4**：是否对照 authoring_guide 校验字段，发现不一致时自动修正
- [ ] **Prompt 生产 P6**：是否自动追加 prompt_registry.md 记录（不依赖用户手动操作）
- [ ] **隔离性**：Prompt 生产流程是否未修改 master_task.json / batch_seq / retro 等批次任务文件
- [ ] **全自动化约束**：全流程是否未向用户要求任何人工介入（attach Tab / 点击 / 确认 / 提供数据）？若任务因环境缺失失败，是否已回写 `task_state: "failed"` + 失败原因，而非停下来等待？
- [ ] **Step 0**：若 `trigger_source = auto_hook`，是否从上一个 master_task 继承 `remaining` 而非重新读取 hook_config
- [ ] **Step 4**：所有 task 完成后，是否触发 `on_batch_complete` 钩子，检查 `remaining` 并决定是否继续
- [ ] **Step 4**：有 task failed 时，是否**不中断流程**，直接继续判断 `remaining` 推进至 Step 5→6（失败状态已回写 task_result，复盘兜底）
- [ ] **Step 4**：自动连续运行时，是否在每个 batch 完成后发送简短进度通知（含失败任务数），但不等待用户回复
- [ ] 任务 JSON 是否包含全部字段（含 `goal_web` / `core_flow` / `task_script_seq` / `task_script`）
- [ ] `goal_web / core_goal / core_flow / date / batch_seq` 是否与 core_goal.json 和上游保持一致
- [ ] **Step 2（core_flow 非空）**：每个 task 是否含 `flow_step` 字段，且任务顺序是否与 `core_flow` 流程步骤严格一致
- [ ] **Step 2（core_flow 非空）**：无法执行的流程环节是否以 `task_state: blocked` 的占位任务显式表示
- [ ] **Step 4（core_flow 非空）**：每个 task 执行完毕后是否回写了 `flow_compliant` 字段（true/false/null）
- [ ] **Step 6（core_flow 非空）**：retro JSON 是否含 `flow_violations` 字段，列出所有 `flow_compliant=false` 的任务及归因
- [ ] **Step 6（core_flow 透传）**：retro JSON 是否含 `core_flow` 字段，值与上游一致（null→null，非空→原样）
- [ ] 任务 JSON 是否保存至 `tasks/{goal_web}_tasks_{batch_seq}.json`
- [ ] `task_state` 是否已明确设置（`done` / `failed`），不存在 `pending` 状态的已执行任务
- [ ] `task_result` 是否已写回（非 null）
- [ ] 若产生技术方案：是否按命名规范保存为 Markdown，且包含 `{goal_web}` 平台约束
- [ ] 脚本注册表是否已写入本批次新开发脚本的 score、script_description 与 **`target_web`**（必填，值为当前 `goal_web`）
- [ ] 若 `script_score < 0.8`：注册表中对应脚本 score 是否已降级回写，且 `target_web` 字段是否已填写
- [ ] Step 6 复盘 JSON 的 `next_batch_guidance` 是否含 `blacklist` 字段（结构化路径列表）
- [ ] 运行日志是否已生成并保存
- [ ] Step 6 复盘 JSON 是否已写入以下两个路径：
  - `tasks/{goal_web}_retro_{batch_seq}.json`（Step 1 上游读取用）
  - `run/{date}/{batch_seq}/retro_output.json`（日志归档用）
- [ ] Step 6 复盘 JSON 中是否含 `goal_web` 字段，确保下一批次可正确继承
- [ ] 若本批次有用户反馈：retro JSON 中是否含 `user_feedback` 字段，`priority` 是否为 `HIGH`，`feedback` 数组是否完整写入
- [ ] Step 1 读取上游 retro 时，若含 `user_feedback`：是否已将每条 feedback 转化为本批次任务约束（优先级高于 `next_batch_guidance`）
- [ ] Step 1 读取上游时，是否严格按 `tasks/{goal_web}_retro_*` 过滤，未跨平台读取
- [ ] 若该平台在 `tasks/` 下无历史文件：`batch_seq` 是否从 `001` 开始，且任务 JSON 已写入 `tasks/{goal_web}_tasks_001.json`

### V2.0 新增检查项

- [ ] **Step 2（DAG）**：任务 JSON 中每个任务是否均有 `depends_on` 字段（空数组或前置 ID 列表），无缺漏
- [ ] **Step 2（DAG）**：是否设计了至少一对可并发执行的无依赖任务（`depends_on: []`），而非全链式串行
- [ ] **Step 3.2（沙盒预检）**：新开发脚本是否执行了 `python3 -m py_compile` 或 `bash -n` 静态检查
- [ ] **Step 3.2（自愈）**：若检查失败，是否进入局部自愈循环（最多 3 次重试），超限后是否标记 failed 而非无限重试
- [ ] **Step 3.2（放行）**：只有通过静态检查的脚本路径，才写入 `task_script` 字段
- [ ] **Step 4（并发）**：执行引擎是否按 DAG 就绪态调度，而非按数组顺序串行执行
- [ ] **Step 4（blocked）**：前置任务 failed 时，后继任务是否标记为 `blocked`（而非 pending 或直接 failed）
- [ ] **Step 4（双轨日志）**：是否在所有 task 回写完成后，**同时**生成 `运行日志_*.md`（轨道A）和 `compressed_log.json`（轨道B）
- [ ] **Step 4（compressed_log）**：`compressed_log.json` 中 `action_sequence` 是否为关键动作序列（非原始 stdout），`error_trace` 是否只含最底层异常行
- [ ] **Step 5（source 字段）**：任务 JSON 中是否记录了 `source` 字段（`registry` 或 `new`）
- [ ] **Step 5（OB 老化）**：若 `source=registry` 且 `script_score < 0.8`，是否执行了两步降级：①注册表 score 下调至旧值×0.7 ②追加 `needs_update` / `deprecated_by_{date}` 标签
- [ ] **Step 6（压缩日志）**：`{past_3_runs_logs}` 变量是否读取的是 `compressed_log.json` 而非原生 .md（若无压缩日志则已 fallback）
- [ ] **Step 7（筛选）**：是否扫描了本批次 `source=new` + `score>=0.8` + `done` 的任务
- [ ] **Step 7（评估）**：对候选任务是否完成了通用价值三问评估（非特例性 / 平台可复用 / 无重叠）
- [ ] **Step 7（写入）**：满足条件的脚本是否在 `script_registry.json` 中追加了 `ingested_at` / `ingestion_reason` / `tags`
- [ ] **Step 7（日志）**：`compressed_log.json` 中是否含 `step7_ingestion` 字段，记录候选数 / 入库数 / 跳过原因

### V2.1 新增检查项（元学习进化）

- [ ] **Step 0.2（初始化）**：master_task.json 中是否含 `branch_context.meta_optimization` 字段（`prompt_iteration_seq` + `batches_since_last_opt`）
- [ ] **Step 0.2（继承）**：续批次时 `meta_optimization` 是否从上一个 master_task.json 继承，而非重置为 0
- [ ] **Step 0.2（跨平台隔离）**：goal_web 切换时，`meta_optimization` 是否各自独立，不互相污染
- [ ] **Step 6（计数）**：每次 Step 6 retro 写入完成后，是否执行 `batches_since_last_opt += 1` 并写回 master_task.json
- [ ] **Step 6（触发判断）**：计数器更新后，是否判断 `batches_since_last_opt == 10`，满足则切入 Step 6.5，不满足则继续正常流程
- [ ] **Step 6.5（上下文提纯）**：是否只读取近 5 批次 retro 的 `historical_patterns` + `lessons_learned` 两个字段，而非全量 retro 内容
- [ ] **Step 6.5（meta_prompt）**：是否读取了 `references/prompts/meta_prompt.md` + `references/prompts/prompt_authoring_guide.md` 作为生成约束
- [ ] **Step 6.5（版本控制）**：新 Prompt 是否以 `goal_prompt_{goal_web}_v{seq}.md` / `retro_prompt_{goal_web}_v{seq}.md` 命名另存，而非覆盖旧文件
- [ ] **Step 6.5（注册表更新）**：`prompt_registry.md` 中对应平台的 `path` 指针是否已切换到新版本文件
- [ ] **Step 6.5（计数器重置）**：进化完成后，`prompt_iteration_seq` 是否进位，`batches_since_last_opt` 是否清零
- [ ] **Step 6.5（进化通知）**：是否向用户发送了包含版本号和核心改进点的进化完成通知
- [ ] **Step 6.5（回滚条款）**：若新版本导致连续 2 批次全失败，retro 的 `development_constraints` 中是否写入了回滚指令
