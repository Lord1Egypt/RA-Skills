## Description:

Builds and maintains a local OpenClaw user profile so an agent can personalize onboarding, tone, goals, timezone-aware responses, and profile updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyhetech](https://clawhub.ai/user/billyhetech)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this skill to create a user-editable profile that captures identity, role, timezone, goals, and communication preferences for personalized sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores basic identity and preference details in a local profile file.

Mitigation: Install only when local personalization is desired, and review or edit ~/.openclaw/workspace/me.json to see what is stored.

Risk: Users may try to save sensitive personal data in the profile.

Mitigation: Avoid adding passwords, financial data, health records, or other sensitive information; the skill guidance says to leave that data out.

Risk: Profile details could become inaccurate if updated from passing remarks.

Mitigation: Update profile information only after explicit user confirmation and record changes in the profile history.

## Reference(s):

- [Profile Schema Reference](references/profile-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/billyhetech/skills/personal-context)
- [Publisher Profile](https://clawhub.ai/user/billyhetech)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON profile file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update ~/.openclaw/workspace/me.json after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
