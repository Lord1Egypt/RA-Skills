---
name: prompt-engineering-plus
description: "Enhanced prompt engineering with model-specific optimization, advanced techniques, prompt templates, and evaluation metrics. Covers LLMs, image generators, video models with chain-of-thought, few-shot, system prompts, and negative prompts."
metadata:
  author: opencode
  version: 2.0
  tags: prompt-engineering, llm, image-generation, video, optimization
  compatibility: opencode
  license: MIT
---

# Prompt Engineering Plus

Enhanced prompt engineering with model-specific optimization, advanced techniques, and evaluation metrics.

## Features

- **Model-Specific Tips**: Optimized prompts for Claude, GPT-4, Gemini, FLUX, Veo
- **Advanced Techniques**: Chain-of-thought, few-shot, system prompts
- **Prompt Templates**: Ready-to-use templates for common tasks
- **Evaluation Metrics**: Measure prompt effectiveness
- **Optimization Workflow**: Iterative improvement process

## Quick Reference

| Task | Technique | Template |
|------|-----------|----------|
| Code review | Role + constraints | Review this [language] code for... |
| Content writing | Audience + tone | Write a [type] about [topic] for [audience] |
| Image generation | Subject + style + composition | [Subject], [style], [lighting], [quality] |
| Data extraction | Schema + examples | Extract fields matching this schema... |
| Analysis | Step-by-step | Analyze [data] by [method] |

## LLM Prompting

### Basic Structure

```
[Role/Context] + [Task] + [Constraints] + [Output Format]
```

### Role Prompting

```python
# Expert role
"You are a senior software engineer with 15 years of experience in [domain]."

# Teaching role
"You are a patient teacher explaining [topic] to a beginner."

# Critic role
"You are a constructive critic reviewing [work] with specific feedback."
```

### Chain-of-Thought

```python
# Explicit steps
"Think through this step by step before giving the final answer."

# Structured reasoning
"1. First, identify the key facts...
2. Then, analyze the relationships...
3. Finally, draw conclusions..."
```

### Few-Shot Examples

```python
# Example format
"Convert these sentences to formal business English:

Example 1:
Input: gonna send u the report tmrw
Output: I will send you the report tomorrow.

Example 2:
Input: cant make the meeting, something came up
Output: I apologize, but I will be unable to attend the meeting due to an unforeseen circumstance.

Now convert:
Input: hey can we push the deadline back a bit?"
```

### Output Format Specification

```python
# JSON schema
"Return a JSON array with objects containing 'text', 'sentiment' (positive/negative/neutral), and 'confidence' (0-1)."

# Structured output
"For each issue found, provide:
- Line number
- Issue description
- Severity (high/medium/low)
- Suggested fix"
```

### Constraint Setting

```python
# Word limits
"Summarize in exactly 3 bullet points, each under 20 words."

# Format constraints
"Return only valid JSON, no explanation."

# Content constraints
"Focus only on actionable insights, not background information."
```

## Image Generation Prompting

### Basic Structure

```
[Subject] + [Style] + [Composition] + [Lighting] + [Technical]
```

### Style Keywords

```python
# Photography
"shot on Kodak Portra 400 film, soft natural lighting, shallow depth of field"

# Digital art
"digital painting, concept art, artstation, trending"

# Oil painting
"oil painting, masterpiece, classical, detailed brushwork"

# 3D render
"3D render, octane render, cinema 4D, detailed"
```

### Quality Keywords

```python
# High quality
"photorealistic, 8K, ultra detailed, sharp focus, professional, masterpiece"

# Artistic
"intricate details, award-winning, best quality"

# Technical
"high resolution, 4K, detailed texture, sharp"
```

### Negative Prompts

```python
# Common negatives
"blurry, distorted, extra limbs, watermark, text, low quality, cartoon, anime"

# Photography negatives
"overexposed, underexposed, grainy, noisy, artifacts"

# Art negatives
"ugly, deformed, disfigured, poor proportions, bad anatomy"
```

## Video Prompting

### Basic Structure

```
[Shot Type] + [Subject] + [Action] + [Setting] + [Style]
```

### Camera Movement

```python
# Tracking
"Slow tracking shot following [subject] through [setting]"

# Pan
"Smooth pan across [scene] revealing [subject]"

# Zoom
"Slow zoom into [subject] with [effect]"

# Handheld
"Handheld camera following [subject] with natural movement"
```

