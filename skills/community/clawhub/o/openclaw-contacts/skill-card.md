## Description:

Contacts helps an agent look up and maintain contact records, messaging identifiers, and communication preferences in a local YAML-based contacts memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and agent operators use this skill to find contact details, record new contacts, and preserve communication preferences for future interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep persistent contact memory that includes messaging identifiers and communication preferences.

Mitigation: Install only when persistent contacts memory is desired, and require explicit confirmation before adding or updating contact records.

Risk: The contact lookup script accepts an unvalidated contact_id and can read YAML files outside the intended contacts folder.

Mitigation: Restrict contact_id values to letters, numbers, underscores, and hyphens before invoking helper scripts.

## Reference(s):

- [Contact Schema](artifact/memory/contacts/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or maintain per-agent YAML contact records containing messaging identifiers and communication preferences.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
