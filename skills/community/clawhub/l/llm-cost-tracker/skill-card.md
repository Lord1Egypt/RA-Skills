## Description: <br>
Track, analyze, and optimize LLM API spending across providers with spend summaries, per-model cost analysis, budget threshold alerts, and cost reduction recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor LLM provider spend, review token and model-level cost breakdowns, configure budget thresholds, and identify cost optimization opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read LLM provider API keys from environment variables and query usage or billing data. <br>
Mitigation: Run it only in environments scoped to the intended provider accounts, use least-privilege keys where available, and avoid exposing logs that include billing metadata. <br>
Risk: Budget and usage summaries are stored under ~/.openclaw, and external alert channels could share billing or usage metadata. <br>
Mitigation: Review local file permissions and enable only trusted alert destinations approved to receive usage and billing information. <br>


## Reference(s): <br>
- [API Cost Optimization Guide](references/optimization-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with tables plus inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read provider API keys from environment variables and store local budget or usage data under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
