## Description: <br>
Use when working with Google Stitch through a disciplined MCP-first workflow for project inspection, controlled screen generation and editing, prompt structuring, and failure recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luischarro](https://clawhub.ai/user/luischarro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agent operators use this skill to run Google Stitch as a controlled design exploration workflow: inspect projects, generate or edit one screen at a time, review visual artifacts, and hand off accepted directions to implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on external Google Stitch and MCP services that may require credentials or account access. <br>
Mitigation: Use only approved external services, keep API keys scoped, and confirm the active project before generation, editing, or export. <br>
Risk: Agent actions can create or revise design screens and may continue after client-side timeouts. <br>
Mitigation: Inspect projects and screens first, poll for timed-out generations before retrying, and review the actual visual artifact before further edits. <br>
Risk: Generated exports or code can be mistaken for production-ready implementation. <br>
Mitigation: Treat Stitch code as a seed, require an accepted canonical screen, and run parity, accessibility, routing, state, and data-boundary checks before completion. <br>
Risk: Some Stitch browser features may not be available through the MCP surface. <br>
Mitigation: Verify available tools in the active runtime and request browser-side export or preview steps when MCP cannot provide the needed artifact. <br>
Risk: Setup or handoff steps may involve package installs, GitHub pushes, cloud publishing, registry setup, or agent configuration changes. <br>
Mitigation: Require explicit user approval before those operations and keep changes scoped to the intended workflow. <br>


## Reference(s): <br>
- [Google Stitch Workflow](https://clawhub.ai/luischarro/google-stitch-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/luischarro) <br>
- [Complete Operator Manual](references/complete-operator-manual.md) <br>
- [Core Operating Model](references/sections/core-operating-model.md) <br>
- [MCP API and Failure Recovery](references/sections/mcp-api-and-failure-recovery.md) <br>
- [Prompt Structuring](references/prompt-structuring.md) <br>
- [Visual Review and Artifacts](references/visual-review-and-artifacts.md) <br>
- [Export and Code Translation](references/sections/export-and-code-translation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, and implementation handoff instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Google Stitch MCP server or an equivalent runtime tool-call interface for Stitch operations.] <br>

## Skill Version(s): <br>
1.8.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
