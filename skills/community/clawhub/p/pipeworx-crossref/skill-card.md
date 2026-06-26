## Description: <br>
Search academic papers by keyword, look up metadata by DOI, and fetch journal info via Crossref <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to search scholarly works, resolve DOI metadata, look up journal information by ISSN, and support literature review, citation verification, bibliography, and research trend workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, DOIs, and ISSNs may be sent through Pipeworx when the skill is used. <br>
Mitigation: Avoid submitting private, sensitive, or embargoed research details unless sharing them with the Pipeworx service is acceptable. <br>
Risk: The optional MCP setup uses an npm-based remote connector to reach the Pipeworx endpoint. <br>
Mitigation: Review and approve the MCP remote configuration before enabling it in an agent client. <br>


## Reference(s): <br>
- [Pipeworx Crossref Pack](https://pipeworx.io/packs/crossref) <br>
- [Pipeworx Crossref MCP Endpoint](https://gateway.pipeworx.io/crossref/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-crossref) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with scholarly work, DOI, and journal metadata, plus Markdown guidance with command and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented example and can be connected through an MCP remote endpoint; returned metadata can include titles, authors, DOIs, publication dates, citation counts, abstracts, references, funders, licenses, publishers, subject areas, and coverage dates.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
