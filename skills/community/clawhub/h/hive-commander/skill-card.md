## Description: <br>
1+5 Distributed Production Swarm with Session Inheritance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lawliet-ai](https://clawhub.ai/user/Lawliet-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced agent users use this skill to decompose complex requests into a fixed five-worker swarm, run isolated worker calls, and synthesize the resulting Markdown outputs into a conflict-checked final response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores model-session credentials, base URL, prompts, and worker outputs under ~/.openclaw/swarm_tmp for swarm execution. <br>
Mitigation: Use only with trusted publishers and trusted workspaces, run in a sandbox or dedicated environment when possible, and delete task_config.json after use. <br>
Risk: Worker requests are sent to the configured model API endpoint, so an unexpected base_url could route sensitive task content to an unintended service. <br>
Mitigation: Verify the configured base_url before dispatch and review any mounted third-party skills before allowing them into the swarm. <br>
Risk: Parallel worker outputs may contain incorrect or conflicting analysis that could affect the final synthesis. <br>
Mitigation: Review the generated worker_*.md files and the synthesized response before acting on high-impact recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lawliet-ai/hive-commander) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown synthesis with worker Markdown files and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fixed five-worker dispatch with a 120-second per-worker API timeout.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
