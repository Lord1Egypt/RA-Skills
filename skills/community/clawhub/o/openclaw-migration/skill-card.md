## Description: <br>
Guides the renaming of the Clawd project to OpenClaw by detailing file moves, reference updates, testing, and documentation steps for a consistent migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyuan99](https://clawhub.ai/user/chenyuan99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, maintainers, and reviewers use this skill while migrating a repository from the Clawd name to OpenClaw. It provides a shared checklist for directory moves, metadata updates, reference replacement, tooling verification, and contributor communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration checklist could be applied in the wrong repository or project state. <br>
Mitigation: Confirm the target repository and migration scope before allowing an agent to apply the checklist. <br>
Risk: Renaming directories, configuration, and agent metadata can break builds, automation, or onboarding files. <br>
Mitigation: Use version control, inspect metadata and configuration changes, and run the repository's tests, linting, and documentation build checks after changes. <br>
Risk: Deleting or archiving the old project directory can remove useful migration history or active files. <br>
Mitigation: Require explicit approval before deletion or archival and keep a traceable reference until the new OpenClaw structure is stable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenyuan99/openclaw-migration) <br>
- [Publisher profile](https://clawhub.ai/user/chenyuan99) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklist steps and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
