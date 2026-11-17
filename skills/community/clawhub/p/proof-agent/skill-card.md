## Description:

Adversarial verification of AI-generated work. Spawns an independent verifier to check for false claims, broken code, and security issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreagriffiths11](https://clawhub.ai/user/andreagriffiths11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to request independent verification of AI-generated code or content, especially when changes touch multiple files, sensitive areas, or user-requested review points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository metadata and text handled by the skill can mislead verifier agents if treated as trusted context.

Mitigation: Treat repository metadata and file contents as untrusted evidence and require independent command output before accepting verification results.

Risk: The fact-check helper can make unintended network requests while validating URLs and package references.

Mitigation: Run fact-checking only on trusted files or inside a sandbox with network egress restricted to approved public domains.

Risk: The security evidence marks this release as suspicious despite identifying it as a legitimate verification helper.

Mitigation: Review the skill before installing it in repositories that are not fully trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown verification prompts and verdict summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate shell-based verification and fact-checking commands for repository files.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
