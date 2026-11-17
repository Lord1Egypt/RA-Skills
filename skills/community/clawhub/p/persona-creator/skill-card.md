## Description:

Persona Creator analyzes at least 10 messages from memory/*.md to create, refresh, reset, and use persona JSON profiles for style-aware role play.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taget](https://clawhub.ai/user/taget)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create reusable persona profiles from chat history, refresh them as new memory files arrive, reset or delete them, and use them for style-based role play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local memory files that may contain private conversation history and sends sampled text through the model for style analysis.

Mitigation: Require explicit user consent, limit analysis to intended memory files, review sampled text before model submission, and avoid processing sensitive conversations.

Risk: Persona profiles and temporary analysis files can contain reusable style and identity data.

Mitigation: Store persona output only in the intended persona directory, restrict access to generated profiles, and clean up temporary analysis files after use.

Risk: Unsafe username or path handling could affect unintended persona files.

Mitigation: Validate usernames and enforce containment within the persona directory before reading, writing, deleting, or resetting profiles.

Risk: Real-person style imitation can be misused or misunderstood.

Mitigation: Disclose style imitation, restrict imitation to consenting users, and avoid presenting generated responses as the real person.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taget/skills/persona-creator)
- [Skill definition](artifact/SKILL.md)
- [Persona template](artifact/persona/yourself.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages and summaries, JSON persona profiles, and shell command invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persona/<user>.json profiles and may use temporary analysis prompt/result metadata under /tmp during generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
