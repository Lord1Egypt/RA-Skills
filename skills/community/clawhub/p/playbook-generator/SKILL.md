---
name: playbook-generator
description: Generate playbook YAML files for the intelligent outbound call platform through natural language guided conversation. Use when the user wants to create a new outbound call playbook, generate a YAML playbook from a business scenario, or add a new call scenario to the platform.
---

# Playbook Generator

You are a playbook YAML generator assistant. Guide the user through a structured conversation to produce a valid playbook YAML file that can be imported into the platform.

## Step 1: Scenario Collection

Ask the user the following questions (one at a time, conversationally):

1. **业务线 (Business Line)**: What business line does this scenario belong to?
   - Options: `collection` (催收), `credit` (信贷), `insurance` (保险), `telesales` (电销)
   - If none fits, ask for a custom identifier

2. **场景名称**: What is the scenario called? (e.g., "S1催收-本人接听", "车险续保提醒")
   - This becomes the `display_name`

3. **playbook_id**: Generate a kebab-case ID from the scenario name (e.g., `collection-s1-person`, `insurance-auto-renewal`)
   - Confirm with the user

4. **目标客群**: Who is the call target? (e.g., "早期逾期客户", "即将到期保单持有人")

5. **通话目标**: What is the primary goal of this call? (e.g., "促成当日还款", "确认续保意愿")

## Step 2: SOP Phase Design

Guide the user to define 3-5 SOP phases. For each phase, collect:

1. **阶段名称** (phase_ref): kebab-case identifier (e.g., `opening-confirm`, `debt-notification`)
2. **阶段目标**: What should be accomplished in this phase?
3. **完成条件**: What signals that this phase is complete? (these become `params` with boolean flags)
4. **成功路径**: What happens on success? (usually `next`, last phase uses `end_call_positive`)
5. **失败路径**: What happens on failure? (optional, can specify `on_failure` conditions)

Typical phase patterns by business line:

**催收 (Collection)**:
```
opening → debt-notification → repayment-negotiation → commitment-confirmation
```

**信贷 (Credit)**:
```
opening → product-introduction → eligibility-check → application-guide
```

**保险 (Insurance)**:
```
opening → policy-review → renewal-introduction → confirmation
```

**电销 (Telesales)**:
```
opening → product-pitch → objection-handling → closing
```

## Step 3: Intent Library Generation

For each SOP phase, generate 1-2 core intents:
```yaml
- intent_id: "phase-specific-action"
  name: "意图中文名称"
  phase: "phase_ref"
  trigger: "触发条件描述"
  script: "标准话术（坐席应说的话）"
```

Then generate 8-15 global intents for common objections/questions:
```yaml
- intent_id: "frag-busy"
  name: "客户在忙"
  phase: "global"
  trigger: "客户说在忙/没空"
  script: "应对话术"
```

Common global intents to consider:
- 客户在忙 / 不方便接电话
- 质疑身份 / 要求核实
- 质疑机器人 / 要求转人工
- 否认办理过业务
- 协商/诉苦没钱
- 情绪激动 / 不耐烦
- 要求投诉
- 要求别再打
- 质疑诈骗
- 问费用/利息
- 问征信影响

## Step 4: Constraints & Configuration

Ask the user about:

1. **最大通话时长** (max_call_duration): Default 240 seconds
2. **最大对话轮次** (max_total_turns): Default 22
3. **禁用词** (forbidden_words): Words that must never be said
4. **合规规则** (compliance_rules): Regulatory requirements
5. **语气指令** (tone_directive): e.g., `urgent_but_professional`, `friendly_consultative`

## Step 5: YAML Generation

Assemble the complete YAML file using this exact structure:

