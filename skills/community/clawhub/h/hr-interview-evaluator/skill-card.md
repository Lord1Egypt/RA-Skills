## Description: <br>
HR面试评价助手 combines a job description, resume, and optional interview notes to produce a structured interview evaluation report with five-dimension scoring, risk assessment, and a hiring recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CloudMusicCIO](https://clawhub.ai/user/CloudMusicCIO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, recruiters, and hiring managers use this skill to evaluate candidates by comparing JD requirements with resume and optional interview-note evidence. It produces decision-support reports with scored dimensions, risk notes, and a suggested hiring outcome for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate resumes, job descriptions, and interview notes may contain sensitive personal or hiring data. <br>
Mitigation: Use the skill only in environments authorized to process candidate data, and apply the organization's privacy, retention, and access-control requirements. <br>
Risk: Generated scores and hire/no-hire recommendations may be incomplete, biased, or incorrect. <br>
Mitigation: Treat the report as decision support and require qualified human review before taking any hiring action. <br>
Risk: Exporting reports to PDF or PNG can expose candidate data if export tools, scripts, or destinations are not controlled. <br>
Mitigation: Verify export dependencies and output locations before running exports or sharing generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CloudMusicCIO/hr-interview-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with scoring tables, risk assessment, hiring recommendation, and optional PDF/PNG exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JD text and a resume; interview notes are optional. Recommendations require human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
