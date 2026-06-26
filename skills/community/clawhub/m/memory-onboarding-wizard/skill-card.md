## Description: <br>
Bootstrap a new OpenClaw agent's memory system in one command by setting up MEMORY.md, daily memory files, HEARTBEAT.md, and USER.md after asking three quick questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize a local agent memory workspace with starter memory, daily note, heartbeat, and user profile files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: USER.md stores basic personal context for future agent sessions. <br>
Mitigation: Review USER.md after setup and remove sensitive personal details that should not be loaded by future agents. <br>
Risk: The wizard creates local memory files in the configured workspace. <br>
Mitigation: Confirm the workspace path before running the wizard, especially when using the --workspace option. <br>
Risk: The starter HEARTBEAT.md includes default reminder checks that may not match the user's preferences. <br>
Mitigation: Review HEARTBEAT.md after setup and remove default heartbeat tasks that are not wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stevojarvisai-star/memory-onboarding-wizard) <br>
- [GetAgentIQ](https://getagentiq.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or preserves local MEMORY.md, memory/YYYY-MM-DD.md, HEARTBEAT.md, and USER.md files in the selected workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
