## Description: <br>
Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujiang817](https://clawhub.ai/user/liujiang817) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search web, image, news, IT, and science results through a configured SearXNG instance while keeping the agent workflow lightweight and dependency-free. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are visible to the configured SearXNG instance and may be visible to upstream engines. <br>
Mitigation: Configure scripts/searxng.ini to use an instance you control or explicitly trust, and avoid sensitive queries on public instances. <br>
Risk: HTTPS certificate verification is disabled by the script. <br>
Mitigation: Use the skill only with trusted local or private-network instances unless the script is updated to enforce TLS verification. <br>
Risk: The bundled configuration points to a specific SearXNG URL that may not be appropriate for every user. <br>
Mitigation: Review and edit scripts/searxng.ini before installing or running searches. <br>


## Reference(s): <br>
- [SearXNG](https://searxng.org) <br>
- [SearXNG installation guide](https://docs.searxng.org/admin/installation.html) <br>
- [SearXNG documentation](https://docs.searxng.org/) <br>
- [ClawHub skill page](https://clawhub.ai/liujiang817/my-searxng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text search-result tables by default, with optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to 10 results; supports category, language, result-count, and time-range filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
