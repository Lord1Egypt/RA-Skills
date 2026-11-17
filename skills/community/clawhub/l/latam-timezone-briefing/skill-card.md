## Description:

Generates a daily morning briefing for Argentina and LATAM with ART timezone handling, Spanish dates, workweek context, Argentine holidays, and optional ARCA tax due dates when the related fiscal calendar skill is installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[centriqs](https://clawhub.ai/user/centriqs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams in Argentina or LATAM use this skill to get concise daily or weekly briefings with local date, timezone, holiday, agenda, and optional fiscal-deadline context. It is suited for private operational planning rather than public broadcast of sensitive agenda details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad natural-language aliases can activate the briefing during casual greetings or daily check-ins.

Mitigation: Review the aliases before installation and adjust local usage if greetings are often used outside briefing intent.

Risk: Local agenda or configuration files may contain sensitive meetings, client names, or tax details.

Mitigation: Use agenda and tax configuration data only in private one-to-one briefings and avoid placing sensitive details in shared channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/centriqs/skills/latam-timezone-briefing)
- [Centriqs homepage](https://centriqs.io)
- [OpenClaw](https://openclaw.ai)
- [argentina-fiscal-calendar related skill](https://clawhub.ai/centriqs/argentina-fiscal-calendar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style briefing text with optional inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish-language briefings use DD/MM/YYYY dates and local LATAM timezone context, defaulting to ART.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
