## Description: <br>
AI 学术论文润色 helps polish academic manuscript text, normalize formatting, check citation compliance, and produce side-by-side revision reports using journal and discipline reference data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic authors use this skill to refine manuscript paragraphs before submission, including grammar, academic tone, terminology consistency, citation style, and target-journal formatting checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to send manuscript text to an external paid service, which may expose unpublished, confidential, regulated, or proprietary research content. <br>
Mitigation: Avoid submitting sensitive manuscript text unless the service provides clear privacy, retention, and data-handling terms that meet the user's requirements. <br>
Risk: The documented payment flow uses a plain-HTTP service endpoint and payment credential headers. <br>
Mitigation: Do not transmit payment credentials unless the service provides HTTPS, clear payment-token handling, and an acceptable security posture. <br>
Risk: Academic polishing, citation, and journal-format suggestions may be incomplete or incorrect for a specific target journal or discipline. <br>
Mitigation: Review generated edits against the target journal's current author instructions and keep author responsibility for final manuscript content. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ai-gaoqian/journal-submission) <br>
- [Academic polish reference data](references/academic-polish.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [JSON polishing report with original and revised text, change reasons, statistics, and citation suggestions; may also provide human-readable manuscript guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Basic tier documents a single paragraph up to 2,000 words; premium full-analysis and PDF output are described as reserved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
