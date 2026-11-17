## Description:

Phy Crypto Audit scans Python, JavaScript/TypeScript, Go, Java, and PHP source code for weak cryptography patterns aligned to OWASP A02:2021, including weak password hashing, insecure randomness, hardcoded keys or IVs, risky algorithms, weak JWT secrets, low password-hashing work factors, and deprecated TLS versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to add a local static-analysis scanner for weak cryptography in application source and to produce CI-friendly findings with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local scanner reads source paths provided by the user and may print matching lines that contain secrets or sensitive implementation details.

Mitigation: Run it only on intended local paths and handle generated reports as sensitive security output.

Risk: Results are heuristic, with documented coverage and severity caveats, so findings may be incomplete or require context-specific review.

Mitigation: Review findings manually before using them as a merge blocker or compliance signal, and tune CI usage to the team's risk tolerance.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-crypto-audit)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local scanner output may include file paths, matching source lines, severity labels, CWE mappings, suggested fixes, and CI exit behavior.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
