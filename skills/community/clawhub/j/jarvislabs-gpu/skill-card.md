## Description: <br>
Agent guide for running and monitoring GPU experiments with the jl CLI on JarvisLabs.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladiator07](https://clawhub.ai/user/gladiator07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, monitor, troubleshoot, and clean up JarvisLabs GPU instances and managed training runs through the jl CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to use JarvisLabs credentials or authentication tokens. <br>
Mitigation: Use a protected JL_API_KEY or interactive jl setup authentication, and avoid exposing tokens in command history or shared logs. <br>
Risk: The skill can guide actions that create, pause, destroy, or modify GPU resources, filesystems, SSH access, uploads, downloads, and long-running jobs. <br>
Mitigation: Review resource-changing commands before execution, monitor billing-impacting runs, and pause or destroy unused instances after work completes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gladiator07/jarvislabs-gpu) <br>
- [JarvisLabs CLI Documentation](https://docs.jarvislabs.ai/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational guidance for authentication, GPU instance lifecycle, managed runs, logs, file transfer, and cleanup.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
