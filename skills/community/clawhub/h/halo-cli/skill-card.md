## Description: <br>
Routes general Halo CLI tasks to the right domain workflow for authentication, content, search, operations, moderation, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruibaby](https://clawhub.ai/user/ruibaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to choose the correct Halo CLI workflow, inspect command help, select profiles, request JSON output for automation, and handle destructive operations carefully. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Halo CLI guidance can involve authenticated profiles and account-changing operations, including destructive non-interactive actions. <br>
Mitigation: Review commands before execution, select the intended profile explicitly, prefer JSON output for automation, and use force options only after confirming the requested destructive action. <br>
Risk: Available security evidence is limited to clean scanner context and a single SKILL.md artifact. <br>
Mitigation: Review the artifact and any linked domain skills before installation or use with credentials, network access, background processes, or commands that modify accounts or local files. <br>


## Reference(s): <br>
- [Halo Cli on ClawHub](https://clawhub.ai/ruibaby/halo-cli) <br>
- [Publisher profile](https://clawhub.ai/user/ruibaby) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline Halo CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the halo binary; authenticated tasks may depend on the selected profile, and automation can request JSON output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
