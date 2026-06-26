## Description: <br>
Clockify (clockify.me). Use this skill for reading, creating, updating, and deleting Clockify data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to manage Clockify workspaces, projects, tasks, users, and time entries through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Clockify API key and uses OOMOL as an intermediary for Clockify data. <br>
Mitigation: Install only when the user is comfortable with that intermediary role and has connected the intended Clockify account. <br>
Risk: Project, task, time-entry, and delete actions can change or remove Clockify data. <br>
Mitigation: Review exact payloads and obtain explicit user confirmation before approving write or destructive actions. <br>
Risk: The documented first-time setup includes pipe-to-shell installation commands for the oo CLI. <br>
Mitigation: Prefer a reviewed or official package path, and inspect installation scripts before running them. <br>


## Reference(s): <br>
- [ClawHub Clockify skill](https://clawhub.ai/oomol/oo-clockify) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Clockify homepage](https://clockify.me) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through the oo CLI and may return JSON connector responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
