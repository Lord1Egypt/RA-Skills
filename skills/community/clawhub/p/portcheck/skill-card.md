## Description:

Portcheck provides plain-text reference documentation for devtools workflows, including intro, quickstart, patterns, debugging, performance, security, migration, and cheatsheet topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Portcheck as a local reference helper for devtools concepts, troubleshooting patterns, security considerations, migration guidance, and quick command lookup. It is best suited for retrieving concise reference text rather than performing live port scans or environment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference text is generic and may be mistaken for environment-specific operational guidance.

Mitigation: Review the generated guidance against the target environment before applying security, migration, or performance recommendations.

Risk: The shell script reports version 2.0.2 while the server release evidence and SKILL.md frontmatter report 2.0.3.

Mitigation: Verify and align the script VERSION value before packaging or presenting command-line version output to users.

## Reference(s):

- [ClawHub Portcheck Skill](https://clawhub.ai/bytesagain1/skills/portcheck)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text with Markdown-style headings, lists, and tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local stdout output only; server security evidence reports no credential, network, or persistent state access.]

## Skill Version(s):

2.0.3 (source: server release evidence and SKILL.md frontmatter; script internal VERSION is 2.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
