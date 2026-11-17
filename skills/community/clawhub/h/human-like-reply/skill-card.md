## Description:

Formats Chinese AI replies to sound more natural by reducing repeated greetings and mechanical phrasing while adjusting tone, sentence endings, and optional emojis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hisongmo](https://clawhub.ai/user/hisongmo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this OpenClaw skill to post-process Chinese assistant replies so they read less repetitive and more conversational. It is suited for casual dialogue flows where configurable greeting frequency, formality, filler words, and emoji use are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically rewrite every outgoing response, which can make formal, safety-critical, or multilingual replies less appropriate.

Mitigation: Review or disable the skill for formal work, safety-critical answers, or non-Chinese conversations; tune formality and emoji settings before deployment.

Risk: The skill stores limited local conversation state for session-aware greeting behavior.

Mitigation: Review local state retention expectations and clear or rotate the memory file when session metadata should not persist.

## Reference(s):

- [Technical Reference](references/technical_reference.md)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Single natural-language reply string, with YAML configuration guidance in the artifact documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May apply randomized tone changes, greetings, emojis, and local session-state-aware formatting based on configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
