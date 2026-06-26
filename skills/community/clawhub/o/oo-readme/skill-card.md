## Description: <br>
ReadMe (readme.com). Use this skill for ANY ReadMe request: reading, creating, updating, and deleting ReadMe project data through the OOMOL `readme` connector and `oo` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation teams, and agents use this skill to search, read, create, update, and delete ReadMe project resources through an OOMOL-connected ReadMe account. It is suited for maintaining ReadMe docs, categories, changelogs, custom pages, versions, API specifications, and project metadata while inspecting live connector schemas before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fallback setup path may run an unpinned remote installer script for the oo CLI. <br>
Mitigation: Review the installer before execution and prefer an official signed or checksum-verified installation path when available. <br>
Risk: The connected ReadMe account may allow write or destructive actions. <br>
Mitigation: Connect an account with permissions scoped to the intended task and approve exact targets and payloads before any write or destructive action. <br>
Risk: The skill requires sensitive ReadMe credentials through the OOMOL connection. <br>
Mitigation: Use only the OOMOL-connected account needed for the task and avoid broad or unnecessary project access. <br>


## Reference(s): <br>
- [ClawHub ReadMe Skill](https://clawhub.ai/oomol/oo-readme) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [ReadMe Homepage](https://readme.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution; ReadMe write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
