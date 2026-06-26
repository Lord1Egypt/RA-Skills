## Description: <br>
Query, analyze, and manage Matomo Analytics with API integration, custom reports, and goal tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site owners, and analytics operators use this skill to query their own Matomo instance, generate traffic and conversion reports, and manage site analytics context without storing tokens in plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Matomo auth tokens or analytics details could be exposed if stored in plain text or left in shared local memory files. <br>
Mitigation: Use a least-privilege Matomo token, store it in an environment variable or system keychain, and review ~/matomo/memory.md on shared machines. <br>
Risk: Generated curl commands can be unsafe or misleading if user-provided URLs, token values, site IDs, dates, or query parameters are not validated and quoted. <br>
Mitigation: Confirm the Matomo URL and target site, validate query parameters, and quote shell values before running commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/matomo) <br>
- [Skill Homepage](https://clawic.com/skills/matomo) <br>
- [Setup](artifact/setup.md) <br>
- [Matomo API Reference](artifact/api.md) <br>
- [Report Templates](artifact/reports.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Matomo API query patterns, report templates, and local configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
