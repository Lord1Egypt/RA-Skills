## Description: <br>
Query OnlyFans data and analytics through OnlyFansAPI.com, including revenue summaries, model performance, free trial and tracking link conversion rates, and earnings comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martingalovic](https://clawhub.ai/user/martingalovic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agency operators use this skill to ask an agent for OnlyFans account, revenue, model performance, and campaign conversion analytics from OnlyFansAPI.com. It is intended for workflows where the user provides a valid OnlyFansAPI API key and wants summarized results across one or more connected accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API key and may return sensitive account, revenue, and conversion analytics. <br>
Mitigation: Run it only in a trusted environment, treat the API key and returned analytics as sensitive, and prefer the least-privileged or read-only key available. <br>
Risk: Broad or ambiguous requests could expose more account data than intended. <br>
Mitigation: Ask for a specific account, date range, metric, or report scope before making API calls when the request is unclear. <br>
Risk: Unexpected shell commands or requests to untrusted domains could misuse credentials or local data. <br>
Mitigation: Review any curl command that targets a domain other than app.onlyfansapi.com or attempts local file reads before execution. <br>


## Reference(s): <br>
- [OnlyFansAPI Docs](https://docs.onlyfansapi.com) <br>
- [OnlyFansAPI Console](https://app.onlyfansapi.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/martingalovic/onlyfans-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise explanatory text with shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive account, revenue, and conversion analytics returned by OnlyFansAPI.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
