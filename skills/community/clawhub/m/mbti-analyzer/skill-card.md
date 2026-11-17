## Description:

Analyze a user's MBTI from authorized OpenClaw memory, session history, and workspace notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofsoysauce](https://clawhub.ai/user/kingofsoysauce)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use this skill to infer a best-fit MBTI hypothesis from authorized conversation history, memory, and workspace notes, then generate traceable HTML, Markdown, and JSON reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes and stores broad OpenClaw history and workspace memory during MBTI analysis.

Mitigation: Approve only the source categories needed for the run, prefer workspace memory and sessions, and delete the .mbti-reports output directory after use.

Risk: Sensitive-path exclusion is reported as incomplete in the security evidence.

Mitigation: Review the discovered source manifest before ingestion, avoid memory-index, task-run, and cron-run categories unless explicitly needed, and use quote-mode none for sensitive histories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kingofsoysauce/skills/mbti-analyzer)
- [OpenClaw](https://openclaw.ai/)
- [Interactive Report Demo](https://kingofsoysauce.github.io/mbti-skill/)
- [Analysis Framework](references/analysis_framework.md)
- [Evidence Rubric](references/evidence_rubric.md)
- [Report Copy Contract](references/report_copy_contract.md)
- [Report Structure](references/report_structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, guidance]

**Output Format:** [HTML report, Markdown summary, JSON analysis artifacts, and concise chat guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary deliverable is report.html; supporting outputs include report.md, analysis_result.json, and evidence_pool.json.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
