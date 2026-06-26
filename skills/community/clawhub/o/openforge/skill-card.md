## Description: <br>
OpenForge executes structured PRDs through staged OpenClaw phases with model routing, validation gates, automatic retries, and review-to-fix loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use OpenForge to turn a reviewed PRD into coordinated implementation, testing, and review phases inside an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PRDs and gate commands can cause an agent to edit a workspace or run commands. <br>
Mitigation: Use trusted PRDs, review every Gate command before execution, and avoid Shell-Gate unless the command has been explicitly reviewed. <br>
Risk: Workspace edits may affect important project files. <br>
Mitigation: Run OpenForge on a clean branch or disposable workspace for higher-risk changes, then review generated changes before relying on them. <br>
Risk: Secrets included in PRD text may be passed to sub-agents. <br>
Mitigation: Keep API keys, credentials, and other secrets out of PRD files; use environment variables or the host environment's secret handling instead. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown phase summaries, review findings, code or file changes, and shell gate results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a run summary under .openforge when a working directory is specified.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
