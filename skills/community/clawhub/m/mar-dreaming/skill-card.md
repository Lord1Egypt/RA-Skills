## Description:

Creative exploration during quiet hours that turns idle heartbeat time into freeform thinking and writes markdown entries for later human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent decide during quiet hours whether to produce reflective, exploratory markdown entries instead of only returning heartbeat status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script reads dreamChance from data/dream-state.json and the security summary reports that this value can become executable Python code.

Mitigation: Treat the skill data directory as trusted, prevent untrusted users or automation from modifying data/dream-state.json, and review the parsing behavior before deployment.

Risk: The skill writes journal-like markdown files during quiet hours.

Mitigation: Install only where quiet-hours file creation under memory/dreams is expected, and review generated entries before relying on or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-dreaming)
- [Publisher profile](https://clawhub.ai/user/marjoriebroad)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown entries and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dream entries under memory/dreams and updates JSON state under data.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
