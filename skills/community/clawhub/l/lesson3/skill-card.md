## Description:

Create new skills, modify and improve existing skills, and measure skill performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to create new agent skills, refine existing skills, design evaluation prompts, compare outputs, and package completed skill releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release was flagged for review because the bundled local viewer can execute injected browser code from crafted evaluation outputs.

Mitigation: Treat evaluation outputs as untrusted, prefer static review output or a known-free port, and review generated reports before opening them in a browser.

Risk: The toolkit can run local Python scripts, Claude subprocesses, browser or local-server tooling, and workspace file writes.

Mitigation: Install only in a controlled workspace where these actions are expected, inspect scripts before use, and avoid exposing sensitive credentials or files during evaluations.

Risk: The package includes unrelated bundled content, including the daily-menu directory and a .codebuddy memory file.

Mitigation: Remove the bundled daily-menu directory and .codebuddy memory file before use or redistribution unless they are intentionally needed.

Risk: The local review server can terminate another process that is listening on its selected port.

Mitigation: Use static review output or choose a known-free port before launching the viewer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yequanzheng/skills/lesson3)
- [Schemas Reference](references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, JSON schemas, shell commands, and generated files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write skill files, evaluation workspaces, benchmark reports, packaged skill archives, and static or local HTML review reports.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
