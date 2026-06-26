## Description: <br>
Search and look up books via Open Library — titles, authors, ISBNs, and cover images from the world's largest open book catalog <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search book records, look up ISBN metadata, retrieve author details, and enrich reading or recommendation workflows with Open Library data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book search terms, ISBNs, and author lookup requests are sent to the Pipeworx gateway. <br>
Mitigation: Avoid entering sensitive personal data in searches unless sending it to the Pipeworx/Open Library gateway is acceptable. <br>
Risk: The optional MCP configuration runs mcp-remote@latest from npm through npx. <br>
Mitigation: Review and pin the MCP dependency or approve the latest-package behavior before using the optional MCP setup in controlled environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-books) <br>
- [Pipeworx Books Homepage](https://pipeworx.io/packs/books) <br>
- [Pipeworx Books MCP Gateway](https://gateway.pipeworx.io/books/mcp) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON MCP configuration; runtime calls return structured book metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests, ISBNs, and author lookup inputs are sent to the Pipeworx/Open Library gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
