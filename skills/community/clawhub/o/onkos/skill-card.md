## Description:

Onkos helps agents manage long-form fiction projects by retrieving story context, tracking facts and hooks, guiding chapter writing and revision workflows, and maintaining project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallroya](https://clawhub.ai/user/smallroya)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and writing agents use Onkos to support long-form fiction projects that need cross-chapter consistency, fact tracking, foreshadowing management, continuity checks, revision workflows, and style guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist chapter text and derived facts longer than a user may expect.

Mitigation: Use it only in an isolated novel project and avoid one-off fiction prompts when persistent storage is not desired.

Risk: Import, update, delete, and chapter revision workflows can overwrite or delete project data.

Mitigation: Review those operations before execution and run the skill only against a dedicated project path.

Risk: Mandatory activation and pipeline language can over-constrain agent behavior outside the intended fiction workflow.

Mitigation: Activate it only for long-form fiction tasks and keep unrelated, short-form, or non-fiction requests outside the skill workflow.

## Reference(s):

- [Onkos ClawHub release page](https://clawhub.ai/smallroya/skills/onkos)
- [Agent roles](references/agent_roles.md)
- [Command index](references/command_index.md)
- [Command reference](references/command_reference.md)
- [Creation guide](references/creation_guide.md)
- [Settings format](references/settings_format.md)
- [Workflows](references/workflows.md)
- [text2vec-base-chinese model](https://huggingface.co/shibing624/text2vec-base-chinese)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with command-oriented workflow guidance and generated fiction text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local project files, Markdown outlines, JSON configuration, and SQLite project memory through bundled scripts.]

## Skill Version(s):

1.6.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
