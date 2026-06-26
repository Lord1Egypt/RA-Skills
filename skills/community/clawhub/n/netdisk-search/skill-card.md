## Description: <br>
NetDisk Search lets an agent search multiple cloud-storage and net-disk sources through a configured search API, filter results, check share links, and help deploy the search service with Docker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godzx001-dot](https://clawhub.ai/user/godzx001-dot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search net-disk resources, filter results by provider or keyword, check whether shared links are still valid, and deploy or connect to the supporting search API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can deploy and expose a Docker-based search API service. <br>
Mitigation: Use a trusted local endpoint where possible, bind or firewall the service, enable authentication with a throwaway password when exposing it, and review deployment commands before execution. <br>
Risk: Search terms, share links, and extraction passwords may be sent to a configured API endpoint. <br>
Mitigation: Avoid remote HTTP APIs for private links or extraction codes, and confirm the API endpoint before running searches or link checks. <br>
Risk: The security review marked the release suspicious because API exposure and data-handling boundaries require review. <br>
Mitigation: Install only when the user intends to run this net-disk search service and understands the Docker and API exposure described in the security guidance. <br>


## Reference(s): <br>
- [NetDisk Search on ClawHub](https://clawhub.ai/godzx001-dot/netdisk-search) <br>
- [API Reference](references/api-reference.md) <br>
- [Upstream pansou project](https://github.com/fish2018/pansou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown tables, JSON responses, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud-storage URLs, extraction passwords, result metadata, Docker deployment commands, and API endpoint configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
