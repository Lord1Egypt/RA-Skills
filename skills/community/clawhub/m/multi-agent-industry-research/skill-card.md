## Description:

Multi-agent collaborative industry research for OpenClaw that assigns research roles, runs parallel research with optional Codex, Gemini, or Claude CLI cross-validation, reviews quality, merges findings, and outputs a structured Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shineliang](https://clawhub.ai/user/shineliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to coordinate multi-agent industry research in OpenClaw, including role assignment, source-backed findings, quality review, merge convergence, and final Markdown report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed research findings may be sent to external AI CLIs during cross-validation.

Mitigation: Review topics before use and set RESEARCH_CROSS_MODEL=none unless external validation is acceptable.

Risk: The skill uses shared temporary files during CLI cross-validation.

Mitigation: Avoid confidential, proprietary, regulated, or customer-related topics unless the workspace and external tools are approved for that data.

Risk: The cleanup flow can delete listed historical research paths if the user chooses the delete option.

Mitigation: Prefer archiving or verify every listed path before selecting deletion.

## Reference(s):

- [Industry Research Skill Homepage](https://github.com/shineliang/industry-research-skill)
- [ClawHub Skill Page](https://clawhub.ai/shineliang/skills/multi-agent-industry-research)
- [CLI Cross-Validation Protocol](references/cross-validation.md)
- [Claude Code to OpenClaw Tool Mapping](references/tool-mapping.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-topic working files for configuration, research briefs, agent findings, reviews, merged drafts, and the final report.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
