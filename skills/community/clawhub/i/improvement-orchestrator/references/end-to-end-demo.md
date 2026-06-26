# End-to-End Demo — generic-skill lane 完整示例

**版本**: v0.1  
**状态**: 基于 first runnable version 的真实执行记录

---

## 概述

本文档演示 `generic-skill` lane 一次完整的四角色流程：

```
Proposer → Critic → Executor → Gate
```

包含每一步的输入/输出样例、artifact 路径、以及不同 gate 决策的差异。

---

## 场景设定

**目标**: 对 `newsletter-creation-curation` skill 进行自动改进

**输入来源**: 用户反馈文件 `$OPENCLAW_ROOT/shared-context/intel/auto-improvement/demo-feedback/newsletter-creation-curation-demo.feedback.md`

**反馈内容摘要**:
- 缺少行业特定模板
- 没有自动化工作流示例
- 需要添加 cadence 建议

---

## Step 1: Proposer

### 执行命令

```bash
python scripts/propose_candidate.py \
  --target $OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation \
  --source $OPENCLAW_ROOT/shared-context/intel/auto-improvement/demo-feedback/newsletter-creation-curation-demo.feedback.md
```

### 输入

**目标路径**: `$OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation`

**反馈来源**:
```markdown
# 用户反馈

## 问题
1. 缺少行业特定模板（科技/金融/教育）
2. 没有自动化工作流示例
3. 需要添加 cadence 建议

## 期望
- 增加 3 个行业模板
- 补充 Zapier/Make/n8n 集成示例
- 添加发布频率建议
```

### 输出（Candidate Artifact）

**路径**: `$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/candidate_versions/run-20260401-143022.json`

**内容示例**:
```json
{
  "run_id": "run-20260401-143022",
  "timestamp": "2026-04-01T14:30:22+08:00",
  "stage": "proposer_complete",
  "status": "success",
  "next_step": "critic",
  "next_owner": "run_critic.py",
  "truth_anchor": {
    "target_path": "$OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation",
    "source_path": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/demo-feedback/newsletter-creation-curation-demo.feedback.md"
  },
  "candidates": [
    {
      "id": "cand-001",
      "title": "添加行业特定模板章节",
      "target_path": "$OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation/SKILL.md",
      "category": "reference",
      "rationale": "用户反馈缺少行业模板，补充后可提升技能实用性",
      "risk_level": "low",
      "proposed_change_summary": "在 SKILL.md 中新增'行业模板'章节，包含科技/金融/教育三个行业的 newsletter 模板示例",
      "change_type": "append_markdown_section",
      "section_title": "## 行业模板示例",
      "section_content": "..."
    },
    {
      "id": "cand-002",
      "title": "补充自动化工作流集成",
      "target_path": "$OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation/references/workflows.md",
      "category": "reference",
      "rationale": "用户需要 Zapier/Make/n8n 集成示例",
      "risk_level": "low",
      "proposed_change_summary": "新增 workflows.md 文件，描述三种自动化工具的集成步骤",
      "change_type": "create_file",
      "file_content": "..."
    },
    {
      "id": "cand-003",
      "title": "添加发布频率建议",
      "target_path": "$OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation/SKILL.md",
      "category": "docs",
      "rationale": "用户需要 cadence 建议",
      "risk_level": "low",
      "proposed_change_summary": "在 SKILL.md 中新增'发布频率建议'章节",
      "change_type": "append_markdown_section",
      "section_title": "## 发布频率建议",
      "section_content": "..."
    }
  ]
}
```

---

## Step 2: Critic

### 执行命令

```bash
python scripts/run_critic.py \
  --input $OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/candidate_versions/run-20260401-143022.json \
  --use-evaluator-evidence
```

### 输入

读取上一步生成的 candidate artifact。

### 输出（Ranking Artifact）

**路径**: `$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/rankings/run-20260401-143022.json`

