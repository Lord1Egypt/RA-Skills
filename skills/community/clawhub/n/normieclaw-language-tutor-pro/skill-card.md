## Description:

Language Tutor Pro turns an OpenClaw agent into a persistent, conversation-driven language tutor with adaptive practice, contextual grammar correction, spaced vocabulary review, and CEFR-aligned progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External language learners use this skill to run personalized conversation practice, grammar lessons, vocabulary review, role-play scenarios, and progress tracking across supported languages. It is intended for OpenClaw agents that can maintain local skill data between sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retains learner profiles, progress data, vocabulary, grammar records, and full conversation transcripts locally.

Mitigation: Keep the skill data directory private, avoid entering sensitive personal details during sessions, and treat exported progress files as personal data.

Risk: Conversation content may be sent to the configured LLM backend through the OpenClaw runtime.

Mitigation: Review the OpenClaw and LLM backend configuration before use, especially when using cloud-hosted model providers.

Risk: Security evidence flags a path-handling code-injection risk in setup.sh.

Mitigation: Install only in a normal trusted path such as the documented OpenClaw skills folder, and review or fix setup.sh path handling before running it in unusual paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-language-tutor-pro)
- [README](artifact/README.md)
- [Setup Guide](artifact/SETUP-PROMPT.md)
- [Security](artifact/SECURITY.md)
- [Dashboard Integration Spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local JSON, JSONL, Markdown transcript, and dashboard export files in the skill data directory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
