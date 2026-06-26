## Description: <br>
Security vetting protocol before installing any AI agent skill. Red flag detection for credential theft, obfuscated code, exfiltration. Risk classification LOW/MEDIUM/HIGH/EXTREME. Produces structured vetting reports. Never install untrusted skills without running this first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-liu-lang](https://clawhub.ai/user/mr-liu-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to vet AI agent skills before installation by checking source reputation, code red flags, permission scope, and overall risk. It produces a structured vetting report with a risk level and installation recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a cautionary workflow that suggests installing target skills into a temporary directory for review. <br>
Mitigation: Review raw files, inspect archives, or use an isolated sandbox before running any installer logic for an unknown skill. <br>


## Reference(s): <br>
- [Openclaw Skill Checker ClawHub page](https://clawhub.ai/mr-liu-lang/openclaw-skill-checker) <br>
- [Publisher profile: mr-liu-lang](https://clawhub.ai/user/mr-liu-lang) <br>
- [ClawHub homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with checklists, report templates, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq for optional GitHub and ClawHub review commands; supports linux, darwin, and win32 per ClawHub metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
