## Description: <br>
TalentHR (talenthr.io). Use this skill for ANY TalentHR request: searching, reading data, and changing an employee role through the OOMOL TalentHR connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and HR operators use this skill to route TalentHR requests through an OOMOL-connected account, including schema-checked execution of the employee role change action. The skill requires explicit confirmation before state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags a mismatch between the skill's read/search-oriented description and its role-changing TalentHR action. <br>
Mitigation: Review before installing and require explicit confirmation of the employee, new role, and business reason before running the role change action. <br>
Risk: The skill requires sensitive connected-account credentials to operate TalentHR through OOMOL. <br>
Mitigation: Use only with an intentionally connected OOMOL account and avoid exposing raw credentials in prompts, files, or command output. <br>


## Reference(s): <br>
- [ClawHub TalentHR skill listing](https://clawhub.ai/oomol/oo-talenthr) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [TalentHR homepage](https://www.talenthr.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; state-changing payloads require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
