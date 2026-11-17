## Description:

Automate web browser tasks using CLI commands for navigation, interaction, data extraction, screenshots, and form handling locally or via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control a browser from natural-language CLI commands for navigation, page interaction, screenshots, and structured web data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser actions, prompts, and entered credentials may be processed by SkillBoss API Hub in remote mode.

Mitigation: Avoid real accounts, internal sites, regulated data, payment flows, and secrets unless that external processing is approved for the use case.

Risk: Screenshots, downloads, cached analysis, cookies, and profile data may persist locally.

Mitigation: Use a fresh isolated browser profile, review generated artifacts, and clear local state after sensitive sessions.

Risk: Natural-language browser actions may target the wrong element or perform unintended operations.

Mitigation: Navigate deliberately, use observe and screenshots to verify page state, and break sensitive workflows into small confirmed steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/godferylindsay/skills/godfery-browser-automation)
- [Browser Automation Setup Guide](https://skillboss.co/skill.md)
- [SKILL.md](artifact/SKILL.md)
- [REFERENCE.md](artifact/REFERENCE.md)
- [EXAMPLES.md](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance, Files]

**Output Format:** [CLI commands and JSON results, with screenshots and downloads written as files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser state, screenshots, downloads, cached analysis, cookies, and profile data may persist locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
