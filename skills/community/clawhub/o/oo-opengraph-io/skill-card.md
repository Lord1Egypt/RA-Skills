## Description: <br>
OpenGraph.io helps agents inspect OpenGraph.io connector schemas and run URL metadata, scrape, raw HTML, and screenshot actions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to retrieve site metadata, fetch page HTML, or capture webpage screenshots through OpenGraph.io without handling raw API tokens directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected OpenGraph.io credentials through OOMOL. <br>
Mitigation: Confirm the publisher and connected OpenGraph.io account before installation or use. <br>
Risk: URL scrape and screenshot requests may send private or internal page URLs through the OOMOL/OpenGraph.io service. <br>
Mitigation: Avoid using the skill on sensitive internal or private pages unless that routing is intended and approved. <br>
Risk: Connector action parameters can affect caching, proxying, rendering, retries, viewport, delay, and element selection. <br>
Mitigation: Inspect the live connector schema before constructing payloads and review unusual scrape or screenshot options before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-opengraph-io) <br>
- [OpenGraph.io homepage](https://www.opengraph.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON from the oo CLI when actions are executed with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
