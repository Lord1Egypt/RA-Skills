## Description: <br>
Builds or updates vulnerability pattern skills from GitHub Security Advisories, HackerOne Hacktivity, and NVD sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhy0](https://clawhub.ai/user/yhy0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to build or refresh vulnerability-audit and pentest skills from advisory, CVE, and public bug bounty data. It guides data fetching, candidate analysis, skill file creation, and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to run local scripts and persist generated vulnerability skills in a workspace. <br>
Mitigation: Use it only in a trusted workspace, inspect or provide referenced scripts before running commands, and review generated skills before enabling or publishing them. <br>
Risk: The skill has broad security-research triggers and may activate around general vulnerability or advisory discussions. <br>
Mitigation: Invoke it only when intentionally generating or updating vulnerability and pentest skills, and confirm scope, data sources, and credentials before execution. <br>


## Reference(s): <br>
- [Vulnerability Pattern Skill Structure Specification](references/skill-structure.md) <br>
- [Vulnerability Case Template](references/case-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated skill-file structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local skill files and reference case libraries when the user directs it.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
