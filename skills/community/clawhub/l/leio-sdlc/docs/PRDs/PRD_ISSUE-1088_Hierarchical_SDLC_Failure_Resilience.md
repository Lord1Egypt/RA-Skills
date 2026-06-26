---
Affected_Projects: [leio-sdlc]
Status: Implemented
Date: 2026-04-09
---

# PRD: ISSUE-1088_Hierarchical_SDLC_Failure_Resilience

## 1. Context & Problem (业务背景与核心痛点)
当前 leio-sdlc 引擎在 PR 生成和重试机制上存在设计缺陷：
1. **Planner 模板失控**：PR 合约头部（如 `status: open`）由 Planner Agent 全量生成，导致头部信息经常缺失，产生流水线空转。
2. **重试机制单一**：无论失败原因，系统均采取“硬重置 + 丢弃会话”的策略，摧毁了 Coder 的增量工作成果。

## 2. Requirements & User Stories (需求定义)
1. **Scaffold-then-Fill (初始化即契约)**：Planner 思考完切分方案后，第一步动作必须是调用脚本 Scaffold 出所有 PR 骨架文件，然后再逐个填充内容。
2. **四级路径防御体系 (Four-Path Resilience)**：
   - **Green**: 直接过审合并。
   - **Yellow (增量)**: Review 失败但次数 < N -> 在原 Session 增量修改，**不准** Reset。
   - **Red (换人)**: 连续 N 次 Yellow 失败 -> 执行 `git reset --hard` 并**强制更换 Session ID**，模拟“换个新人重写”。
   - **Black (熔断)**: 连续 M 次 Red 失败 -> 任务打回 Planner 二次切分。
3. **参数化控制**：N 和 M 在 `config/sdlc_config.json` 中可调，且部署不丢失。

## 3. Architecture & Technical Strategy (架构设计与技术路线)
### 3.1 状态机重构 (orchestrator.py)
- **存量清理 (Blast Radius Control)**: 状态机启动时，强制扫描并物理删除工作区所有的 `.coder_session` 文件，彻底解决旧格式会话导致的逻辑崩溃风险。
- **重试逻辑**: 引入 `yellow_counter` 和 `red_counter`。
- **异常收编**: 将“超时 (Timeout)”与“仲裁失败”统一映射为 Red Path 的一次失败。

### 3.2 模板生成
- **create_pr_contract.py**: 新增 `--only-scaffold` 模式，由脚本根据 `TEMPLATES/PR_Contract.md.template` 物理创建带有标准头部的 PR 文件并返回路径。

### 3.3 部署保护
- **Hot Preservation**: `deploy.sh` 在执行目录交换前，备份现有的 `config/sdlc_config.json` 并在交换后迁回。

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: 物理模板强绑定**
  - **Then** PR 文件的第一行必须是 `status: open`，Planner 无法通过 `write` 抹除初始化脚本生成的头部。
- **Scenario 2: 会话延续性**
  - **Given** Yellow Path 触发。
  - **Then** 之前的代码修改必须保留，且 Session ID 不变。
- **Scenario 3: 物理换人**
  - **Given** 触发 Red Path。
  - **Then** 必须观察到 `git reset --hard` 被执行，且后续 Coder 调用的 Session ID 发生了变更。

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **专项测试**: `scripts/e2e/e2e_test_hierarchical_resilience.sh`
- **压力测试**: 模拟 $M \times N$ 次连续失败，验证状态机能精准按路径演进。

## 6. Framework Modifications
- `scripts/orchestrator.py`
- `scripts/spawn_coder.py`
- `scripts/create_pr_contract.py`
- `deploy.sh`
- `config/prompts.json`
- `config/sdlc_config.json.template`

## 7. Hardcoded Content (必须排在第七章以通过审计脚本检测)
为了防止 Agent 幻觉，以下核心状态字符串和消息模板必须严格遵守：
- **参数名**: `YELLOW_RETRY_LIMIT`, `RED_RETRY_LIMIT`
- **Fallback 默认值**: N=3, M=2
- **PR 状态**: `status: open`, `status: in_progress`, `status: closed`, `status: superseded`
- **Review 判定**: `APPROVED`, `ACTION_REQUIRED`
- **路径标识**: `Green Path`, `Yellow Path`, `Red Path`, `Black Path`
- **错误代码**: `[FATAL_ESCALATION]`, `[DEAD_END]`
- **Planner 占位符**: `# PR-[ID]: [Title]`

## 8. Rollback Plan (回滚计划)
- **物理回滚**: 若新版状态机导致死锁或异常，管理员需手动执行：
  `bash scripts/rollback.sh`
- **机制**: 该脚本将调用 `deploy.sh` 自动生成的物理备份，将 `~/.openclaw/skills/leio-sdlc` 恢复至升级前的原子快照。

---

## Appendix: Architecture Evolution Trace
- **v1.0-v8.0**: 响应 Boss 需求与审计反馈，完善防御路径、配置保护与章节规范。
- **v9.0 Revision Rationale**: 严格遵循审计脚本对“第七章必须是 Hardcoded Content”的物理位置要求，将回滚计划移至第八章。
