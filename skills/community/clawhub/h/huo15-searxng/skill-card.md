## Description: <br>
Huo15 SearXNG deploys a local self-hosted SearXNG search service with Docker Compose and configures OpenClaw to use it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, check, and remove a local SearXNG instance for private web search integration with OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and manages a persistent local SearXNG Docker service. <br>
Mitigation: Review the generated Docker Compose configuration and port binding before use, and run the status script after installation. <br>
Risk: The install and uninstall scripts edit ~/.zshrc to add or remove SEARXNG_BASE_URL. <br>
Mitigation: Inspect shell-profile changes before and after execution, then reload the shell profile only after confirming the expected value. <br>
Risk: The Docker Compose configuration pulls the searxng/searxng:latest image. <br>
Mitigation: Pin the image tag or digest in the generated Compose file when reproducibility or supply-chain review is required. <br>
Risk: Uninstall may leave Docker state behind if the container name or Compose state differs from the script's expectations. <br>
Mitigation: After uninstall, verify with docker ps -a and inspect ~/docker/searxng to confirm the service and local data were removed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/huo15-searxng) <br>
- [SearXNG Documentation](https://docs.searxng.org/) <br>
- [OpenClaw SearXNG Configuration](https://docs.openclaw.ai/tools/searxng-search) <br>
- [SearXNG GitHub](https://github.com/searxng/searxng) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Docker Compose files, local SearXNG configuration, and a SEARXNG_BASE_URL shell-profile entry when the install script is run.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
