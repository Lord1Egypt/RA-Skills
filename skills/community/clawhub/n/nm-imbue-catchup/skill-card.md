## Description: <br>
Summarizes recent git changes for context recovery after session breaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team members use this skill to catch up on recent repository, document, meeting, sprint, or log changes after an absence, handoff, or interrupted work session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session catchup can preserve or restate sensitive context from previous work. <br>
Mitigation: Avoid using the skill with secrets or confidential material, and periodically clean up named sessions that are no longer needed. <br>
Risk: Generated summaries may omit, misprioritize, or misinterpret recent changes. <br>
Mitigation: Review source files, diffs, logs, or documents before relying on the summary for planning, reviews, or handoffs. <br>
Risk: Suggested shell commands for git or log analysis may be run in the wrong repository, branch, or time window. <br>
Mitigation: Confirm the working directory, branch, baseline, and target scope before running commands or acting on their results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-catchup) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise summaries, action lists, blockers, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local files, git ranges, logs, documents, and session context; no executable code is bundled.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
