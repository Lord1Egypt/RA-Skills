## Description: <br>
Provides package-registry metadata workflows for npm, PyPI, and Maven Central through Pilot Protocol service agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query package metadata, versions, maintainers, dependencies, and recent releases across npm, PyPI, and Maven Central via Pilot Protocol service agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may include secrets, private package names, or sensitive project context that traverse the Pilot overlay or are used in generated summaries. <br>
Mitigation: Avoid sending secrets or sensitive dependency context, and treat /summary output as externally processed prose. <br>
Risk: The skill depends on a trusted Pilot Protocol setup, pilotctl binary, daemon, and network 9 connectivity. <br>
Mitigation: Install and use it only in a trusted Pilot Protocol environment with the expected pilotctl binary and daemon configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-service-agents-packages) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Publisher skill index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May point the agent to asynchronous Pilot Protocol inbox responses and Gemini-generated summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
