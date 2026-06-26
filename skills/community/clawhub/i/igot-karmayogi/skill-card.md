## Description: <br>
Automates the iGOT Karmayogi portal using OpenClaw's managed browser to help a logged-in user enroll in courses, play course videos, complete assessments, download certificates, and track progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koppakanagaharsha-lang](https://clawhub.ai/user/koppakanagaharsha-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and learners who use iGOT Karmayogi can use this skill to operate their training portal session end to end, including assigned coursework, progress tracking, assessments, and certificate download. It is intended for supervised automation of an existing authenticated account. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in iGOT account end to end, including course enrollment, video playback, assessment submission, and certificate download. <br>
Mitigation: Use it only when that level of account automation is intended, keep the browser session supervised, and stop the run if it performs an unexpected action. <br>
Risk: Automated coursework or assessment completion may conflict with platform, employer, or program rules. <br>
Mitigation: Review the applicable iGOT, employer, or training-program rules before using the skill for assigned courses or assessments. <br>
Risk: The skill may retain session data, progress state, or learning-history context in the browser profile and workspace state file. <br>
Mitigation: Clear the saved state and browser profile after use if persistent login state or learning-history data should not remain on the machine. <br>
Risk: Shell-based browser fallbacks can increase local execution risk if the environment is not trusted. <br>
Mitigation: Prefer the managed browser path and use shell fallbacks only in a trusted local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/koppakanagaharsha-lang/igot-karmayogi) <br>
- [Publisher profile](https://clawhub.ai/user/koppakanagaharsha-lang) <br>
- [iGOT Karmayogi portal](https://portal.igotkarmayogi.gov.in/page/home) <br>
- [Course IDs reference](references/course-ids.md) <br>
- [Selectors reference](references/selectors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Operational browser actions with concise user status messages and local state JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save course certificates as PDF files and persist progress state in the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
