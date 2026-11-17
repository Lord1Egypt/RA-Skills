## Description:

Static code analysis tool that detects security vulnerabilities, code smells, and complexity issues across 17 languages while running analysis locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artvepa80](https://clawhub.ai/user/artvepa80)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to run local static analysis on project directories for security, quality, complexity, and DevOps configuration issues across supported languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external pip package for its analyzer behavior.

Mitigation: Install in a sandbox or virtual environment, trust the package publisher and index, and pin or independently review the package version before use on sensitive repositories.

Risk: Static analysis may inspect repositories that contain secrets or sensitive source code.

Mitigation: Limit analysis to intended project directories and review repository contents before running the analyzer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/artvepa80/skills/hefestoai-auditor)
- [HefestoAI product site](https://hefestoai.narapallc.com)
- [HefestoAI setup guide](https://hefestoai.narapallc.com/setup)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks; the underlying CLI can emit text, JSON, or HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be filtered by severity, capped by issue count, or configured to fail CI on selected severity thresholds.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
