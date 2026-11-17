## Description:

Scans public GitHub repositories, folders, or files containing agent skills with Longxia's static pre-install security scanner before installation or review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[john-dong-ai](https://clawhub.ai/user/john-dong-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent users use this skill to scan public GitHub-hosted agent skills before installing or reviewing them. It helps inspect risky instructions, scripts, permissions, credential access, network behavior, package installation, and supply-chain signals without executing target source code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends public GitHub repository, folder, or file URLs to Longxia for static analysis and may receive a public share report.

Mitigation: Use only public GitHub URLs and avoid private repositories, local files, credentials, cookies, authorization headers, or sensitive content.

Risk: Static analysis reports are advisory and cannot prove that a skill is safe or malicious.

Mitigation: Use the verdict, findings, and capability summary as review inputs before installation, and manually inspect any high-impact behavior.

## Reference(s):

- [Longxia](https://longxia.cool)
- [ClawHub listing](https://clawhub.ai/john-dong-ai/skills/longxia-scan)
- [Publisher profile](https://clawhub.ai/user/john-dong-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with scan-result summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scanner verdict, risk score, finding counts, notable findings, detected capabilities, inspected files, report expiry, share URL when available, and remaining anonymous scans.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
