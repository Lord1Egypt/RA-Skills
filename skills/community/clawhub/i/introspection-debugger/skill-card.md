## Description:

AI Agent 自省调试框架 helps agents capture errors, analyze likely root causes, attempt automatic fixes, and generate structured debugging reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danihe001](https://clawhub.ai/user/danihe001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add self-diagnosis, root-cause analysis, repair suggestions or actions, reporting, and human notification flows to JavaScript-based agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change files, permissions, and dependencies with weak scoping and control.

Mitigation: Review before installing and run only in a disposable or tightly sandboxed workspace unless the skill is changed to ask before making local changes.

Risk: Diagnostic reports may be sent through a configured webhook and could expose sensitive project information.

Mitigation: Use notification webhooks only with trusted destinations and redact reports before enabling them for sensitive projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danihe001/skills/introspection-debugger)
- [Project homepage](https://github.com/tvvshow/openclaw-evomap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JavaScript module behavior plus structured report objects and human-facing debugging guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local files, change permissions, install dependencies, and send diagnostic reports when configured.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
