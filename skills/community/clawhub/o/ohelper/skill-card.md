## Description: <br>
Manage and maintain OpenClaw chat sessions by helping users compact current context, start a fresh session, or reset the current session state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage long or stale chat sessions by choosing between context compaction, a fresh session, or a lighter reset. It emphasizes explicit confirmation before disruptive context changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental or insufficiently confirmed changes to active chat context can compress, replace, or reset useful conversation state. <br>
Mitigation: Require explicit user confirmation before running /compact or /new, and treat /reset as a deliberate session-maintenance action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/ohelper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands affect OpenClaw session state and should be run only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
