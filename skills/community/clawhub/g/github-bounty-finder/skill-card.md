## Description: <br>
Scans GitHub Issues and Algora bounties, scores opportunities by value, competition, and freshness, and returns recommendations for developers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, open source contributors, bounty hunters, and agencies use this skill to find bounty opportunities, compare competition, prioritize work, and export scan results for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can use GitHub and Algora credentials for authenticated searches. <br>
Mitigation: Use fine-grained or least-privilege tokens and rotate credentials if exposure is suspected. <br>
Risk: Local .env files and exported result files may contain sensitive workflow data. <br>
Mitigation: Keep .env files out of version control and shared archives, and protect generated result files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/github-bounty-finder) <br>
- [GitHub personal access token settings](https://github.com/settings/tokens) <br>
- [Algora API settings](https://algora.io/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [CLI text output and optional JSON export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include bounty URLs, scores, competition levels, recommended actions, and pricing recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
