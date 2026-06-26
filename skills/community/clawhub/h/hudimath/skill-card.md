## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hud941227](https://clawhub.ai/user/hud941227) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to draft, update, validate, evaluate, benchmark, package, and optimize agent skills through a repeatable workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify local files while drafting, evaluating, packaging, and improving skills. <br>
Mitigation: Run it in a dedicated workspace and review generated skill files, evaluation metadata, reports, and packages before using or publishing them. <br>
Risk: Evaluation and description optimization helpers may use the local Claude CLI session with prompts, outputs, and skill content. <br>
Mitigation: Remove secrets, credentials, proprietary data, and sensitive examples from prompts, outputs, and skill files before running those helpers. <br>
Risk: The local review viewer can interact with a local port and may terminate a process already listening on the requested port. <br>
Mitigation: Check whether the viewer port is in use first, choose a different port when needed, or generate a static HTML review page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hud941227/hudimath) <br>
- [Workflows reference](references/workflows.md) <br>
- [Schemas reference](references/schemas.md) <br>
- [Output patterns reference](references/output-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated files, JSON evaluation metadata, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local skill files, evaluation workspaces, packaged skill archives, benchmark reports, and static or local HTML review views.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
