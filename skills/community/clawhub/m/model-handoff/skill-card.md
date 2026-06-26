## Description: <br>
Maintain a HANDOFF.md file in the workspace so context survives when switching between LLM models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwiley1989](https://clawhub.ai/user/bwiley1989) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve project context when moving work between models or long-running sessions. It guides an agent to create and maintain HANDOFF.md with active project state, next steps, behavioral expectations, and references to supporting files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive handoff details or future-agent instructions in workspace files without a clear approval step. <br>
Mitigation: Require the agent to show diffs and ask before editing HANDOFF.md or AGENTS.md. <br>
Risk: HANDOFF.md could include personal details, secrets, API keys, credential filenames, or secret locations. <br>
Mitigation: Omit personal details unless explicitly needed and do not record secrets, API keys, credential filenames, or secret locations. <br>


## Reference(s): <br>
- [HANDOFF.md Starter Template](references/template.md) <br>
- [Model Handoff on ClawHub](https://clawhub.ai/bwiley1989/model-handoff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown file content and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update HANDOFF.md and add a reference to AGENTS.md when the workspace uses that file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
