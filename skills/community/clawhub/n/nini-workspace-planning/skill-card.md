## Description:

Workspace Planning helps agents manage project schedules by reviewing and updating modules, milestones, phases, and delivery status stored in YAML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and project teams use this skill to inspect delivery progress, update module status, link OpenSpec changes, and coordinate YAML-backed schedules with optional Yunxiao work items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The planning CLI can automatically bootstrap PyYAML into a persistent home-directory virtual environment without a pinned version.

Mitigation: Preinstall and pin PyYAML in the deployment environment, or review and control dependency installation before enabling the script.

Risk: Schedule files can reference additional module files, and untrusted module_files entries may point outside the intended schedule set.

Mitigation: Use this skill only with trusted schedule YAML and review module_files paths before running review, update, or link workflows.

Risk: Yunxiao sync can create business work items and write returned IDs back into YAML.

Mitigation: Require explicit user confirmation for the exact items to be created and inspect the resulting YAML changes before committing them.

## Reference(s):

- [Schedule YAML Schema Reference](references/yaml-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/niracler/skills/nini-workspace-planning)
- [Release v0.3.0 Changelog](https://github.com/niracler/skill/releases/tag/v0.3.0)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command results and YAML configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses schedule YAML under planning/schedules/*.yaml; update and link workflows validate with the bundled CLI before the agent edits YAML.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
