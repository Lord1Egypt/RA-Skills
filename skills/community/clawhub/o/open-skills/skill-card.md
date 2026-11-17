## Description:

open-skills is an interactive CLI that helps developers browse categories, multi-select AI agent skills, and install or sync them across supported editors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumacoder](https://clawhub.ai/user/lumacoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use open-skills to manage agent skill distribution across multiple AI coding editors from a single CLI. It supports browsing local and remote skill registries, installing selected skills, synchronizing remote sources, updating installed skills, and creating local skill scaffolds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer, update, sync, and cleanup operations can modify or delete local skill files.

Mitigation: Back up existing Claude, Cursor, Hermes, and other agent skill directories before installing, updating, or synchronizing skills.

Risk: Synchronizing from untrusted or editable registry data can introduce unsafe skill content or overwrite local bundles.

Mitigation: Use trusted registries only, review registry entries before sync, and prefer immutable remote skill revisions.

Risk: The developer server may expose registry management behavior if started on a shared or untrusted network.

Mitigation: Run the developer server only in a trusted local environment and avoid exposing it beyond localhost.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lumacoder/skills/open-skills)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [IDE Engine design notes](artifact/docs/ide-engine.md)
- [V3 PRD](artifact/docs/PRD-V3.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and CLI text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, synchronize, or remove local skill files depending on the selected command and target editor.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and package.json list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
