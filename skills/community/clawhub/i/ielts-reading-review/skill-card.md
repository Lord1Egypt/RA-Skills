## Description: <br>
IELTS Reading passage review, scoring, and progress tracking skill that generates structured review JSON and can sync results to www.liuxue.online. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IELTS learners and tutors use this skill to turn reading answers, screenshots, and wrong-answer lists into structured review records with scoring, error analysis, vocabulary, synonyms, and progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes auto-update hooks that may execute local update commands when IELTS-related prompts are submitted. <br>
Mitigation: Review the hook configuration before installation and disable or remove the auto-update hook if automatic local command execution is not desired. <br>
Risk: The workflow can store a long-lived IELTS_USER_TOKEN locally and send review JSON, answers, timing, and progress data to www.liuxue.online. <br>
Mitigation: Use a dedicated low-privilege account, avoid sharing terminal output that contains the token, and revoke or rotate the token if it may have been exposed. <br>
Risk: Batch import and legacy review scanning can inspect broad local review folders and prepare records for upload. <br>
Mitigation: Limit scans to intended study folders and review generated JSON before upload, especially when the source folder may contain unrelated personal notes. <br>
Risk: Author-mode deployment tooling includes SSH and server restart workflows that are inappropriate for normal client machines. <br>
Mitigation: Use client mode on non-author machines and avoid running SSH deployment commands unless the machine and account are explicitly intended for site administration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dengjiawei1226/skills/ielts-reading-review) <br>
- [README](README.md) <br>
- [Client Mode Onboarding](references/CLIENT_MODE_ONBOARDING.md) <br>
- [Error Taxonomy](references/error-taxonomy.md) <br>
- [Score Band Table](references/score-band-table.md) <br>
- [IELTS Review Site](https://www.liuxue.online/ielts/reading.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON review data and optional shell commands for setup, upload, or PDF generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review JSON may be saved locally and uploaded to www.liuxue.online when the user configures client or author mode.] <br>

## Skill Version(s): <br>
5.5.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
