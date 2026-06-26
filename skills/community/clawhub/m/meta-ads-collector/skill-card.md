## Description: <br>
Scans the Meta Ad Library API to count active ads, identify ad formats and ad types, track the longest-running ad, and estimate spend for a given brand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdarshVMore](https://clawhub.ai/user/AdarshVMore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketing audit teams use this skill to collect public Meta ad activity for a brand and feed paid advertising metrics into audit reports. It is intended for workflows that can supply approved Meta Ad Library API credentials and tolerate graceful fallback when data is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Meta access token or app credentials for Ad Library access. <br>
Mitigation: Confirm credential handling is acceptable before installation and keep Meta credentials private. <br>
Risk: Separate implementation files may add behavior beyond the documented collector pattern if supplied later. <br>
Mitigation: Review any additional implementation files before use. <br>
Risk: Meta Graph API rate limits, approval requirements, or token failures can prevent live ad collection. <br>
Mitigation: Use the documented fallback behavior so the audit pipeline returns typed empty data with an error field instead of blocking. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AdarshVMore/meta-ads-collector) <br>
- [Meta Ad Library API endpoint](https://graph.facebook.com/v19.0/ads_archive) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, API calls] <br>
**Output Format:** [Markdown with TypeScript interfaces, implementation notes, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces collector behavior guidance and typed fallback output; requires Meta API credentials for live Ad Library access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
