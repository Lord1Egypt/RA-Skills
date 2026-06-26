## Description: <br>
Performs private, multi-round deep web searches excluding Google/Bing, synthesizes results with citations, and does not retain user data or logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romancircus](https://clawhub.ai/user/romancircus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and external users use this skill to run self-hosted SearXNG searches and generate multi-source Markdown research reports with citations from fetched web pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and fetched page requests can still leave the local machine through external search engines and visited websites. <br>
Mitigation: Use the skill only for searches suitable for those services, and route traffic through an approved VPN when stronger network privacy is required. <br>
Risk: The Docker service can persist after setup and may be reachable beyond localhost depending on host and Docker networking. <br>
Mitigation: Bind the service to 127.0.0.1 where possible, review Docker exposure before use, and stop or remove the container when finished. <br>
Risk: Using the floating searxng/searxng:latest image can change runtime behavior across installs. <br>
Mitigation: Pin the SearXNG image to a reviewed version before deployment. <br>
Risk: Remote autocomplete may disclose sensitive partial queries. <br>
Mitigation: Disable remote autocomplete for sensitive use cases. <br>


## Reference(s): <br>
- [Private Deep Search ClawHub listing](https://clawhub.ai/romancircus/privatedeepsearch-melt) <br>
- [SearXNG project](https://github.com/searxng/searxng) <br>
- [Privacy guide](docs/PRIVACY.md) <br>
- [Troubleshooting guide](docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports with source citations, plus command-line search output and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deep research runs up to five search iterations, fetches page content concurrently, and limits each source to a configured word cap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
