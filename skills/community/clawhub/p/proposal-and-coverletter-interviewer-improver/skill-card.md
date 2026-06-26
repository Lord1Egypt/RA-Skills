## Description: <br>
Structured interview skill that discovers personal and professional facts, drafts reusable proposal and cover letter statements, and supports approval-based reuse across platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drafthead](https://clawhub.ai/user/drafthead) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Applicants, freelancers, and proposal writers use this skill to interview a person or company, capture professional facts, and turn approved facts into reusable statements for Upwork, LinkedIn, email, job portals, grants, and cover letters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a long-lived local folder of professional and biographical facts. <br>
Mitigation: Install only when local retention is acceptable, periodically review and prune stored profile, fact, preference, coherence, and statement files, and avoid adding sensitive details unless explicitly needed. <br>
Risk: Reusable proposal and cover letter statements can become outdated, overly broad, or misleading if not reviewed. <br>
Mitigation: Use the approval loop, keep statements grounded in captured facts, reject fabricated or exaggerated claims, and review generated text before sending it to employers, clients, or grant reviewers. <br>
Risk: Optional scheduled follow-up can continue collecting personal context over time. <br>
Mitigation: Enable scheduled runs only deliberately, keep each follow-up scoped to the intended person or company, and review accumulated files after recurring sessions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown questions, candidate statements, approval prompts, and local Markdown profile and statement files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores append-only facts and approved statements under skills/proposal-interview/ with editable profile snapshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
