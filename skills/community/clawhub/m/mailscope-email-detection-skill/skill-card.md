## Description:

Email security detection and analysis for .eml files, including phishing detection, spoofing analysis, malicious attachment scanning, and general email threat assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddgszc](https://clawhub.ai/user/ddgszc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts use this skill to configure Mailscope access, upload intended .eml samples, and receive a human-readable email threat assessment covering sender authentication, links, attachments, and AI analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email samples may include sensitive headers, body content, links, and attachments that are uploaded to a third-party Mailscope service.

Mitigation: Analyze only email samples that are intended for upload, and avoid confidential or regulated messages unless organizational approval is in place.

Risk: The Mailscope API key is stored locally in `config.json`.

Mitigation: Protect local configuration files, avoid sharing `config.json`, and rotate the API key if it may have been exposed.

Risk: The script can upload any readable file path supplied to it.

Mitigation: Verify that the path points to the intended .eml sample before running the analysis command.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/ddgszc/mailscope-email-detection-skill)
- [ClawHub skill page](https://clawhub.ai/ddgszc/skills/mailscope-email-detection-skill)
- [Mailscope API portal](https://x.lizhisec.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style guidance with shell commands and a terminal security analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The analysis report includes risk tier, confidence, sender authentication, domain profile, body preview, URL and attachment details, AI analysis, and recommended actions.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 0.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
