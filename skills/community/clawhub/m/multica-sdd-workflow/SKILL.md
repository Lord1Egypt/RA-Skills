---
name: multica-sdd-workflow
description: >
  SDD + Multica 多智能体开发工作流。当用户提到"新建任务"、"发布给 multica"、"创建小队"、
  "分配 issue"、"开始新功能"、"组建小队执行"、"按 SDD 流程"、"新增功能"、"功能更新"时触发。
  覆盖从 SDD 规范文档编写、multica 小队创建、Issue 发布执行，到完成后记录归档的完整流程。
version: 2.0.0
user-invocable: true
tools: Read, Glob, Grep, Bash
---

# Multica SDD 工作流

每次新增或更新功能，必须留有完整的 SDD 记录。流程如下：

```
0. 编写 SDD 规范文档（开工前必须）
       ↓
1. 读取项目配置 + 确认小队
       ↓
2. 创建父 Issue + 子 Issue + Leader Kickoff
       ↓
3. 依赖链规划
       ↓
4. 监控进度
       ↓
5. 完成后更新 SDD 记录（收尾必须）
```

---

## Step 0：编写 SDD 规范文档（开工前必须）

> **宪法 Article II § 2.2（API First）+ Article IX § 9.2（Required Documentation）**
>
> 任何功能，必须先写规范文档，再创建 Issue，再执行。

### 0.0 模式判断

检测 `specs/` 是否已有规范文档：

- **无 `specs/` 目录** → 进入 **0-A 新建模式**
- **已有 `specs/` 目录** → 进入 **0-B 续接模式**

---

### 0-B 续接模式

> **目标**：不重写已有规范，只补全缺失信息，确保任何 agent 能直接接手。

**1. 扫描未完成任务**：读取所有 `specs/*/tasks.md`，统计 `[ ]` 条目，了解当前进度。

**2. 补全格式缺口**：对每个未完成的 Task，确认它有 `Steps` 和 `Acceptance Criteria`。缺失的就地补全，不新建文件。格式要求见下方 0-A 的 tasks.md 规范。

**3. 更新 CLAUDE.md**：将「下一步行动」章节精确同步到当前未完成任务，按依赖顺序列出，标注 TDD 阶段（RED/GREEN）和目标文件路径。

> 完成后直接进入 Step 1，基于现有 specs 继续创建 Issue。`tasks.md` 和 `CLAUDE.md` 是唯一真相来源，无需生成额外文档。

---

### 0-A 新建模式：编写全新规范

### 文档目录结构

```
specs/
└── <NNN>-<feature-name>/     # NNN 三位数字序号，如 002-ipc-handlers
    ├── spec.md               # 需求规范
    ├── plan.md               # 技术方案
    └── tasks.md              # 任务清单
```

三个文档的格式规范见 [sdd-templates.md](sdd-templates.md)。

---

## Step 1：读取项目配置

**在执行任何后续步骤前，必须先从 `.multica/squad.md` 读取配置。**

```bash
PROJECT_ID=$(grep '| project-id'       .multica/squad.md | cut -d'`' -f2)
SQUAD_ID=$(grep '| squad-id'           .multica/squad.md | cut -d'`' -f2)
LEADER_ID=$(grep '| leader-id'         .multica/squad.md | cut -d'`' -f2)
EXECUTOR_ID=$(grep '| executor-id'     .multica/squad.md | cut -d'`' -f2)
EXECUTOR_NAME=$(grep '| executor-name' .multica/squad.md | cut -d'`' -f2)
WORK_DIR=$(grep '| work-dir'           .multica/squad.md | cut -d'`' -f2)
TEST_CMD=$(grep '| test-cmd'           .multica/squad.md | cut -d'`' -f2)
TYPECHECK_CMD=$(grep '| typecheck-cmd' .multica/squad.md | cut -d'`' -f2)

# 验证——任何变量为空说明 squad.md 格式有误
echo "PROJECT_ID:    $PROJECT_ID"
echo "SQUAD_ID:      $SQUAD_ID"
echo "LEADER_ID:     $LEADER_ID"
echo "EXECUTOR_ID:   $EXECUTOR_ID"
echo "EXECUTOR_NAME: $EXECUTOR_NAME"
echo "WORK_DIR:      $WORK_DIR"
echo "TEST_CMD:      $TEST_CMD"
echo "TYPECHECK_CMD: $TYPECHECK_CMD"
```

### 确认小队在线

```bash
multica agent list --output json | grep -E '"name"|"status"'
multica squad list --output json
```

### 新项目初始化（首次使用时）

如果项目尚未有小队，执行以下步骤一次性配置：

```bash
# 1. 在 multica 创建项目
multica project create --name "<项目名>" --output json
# 记录返回的 project-id → 填入 .multica/squad.md

# 2. 创建小队
multica squad create --name "<squad-name>" --description "<desc>" \
  --leader "$LEADER_ID" --output json
# 记录返回的 squad-id → 填入 .multica/squad.md

# 3. 添加执行 agent 到小队
multica squad member add "$SQUAD_ID" --member-id "$EXECUTOR_ID" --role member
```

`.multica/squad.md` 配置表格式（8 个字段，字段名固定）：

```markdown
| 字段 | 值 |
|------|---|
| project-id    | `<multica-project-uuid>` |
| squad-id      | `<multica-squad-uuid>` |
| leader-id     | `<leader-agent-uuid>` |
| executor-id   | `<executor-agent-uuid>` |
| executor-name | `<EXECUTOR-AGENT-NAME>` |
| work-dir      | `<项目绝对路径>` |
| test-cmd      | `<测试命令，如 npm test>` |
| typecheck-cmd | `<类型检查命令，如 npm run typecheck>` |
```

---

## Step 2：创建 Issue

### 2.1 父 Issue（Phase 级别）

```bash
multica issue create \
  --project "$PROJECT_ID" \
  --title "Phase N: <阶段名>（Tasks N.1-N.M）" \
  --description-file /tmp/phase_desc.txt \
  --assignee-id "$SQUAD_ID" \
  --priority high \
  --output json
