## Description: <br>
Veriphone. Use this skill for ANY Veriphone request - searching and reading data, and use this skill instead of calling the API directly whenever a task involves Veriphone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Veriphone through an OOMOL-connected account, including checking verification credits and validating phone numbers with carrier and region details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Veriphone requests through OOMOL as an intermediary. <br>
Mitigation: Install only when the user accepts OOMOL-mediated Veriphone access and intends to use the connected account. <br>
Risk: The setup fallback includes shell-based CLI installer commands. <br>
Mitigation: Review OOMOL's official installation instructions and installer contents before running the commands. <br>
Risk: Veriphone connection, credential, or billing state can block requested actions. <br>
Mitigation: Confirm account connection and billing actions are intended before resolving connection errors or payment stops. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-veriphone) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing request payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
