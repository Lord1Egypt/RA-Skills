## Description:

Static ReDoS (Regular Expression Denial of Service) vulnerability scanner and regex quality auditor for codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit codebases for risky regular expressions, ReDoS patterns, missing anchors, locale assumptions, and high-risk call sites before shipping or during review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads source files in the target project to identify regex patterns.

Mitigation: Invoke it with an explicit file, directory, language, or --pattern value when a narrow review is sufficient.

Risk: Optional npm/npx helper commands may run unpinned packages.

Mitigation: Pin package versions or run those commands in an isolated environment before relying on their output.

Risk: Static regex analysis can produce findings that need engineering judgment before code changes are applied.

Mitigation: Review each finding, prioritize high-risk call sites, and test proposed rewrites against expected valid and invalid inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-regex-audit)
- [Canlah AI Homepage](https://canlah.ai)
- [OWASP Regular Expression Denial of Service](https://owasp.org/www-community/attacks/ReDoS)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with code snippets, shell command examples, and optional JSON-oriented CI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity-ranked findings, file and line references, dangerous sub-patterns, attack input examples, and suggested rewrites.]

## Skill Version(s):

1.0.3 (source: evidence.release, evidence.parsed.metadata, artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
