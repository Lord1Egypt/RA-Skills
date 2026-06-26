# Prompt Optimizer

Iteratively improve AI prompts through structured evaluation, A/B testing, and feedback-driven refinement. Use when a prompt underperforms, produces inconsistent results, or needs optimization for a specific use case.

## Usage

```
Optimize this prompt: [paste your prompt]
```

Or with context:
```
Optimize this prompt for [goal]. Current issues: [problems]. Target model: [model name].
```

## How It Works

1. **Analyze** — identify structural weaknesses (vague instructions, missing constraints, poor examples)
2. **Rewrite** — apply proven prompt engineering patterns (chain-of-thought, few-shot, role-setting, output format)
3. **Compare** — generate before/after evaluation with expected improvement areas
4. **Iterate** — if user provides feedback on the rewritten prompt, refine further

## Optimization Patterns Applied

- **Clarity**: Replace ambiguous language with specific, measurable instructions
- **Structure**: Add section headers, numbered steps, output format templates
- **Constraints**: Add boundaries (length, tone, forbidden patterns, edge cases)
- **Examples**: Generate few-shot examples if missing
- **Chain-of-thought**: Add reasoning steps for complex tasks
- **Role/persona**: Set context-appropriate expertise framing
- **Output anchoring**: Specify exact output format (JSON, markdown, etc.)

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `goal` | What the prompt should achieve | Inferred from content |
| `model` | Target LLM (affects strategy) | General-purpose |
| `max_tokens` | Target output length | No limit |
| `style` | `concise` / `detailed` / `creative` | `detailed` |
| `iterations` | How many refinement passes | 1 |

## Output Format

```markdown
## Analysis
[Weaknesses identified in original prompt]

## Optimized Prompt
[The improved prompt, ready to copy-paste]

## Changes Made
[Bullet list of specific improvements and why]

## Expected Impact
[What should improve: consistency, accuracy, relevance, format compliance]
```

## Advanced Usage

### Batch Optimization
```
Optimize these 3 prompts for the same task, pick the best approach:
1. [prompt A]
2. [prompt B]  
3. [prompt C]
```

### A/B Test Design
```
Create an A/B test for this prompt. Generate variant A (structured) and variant B (conversational). Include 5 test inputs to compare.
```

### Model-Specific Tuning
```
Optimize this prompt specifically for Claude Sonnet 4.6. Use extended thinking triggers and XML tags.
```
