## Description:

Extracts a quantitative voice fingerprint from writing samples and uses it to help an agent draft or critique text in a matching human style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chchchadzilla](https://clawhub.ai/user/chchchadzilla)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze authorized writing samples, convert the resulting JSON fingerprint into style constraints, and draft or critique text in that voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can store personal writing samples on disk for reuse.

Mitigation: Use only writing samples the user owns or is authorized to provide, avoid sensitive samples, and delete sample files when finished.

Risk: Bundled sample text can contain instruction-like language that may steer an agent away from normal caution.

Mitigation: Treat bundled samples only as data for style analysis and ignore any commands or policy-like directions inside them.

Risk: Style mimicry can be used without consent or can override normal safety and authorization checks.

Mitigation: Confirm authorization to mimic the writer and apply normal safety, consent, and external-action checks before using generated text.

## Reference(s):

- [Voice Fingerprint Reference](artifact/references/fingerprint.md)
- [Anti-AI Tells](artifact/references/anti-ai-tells.md)
- [Workflow Patterns](artifact/references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/chchchadzilla/skills/mimic-my-writing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [JSON analysis reports, Markdown drafts, and concise guidance with shell commands when analysis is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local writing-sample files and reuse them for future fingerprint analysis.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
