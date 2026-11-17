## Description:

Islamic prayer times skill that provides prayer schedules, reminders, spiritual todo management, and daily reflection tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrrqd](https://clawhub.ai/user/jrrqd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Islamic prayer times for a chosen city, set a remembered location, manage spiritual todos, keep short journal entries, and enable prayer reminder settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The todo completion command can execute unintended local commands through malformed input.

Mitigation: Fix command parsing before broad use, and install only in a restricted environment until the fix is reviewed.

Risk: The skill stores location, todo, journal, and reminder data locally.

Mitigation: Tell users what is stored, keep the memory directory permission-restricted, and avoid entering sensitive journal or task content.

Risk: Prayer-time lookups send city data to the external Aladhan API.

Mitigation: Disclose the external API call and let users choose whether to provide precise or approximate city information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jrrqd/skills/islamic-prayer-times-skill)
- [Aladhan API](https://api.aladhan.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Plain text responses with local JSON and Markdown state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Aladhan API and write local memory files for location, todos, journal entries, and reminder settings.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
