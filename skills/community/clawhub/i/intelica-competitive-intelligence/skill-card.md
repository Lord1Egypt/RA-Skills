## Description:

Competitive intelligence API for autonomous AI agents that analyzes a URL or company description and returns structured JSON with market positioning, pain points, competitors, battlecards, verified sources, market signals, and Market Score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teodorofodocrispin-cmyk](https://clawhub.ai/user/teodorofodocrispin-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to request structured competitive intelligence for a specific public company, product, or market after the user has approved third-party data submission and any paid API use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, URLs, descriptions, and context are sent to Intelica's third-party API.

Mitigation: Use only public company or market information and do not submit confidential plans, regulated data, PII, or internal strategy.

Risk: Autonomous use can trigger paid API calls when payment is configured.

Mitigation: Set explicit budget limits, use the free demo or trial key first, and require user approval before enabling paid calls.

Risk: Competitive intelligence may be low confidence or have limited source support.

Mitigation: Check returned sources, confidence, and market_score fields before using the analysis for downstream autonomous actions.

## Reference(s):

- [Intelica API](https://api.intelica.dev)
- [Intelica OpenAPI](https://api.intelica.dev/openapi.json)
- [Intelica Full Reference](https://api.intelica.dev/llms-full.txt)
- [Intelica x402 Manifest](https://api.intelica.dev/.well-known/x402.json)
- [Intelica Try Page](https://teodorofodocrispin-cmyk.github.io/Intelica-docs/try.html)
- [ClawHub Skill Page](https://clawhub.ai/teodorofodocrispin-cmyk/skills/intelica-competitive-intelligence)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Guidance]

**Output Format:** [Structured JSON with sources, confidence, market_score, and analysis fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve third-party API calls and paid x402 payments; trial access is available for the first 5 calls.]

## Skill Version(s):

4.5.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
