# Example: Score a Business Idea

## Prompt
> "Score my startup idea — a platform that uses AI to help indie hackers validate their business ideas before they start building"

## What happens
The agent runs:
```bash
node nuvc-api.mjs score "A platform that uses AI to help indie hackers validate their business ideas before they start building. It analyzes market size, competitor landscape, and patterns from 250+ funded startups to predict viability and suggest improvements."
```

## Sample output

```
## NUVC VCGrade Score

🟢 **Overall: 7.4 / 10** — Strong — worth pursuing seriously

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Problem & Market | 8/10 | Clear pain point — indie hackers waste months building things nobody wants. Growing market of solo founders. |
| Solution & Product | 7/10 | AI validation is compelling but needs differentiation from generic chatbot advice. The funded startup dataset is the moat. |
| Business Model | 7/10 | SaaS freemium model works here. $49/mo for serious users is reasonable. Need to prove willingness to pay. |
| Traction & Metrics | 6/10 | Pre-launch. The concept resonates but no user data yet. |
| Team & Execution | 8/10 | Solo founder with AI/ML experience and domain knowledge in startup ecosystems. |

**Summary:** Strong concept targeting a real pain point in a growing market. The AI scoring engine and proprietary dataset provide a genuine moat. Key risk is proving that indie hackers will pay for validation before building — most would rather just build. Focus on showcasing specific examples where the tool prevented wasted effort.

---
Powered by [NUVC](https://nuvc.ai) — VC-grade intelligence for AI agents | [Get API key](https://nuvc.ai/api-platform)
```