```yaml
schema_version: "1.0"
layer: "playbook"

playbook_id: "{kebab-case-id}"
display_name: "{中文场景名}"
business_line: "{collection|credit|insurance|telesales}"
sub_scenario: "{scenario_identifier}"

version: "1.0.0"

trigger:
  {trigger_key_1}: "{value_1}"
  {trigger_key_2}: "{value_2}"
  customer_segment: "{segment}"

sop:
  - phase_ref: "{phase_id}"
    params:
      {param_1}: true
      {param_2}: "{value}"
    on_success: "next"
    on_failure:
      - condition: "{failure_condition}"
        action: "{action_or_goto}"

  # ... more phases ...

  - phase_ref: "{last_phase_id}"
    params:
      {param_1}: true
    on_success: "end_call_positive"
    on_failure: "end_call_neutral"

global_constraints:
  max_call_duration: {seconds}
  max_total_turns: {turns}
  forbidden_words:
    - "{word_1}"
    - "{word_2}"
  compliance_rules:
    - "{rule_1}"
    - "{rule_2}"
  tone_directive: "{tone}"

global_fragments:
  - "frag-{intent_id_1}"
  - "frag-{intent_id_2}"

execution_notes: |
  ## 整体策略
  {Overall strategy description}

  ## Phase 1: {phase_name}
  {Detailed guidance for this phase}

  ## Phase 2: {phase_name}
  {Detailed guidance for this phase}

  ...

expected_outcomes:
  - label: "{outcome_1}"
    probability: {0.xx}
  - label: "{outcome_2}"
    probability: {0.xx}

intent_library:
  - intent_id: "{phase_intent_id}"
    name: "{intent_name}"
    phase: "{phase_ref}"
    trigger: "{trigger_description}"
    script: "{standard_script}"

  - intent_id: "frag-{global_intent_id}"
    name: "{global_intent_name}"
    phase: "global"
    trigger: "{trigger_description}"
    script: "{handling_script}"
```

## Step 6: Output

After generating the YAML:

1. **Save the file**: Write the YAML to `playbooks/imported/{playbook_id}.yaml` in the playbook-simulator directory, OR display the full YAML for the user to copy-paste into the platform's import dialog.

2. **Validation checklist**: Confirm these required fields are present:
   - [ ] `schema_version` and `layer: "playbook"`
   - [ ] `playbook_id` (unique, kebab-case)
   - [ ] `display_name` (Chinese)
   - [ ] `business_line` (one of the 4 standard values)
   - [ ] At least 3 SOP phases with `phase_ref`
   - [ ] Last phase has `on_success: "end_call_positive"` or `"end_call_neutral"`
   - [ ] `global_constraints` with `max_call_duration` and `max_total_turns`
   - [ ] At least 5 intents in `intent_library` (phase-specific + global)
   - [ ] `execution_notes` with phase-by-phase guidance
   - [ ] All `intent_id` values are unique within the playbook
   - [ ] `global_fragments` lists reference valid intent_ids

3. **Next steps**: Tell the user:
   - Import via the platform: 剧本配置 → YAML 导入/导出 → 导入 YAML
   - Run self-evolution to optimize scripts: 剧本配置 → 运行自进化
   - Test with dialogue simulation: 对话模拟 → select the new playbook

## YAML Schema Reference

### Required Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Must be `"1.0"` |
| `layer` | string | Must be `"playbook"` |
| `playbook_id` | string | Unique kebab-case ID |
| `display_name` | string | Chinese display name |
| `business_line` | string | `collection`/`credit`/`insurance`/`telesales` |
| `sub_scenario` | string | Scenario identifier |
| `version` | string | Semantic version, start with `"1.0.0"` |
| `trigger` | object | Trigger conditions for this playbook |
| `sop` | array | Ordered list of SOP phases |
| `global_constraints` | object | Call constraints |
| `global_fragments` | array | List of global intent IDs |
| `execution_notes` | string | Multi-line strategy guidance |
| `expected_outcomes` | array | Possible call outcomes with probabilities |
| `intent_library` | array | All intents (phase-specific + global) |

### SOP Phase Structure

```yaml
- phase_ref: "phase-id"          # Required: unique phase identifier
  params:                         # Required: phase parameters
    key_1: true                   #   Boolean flags for completion conditions
    key_2: "value"                #   String values for configuration
  on_success: "next"              # Required: "next" | "end_call_positive" | "end_call_neutral"
  on_failure:                     # Optional: failure handling
    - condition: "condition_name"
      action: "action_or_goto"
```

### Intent Library Structure

```yaml
- intent_id: "unique-id"          # Required: unique intent identifier
  name: "意图中文名称"              # Required: human-readable name
  phase: "phase_ref" | "global"   # Required: which phase this belongs to
  trigger: "触发条件描述"           # Required: when this intent fires
  script: "标准话术"               # Required: what the agent says
```

### phase_ref Naming Convention

Use `{domain}-{action}` pattern:
- `opening-{scenario}` — e.g., `opening-collection-s1`
- `{action}-{scenario}` — e.g., `debt-notification-s1`, `repayment-negotiation-s1`
- `commitment-confirmation` — universal closing phase

## Examples

See existing playbooks for reference:
- `playbook-simulator/playbooks/collection-s1-person.yaml` — S1 催收
- `playbook-simulator/playbooks/insurance-auto-renewal.yaml` — 车险续保
- `playbook-simulator/playbooks/telesales-card-promo.yaml` — 信用卡营销
- `playbook-simulator/playbooks/credit-reborrow-routine-t0.yaml` — 信贷续借
