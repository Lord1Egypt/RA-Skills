## Description: <br>
[Didoo AI] Analyzes Meta Ads audience efficiency across audience types, overlap, demographics, and budget allocation. Use when reviewing targeting strategy, planning audience expansion or narrowing, or auditing budget distribution across audience segments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and agent users use this skill to analyze Meta Ads audience efficiency before launches, during planning, or when audience mismatch may be driving underperformance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Meta Ads credentials and read-only ad account access. <br>
Mitigation: Use the narrow ads_read scope, avoid broad or long-lived tokens when possible, and install only for intended ad accounts. <br>
Risk: Audience and budget findings may influence later recommendation workflows. <br>
Mitigation: Review downstream recommendation output before letting an agent act on stored audience and budget findings. <br>


## Reference(s): <br>
- [Meta Ads Audience Analysis on ClawHub](https://clawhub.ai/elias-didoo/meta-ads-audience-analysis) <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with structured sections and session context findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores budget_reallocation_plan and audience_issues for a related recommendation workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
