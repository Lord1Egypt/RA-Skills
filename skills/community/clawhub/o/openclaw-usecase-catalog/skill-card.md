## Description: <br>
Comprehensive catalog of what people are doing with OpenClaw, covering use cases, examples, sources, and inspiration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and community maintainers use this skill to answer OpenClaw use-case questions, gather project inspiration, and maintain a bilingual catalog of examples and findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt web research, file writes, commits, and pushes while maintaining the catalog. <br>
Mitigation: Require explicit user confirmation before web research, file writes, commits, or pushes, and review diffs and remote destinations before execution. <br>
Risk: Catalog entries may include private user context or sensitive examples. <br>
Mitigation: Avoid storing private user context in findings and redact sensitive details before saving or publishing entries. <br>
Risk: Some catalog examples describe anti-detection or sensitive-data handling patterns. <br>
Mitigation: Treat those examples as risk signals for review rather than recommended implementation guidance. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/chunhualiao/openclaw-usecase-catalog) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Findings - 2026-02-04](artifact/findings/2026-02-04.md) <br>
- [OpenClaw Use Cases Research Findings](artifact/findings/2026-02-05.md) <br>
- [OpenClaw Use Cases for Leo Liao](artifact/findings/2026-02-05-leo-personalized.md) <br>
- [Executive Summary: OpenClaw for Leo Liao](artifact/findings/2026-02-05-leo-summary.md) <br>
- [Findings - 2026-02-09](artifact/findings/2026-02-09.md) <br>
- [Findings - 2026-02-12](artifact/findings/2026-02-12.md) <br>
- [ClawHub Registry](https://clawhub.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bilingual finding entries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dated finding entries and repository maintenance commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
