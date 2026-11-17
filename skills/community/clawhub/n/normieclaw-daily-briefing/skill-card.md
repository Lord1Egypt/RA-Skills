## Description:

Supercharged Daily Briefing helps an agent discover topic sources, fetch and synthesize recent web content, and deliver a personalized morning briefing with source management and feedback tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to monitor chosen topics, maintain a source registry, receive recurring chat briefings, and tune coverage through natural-language feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can periodically search the web, fetch third-party content, save local briefing history and preferences, and deliver results through a configured chat channel.

Mitigation: Use it only with acceptable topics and chat-channel privacy, review configured sources, and avoid sensitive monitoring topics unless local archive and delivery privacy are appropriate.

Risk: Server security evidence flags setup and scheduler shell errors that affect automation reliability.

Mitigation: Fix and test the setup prompt and scheduler helper before enabling recurring delivery.

Risk: The artifact makes strong privacy and security claims and includes a default promotional footer in generated briefings.

Mitigation: Review the claims against the actual deployment environment and disable or edit promotional footer behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-daily-briefing)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [OpenClaw](https://openclaw.com)
- [NormieClaw](https://normieclaw.ai)
- [NormieClaw security](https://normieclaw.ai/security)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefings, concise chat messages, JSON configuration updates, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled or on-demand briefings with links, source attributions, local archive records, and optional dashboard data.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
