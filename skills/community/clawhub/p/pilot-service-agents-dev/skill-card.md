## Description: <br>
Developer-platform metadata for GitHub, Docker Hub, crates.io, and other ecosystem registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover public developer-platform service agents and query repository, package, container image, and release metadata through Pilot Protocol agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the local Pilot Protocol setup, pilotctl binary, and reachable overlay service agents, so behavior depends on that trusted environment. <br>
Mitigation: Install it only in trusted Pilot Protocol environments and verify pilotctl, daemon/network state, and the target agent contract before use. <br>
Risk: Queries intended for public metadata could expose sensitive project names or authenticated registry details if operators include private data. <br>
Mitigation: Use it for public metadata lookups only, and avoid private repositories, private package names, credentials, tokens, or authenticated registry data. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-dev) <br>
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only metadata queries depend on pilotctl, a running Pilot Protocol daemon, network 9, and reachable service agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
