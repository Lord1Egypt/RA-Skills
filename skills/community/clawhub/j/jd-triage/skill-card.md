## Description: <br>
Evaluates a pasted job description against the user's stored career criteria, bootstrapping or refreshing that profile when needed, and returns a verdict with multi-axis 5-star scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwancoding](https://clawhub.ai/user/bwancoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to triage pasted job descriptions against their own hard gates and soft preferences, then decide whether to apply, skip, or ask recruiters targeted follow-up questions. It also maintains local criteria and evaluation history so later roles can be compared against prior decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Career criteria, salary preferences, and JD evaluation history may be stored as local plaintext files. <br>
Mitigation: Keep the default standard history level unless raw JD storage is intentional, and periodically review or delete jd_criteria.md and jd_history.md if they contain sensitive data. <br>
Risk: Full history mode can persist raw JD text that may include recruiter contact details, compensation, or employer-specific information. <br>
Mitigation: Confirm before enabling full history, redact sensitive JD content where practical, and avoid syncing the workspace to public or shared storage. <br>


## Reference(s): <br>
- [Bootstrap questions](references/bootstrap-questions.md) <br>
- [History format](references/history-format.md) <br>
- [Scoring rubric](references/scoring-rubric.md) <br>
- [ClawHub skill page](https://clawhub.ai/bwancoding/jd-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown evaluation report with local Markdown history and YAML-like criteria files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese/English responses; stores career criteria and evaluation history as local plaintext files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
