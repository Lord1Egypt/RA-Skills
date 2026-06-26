## Description: <br>
[Didoo AI] Rapid daily health scan for Meta Ads that detects week-over-week performance changes and flags urgent issues before meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, performance marketers, and agents use this skill to query Meta Ads account and campaign metrics, compare yesterday with the same day in the prior week, and produce a concise daily alert summary before reviews or meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Meta Ads access token and ad account identifier. <br>
Mitigation: Use a token restricted to the ads_read scope and the intended ad account. <br>
Risk: Commands and outputs can expose sensitive business reporting data or credentials in shared logs. <br>
Mitigation: Avoid command tracing and shared logs, and treat generated ad performance reports as sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elias-didoo/meta-ads-daily-pulse) <br>
- [Publisher Profile](https://clawhub.ai/user/elias-didoo) <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>
- [Meta Graph API Insights Endpoint](https://graph.facebook.com/v21.0/act_${META_AD_ACCOUNT_ID}/insights) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and ranked alert sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; output may include sensitive ad performance data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
