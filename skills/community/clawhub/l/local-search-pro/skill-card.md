## Description: <br>
Free Brave API alternative for OpenClaw with local SearXNG-backed web search, no API key requirement, and localhost-only deployment by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipepi](https://clawhub.ai/user/pipepi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and query a local SearXNG search service as a no-key web search alternative. It is useful when users want local default binding, safe search and rate limiting enabled by default, and shell-scripted setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install script creates a persistent local Docker service that can continue running after the agent exits and restart on reboot. <br>
Mitigation: Install only when a persistent local service is acceptable, and remove it with docker rm -f searxng-local when it is no longer needed. <br>
Risk: Changing SEARXNG_BASE_URL can direct searches to a non-default service. <br>
Mitigation: Leave SEARXNG_BASE_URL unset unless the target service is trusted. <br>
Risk: Development mode disables safe search and the request limiter. <br>
Mitigation: Avoid dev mode for normal use; use the default install mode for safe search and limiter protections. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pipepi/local-search-pro) <br>
- [Publisher profile](https://clawhub.ai/user/pipepi) <br>
- [Local SearXNG endpoint](http://127.0.0.1:8080) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output is limited to the first 10 SearXNG results.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
