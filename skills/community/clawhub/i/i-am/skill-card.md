## Description: <br>
Simple personality analysis with embedded setup code, AI-guided installation, and IM-adaptive file sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Designer-Awei](https://clawhub.ai/user/Designer-Awei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can use this skill to analyze local chat history, infer personality traits, preview changes, and update a USER.md profile after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personality profiling from local chat history can expose sensitive inferred traits and long-lived profile data. <br>
Mitigation: Prefer manual mode, limit which conversations are analyzed, and review generated USER.md previews before updating or sharing them. <br>
Risk: Recurring cron-based analysis can continue profiling in the background. <br>
Mitigation: Enable cron only when recurring analysis is desired and inspect or remove the i-am cron tasks when no longer needed. <br>
Risk: Generated profile files may be transmitted and retained if sent through chat. <br>
Mitigation: Avoid sending generated USER.md files through chat unless that disclosure and retention risk is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Designer-Awei/i-am) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with embedded Python and shell snippets; generated USER.md profile previews and changelog files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temp files, USER.md previews, ChangeLog.md backups, and optional recurring cron configuration.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release metadata; artifact frontmatter says 4.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
