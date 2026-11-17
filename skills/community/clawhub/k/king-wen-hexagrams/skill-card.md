## Description:

Guides Chinese-language King Wen hexagram workflows for profile setup, question clarification, hexagram lookup, structured readings, daily fortune prompts, and follow-up guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjp-cn](https://clawhub.ai/user/wjp-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to conduct or support King Wen hexagram readings: clarifying the question, normalizing coin or numeric inputs, looking up hexagram meanings, producing structured interpretations, and setting up optional daily fortune prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect or store lunar birthday, gender, optional birth hour, question context, and daily schedule data.

Mitigation: Install and run it only where that local personal data exposure is acceptable, and clear stored state when the profile is no longer needed.

Risk: Install or scheduled-task flows may expose personal profile details in command output or logged environments.

Mitigation: Avoid CI, shared machines, and highly logged environments until output redaction is reviewed.

Risk: Generated cron commands may need manual review before execution.

Mitigation: Review any scheduled-task command and shell quoting before running it.

Risk: Hexagram readings may be mistaken for decisive advice on medical, legal, financial, or other high-impact decisions.

Mitigation: Use readings as reflective guidance only and rely on qualified professional advice for high-impact decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjp-cn/skills/king-wen-hexagrams)
- [README](artifact/README.md)
- [User guide](artifact/guide.md)
- [Daily fortune and scheduled task guide](artifact/daily-fortune.md)
- [Onboarding guide](artifact/onboarding.md)
- [Hexagram catalog](artifact/hexagrams/catalog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text responses with optional shell commands for initialization and scheduling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python for local helper scripts; optional profile and schedule data may be stored locally.]

## Skill Version(s):

1.1.0 (source: server release metadata, package.json, skill.json, README, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
