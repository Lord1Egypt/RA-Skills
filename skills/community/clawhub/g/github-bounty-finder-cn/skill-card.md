## Description: <br>
Github Bounty Finder scans GitHub Issues and Algora bounties to surface high-value, low-competition opportunities with automated scoring and actionable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, open source contributors, freelance developers, and bounty hunters use this skill to discover GitHub and Algora bounty opportunities and prioritize which issues to pursue. It supports CLI scanning, API-style Node.js integration, filtering, scoring, and JSON export for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub and Algora credentials are stored locally and used by the scanner. <br>
Mitigation: Use least-privilege credentials, keep .env out of version control, and rotate any token that may have been exposed. <br>
Risk: Logs or exported result files may reveal private issue data when privileged credentials are used. <br>
Mitigation: Review scan output before sharing it and avoid publishing result files that include sensitive repository or issue details. <br>
Risk: The package depends on the npm dependency chain and external GitHub and Algora APIs. <br>
Mitigation: Install only from a trusted package source, review dependencies during deployment, and account for API rate limits or service changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lvjunjie-byte/github-bounty-finder-cn) <br>
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte) <br>
- [GitHub token settings](https://github.com/settings/tokens) <br>
- [Algora API settings](https://algora.io/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript examples, and JSON result structures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can write scan results to a JSON file when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
