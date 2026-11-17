## Description:

Multi-agent collaborative system for writing ultra-long feasibility study reports, from requirements confirmation and outline planning through parallel chapter drafting, consistency review, and styled DOCX output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqiu193](https://clawhub.ai/user/jinqiu193)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-writing agents use this skill to plan, draft, review, and assemble long feasibility studies or technical proposals with parallel sub-agent writing and document-formatting support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project status and report details may be sent to the configured openclaw-weixin notification channel.

Mitigation: Disable or explicitly approve notifications before using confidential project names, report content, or reference material.

Risk: Report inputs and intermediate files are stored in a Windows-specific local workspace under F:/agent/chapters.

Mitigation: Review local file retention, access controls, and cleanup procedures before processing sensitive reference materials.

Risk: The workflow may spawn multiple writing agents and run local dependency checks that are not pinned by the release evidence.

Mitigation: Run the skill in a controlled environment with approved dependencies and operator oversight for parallel agent activity.

## Reference(s):

- [Phase 0 Requirements Confirmation Guide](references/phase0_guide.md)
- [Phase 1 Planner Guide](references/phase1_guide.md)
- [Phase 2 Sub-Agent Writing Guide](references/phase2_guide.md)
- [Markdown Table Format Specification](references/table_format_guide.md)
- [Bug Troubleshooting and Forced Rebuild Guide](references/bug_fix_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline Python and shell commands; generated artifacts include TXT chapter drafts, JSON state files, Markdown snapshots, and styled DOCX reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local chapter, glossary, reference, progress, and cache files under the configured report workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 3.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
