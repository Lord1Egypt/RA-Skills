## Description: <br>
Give your agent a virtual board of 8 specialized reasoning frameworks (strategy, risk, market, operations, ethics, forecasting, execution, AI-engineering) that independently evaluate a decision and synthesize a go/hold/kill verdict with confidence and concrete findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roberthill0475-lang](https://clawhub.ai/user/roberthill0475-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run LLM-backed decision gates across business, product, campaign, venture, or AI-engineering decisions before proceeding. It returns structured council findings, risks, confidence, and a synthesized go/hold/kill verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision prompts and optional context are submitted to OpenRouter and downstream model providers using the user's API key. <br>
Mitigation: Avoid confidential, regulated, customer-identifying, or secret data unless provider terms and local policy allow it. <br>
Risk: Local prompt-preview, cost, and execution logs may expose sensitive decision context if retained or shared. <br>
Mitigation: Disable or tighten local logging, keep logs in controlled storage, and apply retention rules appropriate for the data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roberthill0475-lang/skills/multi-council-decision-engine) <br>
- [OpenRouter model catalog](https://openrouter.ai/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Structured Python dictionaries and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Council outputs include recommendations, confidence scores, findings, concerns, cost estimates, and synthesized go/hold/kill verdicts.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
