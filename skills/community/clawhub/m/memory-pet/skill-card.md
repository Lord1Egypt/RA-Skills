## Description:

Memory Pet gives an agent a playful ASCII pet interface for saving conversation summaries and keywords into local pet memories, recalling them later, and managing pet state through a Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders can use this skill to add a lightweight pet-themed memory workflow that stores summaries, keywords, pet state, and recallable interaction history. It is intended for playful long-running agent interactions where local persistence is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation summaries and keywords may be saved to local pet memory files and food-log audit records.

Mitigation: Use the skill only in conversations that do not contain secrets, credentials, private work, or sensitive personal details.

Risk: Pet memory directories may be permanently deleted when affinity decay, escape behavior, or fusion behavior removes a pet.

Mitigation: Back up any memory data that must be retained before using decay-sensitive or fusion-related workflows.

Risk: Permission and retention disclosures are inconsistent across the artifact and server security evidence.

Mitigation: Review the server security summary and the local data directory behavior before deploying the skill in shared or production agent environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ldxs001/skills/memory-pet)
- [Publisher Profile](https://clawhub.ai/user/ldxs001)
- [Guide](references/guide.md)
- [Permissions](references/permissions.md)
- [Examples](references/examples.md)
- [FAQ](references/faq.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-oriented CLI output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pet interaction text, ASCII art, local memory summaries, keyword lists, and pet-state management guidance.]

## Skill Version(s):

0.5.0 (source: server release evidence, artifact frontmatter, artifact _meta.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
