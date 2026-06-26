# Issue Templates

Step 2 创建 Issue 时使用的 description 模板。

---

## 父 Issue（写入 /tmp/phase_desc.txt）

```markdown
## Phase N: <阶段名>（Tasks N.1-N.M）

### 规范文档
- spec.md: specs/<NNN>-<feature>/spec.md
- plan.md: specs/<NNN>-<feature>/plan.md
- tasks.md: specs/<NNN>-<feature>/tasks.md

### 任务清单
| 任务 | 内容 | 依赖 |
|------|------|------|
| Task N.1 RED   | <测试描述> | — |
| Task N.2 GREEN | <实现描述> | N.1 |

### 技术约束
- 工作目录：${WORK_DIR}
- <来自 CLAUDE.md / constitution.md 的项目特定约束>

### 验收标准
- 所有测试通过（${TEST_CMD}）
- TypeScript strict 无错误（${TYPECHECK_CMD}）
```

---

## 子 Issue（写入 /tmp/task_desc.txt）

```markdown
## Task N.X RED + Task N.Y GREEN：<功能名>

### 依赖
Task N.(X-2) 必须先完成（<WS-XX>）

### Task N.X RED — 测试：tests/<path>/<file>.test.ts

测试用例：
1. should <预期行为>

提交：git commit -m "test(<scope>): add <func> tests (Task N.X RED)"

### Task N.Y GREEN — 实现：src/<path>/<file>.ts

```typescript
// 关键接口签名
export function myFunc(input: Input): Output
```

提交：git commit -m "feat(<scope>): implement <func> (Task N.Y GREEN)"

### 验收标准
- [ ] 测试全部通过
- [ ] TypeScript strict 无错误
- [ ] RED 和 GREEN 分别提交
```

---

## Leader Kickoff Issue（写入 /tmp/kickoff.txt）

```markdown
## 任务目标
推进 Phase N <阶段名>，协调 ${EXECUTOR_NAME}（${EXECUTOR_ID}）完成所有子 Issue。

## 配置
- Squad ID: ${SQUAD_ID}
- Project ID: ${PROJECT_ID}
- 工作目录: ${WORK_DIR}

## 派发计划

### 第1批（立即并行派发，无依赖）
```bash
multica issue assign <WS-XX> --to ${SQUAD_ID}
multica issue assign <WS-YY> --to ${SQUAD_ID}
```

### 第2批（触发条件：第1批全部达到 `in_review` 或 `done`）
```bash
multica issue assign <WS-ZZ> --to ${SQUAD_ID}
```

## Leader 审核循环（持续执行，直到 Phase 全部完成）

每当有 Issue 进入 `in_review` 状态，执行：

```bash
# 1. 验证代码
cd ${WORK_DIR}
${TEST_CMD}           # 所有测试通过
${TYPECHECK_CMD}      # TypeScript strict 无错误

# 2. 审核通过后标记完成
multica issue update <WS-XX> --status done

# 3. 检查是否有依赖该 Issue 的下一批任务需要派发
multica issue assign <WS-YY> --to ${EXECUTOR_ID}

# 4. 当前 Phase 所有子 Issue 均为 done 后，关闭父 Issue
multica issue update <parent-WS-XX> --status done
```

## 执行约束

- TDD：RED（写测试）必须在 GREEN（写实现）之前独立提交
- ${EXECUTOR_NAME} 在每个 Issue 设为 `in_review` 后，必须立即领取下一个 `todo` Issue，不等待审核
- **本 kickoff Issue 状态约束**：
  - `in_progress`：从派发第一个 Issue 开始，保持此状态
  - `done`：仅当所有子 Issue 均为 `done` 之后才可设置
  - **严禁设为 `in_review`**：提前设为 `in_review` 会导致 review loop 终止，子 Issue 积压无人处理
```
