## Description: <br>
Monitor Docker container health, including running status, CPU and memory usage, restart counts, and available image updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laolaoqi](https://clawhub.ai/user/laolaoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to run Docker container health checks and review status, resource usage, restart counts, and image freshness from a shell report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default full health report can run image checks that contact registries and may change local Docker image cache state. <br>
Mitigation: Use targeted read-only checks such as --status, --resources, or --restarts when registry access or image cache changes are not acceptable. <br>
Risk: The skill requires Docker daemon access and may operate against local or remote Docker contexts. <br>
Mitigation: Run it only in an intended Docker context with appropriate permissions, especially before using it on production or remote Docker hosts. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and terminal report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs formatted Docker health reports to stdout; image checks may access registries and update local image cache state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
