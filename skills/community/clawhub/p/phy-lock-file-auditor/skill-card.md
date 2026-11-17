## Description:

Audits common JavaScript, Python, Go, and Rust lockfiles for drift, phantom dependencies, integrity hash anomalies, conflicting pins, and CI freshness checks using local project files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to inspect project lockfiles for dependency drift, unexpected packages, weak or malformed integrity data, and duplicate version pins. It can also draft CI freshness checks and remediation guidance for review before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate supply-chain coverage and give users false confidence in lockfile audit results.

Mitigation: Treat results as a limited local review aid and keep established dependency, vulnerability, and release controls in place.

Risk: Suggested lockfile regeneration, npm install, or CI gate changes may alter dependency resolution or workflow behavior.

Mitigation: Manually review generated commands and dependency diffs before applying or committing them.

Risk: Coverage for non-npm ecosystems may be less complete than the skill description implies.

Mitigation: Use ecosystem-native verification tools and manual review before relying on findings for non-npm projects.

## Reference(s):

- [Phy Lock File Auditor on ClawHub](https://clawhub.ai/phy041/skills/phy-lock-file-auditor)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI freshness gate snippets and remediation guidance; no external API calls are described.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
