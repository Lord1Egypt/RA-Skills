## Description: <br>
Process Street lets an agent read, create, and update Process Street workflows, workflow runs, tasks, and form fields through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to inspect Process Street workflow data and, with confirmation, create workflow runs or update run fields and task status from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a connected OOMOL account to create Process Street workflow runs or update workflow run fields and task status. <br>
Mitigation: Confirm the exact write payload and expected effect with the user before running write actions. <br>
Risk: The skill requires access to a connected Process Street account through OOMOL. <br>
Mitigation: Use only the intended OOMOL Process Street connection and resolve authentication or scope errors before retrying. <br>


## Reference(s): <br>
- [Process Street homepage](https://www.process.st/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before constructing action payloads; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
