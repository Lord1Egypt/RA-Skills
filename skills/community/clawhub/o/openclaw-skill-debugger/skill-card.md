## Description: <br>
Identifies common OpenClaw AgentSkill installation, configuration, dependency, and script execution issues and guides agents through debugging and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alessandropcostabr](https://clawhub.ai/user/alessandropcostabr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to debug OpenClaw AgentSkills that fail to install, run scripts, document dependencies, or behave consistently across environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic scripts can expose file paths or dependency names from the target skill in the agent session. <br>
Mitigation: Run the scripts only against skill directories you intend to inspect and avoid sharing diagnostic output that contains sensitive paths or environment details. <br>
Risk: Debugging untrusted or newly installed skills may involve inspecting third-party content. <br>
Mitigation: Use an isolated environment when diagnosing untrusted skills before promoting them to a production workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alessandropcostabr/openclaw-skill-debugger) <br>
- [Common OpenClaw skill issues](references/common-skill-issues.md) <br>
- [OpenClaw skill debugging workflow](references/debug-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and diagnostic findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may print matched file paths and dependency names from the target skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
