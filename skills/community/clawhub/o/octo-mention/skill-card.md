## Description:

Analyzes DMWork/OpenClaw group members and message history to build confidence-scored nickname, alias, and bot-name mappings with evidence, conflicts, and incremental merge support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovejing0306](https://clawhub.ai/user/lovejing0306)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using DMWork/OpenClaw group data use this skill to identify member nicknames, aliases, common forms of address, and bot names, then maintain a person-centered mention mapping across groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated mapping database can contain names, aliases, group IDs, uid links, and message evidence snippets for people across multiple groups.

Mitigation: Use the skill only with appropriate group consent, keep the database on a private account or machine, restrict file permissions, and avoid publishing generated JSON or Markdown outputs.

Risk: Local plaintext storage of group-chat identity evidence may persist longer than intended.

Mitigation: Define a retention and cleanup process for generated files under the mention database path before deployment.

Risk: Alias inference may misbind a nickname or common word to the wrong person.

Mitigation: Review conflicts and low-confidence candidates, use the manual correction workflow to lock confirmed aliases, and reject terms that should not be collected.

## Reference(s):

- [Octo Mention ClawHub Skill Page](https://clawhub.ai/lovejing0306/skills/octo-mention)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSON mention databases, Markdown summaries, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores member aliases, uid links, group IDs, confidence scores, evidence snippets, conflicts, and manual corrections in local files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
