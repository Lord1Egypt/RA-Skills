## Description: <br>
Meta Ads data analysis and reporting via meta-ads-open-cli for checking Facebook, Instagram, Messenger, and Audience Network advertising performance, account structure, creatives, audiences, pixels, and lead forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, operators, and developers use this skill to query read-only Meta Ads data, inspect campaign hierarchy and creatives, analyze performance trends and breakdowns, check pixel events, and retrieve lead form submissions when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external CLI package that the instructions install without pinning a trusted version. <br>
Mitigation: Review the package and publisher before installation, pin a trusted version, and avoid global installs in shared environments when possible. <br>
Risk: Meta OAuth tokens can grant broad access to advertising accounts, pages, business data, and lead retrieval endpoints. <br>
Mitigation: Use the narrowest Meta token and permissions needed for the task, keep tokens out of chat, logs, shell history, screenshots, and shared files, and rotate exposed credentials. <br>
Risk: Lead form commands can retrieve personal data from lead submissions. <br>
Mitigation: Retrieve leads only with authorization and a clear business need, and redact or summarize personal data by default before sharing results. <br>


## Reference(s): <br>
- [meta-ads-open-cli documentation](https://github.com/Bin-Huang/meta-ads-open-cli) <br>
- [Meta Marketing API overview](https://developers.facebook.com/docs/marketing-apis/) <br>
- [Meta Ad Insights API](https://developers.facebook.com/docs/marketing-api/insights/) <br>
- [Meta Custom Audiences API](https://developers.facebook.com/docs/marketing-api/audiences/) <br>
- [Meta Lead Ads API](https://developers.facebook.com/docs/marketing-api/guides/lead-ads/) <br>
- [Meta Ad Creative reference](https://developers.facebook.com/docs/marketing-api/reference/ad-creative) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-oriented analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands return pretty-printed JSON by default, support compact JSON output, and may use cursor-based pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
