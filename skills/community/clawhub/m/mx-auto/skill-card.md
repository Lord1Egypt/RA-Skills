## Description: <br>
mx-auto is a local Runtime automation entrypoint for App triggers, read-only browser sandbox inspection, and local script execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiming1001](https://clawhub.ai/user/yiming1001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list or run Runtime triggers, inspect existing browser sandbox tabs and snapshots without changing browser state, and list, show, or run local App scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Runtime admin credentials and contacts localhost Runtime APIs. <br>
Mitigation: Install only when local Runtime automation is needed, verify the publisher, and keep Runtime admin tokens out of logs and shared outputs. <br>
Risk: Trigger and script execution can change local app state. <br>
Mitigation: Review the exact trigger or script name and input JSON before execution, and prefer list/show commands when inspecting available actions. <br>
Risk: Cloud command and cloud-token handling paths are under-disclosed in the release evidence. <br>
Mitigation: Review or remove the cloud dispatch script and avoid storing cloud tokens in preferences unless that remote command path is intentionally accepted. <br>


## Reference(s): <br>
- [Trigger Workflow](references/triggers.md) <br>
- [Sandbox Workflow](references/sandbox.md) <br>
- [Scripts Workflow](references/scripts.md) <br>
- [mx-auto Learning Guide](references/learning-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and optional JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route local Runtime operations that read admin credentials, inspect existing browser tabs, or execute exact-match triggers and scripts.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
