## Description: <br>
[Didoo AI] Generates a structured weekly performance report for Meta Ads accounts that reviews performance, explains changes, and identifies what needs attention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers and ads operators use this skill to produce a weekly Meta Ads performance report with week-over-week KPI changes, performance drivers, and issues requiring action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Meta Ads reporting data for the configured ad account. <br>
Mitigation: Use a Meta access token limited to the read-only ads_read scope and only for the intended ad account. <br>
Risk: Long-lived or overly broad credentials could expose ad account reporting data beyond the intended use. <br>
Mitigation: Avoid broader ad management permissions, rotate or revoke the token when no longer needed, and store credentials outside generated reports. <br>


## Reference(s): <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>
- [ClawHub Skill Page](https://clawhub.ai/elias-didoo/meta-ads-weekly-performance) <br>
- [Publisher Profile](https://clawhub.ai/user/elias-didoo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with KPI table and concise bullet sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; intended to use read-only ads_read access.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
