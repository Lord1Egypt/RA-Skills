## Description: <br>
Retrieves structured patent bibliographic metadata from the Eureka patent platform, including titles, abstracts, applicants, inventors, classifications, priority claims, citations, related documents, and estimated expiry dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and patent-focused teams use this skill to retrieve patent bibliography and metadata for one or more patent IDs or publication numbers. It supports lookup of titles, abstracts, applicants, inventors, classifications, priority claims, cited references, related documents, and estimated expiry dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key for patent bibliography lookups. <br>
Mitigation: Configure LINKFOXAGENT_API_KEY only in trusted agent environments and review API calls before use with sensitive patent queries. <br>
Risk: The automatic feedback section may send user comments or intent details to a separate LinkFox endpoint. <br>
Mitigation: Install only if that secondary data flow is acceptable, or remove or disable the feedback instructions before use. <br>


## Reference(s): <br>
- [Eureka API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-eureka-bibliography) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; queries accept patentId or patentNumber, with comma-separated batches up to 100 identifiers.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
