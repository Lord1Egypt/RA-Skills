## Description: <br>
Search and explore 500,000+ artworks in the Metropolitan Museum of Art's open-access collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search the Met Museum open-access collection, retrieve detailed artwork records, list departments, and build educational or recommendation workflows from structured art metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security guidance notes that some listed maintainer workflows can affect users or public content. <br>
Mitigation: Install only when those workflows are intended for the agent, and review any moderation or public-content actions before execution. <br>
Risk: The security guidance notes that autoreview workflows may default to a full-access nested review mode unless disabled. <br>
Mitigation: Disable or constrain nested autoreview access unless full-access review behavior is explicitly required. <br>


## Reference(s): <br>
- [Pipeworx Art Pack](https://pipeworx.io/packs/art) <br>
- [Pipeworx Art MCP Endpoint](https://gateway.pipeworx.io/art/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-art) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON responses with artwork metadata, plus Markdown guidance with command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented example and an MCP remote endpoint; artwork records can include image URLs, object URLs, departments, culture, period, and medium.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
