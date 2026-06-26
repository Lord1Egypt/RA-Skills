## Description: <br>
Summarize end-of-session development progress and sync project handoff documentation in Chinese or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loo-y](https://clawhub.ai/user/loo-y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill at the end of a development session to inspect repository evidence, write a concrete handoff, and keep README, handover, TODO, or runbook notes aligned for the next teammate or agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit several repository documentation files when invoked for handoff synchronization. <br>
Mitigation: Ask for a dry run or name the exact files to update when only a summary or a narrower documentation change is desired. <br>
Risk: Handoff content can become misleading if proposed changes are accepted without checking the repository evidence and validation status. <br>
Mitigation: Review the generated handoff and changed documentation before relying on it, especially the stated validations, unresolved issues, and next steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loo-y/handover-sync) <br>
- [README.en.md](artifact/README.en.md) <br>
- [README.md](artifact/README.md) <br>
- [English session summary template](artifact/references/session_summary_template.en.md) <br>
- [Chinese session summary template](artifact/references/session_summary_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown handoff summaries and documentation edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update handoff, README, TODO, and runbook files when the request or repository state calls for synchronized documentation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
