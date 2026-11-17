## Description:

Provides a Chinese-language OpenClaw beginner guide with large-model background, FAQs, command references, and optimization guidance, launched through a local web interface on port 34567.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunyashaw](https://clawhub.ai/user/kunyashaw)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to start a local beginner-help web guide and quickly find onboarding material, common troubleshooting answers, command examples, and basic optimization advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start a local web guide service on port 34567 that may continue running outside normal activation control.

Mitigation: Install only from a trusted ClawHub release, confirm the service binds only where expected, and be prepared to manually stop the Node.js process after use.

Risk: The included guidance mentions elevated npm installation patterns that may be risky for users who do not understand permission changes.

Mitigation: Prefer a pinned or trusted ClawHub installer and avoid sudo npm commands unless the operational risk is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kunyashaw/skills/openclaw-newbie-faq)
- [Publisher profile](https://clawhub.ai/user/kunyashaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Local HTML guide with embedded text, command examples, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a Node.js local web service on port 34567 when activated.]

## Skill Version(s):

1.0.44 (source: ClawHub release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
