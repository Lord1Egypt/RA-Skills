## Description:

Helps agents plan, parallelize, review, and assemble long feasibility-study reports into polished DOCX outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqiu193](https://clawhub.ai/user/jinqiu193)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and report-writing agents use this skill to gather requirements, build an outline, coordinate parallel chapter drafting, check cross-chapter consistency, and assemble long feasibility-study reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run external tooling, including Mermaid rendering through command-line tools.

Mitigation: Review before installing and remove or disable the npx Mermaid fallback unless a verified Mermaid CLI is installed.

Risk: The skill stores report reference material and generated working files.

Mitigation: Use a dedicated workspace, set LOBAI_CHAPTERS_DIR and LOBAI_OUTPUT_DIR to controlled folders, and avoid sensitive reference material unless local retention is acceptable.

Risk: Optional Feishu and WeChat notification integrations may send messages outside the local environment.

Mitigation: Keep notifications on the default log channel unless Feishu or WeChat use is intentional.

Risk: Automated sub-agent drafting can introduce incorrect or inconsistent report content.

Mitigation: Review generated chapters and run the cross-chapter consistency check before relying on the assembled report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinqiu193/skills/lobsterai-report-agent)
- [Phase 0 guide](references/phase0_guide.md)
- [Phase 1 guide](references/phase1_guide.md)
- [Phase 2 guide](references/phase2_guide.md)
- [Table format guide](references/table_format_guide.md)
- [Bug fix guide](references/bug_fix_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command snippets and generated report artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write plan, glossary, chapter, reference, tracker, and DOCX files under configured report directories.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
