## Description:

Privacy Scanner helps agents scan skill or code directories before publication for possible sensitive data such as webhooks, tokens, username paths, messaging IDs, private and public IPs, SSH private keys, database URLs, and third-party API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m17y](https://clawhub.ai/user/m17y)

### License/Terms of Use:


## Use Case:

Developers and skill publishers use this skill before releasing to ClawHub or public repositories to check project files for sensitive strings and review pass, warning, and failure findings. The bundled shell scanner supports normal and strict modes for release-gating workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan output may reveal secret values or private identifiers that the tool finds.

Mitigation: Review output locally, avoid uploading or sharing scan logs, and prefer redacted reporting that keeps only file paths, line numbers, and finding types.

Risk: Running the scanner in shared terminals, CI, or agent environments may expose findings through logs or transcripts.

Mitigation: Run it only on intended project directories and route output to controlled locations with appropriate access restrictions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m17y/skills/privacy-scanner)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and terminal scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Strict mode can return a non-zero exit code when findings are detected.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
