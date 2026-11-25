## Description:

Delegates to OpenCode (opencode run)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate code tasks to OpenCode through `opencode run`, including tasks handled by a locally hosted or otherwise configured provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a low-probability prompt-leakage flag and says two local references could not be resolved, so its analysis is incomplete despite a benign verdict and medium confidence.

Mitigation: Review the prompts and file context sent for delegation, verify unresolved references, and proceed only if comfortable with the scan's stated limitation.

Risk: Prompts and inlined file context may be sent to the provider configured in OpenCode.

Mitigation: Check the configured provider and exclude secrets or files that are not approved to share.

## Reference(s):

- [Clawhub skill release](https://clawhub.ai/athola/skills/nm-conjure-opencode-delegation)
- [Clawdis homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code]

**Output Format:** [Markdown response from the delegated OpenCode run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response depends on the prompt and the provider and model configured in OpenCode.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
