## Description: <br>
AeroLeads lets agents search and read prospect data through an OOMOL-connected AeroLeads account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting sales, recruiting, or prospect research teams use this skill to retrieve AeroLeads prospect details from public LinkedIn profile URLs. It is intended for users who already have an OOMOL-connected AeroLeads account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting an AeroLeads account or API key through OOMOL and can return emails, phone numbers, and profile details. <br>
Mitigation: Install it only for intended AeroLeads workflows, use authorized accounts, and treat returned contact and profile data as sensitive personal data. <br>
Risk: First-time setup guidance includes remote shell and PowerShell installer commands for the oo CLI. <br>
Mitigation: Review OOMOL's official installation guidance and verify the installer source before running remote installer commands. <br>


## Reference(s): <br>
- [ClawHub AeroLeads skill](https://clawhub.ai/oomol/oo-aeroleads) <br>
- [AeroLeads homepage](https://aeroleads.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OOMOL-connected AeroLeads account; connector responses may include personal contact and profile data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
