## Description: <br>
Coordinates multiple HTTP API robots through adapter generation, task planning, state feedback, and parallel or sequential execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alan1112223331](https://clawhub.ai/user/alan1112223331) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics operators use this skill to let an AI agent generate robot adapters from API documentation, register robots, and coordinate multi-robot task plans. It is intended for robots controlled through HTTP APIs, including manipulator and quadruped examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-planned robot actions may cause unsafe physical motion or manipulation when used with live hardware. <br>
Mitigation: Use simulation or dry-run by default, require human approval before every motion or manipulation command, and verify emergency-stop and workspace safety procedures before live use. <br>
Risk: Unrestricted robot endpoints or actions could allow the agent to control unintended robots or perform unintended operations. <br>
Mitigation: Restrict the allowed robot endpoints and actions, and require authenticated robot APIs in the deployment environment. <br>
Risk: Unpinned or unaudited dependencies can introduce supply-chain or runtime risk. <br>
Mitigation: Pin and audit dependencies before installation in a robotics environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alan1112223331/multi-robot-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [USAGE_GUIDE.md](artifact/USAGE_GUIDE.md) <br>
- [OPENCLAW_INTEGRATION.md](artifact/OPENCLAW_INTEGRATION.md) <br>
- [ADAPTER_FIXES.md](artifact/ADAPTER_FIXES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, shell command snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce robot adapter code, structured task plans, API usage guidance, and execution-result summaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
