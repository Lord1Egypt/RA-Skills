## Description: <br>
Control and operate Opencode via slash commands. Use this skill to manage sessions, select models, switch agents (plan/build), and coordinate coding through Opencode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Karatla](https://clawhub.ai/user/Karatla) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate Opencode-assisted coding work through explicit provider selection, authentication confirmation, session reuse, planning, and build-mode handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates an agent operating Opencode on the user's behalf. <br>
Mitigation: Use a trusted Opencode installation and review the plan and resulting code changes before accepting them. <br>
Risk: Provider authentication may involve login links or credential-related choices. <br>
Mitigation: Verify any provider login link before opening it and choose the authentication method deliberately. <br>
Risk: Starting the wrong session can lose context or mix decisions from unrelated work. <br>
Mitigation: Reuse existing project sessions when present and create a new session only with explicit user approval. <br>


## Reference(s): <br>
- [Opencode-controller release page](https://clawhub.ai/Karatla/opencode-controller) <br>
- [Command cheatsheet](references/command-cheatsheet.md) <br>
- [Failure handling](references/failure-handling.md) <br>
- [Model selection procedure](references/model-selection.md) <br>
- [Plan versus build modes](references/plan-vs-build.md) <br>
- [Question handling](references/question-handling.md) <br>
- [Session management](references/session-management.md) <br>
- [Standard workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with explicit slash commands and concise operational instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider, authentication, session, plan-mode, and build-mode selection guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
