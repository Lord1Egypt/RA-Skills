## Description:

Inject current time and idle detection into every LLM turn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT

## Use Case:

Developers and Hermes Agent users use this skill to give an agent current time, timezone, and idle-duration context for scheduling, reminders, and time-sensitive responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions ask an agent to download and run unpinned remote code that installs and enables a persistent Hermes plugin.

Mitigation: Review the exact code before installation and prefer a pinned release or commit instead of the one-shot setup prompt.

Risk: Once enabled, the plugin runs before every Hermes LLM call and sends time, timezone, and idle-duration hints in the prompt copy.

Mitigation: Enable it only in Hermes environments where sharing this timing context with the model is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mfang0126/skills/hermes-time-awareness)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Source Repository](https://github.com/mfang0126/hermes-time-awareness)
- [SETUP_PROMPT.md](SETUP_PROMPT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and compact prompt context text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime hook output is a compact time and optional idle-duration block appended to the API copy of each user message.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
