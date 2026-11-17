## Description: <br>
Searches and manages Notion workspace pages and databases, including page lookup, page detail retrieval, page creation, content updates, and database filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to search, read, create, and update Notion pages or query Notion databases through natural-language agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests live Notion workspace read and write access while its privacy, OAuth, and user-control guidance is inconsistent. <br>
Mitigation: Use a Notion integration scoped only to the pages or databases intended for management, avoid broad workspace permissions, and require manual confirmation before create or update actions. <br>
Risk: The artifact claims local-only storage while also describing OAuth, API access, local caching, and network-dependent behavior. <br>
Mitigation: Confirm what data is sent to Notion, what is cached locally, and how OAuth credentials are stored and revoked before using the skill with sensitive workspace content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notion-pages-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown instructions with command examples and structured JSON, text, or CSV result guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition describes single-task operation, optional local caching, and community support.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
