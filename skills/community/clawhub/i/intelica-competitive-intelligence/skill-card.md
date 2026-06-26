## Description: <br>
Intelica analyzes a specific URL, company description, or market target and returns structured JSON with market positioning, pain points, competitors, battlecard, verified sources, market signals, and Market Score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teodorofodocrispin-cmyk](https://clawhub.ai/user/teodorofodocrispin-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, founders, sales teams, investors, and compliance reviewers use this skill to request scoped competitive intelligence for a specific public company, product, protocol, or market after approving third-party data submission and any paid API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company, market, URL, description, and context inputs are sent to the third-party Intelica API. <br>
Mitigation: Use the skill only with public company or market information, and do not submit private strategy, customer data, regulated data, or PII. <br>
Risk: Autonomous calls may incur paid API charges when payment credentials are configured. <br>
Mitigation: Use the free demo or trial key first, require approval for paid calls, and configure explicit budget controls before autonomous use. <br>
Risk: Competitive-intelligence outputs may have low confidence or insufficient sources. <br>
Mitigation: Check the returned sources and confidence fields before using market_score recommendations for autonomous actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teodorofodocrispin-cmyk/intelica-competitive-intelligence) <br>
- [Intelica API](https://api.intelica.dev) <br>
- [OpenAPI reference](https://api.intelica.dev/openapi.json) <br>
- [Full API reference](https://api.intelica.dev/llms-full.txt) <br>
- [x402 payment manifest](https://api.intelica.dev/.well-known/x402.json) <br>
- [Try Intelica](https://teodorofodocrispin-cmyk.github.io/Intelica-docs/try.html) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance, shell commands] <br>
**Output Format:** [Structured JSON responses with markdown API usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include sources, confidence, market_score, analysis, model, tier, mode, and detected_language fields.] <br>

## Skill Version(s): <br>
4.5.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
