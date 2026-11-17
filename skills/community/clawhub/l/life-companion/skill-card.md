## Description:

Life Companion is a local-first personal AI companion for one person, combining reflective destiny-chart readings, daily journaling, career fit, and relationship reflection with consent-gated local memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dong845](https://clawhub.ai/user/dong845)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill with an agent to support private self-reflection, journal continuity, career exploration, relationship processing, and computed chart readings. It is intended to keep interpretation reflective rather than predictive and to avoid medical, financial, or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive profile, birth, mood, journal, and relationship data may be stored locally under COMPANION_HOME.

Mitigation: Review the consent categories before use, protect the local data directory, and use the documented forget/delete flows for removal.

Risk: First use may auto-install unpinned Python dependencies.

Mitigation: Set LIFE_COMPANION_NO_AUTOINSTALL=1 and install reviewed, pinned dependencies manually when stronger supply-chain control is required.

Risk: The optional localhost form can modify sensitive profile state without request authentication.

Mitigation: Prefer chat onboarding for sensitive use, or run the localhost form only briefly on a trusted machine and stop it after submission.

Risk: Maintainer evaluation tools may run from an environment containing real API keys or other secrets.

Mitigation: Do not run maintainer eval tools from a shell that exposes production credentials or unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dong845/skills/life-companion)
- [README](README.md)
- [Skill operating procedure](SKILL.md)
- [Safety, honesty, and privacy](references/safety.md)
- [Profile schema](references/profile-schema.md)
- [Destiny module](references/modules/destiny.md)
- [Career module](references/modules/career.md)
- [Relationships module](references/modules/relationships.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with optional JSON, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local profile, journal, consent, and cache files under COMPANION_HOME when the user grants consent.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
