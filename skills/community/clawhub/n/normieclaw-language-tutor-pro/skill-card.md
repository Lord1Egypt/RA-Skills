## Description: <br>
Language Tutor Pro turns an OpenClaw agent into a persistent language tutor that adapts conversation practice, grammar correction, spaced repetition, and progress tracking to the learner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners use this skill with an OpenClaw agent to practice supported languages through adaptive conversation, guided lessons, situation role-play, and vocabulary review. It is intended for ongoing language learning where local progress, vocabulary, grammar, session logs, and transcripts are retained across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves learner profile details, vocabulary, grammar progress, session logs, and full conversation transcripts locally. <br>
Mitigation: Avoid sensitive personal details during practice, protect the skill data directory, and periodically review or clear retained learning data. <br>
Risk: Conversation text may be processed by the OpenClaw LLM backend configured by the user. <br>
Mitigation: Review the OpenClaw backend and provider data-handling terms before using the skill for private or sensitive conversations. <br>
Risk: Progress exports and dashboard files can contain summaries of personal learning activity. <br>
Mitigation: Treat exported progress files with the same care as the underlying transcripts and avoid sharing them unintentionally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-language-tutor-pro) <br>
- [README](artifact/README.md) <br>
- [Setup guide](artifact/SETUP-PROMPT.md) <br>
- [Security notes](artifact/SECURITY.md) <br>
- [Dashboard integration spec](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown conversation guidance with JSON/JSONL data records and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local learner profile, vocabulary, grammar, session, transcript, and optional dashboard export files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
