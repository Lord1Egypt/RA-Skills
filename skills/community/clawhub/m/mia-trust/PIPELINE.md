# MIA Pipeline 使用指南

## 完整流程

```
用户问题 → guard_blocked → Planner → evaluate_plan → 执行 → 双记忆存储
```

## Step 1: guard_blocked (问题预检) - 必需第一步

```bash
node trust/mia-trust.mjs guard_blocked '{"query":"你的问题"}'
```

**检查流程：**
1. 正则快扫 → 检测明显威胁模式
2. LLM 深度分析 → 6维度安全判断
3. 经验检索 → 借鉴历史方案

**输出：**
- `blocked: true` → 停止，返回错误 ❌
- `blocked: false` → 进入 Step 2 ✅

---

## Step 2: Planner (计划生成)

```bash
node planner/mia-planner.mjs "你的问题"
# 或带参考
node planner/mia-planner.mjs "你的问题" --reference "历史计划"
```

**输出：**
```json
{
  "question": "问题",
  "plan": "计划描述",
  "steps": ["步骤1", "步骤2", ...],
  "reference_used": true/false
}
```

---

## Step 3: evaluate_plan (计划审查) - 必需

```bash
node trust/mia-trust.mjs evaluate_plan '{"query":"问题","plan_draft":"计划","memories":[]}'
```

**检查流程：**
1. 先执行 guard_blocked
2. 计划风险审查（最多 3 轮）
3. 发现风险 → 自动修复 → 下一轮
4. 经验检索 → 借鉴历史
5. 经验蒸馏 → 存入记忆

**输出：**
- `safe: false` → 停止 ❌
- `safe: true` → 返回 final_plan，可执行 ✅

**重要改进：**
- ❌ 不通过应直接停止（不是自动修复后通过）
- ⚠️ 自动修复后应询问用户确认

---

## Step 4: 执行计划

按照 `final_plan` 中的步骤逐一执行。

---

## Step 5: 双记忆存储

| 记忆库 | 文件 | 内容 |
|--------|------|------|
| **Memory** | `memory/memory.jsonl` | question, plan, execution, final_answer |
| **Trust** | `trust/trust_experience.json` | query, passed, iterations, distilled_experience, keywords |

---

## 快速使用脚本

```bash
#!/bin/bash
# mia-workflow.sh - 一键执行完整流程

export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=
export MIA_PLANNER_URL=
export MIA_PLANNER_MODEL=

QUESTION="$1"

echo "=== Step 1: guard_blocked ==="
RESULT=$(node trust/mia-trust.mjs guard_blocked "{\"query\":\"$QUESTION\"}")
echo "$RESULT"

BLOCKED=$(echo "$RESULT" | jq -r '.blocked')
if [ "$BLOCKED" = "true" ]; then
    echo "❌ 被拦截，停止执行"
    exit 1
fi

echo "=== Step 2: Planner ==="
PLAN=$(node planner/mia-planner.mjs "$QUESTION")
echo "$PLAN"

echo "=== Step 3: evaluate_plan ==="
QUESTION_ESCAPED=$(echo "$QUESTION" | jq -Rs .)
PLAN_ESCAPED=$(echo "$PLAN" | jq -Rs .)
RESULT2=$(node trust/mia-trust.mjs evaluate_plan "{\"query\":$QUESTION_ESCAPED,\"plan_draft\":$PLAN_ESCAPED,\"memories\":[]}")
echo "$RESULT2"

SAFE=$(echo "$RESULT2" | jq -r '.safe')
if [ "$SAFE" = "true" ]; then
    echo "✅ 计划通过，可执行"
    echo "$RESULT2" | jq -r '.final_plan'
else
    echo "❌ 计划未通过，停止执行"
    exit 1
fi
```

---

## 环境变量

```bash
export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=your-api-key
export MIA_PLANNER_URL=https://your-api-endpoint/v1/chat/completions
export MIA_PLANNER_MODEL=your-model

export MIA_MEMORY_FILE=memory/memory.jsonl
export MIA_SIMILARITY_THRESHOLD=0.90
export MIA_FEEDBACK_FILE=feedback/feedback.jsonl

export MIA_TRUST_MODE=api
export MIA_TRUST_URL=https://your-api-endpoint/v1/chat/completions
export MIA_TRUST_MODEL=your-model
export MIA_TRUST_API_KEY=your-api-key
export MIA_TRUST_EXPERIENCE_FILE=trust/trust_experience.json
```

---

## 反馈收集

```bash
# 存储反馈
node feedback/mia-feedback.mjs store "问题" "答案" "good/bad"

# 查看反馈
node feedback/mia-feedback.mjs list 10
```