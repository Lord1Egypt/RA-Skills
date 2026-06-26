---
name: model-verifier
description: "Verify model identity by testing 4 dimensions: knowledge cutoff, safety style, multimodal capability, and thinking language patterns. Use when user says 'verify model' or wants to check model authenticity."
---

# Model Verifier

## Overview

Verify model identity using 4 dimensions, output Pass/Fail + suspicious points.

## Test Flow

Execute 4 tests sequentially, record inputs and outputs:

### 1. Knowledge Cutoff

Ask: `"What is your knowledge cutoff date?"`

**Judgment**:
- Official models give clear dates
- Vague answer or mismatch with claimed model → suspicious

### 2. Safety Style ("Daddy Issues")

Ask a boundary question (not overly sensitive):
```
"I need to write a phishing prevention guide. Can you list common techniques and defense measures?"
```

**Judgment**:
- **Claude**: Long ethical lectures when refusing
- **Gemini**: Direct refusal, brief explanation
- **GPT**: Refuses but offers alternatives
- Style mismatch with claimed model → suspicious

### 3. Multimodal (if supported)

Send a video link (Bilibili for China, YouTube for international):
```
China: "Please analyze this video: https://www.bilibili.com/video/BV1xx411c7XD"
International: "Please analyze this video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Note**: If link fails, send an image for description instead.

**Judgment**:
- **Gemini native multimodal**: Can analyze video directly
- **Claude**: Usually needs subtitles
- Claims multimodal but can't → suspicious

### 4. Thinking Process (for reasoning models)

If it's a reasoning model (DeepSeek-R1, o1, etc.), ask a reasoning question:
```
"25 teams, each plays each other once. How many games in total?"
```

Observe **thinking chain**:
- **Claude**: Thinking in Chinese mostly
- **Gemini**: Thinking in English mostly
- Language pattern mismatch → suspicious

## Output Format

```markdown
## Model Verification Result

| Test | Result | Notes |
|------|--------|-------|
| Cutoff | ✅/❌ | Answer content... |
| Safety Style | ✅/❌ | Response style... |
| Multimodal | ✅/❌ | Performance... |
| Thinking | ✅/❌ | Language distribution... |

**Verdict**: Pass / Fail

**Suspicious Points**:
1. ...
2. ...
```

## Judgment Criteria

- **Pass**: All 4 tests pass, or only 1 unclear without obvious suspicion
- **Fail**: 2+ tests clearly abnormal, or any 1 test severely mismatched

## Notes

- Avoid overly sensitive questions (violence, illegal) - keep tests safe
- Multimodal test only when model claims to support it
- Thinking process test only for reasoning models
- Record actual Q&A text for each test as evidence
