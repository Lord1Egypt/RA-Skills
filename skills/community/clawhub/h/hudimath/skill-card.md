## Description:

Helps agents create, improve, evaluate, benchmark, package, and optimize skills through guided workflows and bundled helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hud941227](https://clawhub.ai/user/hud941227)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to draft or update agent skills, design test prompts, run evaluation loops, compare outputs, and package release artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation outputs may be exposed through local browser-based review reports.

Mitigation: Use static or offline review when possible, avoid sensitive evaluation inputs, and avoid ports used by important local services.

Risk: The skill can write evaluation workspaces and invoke local CLI subprocesses.

Mitigation: Review generated commands and files before execution, and run the workflow only in trusted workspaces.

Risk: Untrusted eval output may be unsafe to open in the eval viewer while the HTML injection issue remains unresolved.

Mitigation: Treat eval outputs from untrusted skills as unsafe and avoid browser review for untrusted content until the issue is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hud941227/skills/hudimath)
- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)
- [JSON Schemas](references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell commands, generated files, and local HTML review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write skill files, evaluation workspaces, benchmark summaries, packaged skill artifacts, and browser-viewable review reports]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
