## Description: <br>
BugHerd lets agents read, create, and update BugHerd organization, project, task, comment, and attachment data through OOMOL's BugHerd connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams managing BugHerd feedback use this skill to inspect organization, project, task, comment, and attachment data, and to create or update BugHerd records after confirming write payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access BugHerd through connected account credentials and exposes organization, project, task, comment, and attachment data. <br>
Mitigation: Install only for users who need BugHerd access, keep the OOMOL account connection scoped appropriately, and review returned data before sharing it outside the workspace. <br>
Risk: Write actions can create or update BugHerd projects, tasks, comments, and URL-based attachments. <br>
Mitigation: Confirm the exact target, payload, and intended effect with the user before running any action tagged as write or destructive. <br>


## Reference(s): <br>
- [BugHerd homepage](https://bugherd.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; write actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
