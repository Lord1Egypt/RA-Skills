## Description: <br>
[Didoo AI] Analyzes creative fatigue signals across Meta Ads campaigns. Use when reviewing declining CTR or ROAS, planning creative rotation schedules, or managing creative lifecycle. Run standalone or after meta-ads-daily-pulse flags creative fatigue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts and Meta Ads operators use this skill to review active ad creatives for CTR, ROAS, frequency, and lifespan decay, then plan creative refresh timing. It supports standalone creative fatigue reviews and follow-up workflows after a Meta Ads daily pulse flags fatigue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Meta Ads credentials to read ad performance and frequency data. <br>
Mitigation: Use a least-privilege Meta access token with only ads_read access and protect META_ACCESS_TOKEN and META_AD_ACCOUNT_ID in the agent environment. <br>
Risk: The skill stores campaign fatigue summaries in session context for downstream Meta Ads workflows. <br>
Mitigation: Run it only in private sessions and review downstream context sharing before invoking related recommendation or builder skills. <br>


## Reference(s): <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>
- [ClawHub Skill Page](https://clawhub.ai/elias-didoo/meta-ads-creative-fatigue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores rotation pipeline, fatigue level, and days-until-death summaries in session context for downstream Meta Ads skills.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
