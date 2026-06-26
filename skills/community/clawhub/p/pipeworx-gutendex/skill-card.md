## Description: <br>
Search Project Gutenberg's 70,000+ free ebooks by title, author, topic, or popularity via Gutendex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search Project Gutenberg books, retrieve book details, browse popular or topical public-domain titles, and obtain download links in multiple formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes an external MCP endpoint and demonstrates curl-based network calls. <br>
Mitigation: Review the endpoint and command arguments before use, and enable the MCP server only in environments where outbound access to the Pipeworx Gutendex service is acceptable. <br>


## Reference(s): <br>
- [Pipeworx Gutendex homepage](https://pipeworx.io/packs/gutendex) <br>
- [Pipeworx Gutendex MCP endpoint](https://gateway.pipeworx.io/gutendex/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-gutendex) <br>
- [Publisher profile](https://clawhub.ai/user/b-gutman) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns book metadata, author information, download counts, subjects, and format links from the Gutendex service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
