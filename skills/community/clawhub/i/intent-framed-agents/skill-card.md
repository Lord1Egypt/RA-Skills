## Description: <br>
Frames coding-agent work sessions with explicit intent capture and drift monitoring. Use when a session transitions from planning/Q&A to implementation for coding tasks, refactors, feature builds, bug fixes, or other multi-step execution where scope drift is a risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pskoett](https://clawhub.ai/user/pskoett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to establish a lightweight execution contract before non-trivial coding work, monitor for scope drift during implementation, and record how the intent was resolved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intent frames and drift checks can contain project details that transcript-mining tools may later analyze. <br>
Mitigation: Avoid including secrets or sensitive business details in structured intent blocks when using transcript capture or learning aggregation tooling. <br>


## Reference(s): <br>
- [Entire CLI](https://github.com/entireio/cli) <br>
- [ClawHub skill page](https://clawhub.ai/pskoett/intent-framed-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured intent, check, and resolution blocks plus optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured headings are intended to be parseable from session transcripts when compatible transcript tooling is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
