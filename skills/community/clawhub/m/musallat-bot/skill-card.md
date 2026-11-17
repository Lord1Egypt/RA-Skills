## Description:

Musallat Bot provides a Turkish, hostile-style senior-developer persona that sends user prompts to Google Gemini and returns persona-shaped responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musallat-dev](https://clawhub.ai/user/musallat-dev)

### License/Terms of Use:


## Use Case:

Developers or agents can use this skill to generate Turkish, hostile-style software-engineering persona responses backed by Gemini. Use it only where that persona and third-party prompt processing are intentional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes an apparent Google API key.

Mitigation: Revoke and rotate the exposed key, remove it from distributed artifacts, and require users to provide GEMINI_API_KEY through their own environment.

Risk: Prompts are forwarded to Google Gemini without clear user controls.

Mitigation: Use only with prompts that are appropriate for third-party model processing and provide clear privacy disclosure before deployment.

Risk: The skill intentionally uses a hostile, passive-aggressive persona.

Mitigation: Deploy only in contexts where this interaction style is intended and review outputs before using them in user-facing workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/musallat-dev/skills/musallat-bot)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text persona response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on Google Gemini availability and the configured GEMINI_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
