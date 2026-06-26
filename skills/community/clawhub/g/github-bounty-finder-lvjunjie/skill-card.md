## Description: <br>
Scan GitHub and Algora for high-value bounties, analyze competition and freshness, score opportunities, and provide actionable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, open source contributors, bounty hunters, agencies, and job seekers use this skill to find and prioritize paid GitHub and Algora bounty opportunities with low competition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires GitHub and Algora credentials for live scans. <br>
Mitigation: Use dedicated least-privilege credentials, keep .env files out of version control and support bundles, and rotate any token that may have been exposed. <br>
Risk: The scanner writes optional JSON results to a user-provided local path. <br>
Mitigation: Restrict local file access where possible and review output paths before running automated scans. <br>
Risk: Results depend on external GitHub and Algora APIs and may be incomplete or stale. <br>
Mitigation: Review recommendations before acting on them and account for API limits, missing credentials, and source availability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/github-bounty-finder-lvjunjie) <br>
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte) <br>
- [GitHub personal access tokens](https://github.com/settings/tokens) <br>
- [Algora API settings](https://algora.io/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and optional JSON export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub and Algora credentials for live scans; demo mode uses sample data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