**内容示例**:
```json
{
  "run_id": "run-20260401-143022",
  "timestamp": "2026-04-01T14:31:45+08:00",
  "stage": "critic_complete",
  "status": "success",
  "next_step": "executor",
  "next_owner": "run_executor.py",
  "critic_mode": "rubric_assisted",
  "ranked_candidates": [
    {
      "id": "cand-001",
      "rank": 1,
      "score": 0.85,
      "score_components": {
        "evaluator_score": 0.88,
        "heuristic_score": 0.82,
        "final_score": 0.85
      },
      "evaluator_evidence": {
        "rubric": {"clarity": 0.3, "correctness": 0.4, "maintainability": 0.3},
        "category": "reference",
        "boundary": "low_risk",
        "test_tracks": [],
        "limitations": ["未运行 frozen benchmark", "未执行 hidden tests"]
      },
      "risk_penalty": 0.0,
      "recommendation": "accept_for_execution",
      "reasoning": "低风险文档类修改，直接解决用户反馈的核心问题"
    },
    {
      "id": "cand-002",
      "rank": 2,
      "score": 0.78,
      "score_components": {
        "evaluator_score": 0.80,
        "heuristic_score": 0.76,
        "final_score": 0.78
      },
      "evaluator_evidence": {
        "rubric": {"clarity": 0.3, "correctness": 0.4, "maintainability": 0.3},
        "category": "reference",
        "boundary": "low_risk",
        "test_tracks": [],
        "limitations": ["未运行 frozen benchmark", "未执行 hidden tests"]
      },
      "risk_penalty": 0.0,
      "recommendation": "accept_for_execution",
      "reasoning": "创建新文件，低风险，补充工作流示例"
    },
    {
      "id": "cand-003",
      "rank": 3,
      "score": 0.72,
      "score_components": {
        "evaluator_score": 0.75,
        "heuristic_score": 0.69,
        "final_score": 0.72
      },
      "evaluator_evidence": {
        "rubric": {"clarity": 0.3, "correctness": 0.4, "maintainability": 0.3},
        "category": "docs",
        "boundary": "low_risk",
        "test_tracks": [],
        "limitations": ["未运行 frozen benchmark", "未执行 hidden tests"]
      },
      "risk_penalty": 0.0,
      "recommendation": "hold",
      "reasoning": "有价值但优先级较低，建议先完成前两个候选"
    }
  ]
}
```

---

## Step 3: Executor

### 执行命令

```bash
python scripts/run_executor.py \
  --input $OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/rankings/run-20260401-143022.json \
  --candidate-id cand-001
```

### 输入

读取 ranking artifact 和指定的 candidate ID。

### 输出（Execution Artifact）

**路径**: `$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/executions/run-20260401-143022-cand-001.json`

**内容示例**:
```json
{
  "run_id": "run-20260401-143022",
  "candidate_id": "cand-001",
  "timestamp": "2026-04-01T14:32:30+08:00",
  "stage": "executor_complete",
  "status": "success",
  "next_step": "gate",
  "next_owner": "apply_gate.py",
  "truth_anchor": {
    "target_path": "$OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation/SKILL.md",
    "ranking_path": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/rankings/run-20260401-143022.json"
  },
  "execution_result": {
    "action": "append_markdown_section",
    "success": true,
    "changes_made": true,
    "lines_added": 25,
    "section_title": "## 行业模板示例"
  },
  "diff_summary": {
    "unified_diff": "@@ -45,6 +45,31 @@\n ...\n+## 行业模板示例\n+\n+### 科技行业\n+...\n+### 金融行业\n+...\n+### 教育行业\n+...",
    "files_modified": [
      "$OPENCLAW_ROOT/workspace/skills/newsletter-creation-curation/SKILL.md"
    ]
  },
  "backup": {
    "backup_path": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/executions/backups/run-20260401-143022/SKILL.md.bak",
    "rollback_pointer": "backup-run-20260401-143022-cand-001"
  }
}
```

---

## Step 4: Gate

### 执行命令

```bash
python scripts/apply_gate.py \
  --ranking $OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/rankings/run-20260401-143022.json \
  --execution $OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/executions/run-20260401-143022-cand-001.json
```

### 输入

读取 ranking 和 execution artifact。

### 输出（Gate Receipt）

**路径**: `$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/receipts/run-20260401-143022-cand-001-gate.json`

