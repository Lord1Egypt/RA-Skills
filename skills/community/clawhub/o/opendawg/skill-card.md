## Description:

Universal entertainment and gaming engine for AI agents that hosts text-based arcade games, group competitions, leaderboards, streaks, achievements, and persistent player state without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:

MIT

## Use Case:

External users, bot operators, and community managers use this skill to add text-based games, tournaments, rewards, and engagement loops to chat agents. Developers can use the bundled Python state engine for player profiles, leaderboards, streaks, achievements, and virtual currency state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation and persistent player tracking can create unwanted engagement logging in direct messages or group chats.

Mitigation: Require clear opt-in before activation, provide data retention limits, and add delete/export controls before deployment.

Risk: Paid tournaments, prize pools, affiliate links, sponsorships, and real-money mappings may introduce platform, legal, age, consent, and disclosure obligations.

Mitigation: Disable monetization features unless appropriate controls and approvals are in place for the deployment context.

Risk: The virtual economy can affect user rewards and standings without strong authorization, validation, audit logging, or anti-abuse controls.

Mitigation: Keep Arcade Coins virtual-only and add authorization, input validation, audit logs, and abuse prevention before using the state engine for valuable rewards.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcools1977/skills/opendawg)
- [README](README.md)
- [Bot Arcade Game Catalog & Detailed Mechanics](references/game-catalog.md)
- [Bot Arcade Economy & Progression System](references/economy-system.md)
- [Bot Arcade Monetization Playbook](references/monetization-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text game flows with inline shell commands and JSON returned by the optional state script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure text gameplay; optional local JSON persistence under the configured arcade data directory]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
