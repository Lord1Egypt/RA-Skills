## Description: <br>
Deploy a sovereign LYGO Protocol Stack community node via Docker or docker compose. Builds lygo-node image, starts health API on port 8787, optional Phase 4 worker profile. No secrets; human approval for registry push. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekoracle](https://clawhub.ai/user/deepseekoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy a local LYGO Protocol Stack community node, check its health and badge endpoints, and optionally run scaled worker profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to build and run Docker assets from an external project repository. <br>
Mitigation: Review the referenced repository, docker compose file, and setup script before running the commands. <br>
Risk: The deployed health API listens on port 8787 and could be exposed beyond local use if networking is changed. <br>
Mitigation: Keep port 8787 bound locally unless intentional exposure is approved and protected with TLS and appropriate access controls. <br>
Risk: Publishing images or deploying to cloud infrastructure can change the release boundary. <br>
Mitigation: Require an explicit user request before any registry push or cloud deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-docker-deploy) <br>
- [LYGO Protocol Stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack) <br>
- [LYGO Protocol Stack documentation](https://deepseekoracle.github.io/lygo-protocol-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local Docker, docker compose, curl health checks, and optional non-Docker commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
