## Description: <br>
Meta Ads Healthcheck provides a fast on-demand Meta Ads campaign status check using Green, Yellow, and Red thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers and operators use this skill to check whether Meta Ads campaigns are healthy before meetings or when performance feels off, without running a full diagnostic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Meta Ads credentials and account identifiers to fetch campaign and ad set data. <br>
Mitigation: Provide only the required Meta access token and ad account ID, use the read-only ads_read scope, and avoid sharing credentials in chat or generated reports. <br>
Risk: The skill is a quick health scan and may miss deeper causes of campaign performance changes. <br>
Mitigation: Treat Yellow or Red results as triage signals, confirm normal fluctuation and sample size, and escalate to a fuller diagnostic before making optimization decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elias-didoo/meta-ads-healthcheck) <br>
- [Didoo AI blog](https://didoo.ai/blog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown status report with traffic-light campaign summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; uses read-only ads_read access for campaign and ad set data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
