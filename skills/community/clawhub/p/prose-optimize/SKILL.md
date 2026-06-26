---
name: prose-optimize
description: '优化 OpenProse 文件，减少不必要的 LLM API 调用。触发：修改或编写 .prose 文件时。'
metadata: { "openclaw": { "emoji": "🧬", "requires": { "bins": ["python3", "grep"] } } }
---
# Prose Optimize — 减少 Prose 文件的 LLM Token 消耗

## When to Use

修改或编写 `.prose` 文件时，希望减少 LLM API 调用次数和 token 消耗。

## Steps

1. **审计所有 `session` 和 `agent` 语句** — 逐个标注是否需要语义理解
2. **Python 替代** — 以下场景不需要 LLM：
   - 跑脚本并返回输出
   - 条件分支（if/else）
   - JSON 解析和字段提取
   - 简单的模板渲染（JSON → 报告）
3. **Pipe 连接脚本** — 多个 Python 脚本串联用 `|`，不要中间用 LLM 包装
4. **合并 LLM 调用** — 只做数据传递的 agent 步骤可以合并：
   - analyzer + extractor → 一次调用输出两份 JSON
   - 模式分析 + SKILL.md 生成 → 一次调用输出两份
5. **用 Prose VM 原生条件** — `**if**` 替代让 LLM 判断分支，但不如纯 Python
6. **Python 统一入口** — 把分支逻辑封装到一个 Python 脚本，prose 里一行调用

## Common Pitfalls

- 变量为空时直接拼命令会导致 argparse 参数错位，需要 Python 脚本处理空值（`--topic ""` → falsy）
- 合并 agent 步骤时注意 context 依赖，合并后失去中间变量
- Prose VM 条件分支（`**if**`）仍然消耗当前 turn 的 token，不如纯 Python
- 不要为了合并而合并 — 如果两个步骤逻辑独立，分开更清晰

## Examples

**Before（2 次 LLM）:**

```prose
agent analyzer:
  prompt: "Analyze this conversation and output JSON..."
let analysis = session: analyzer
  prompt: "Analyze..."

agent extractor:
  prompt: "Extract reusable knowledge and output JSON..."
let extraction = session: extractor
  prompt: "Extract..."
  context: analysis
```

**After（1 次 LLM）:**

```prose
agent analyzer_extractor:
  prompt: |
    Read the session, analyze AND extract. Output single JSON:
    { "analysis": {...}, "extraction": {...} }
let combined = session: analyzer_extractor
  prompt: "Read, analyze, and extract:"
```

## Key Commands

```bash
# 审计 prose 文件中的 LLM 调用
grep -c "session\|agent:" my-workflow.prose

# 测试 Python 脚本 pipe
python3 ./src/script1.py --json | python3 ./src/script2.py --from-json

# 检查脚本参数处理（空值安全）
python3 ./src/collect_sessions.py --since 24h --topic "" --limit 5
```

---

_Extracted by EvoSkill_