## Description: <br>
Manage Meta ad campaigns by reading, creating, updating campaigns, ad sets, ads, creatives, and retrieving insights via the Marketing API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing operations agents use this skill to retrieve Meta Ads account data, inspect campaign performance, and prepare or manage campaigns through the Marketing API. It is intended for authenticated ad accounts and for write actions that have been reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live ad-account write operations can create or change campaigns without adequate confirmation. <br>
Mitigation: Require a human-reviewed preview before create, update, activate, pause, or delete actions; create new campaigns as PAUSED by default. <br>
Risk: Meta access tokens and ad account identifiers are sensitive credentials. <br>
Mitigation: Use minimally scoped tokens, prefer ads_read for reporting, grant ads_management only for approved write workflows, and never expose tokens in agent output. <br>
Risk: Pagination, rate limits, and transient API failures can lead to incomplete or repeated operations. <br>
Mitigation: Follow paging with a safe page limit, respect HTTP 429 responses, and retry failed requests with bounded exponential backoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otman-ai/metaads) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with endpoint examples, request payloads, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Meta access token and ad account ID; write actions should be previewed and approved before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