**内容示例（keep 决策）**:
```json
{
  "run_id": "run-20260401-143022",
  "candidate_id": "cand-001",
  "timestamp": "2026-04-01T14:33:00+08:00",
  "stage": "gate_complete",
  "status": "success",
  "decision": "keep",
  "reasoning": "低风险文档类修改，执行成功，符合 auto-keep 条件",
  "truth_anchor": {
    "ranking_path": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/rankings/run-20260401-143022.json",
    "execution_path": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/executions/run-20260401-143022-cand-001.json"
  },
  "next_step": "none",
  "next_owner": "user_or_control_plane",
  "artifact_paths": {
    "candidate": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/candidate_versions/run-20260401-143022.json",
    "ranking": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/rankings/run-20260401-143022.json",
    "execution": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/executions/run-20260401-143022-cand-001.json",
    "receipt": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/receipts/run-20260401-143022-cand-001-gate.json"
  }
}
```

---

## Gate 决策差异

### keep（保留）

**条件**:
- low-risk + docs/reference/guardrail 类别
- 执行成功
- 符合 auto-keep 策略

**结果**:
- 修改保留
- 写入 receipt
- 状态标记为 `completed`

### pending_promote（待晋升）

**条件**:
- Critic recommendation = `hold`
- 或 medium-risk 需要人工审查
- 或有价值但当前不自动执行

**结果**:
- 修改可能已应用但不自动 keep
- 写入 `state/pending_promote.json`
- 等待控制面或人工晋升

**示例**:
```json
{
  "decision": "pending_promote",
  "reasoning": "Critic 推荐 hold，值得保留但需要更强 judge 或人工确认",
  "pending_path": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/state/pending_promote.json"
}
```

### reject（否决）

**条件**:
- Critic recommendation = `reject`
- 或收益不足/风险过高
- 或未修改文件

**结果**:
- 无修改或修改已回滚
- 写入 `state/veto.json`
- 候选被否决

**示例**:
```json
{
  "decision": "reject",
  "reasoning": "收益不足，风险过高",
  "veto_path": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/state/veto.json"
}
```

### revert（回滚）

**条件**:
- Critic recommendation = `reject` 但已修改文件
- 或执行失败但产生中间状态
- 或 Gate 不允许保留已修改文件

**结果**:
- 使用 backup 恢复目标文件
- 写入 receipt 标记为 reverted
- 写入 `state/veto.json`

**示例**:
```json
{
  "decision": "revert",
  "reasoning": "Critic 拒绝但已修改文件，执行回滚",
  "rollback_used": true,
  "backup_restored": "$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/executions/backups/run-20260401-143022/SKILL.md.bak"
}
```

---

## 状态文件更新

执行完成后，以下状态文件会被更新：

### `state/current_state.json`

```json
{
  "last_run_id": "run-20260401-143022",
  "last_update": "2026-04-01T14:33:00+08:00",
  "stage": "gate_complete",
  "status": "success",
  "lane": "generic-skill",
  "total_candidates": 3,
  "kept": 1,
  "pending": 1,
  "rejected": 1
}
```

### `state/last_run.json`

```json
{
  "run_id": "run-20260401-143022",
  "start_time": "2026-04-01T14:30:22+08:00",
  "end_time": "2026-04-01T14:33:00+08:00",
  "duration_seconds": 158,
  "artifacts_generated": 4,
  "decisions": {
    "cand-001": "keep",
    "cand-002": "pending_promote",
    "cand-003": "reject"
  }
}
```

---

## 完整文件树（执行后）

```
$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/
├── candidate_versions/
│   └── run-20260401-143022.json
├── rankings/
│   └── run-20260401-143022.json
├── executions/
│   ├── run-20260401-143022-cand-001.json
│   └── backups/
│       └── run-20260401-143022/
│           └── SKILL.md.bak
├── receipts/
│   └── run-20260401-143022-cand-001-gate.json
└── state/
    ├── current_state.json
    ├── pending_promote.json
    ├── veto.json
    └── last_run.json
```

---

## 注意事项

1. **所有 artifact 都是 machine-readable**
   - 控制面可直接解析 JSON
   - 不依赖聊天记录

2. **truth_anchor 字段**
   - 每个 artifact 都包含关键路径引用
   - 便于追溯和调试

3. **next_step / next_owner**
   - 明确下一步动作和执行者
   - 支持控制面自动推进

4. **保守策略**
   - 当前仅 auto-keep 低风险文档修改
   - 其他候选进入 pending/reject
