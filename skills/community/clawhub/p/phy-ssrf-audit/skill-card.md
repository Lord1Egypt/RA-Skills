## Description:

Server-Side Request Forgery (SSRF) vulnerability scanner (OWASP A10:2021) that detects URL-fetching sinks in Python, Java, Node.js, PHP, Go, and Ruby code, flags cloud metadata endpoint access, and reports CWE-918 findings with fix guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit source code for SSRF patterns, cloud metadata endpoint exposure, missing URL validation guards, and remediation guidance before deployment or CI enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The embedded Python scanner appears broken and could produce unreliable audit results.

Mitigation: Treat results as advisory until the scanner implementation is corrected and tested; avoid using it as a CI gate for release-blocking decisions.

Risk: The skill reads local project source files to identify SSRF patterns.

Mitigation: Run it only on codebases the user is authorized to inspect and review findings before sharing reports externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-ssrf-audit)
- [Canlah AI homepage](https://canlah.ai)
- [OWASP Top 10 A10:2021 Server-Side Request Forgery](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, shell commands, and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CI gate status and CWE-918 finding details when the embedded scanner is used.]

## Skill Version(s):

1.0.3 (source: server release evidence, target metadata, and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
