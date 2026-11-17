---
name: optimize-prompt
description: Optimize, compress, clarify, structure, score, and audit natural-language prompts for LLMs, GPT, Claude, Gemini, AI Agents, and MCP workflows. Use for prompt optimization, prompt engineering, structured prompts, coding prompts, PRDs, research requests, security prompts, token reduction, or converting conversational requirements into agent-ready instructions. Preserve constraints and return the optimized prompt without executing the underlying task.
---

# Optimize Prompt

Transform the user's raw request into a compact natural-language prompt for a downstream Agent. Treat semantic fidelity as more important than compression. Do not execute the optimized request.

Example invocation: `Use $optimize-prompt to optimize this request without executing it: "..."`

## What the user gets

Turn this:

```text
Please help me write a SQL query for recent orders. Make it good, and don't
modify any data. Thanks.
```

Into a compact instruction like this:

```text
Generate a read-only SQL query for recent orders. Do not modify data. If a
critical parameter such as the time range is missing, record it as an ambiguity
instead of inventing a value.
```

Return the optimized prompt, an audit ledger, validation status, and educational feedback explaining what the user wrote well and what to improve next time.

Common uses include coding, PRDs, research, AI Agent instructions, MCP workflows, prompt engineering, and security reviews.

## Workflow

1. Identify the exact raw prompt the user wants optimized. If the invocation contains surrounding discussion, optimize only the clearly designated prompt.
2. Apply the pre-gate. Return the original unchanged when it is:
   - extremely short and already executable;
   - JSON, a tool/function call, or structured XML/MCP context;
   - dominated by Base64, a Data URI, or a large fenced code block.
3. Otherwise, extract an audit ledger with `actions`, `entities`, `constraints`, `outputs`, `ambiguities`, and `risk_flags`.
4. Produce a shorter natural-language prompt only by removing filler, repetition, and unnecessary structure. Never infer missing parameters or strengthen tentative language.
5. Preserve negations and their scope, permissions, numbers, dates, amounts, percentages, versions, URLs, file/function names, output format and language, attachments, quoted source data, and risk limitations.
6. Use `conservative` and return the original unchanged when ambiguity, conflict, or risky execution could make a rewrite misleading.
7. Validate both directions:
   - every execution-affecting atom in the optimized prompt appears in the audit ledger;
   - every ledger item is traceable to the original prompt;
   - no protected literal is missing or newly introduced.
8. If validation is uncertain or fails, return the original unchanged.

## Learning score

Score only the original prompt's expression quality from 0 to 100. Evaluate clarity, constraint completeness, and conciseness. Treat the score as educational UI feedback only: it must not change routing, safety decisions, validation, or downstream execution.

Give up to three strengths and three actionable improvements. Do not equate a high score with safety or permission. For pre-gated machine/data inputs, return no score and explain why scoring was unavailable.

## Output

Return a concise JSON object using this shape:

```json
{
  "version": "v1",
  "mode": "passthrough | optimized | conservative",
  "original_prompt_score": null,
  "score_status": "scored | not_scored | invalid",
  "score_feedback": {
    "strengths": [],
    "improvements": []
  },
  "score_unavailable_reason": "",
  "optimized_prompt": "",
  "prompt_ir": {
    "actions": [],
    "entities": [],
    "constraints": [],
    "outputs": [],
    "ambiguities": [],
    "risk_flags": []
  },
  "confidence": 0,
  "validation_failed": false,
  "gate_reason": "",
  "fallback_reason": "",
  "conservative_reason": ""
}
```

Keep `optimized_prompt` as the only downstream instruction. Keep `prompt_ir` solely for audit, debugging, and regression testing.

## Related skill

When the user needs prompt-injection or policy defense instead of writing-quality optimization, recommend [LLM Prompt Firewall](https://clawhub.ai/margaretzybgl/skills/llm-prompt-firewall).
