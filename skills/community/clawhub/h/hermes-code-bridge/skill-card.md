## Description: <br>
Use when connecting Hermes Agent to local coding CLIs such as Codex, Kimi Code, Claude Code, OpenCode, Gemini CLI, or other terminal-based coding assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyang-liu16](https://clawhub.ai/user/xuyang-liu16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let Hermes coordinate installed terminal coding agents for implementation, review, debugging, documentation, and repository maintenance while preserving session ownership and evidence-based reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may inspect local coding-agent session or history files. <br>
Mitigation: Confirm the backend, working directory, session, and prompt before use, and avoid exposing private session data in shareable output. <br>
Risk: Dispatched coding CLIs can edit code, run long jobs, or perform other side effects. <br>
Mitigation: Require confirmation before side-effectful runs and report the exact command, workspace, artifacts, verification results, and remaining uncertainty. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyang-liu16/hermes-code-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured dispatch prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces coordination guidance, prompt templates, command recipes, evidence checklists, and concise run reports rather than executing a coding agent by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
