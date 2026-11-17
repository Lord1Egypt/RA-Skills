## Description:

HealthFit-cn is a Chinese-language personal health management agent that routes fitness, nutrition, health tracking, traditional Chinese medicine constitution, seasonal wellness, tongue self-check, and sexual-health logging requests to a matrix of specialized advisors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

External users use HealthFit-cn to create and maintain local health profiles, log exercise, nutrition, body metrics, and sensitive wellness records, and receive Chinese-language fitness, nutrition, TCM wellness, and progress-summary guidance. The skill is best treated as an informational health assistant, not a substitute for licensed medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive health and sexual-health records locally in plaintext files.

Mitigation: Use it only in a trusted local environment, avoid entering highly sensitive details unless necessary, review where files are stored, and delete or protect local data when no longer needed.

Risk: Medical, supplement, and TCM guidance may be incomplete or inappropriate for an individual condition.

Mitigation: Treat outputs as informational wellness guidance and consult qualified medical professionals for diagnosis, medications, serious symptoms, pregnancy, chronic disease, or post-surgical recovery.

Risk: The documented npx installation command may fetch an unpinned release.

Mitigation: Prefer a pinned or manually inspected release before installation, especially in environments that handle sensitive personal health records.

## Reference(s):

- [HealthFit-cn ClawHub Skill Page](https://clawhub.ai/chenchen913/skills/healthfit-cn)
- [README_EN.md](artifact/README_EN.md)
- [Evidence Base](artifact/references/evidence_base.md)
- [Storage Schema](artifact/references/storage_schema.md)
- [Commands Reference](artifact/references/commands.md)
- [Evaluation Scenarios](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language Markdown responses with optional code blocks, local file updates, JSON/CSV/Markdown exports, and shell commands for supported tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local plaintext JSON, TXT, and SQLite health data; sexual-health files are isolated and excluded from backup/export by default but are not encrypted by default.]

## Skill Version(s):

4.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
