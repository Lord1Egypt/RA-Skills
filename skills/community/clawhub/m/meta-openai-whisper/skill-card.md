## Description:

Meta OpenAI Whisper is a distilled meta-skill that claims to add self-verification, reflection, orchestration, and continuous learning around an OpenAI Whisper-style workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators can use this skill as orchestration scaffolding for Whisper-related tasks with added self-verification and reflection loops. Reviewers should confirm that the release provides the expected transcription workflow before production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises Whisper capability while the artifact mainly provides meta-learning scaffolding.

Mitigation: Require a clear transcription workflow and verify expected Whisper behavior against the source skill before deployment.

Risk: The packaged learner persists cross-session notes in learned_patterns.json.

Mitigation: Remove packaged learned state before use and constrain or disable learner persistence unless stored notes are treated as untrusted data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qq435912743/skills/meta-openai-whisper)
- [ClawHub Publisher Profile](https://clawhub.ai/user/qq435912743)
- [Distillation Report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with optional code and JSON learner state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cross-session learner state; treat persisted notes as untrusted data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
