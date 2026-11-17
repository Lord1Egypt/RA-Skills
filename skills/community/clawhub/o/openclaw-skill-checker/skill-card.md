## Description:

Security vetting protocol before installing any AI agent skill, with red flag detection for credential theft, obfuscated code, exfiltration, and LOW/MEDIUM/HIGH/EXTREME risk classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-liu-lang](https://clawhub.ai/user/mr-liu-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review untrusted agent skills before installation, checking source reputation, file contents, permissions, and security red flags. It produces structured vetting reports with a risk level and install recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to inspect candidate skill files and source metadata during vetting.

Mitigation: Run vetting in a temporary or least-privilege workspace and review the candidate skill's permissions separately before installation.

Risk: Illustrative examples include malicious URLs and credential-theft patterns that are examples rather than behavior.

Mitigation: Treat examples as detection guidance only and verify actual behavior against the files being vetted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mr-liu-lang/skills/openclaw-skill-checker)
- [Publisher profile](https://clawhub.ai/user/mr-liu-lang)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with checklist items and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewable vetting reports, risk classifications, and installation recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