### Temporal Keywords

```python
# Speed
"slow motion, timelapse, real-time, smooth motion"

# Duration
"continuous shot, quick cuts, frozen moment"

# Transitions
"dissolve, fade, wipe, morph"
```

## Model-Specific Tips

### Claude

- Excels at nuanced instructions
- Responds well to role-playing
- Good at following complex constraints
- Prefers explicit output formats

### GPT-4

- Strong at code generation
- Works well with examples
- Good structured output
- Responds to "let's think step by step"

### Gemini

- Good at multi-modal tasks
- Works well with visual prompts
- Strong at analysis tasks
- Prefers clear instructions

### FLUX

- Detailed subject descriptions
- Style references work well
- Lighting keywords important
- Negative prompts supported

### Veo

- Camera movement keywords
- Cinematic language works well
- Action descriptions important
- Include temporal context

## Evaluation Metrics

### Effectiveness Score

| Metric | Description | Measurement |
|--------|-------------|-------------|
| Clarity | How clear is the prompt? | 1-5 rating |
| Specificity | How specific are the instructions? | Word count, detail level |
| Consistency | How consistent are results? | Variance across runs |
| Quality | How good is the output? | Manual review |

### Prompt Quality Checklist

- [ ] Clear objective stated
- [ ] Constraints defined
- [ ] Output format specified
- [ ] Examples provided (if needed)
- [ ] No conflicting instructions
- [ ] Appropriate length

## Optimization Workflow

### 1. Start Simple

```python
# Basic prompt
"Write a summary of this article."
```

### 2. Add Specificity

```python
# More specific
"Write a 3-sentence summary of this article, focusing on key findings."
```

### 3. Add Constraints

```python
# With constraints
"Write a 3-sentence summary of this article, focusing on key findings. Use formal business English. Include specific statistics if mentioned."
```

### 4. Add Examples

```python
# With examples
"Write a 3-sentence summary of this article, focusing on key findings. Use formal business English. Include specific statistics if mentioned.

Example:
Input: 'Study finds 85% of users prefer interface X over Y.'
Output: 'A recent study reveals that 85% of users demonstrate a preference for Interface X compared to Interface Y. The findings suggest significant usability advantages for Interface X. This data should inform future interface design decisions.'"
```

### 5. Iterate Based on Results

```python
# Refined prompt
"Write a 3-sentence summary of this article, focusing on key findings. Use formal business English. Include specific statistics if mentioned. Avoid technical jargon. Start with the most important finding.

Example:
Input: 'Study finds 85% of users prefer interface X over Y.'
Output: 'A recent study reveals that 85% of users demonstrate a preference for Interface X compared to Interface Y. The findings suggest significant usability advantages for Interface X. This data should inform future interface design decisions.'"
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too vague | Unpredictable output | Add specifics |
| Too long | Model loses focus | Prioritize key info |
| Conflicting | Confuses model | Remove contradictions |
| No format | Inconsistent output | Specify format |
| No examples | Unclear expectations | Add few-shot |

## Prompt Templates

### Code Review

```python
"Review this [language] code for:
1. Bugs and logic errors
2. Security vulnerabilities
3. Performance issues
4. Code style/best practices

Code:
[code]

For each issue found, provide:
- Line number
- Issue description
- Severity (high/medium/low)
- Suggested fix"
```

### Content Writing

```python
"Write a [content type] about [topic].

Audience: [target audience]
Tone: [formal/casual/professional]
Length: [word count]
Key points to cover:
1. [point 1]
2. [point 2]
3. [point 3]

Include: [specific elements]
Avoid: [things to exclude]"
```

### Data Analysis

```python
"Analyze this data:
[data]

Provide:
1. Key insights (3-5 findings)
2. Patterns or trends
3. Anomalies or outliers
4. Recommendations based on findings

Use statistical terms where appropriate. Include confidence levels for key claims."
```

### Image Generation

```python
"[Subject with details], [setting/background], [lighting type],
[art style or photography style], [composition], [quality keywords]"
```

## Best Practices

1. **Start simple** - Begin with basic prompts, add complexity as needed
2. **Be specific** - Vague prompts produce vague results
3. **Use examples** - Few-shot learning improves consistency
4. **Set constraints** - Word limits, formats, tone
5. **Iterate** - Refine based on results
6. **Evaluate** - Measure effectiveness
7. **Document** - Save successful prompts
