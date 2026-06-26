## Description: <br>
Analyze a user's MBTI from authorized OpenClaw memory, session history, and workspace notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofsoysauce](https://clawhub.ai/user/kingofsoysauce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to generate a local, evidence-backed MBTI type hypothesis from authorized memory, session history, and workspace notes without taking a questionnaire. It is intended for personality reflection reports, not clinical diagnosis or mental-health assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect broad private OpenClaw history and workspace memory. <br>
Mitigation: Approve only the narrowest source categories needed before ingestion. <br>
Risk: Generated reports and raw records may persist sensitive material in the local .mbti-reports directory. <br>
Mitigation: Use quote-mode none when excerpts are not desired and delete the generated .mbti-reports directory after use if it contains sensitive material. <br>
Risk: Task or cron metadata may expose operational history that is unnecessary for many personality analyses. <br>
Mitigation: Avoid authorizing task or cron metadata unless that operational history is explicitly needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kingofsoysauce/mbti-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/kingofsoysauce) <br>
- [OpenClaw](https://openclaw.ai/) <br>
- [Interactive demo](https://kingofsoysauce.github.io/mbti-skill/) <br>
- [Analysis Framework](references/analysis_framework.md) <br>
- [Evidence Rubric](references/evidence_rubric.md) <br>
- [Report Copy Contract](references/report_copy_contract.md) <br>
- [Report Structure](references/report_structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML report, Markdown summary, JSON analysis artifacts, and local shell command workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces report.html, report.md, analysis_result.json, evidence_pool.json, raw_records.jsonl, and source_summary.json in a local .mbti-reports directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
