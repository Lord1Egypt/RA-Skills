## Description: <br>
Adaptive-language stock-analysis skill that interprets macro and political news, fuses it with retail/social sentiment, applies quantified value fallback rules, and outputs machine-readable stock ideas with valuation and technical plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yellowzijian](https://clawhub.ai/user/yellowzijian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to produce structured equity research that combines macro and political catalysts, retail sentiment, value screening, and technical trade planning. It is intended for analysis workflows that need a human-readable report plus strict JSON for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce stock analysis and trade-planning ideas that may influence investment decisions. <br>
Mitigation: Verify prices, financial metrics, catalysts, and risk levels independently before using the output in any financial decision. <br>
Risk: Market, news, and sentiment inputs are time-dependent and can become stale quickly. <br>
Mitigation: Use current external data sources and preserve the skill's confidence gates when data is incomplete or stale. <br>
Risk: Retail sentiment sources can be noisy, duplicated, or speculative. <br>
Mitigation: Treat partial sentiment as attention-only, apply duplicate filtering where available, and reduce conviction when source quality or polarity data is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yellowzijian/market-signal-fusion) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report with a strict JSON block when structured output is appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adapts the user-facing language to the prompt and uses stable English keys for machine-readable JSON.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