```

父 Issue、子 Issue、Leader Kickoff 三个 description 模板见 [issue-templates.md](issue-templates.md)。

---

## Step 3：依赖链规划

根据 tasks.md 中的 Dependencies 字段，将任务分批派发：

```
无依赖任务 → 第1批并行
    ↓（第1批全部 in_review 或 done 后触发）
依赖第1批的任务 → 第2批并行
    ↓
汇总任务（集成测试、公共 API 导出等）→ 最后单独一批
```

**示例**：Phase N 有 6 个子 Issue：

```
WS-01（Task N.1 RED,  无依赖）  ─┐
WS-02（Task N.3 RED,  无依赖）   ├─ 第1批并行派发
WS-03（Task N.5 RED,  无依赖）  ─┘
         ↓
WS-04（Task N.2 GREEN, 依赖 WS-01）─┐
WS-05（Task N.4 GREEN, 依赖 WS-02）  ├─ 第2批并行派发
WS-06（Task N.6 GREEN, 依赖 WS-03）─┘
         ↓
WS-07（集成测试, 依赖 WS-04~06）────── 第3批（单独）
```

划分规则：
- RED 任务（写测试）先于其对应的 GREEN 任务（写实现）派发
- 多个互不依赖的任务同批并行
- 有多个前置依赖的任务，等所有前置均达到 `in_review` 或 `done` 后再派

---

## Step 4：监控进度

```bash
# 先加载配置（新 shell 时）
PROJECT_ID=$(grep '| project-id' .multica/squad.md | cut -d'`' -f2)
LEADER_ID=$(grep '| leader-id'   .multica/squad.md | cut -d'`' -f2)

# 查看所有 Issue 状态
multica issue list --project "$PROJECT_ID" --output json \
  | grep -E '"identifier"|"title"|"status"'

# 查看单个 Issue
multica issue get <WS-XX>

# Leader 无响应时重新触发
multica issue assign <kickoff-id> --to "$LEADER_ID"
```

状态流转：`todo` → `in_progress` → `in_review` → `done`

---

## Step 5：完成后更新 SDD 记录（收尾必须）

> **宪法 Article IX § 9.1（Living Documentation）+ Article XI § 11.1（Git Workflow）**
>
> Phase 完成后，必须同步更新以下记录，再提交。

### 5.1 更新 tasks.md

将完成的任务 checkbox 从 `[ ]` 改为 `[x]`，并统计完成情况：

```bash
# 确认还有哪些未完成
grep -n "\[ \]" specs/<NNN>-<feature>/tasks.md

# 统计完成进度
DONE_COUNT=$(grep -c "\[x\]" specs/<NNN>-<feature>/tasks.md)
TOTAL_COUNT=$(grep -c "^### Task" specs/<NNN>-<feature>/tasks.md)
echo "完成进度: $DONE_COUNT / $TOTAL_COUNT"
```

### 5.2 更新 CLAUDE.md 进度

```markdown
## 开发进度

**总进度**: <已完成>/<总任务> 任务完成

### Phase N: <阶段名> ✅ 完成（完成数/本阶段总数 任务）

| 任务 | 状态 | 描述 |
|------|------|------|
| N.1  | ✅   | ...  |
| N.2  | ✅   | ...  |

**已完成成果**:
- ✅ <文件或功能点>
```

CLAUDE.md 需更新的字段：
- `**项目状态**` 百分比
- `**总进度**` 任务数（从 tasks.md 动态统计，不要写死）
- 对应 Phase 的状态从 `🔄 进行中` 改为 `✅ 完成`
- `**最后更新**` 日期

### 5.3 提交记录更新

```bash
DONE_COUNT=$(grep -c "\[x\]" specs/<NNN>-<feature>/tasks.md)
TOTAL_COUNT=$(grep -c "^### Task" specs/<NNN>-<feature>/tasks.md)

git add specs/<NNN>-<feature>/tasks.md CLAUDE.md
git commit -m "docs(sdd): mark Phase N complete, update progress to ${DONE_COUNT}/${TOTAL_COUNT}"
```

### 5.4 更新 .multica/squad.md Issue 历史

在 `.multica/squad.md` 的 Issue 历史清单中追加本次新建的 Issue：

```markdown
| WS-XX | Phase N: <阶段名>（父） | — | ✅ done |
| WS-YY | Task N.X+N.Y: <功能>   | WS-XX | ✅ done |
```

---

## 关键约束（来自 AGENTS.md + 宪法）

| 约束 | 来源 |
|------|------|
| TDD：RED 先提交，GREEN 后提交 | 宪法 Article III |
| 禁止 `git push`、`git add .` | AGENTS.md |
| 提交格式：`<type>(<scope>): <desc> (Task N.X RED/GREEN)` | AGENTS.md |
| 生产依赖 ≤ 10 个 | 宪法 Article IV § 4.2 |
| TypeScript strict 零错误 | 宪法 Article V § 5.2 |
| 启动 < 2s，操作 < 100ms | 宪法 Article VI § 6.1 |
| 零网络调用 | 宪法 Article VII § 7.1 |
| 单元测试覆盖率 ≥ 80% | 宪法 Article III § 3.2 |

> **注意**：以上约束来自 memo-desktop 项目的宪法。其他项目使用此 skill 时，应根据自身 AGENTS.md 和宪法文档替换此约束表。
