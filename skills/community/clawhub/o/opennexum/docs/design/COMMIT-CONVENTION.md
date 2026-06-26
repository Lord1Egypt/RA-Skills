# Commit 规范

> OpenNexum 系统 Commit 行为规范，所有 generator/evaluator 执行的提交均遵循此规范。

---

## 1. 核心原则

**每次任务完成后即时 Commit + Push，不攒批。**

- **原子性** — 一个 commit 对应一个独立任务变更，边界清晰
- **零成本** — AI 时代 commit 没有负担，每次任务结束秒级自动完成
- **及时备份** — 代码即时推送远端，不依赖本地磁盘
- **冲突极少** — 小步提交只涉及 scope 内文件，冲突概率极低
- **可 revert** — 每个任务独立 commit，出问题直接 `git revert <hash>`

---

## 2. Commit Message 格式

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <taskId>: <description>
```

### 示例

```
feat(INFRA-001): INFRA-001: project scaffold and Polymarket Client wrapper
fix(CLI-042): CLI-042: fix eval status transition logic
refactor(NX-007): NX-007: refactor spawn module to async/await
docs(README): README: update deployment docs
chore(CI): CI: add GitHub Actions workflow
```

> **重要：** commit message 必须使用英文。task name 为中文时，generator 自动生成英文摘要（从 taskId 推导）。

---

## 3. 字段说明

| 字段 | 含义 | 来源 | 示例 |
|------|------|------|------|
| `type` | 变更类型 | 从 task name 关键词自动推断 | `feat` |
| `scope` | 变更范围 | contract 文件名（task ID 大写） | `INFRA-001` |
| `taskId` | 任务编号 | task.id | `INFRA-001` |
| `description` | 简短英文描述 | contract.name（ASCII）或 taskId 推导的 slug | `project-scaffold` |

> 注意：`scope` 和 `taskId` 通常一致，冗余保留是为了让 commit 在日志中可直接搜索任务 ID。

---

## 4. Type 类型及判断规则

| Type | 含义 | 触发关键词（task name 包含） |
|------|------|-------------------------------|
| `feat` | 新功能（默认） | 无特殊关键词 |
| `fix` | Bug 修复 | fix、bug、hotfix、修复、修补 |
| `refactor` | 重构 | refactor、重构 |
| `docs` | 文档 | docs、doc、文档、readme、comment |
| `test` | 测试 | test、测试 |
| `perf` | 性能优化 | perf、性能、optimize、优化 |
| `ci` | CI/CD 配置 | ci、cd、pipeline、github |
| `chore` | 杂务/配置 | chore、杂务 |

**默认 `feat`**：大多数 coding 任务都是新功能，未匹配到关键词时自动使用。

---

## 5. 执行时机与流程

### 触发时机

generator 完成任务后，在调用 `nexum callback <taskId>` **之前**，执行 `{{GIT_COMMIT_CMD}}`。

### 完整执行顺序

```bash
# 1. generator 完成全部实现
# 2. 执行（由 nexum spawn 生成注入 prompt）：
git add -- <scope.files>
git commit -m "<type>(<SCOPE>): <taskId>: <description>"
git push -u origin HEAD
# 3. 任务完成，调用：
nexum callback <taskId>
# → 更新 status → generator_done
# → 发 OpenClaw 通知并触发后续编排
```

### 无变更处理

如果 scope 文件无实际变更，git commit 会失败（nothing to commit），generator 应在 Field Report 中说明原因。

---

## 6. 冲突处理

- **原则：用 `git revert` 解决，不手动 merge**
- 冲突极少发生（每次只动 scope 内文件）
- 一旦发生：`git revert <conflicting-commit-hash>` 回滚单次 commit，成本极低
- 不用担心"revert 多不多"——AI 时代 commit 和 revert 都是零成本操作

---

## 7. 分支策略

- 默认直接 push 到 `main`（单人/小团队，无 PR review）
- 多人协作时由项目 `nexum init` 时配置分支策略
- `git push -u origin HEAD` 自动设置 upstream，首次 push 无需额外配置
