## Description: <br>
Init Kb guides an agent through creating or refreshing a project knowledge base by collecting user input, scraping approved URLs with Firecrawl, analyzing the results, and writing structured markdown reference files for future agent work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kevjade](https://clawhub.ai/user/Kevjade) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to bootstrap or update a structured project, business, or client knowledge base for future agent work. It is intended for workflows where the user can approve scraping, answer targeted questions, and review generated workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected URLs and profile content to Firecrawl during scraping. <br>
Mitigation: Review every URL before scraping and only use the skill when external processing by Firecrawl is acceptable. <br>
Risk: The skill may store a Firecrawl API key in .firecrawl/api-key.txt. <br>
Mitigation: Prefer setting FIRECRAWL_API_KEY yourself; if a local key file is used, protect it and ensure it is ignored by version control. <br>
Risk: The skill can make persistent workspace changes, including knowledge base files and AGENTS.md or CLAUDE.md snippets. <br>
Mitigation: Require a diff before accepting changes to generated files or agent configuration files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Kevjade/init-kb) <br>
- [Firecrawl API](https://api.firecrawl.dev/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, shell commands, configuration snippets, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent workspace files, including knowledge base markdown, scraped site-content markdown, Firecrawl cache files, and AGENTS.md or CLAUDE.md guidance snippets.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
