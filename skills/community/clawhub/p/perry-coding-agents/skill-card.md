## Description:

Dispatch coding tasks to OpenCode or Claude Code on Perry workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gricha](https://clawhub.ai/user/gricha)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate coding work, pull request review, and follow-up fixes to OpenCode or Claude Code agents running in Perry workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote agent dispatch can execute broad coding tasks in Perry workspaces with weak scoping.

Mitigation: Use this skill only for trusted Perry workspaces and trusted task text, and define branch, goal, and done criteria before dispatch.

Risk: Prompt or command text can expose bearer tokens or encourage unsafe SSH behavior.

Mitigation: Avoid long-lived bearer tokens in prompts or command lines, prefer strict SSH host-key validation, and do not copy untrusted issue or pull request text into shell templates.

Risk: Reused remote agent sessions can carry context between unrelated tasks.

Mitigation: Reset or isolate remote agent sessions between unrelated tasks.

## Reference(s):

- [Perry Coding Agents ClawHub page](https://clawhub.ai/gricha/skills/perry-coding-agents)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SSH and curl command templates plus task-tracking guidance for remote Perry workspace dispatch.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
