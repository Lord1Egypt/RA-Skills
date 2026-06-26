## Description: <br>
High-conviction AI trading signals - only the strongest ETF calls from 6 opposing analysts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredxyt](https://clawhub.ai/user/fredxyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-focused agents use this skill to fetch public MoltStreet ETF signal summaries and present concise high-conviction trading alerts. It is intended for quick market monitoring, not for automated trading or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts moltstreet.com to retrieve public AI-generated ETF signal summaries. <br>
Mitigation: Install and run it only where outbound requests to moltstreet.com are acceptable. <br>
Risk: ETF alerts and summaries may be inaccurate, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Verify important market information independently and do not trade solely from these alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fredxyt/moltstreet-alerts) <br>
- [MoltStreet](https://moltstreet.com) <br>
- [MoltStreet skill documentation](https://moltstreet.com/skill.md) <br>
- [MoltStreet API base](https://moltstreet.com/api/v1) <br>
- [MoltStreet disclaimer](https://moltstreet.com/disclaimer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline curl commands and summarized market signals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and calls public MoltStreet API endpoints; responses should include the skill's AI-generated, not-financial-advice disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
