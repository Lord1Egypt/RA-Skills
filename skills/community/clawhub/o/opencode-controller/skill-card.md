## Description:

Control and operate Opencode via slash commands to manage sessions, select models, switch between planning and building modes, and coordinate coding work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karatla](https://clawhub.ai/user/karatla)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to route implementation work through Opencode while keeping provider selection, authentication, session reuse, planning, and build-mode transitions explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes coding work through Opencode and may reuse the current project's Opencode session history.

Mitigation: Confirm the provider, authentication method, session selection, and any new session creation with the user before continuing.

Risk: Authentication-dependent providers may require login links or keys before Opencode can proceed.

Mitigation: Pass login links verbatim, wait for the user to confirm completion, and do not assume authentication succeeded.

Risk: An unclear or incorrect plan could lead to unwanted code changes once Build mode starts.

Mitigation: Start in Plan mode, require a step-by-step plan, request revisions when needed, and switch to Build only after the plan is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karatla/skills/opencode-controller)
- [Publisher profile](https://clawhub.ai/user/karatla)
- [Command cheatsheet](references/command-cheatsheet.md)
- [Failure handling](references/failure-handling.md)
- [Model selection](references/model-selection.md)
- [Plan vs build](references/plan-vs-build.md)
- [Question handling](references/question-handling.md)
- [Session management](references/session-management.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with explicit Opencode slash commands and user-facing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes explicit provider, authentication, session, agent-mode, and command selections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
