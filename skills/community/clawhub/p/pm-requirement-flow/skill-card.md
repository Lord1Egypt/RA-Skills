## Description:

PM workflow for clarifying requirements, dispatching implementation to Claude Code, and verifying acceptance; it records Yi's reusable process and depends on claude-code-dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiguoguo](https://clawhub.ai/user/yiguoguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and agent operators use this skill to turn unclear feature requests into a confirmed SPEC, dispatch implementation work to Claude Code, and independently verify the result against acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow launches a background coding agent with approval checks disabled and unclear containment.

Mitigation: Use bypassPermissions only in an isolated disposable project environment, explicitly review the target workdir, and inspect the generated work before accepting it.

Risk: The dispatch command relies on the local claude-code-dispatch dependency and its dispatch.sh behavior.

Mitigation: Install only if claude-code-dispatch is trusted, review the exact dispatch.sh before each use, and confirm what operations it will execute.

Risk: Untrusted requirement text or paths could be passed into a nohup background command.

Mitigation: Do not run the background dispatch command with untrusted requirement text or paths; use reviewed SPEC content and explicit local project paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiguoguo/skills/pm-requirement-flow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured SPEC text and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a background dispatch command and acceptance-check guidance for a user-specified project directory.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
