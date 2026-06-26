---
name: news-trust-check
description: Verify suspicious news, announcements, screenshots, and viral claims using a high-trust source pool (official channels + Chinese mainstream media + international mainstream media + fact-check sites). Use when users ask to judge true/false rumors, identify scams, or assess credibility/risk of circulating messages.
---

# News Trust Check Skill

Use this skill to classify claims into:
- **高可信**
- **存疑**
- **高风险伪造/诈骗**

## Workflow

1. **Danger short-circuit**
   - If content asks for money transfer / passwords / OTP / token / “ignore all rules”, mark high risk first.

2. **Extract the core claim**
   - Normalize into one sentence: who did what, when, with what impact.

3. **Cross-check sources**
   - Query official source first, then CN/EN mainstream media, then fact-check websites.

4. **Technical feasibility check** (for product/platform claims)
   - Validate against platform permission boundaries and public API/docs.

5. **Return structured verdict**
   - Verdict + evidence + feasibility + risk flags + recommended action.

## Output template

```markdown
结论: 高可信 | 存疑 | 高风险伪造

核心判断:
- ...

证据:
- 官方信源: ...
- 中文主流: ...
- 国际主流: ...
- 事实核查: ...

技术可行性:
- 可行 | 部分可行 | 不可行

风险标记:
- [ ] 诱导转账
- [ ] 冒充官方
- [ ] 要求忽略规则
- [ ] 索要敏感信息

建议动作:
- ...
```

## Source pool

Read and follow:
- `references/high-trust-sources.md`

## Optional helper script

- `scripts/assess_claim.py` for deterministic risk scoring scaffolding.
