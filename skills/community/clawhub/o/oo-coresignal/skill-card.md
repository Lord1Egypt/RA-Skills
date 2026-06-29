## Description: <br>
Coresignal (coresignal.com). Use this skill for ANY Coresignal request -- searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search and read Coresignal Base Company data through an OOMOL-connected Coresignal account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connector calls may access paid or account-bound Coresignal data. <br>
Mitigation: Install and run the skill only when the user intends to use an OOMOL-connected Coresignal account, and inspect the live connector schema before sending payloads. <br>
Risk: The oo CLI installer is invoked only when the command is missing. <br>
Mitigation: Run the CLI installer only from the documented OOMOL source and only after setup is actually needed. <br>


## Reference(s): <br>
- [Coresignal homepage](https://coresignal.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-coresignal) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
