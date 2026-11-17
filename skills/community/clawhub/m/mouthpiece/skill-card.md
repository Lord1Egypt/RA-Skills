## Description:

Mouthpiece helps users draft workplace replies for common workplace conflicts, with empathy, issue analysis, suggested phrasing, and risk reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geekfoxcharlie](https://clawhub.ai/user/geekfoxcharlie)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to describe workplace friction and receive draft responses for overtime requests, responsibility disputes, pushed work, unfulfilled promises, boundary setting, emotional venting, and workplace buzzword translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide workplace context and financial-pressure details for personalization.

Mitigation: Provide only the minimum context needed for a reply, avoid employer-identifying or sensitive dispute facts, and omit debt or financial-pressure details unless they are necessary.

Risk: The artifact promises local-only storage and non-sharing of profile data, but the security evidence says those privacy guarantees cannot be enforced by the skill itself.

Mitigation: Confirm the agent host's retention, inspection, deletion, and sharing behavior before using profile-based personalization.

Risk: Some assertive templates may affect workplace relationships or escalation paths if used without review.

Mitigation: Review suggested replies before sending, prefer lower-risk phrasing when employment consequences are possible, and adapt advice to applicable workplace policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geekfoxcharlie/skills/mouthpiece)
- [ClawHub publisher profile](https://clawhub.ai/user/geekfoxcharlie)
- [README](artifact/README.md)
- [User profile guidance](artifact/user-profile.md)
- [Reply templates](artifact/templates/)
- [Workplace scenarios](artifact/scenarios/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style conversational text with suggested workplace replies and risk reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May tailor responses using workplace profile details such as employer type, role level, financial posture, communication preference, and prior feedback.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
