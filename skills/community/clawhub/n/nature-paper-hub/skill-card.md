## Description:

Nature Paper Hub helps agents support Nature-series journal workflows including journal selection, literature review, manuscript drafting, figure generation, citation verification, pre-submission audit, cover letters, reviewer responses, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1bai](https://clawhub.ai/user/yang1bai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, research teams, and academic-writing agents use this skill to plan, draft, revise, verify, and export manuscripts intended for Nature-series journals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics or manuscript details may be sent to external search or API services.

Mitigation: Confirm each destination and query with the user before use, and avoid sending confidential unpublished material unless explicitly approved.

Risk: The local paper index may include unrelated personal-administration text.

Mitigation: Audit or remove contaminated paper-index records before deployment.

Risk: Dependency installation can expand the local execution surface.

Mitigation: Install dependencies in a dedicated environment with reviewed and pinned versions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1bai/skills/nature-paper-hub)
- [Nature Portfolio Author Guidelines](https://www.nature.com/authors)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with code blocks, document export guidance, and optional generated files such as DOCX, PPTX, LaTeX, BibTeX, RIS, ENW, and plots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose external searches or API calls and may generate local files when the user chooses export workflows.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
