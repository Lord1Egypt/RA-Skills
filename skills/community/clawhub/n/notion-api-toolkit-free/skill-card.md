## Description: <br>
Notion Api Toolkit Free helps agents connect to Notion through hosted OAuth and CLI-driven API operations for page search, database queries, block management, user lookup, and basic read/write workspace actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and small teams use this skill to let an agent query Notion pages and databases, inspect blocks and users, and perform explicitly confirmed basic writes in an authorized workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive CLI-based read and write access to Notion workspaces. <br>
Mitigation: Use it only for explicit Notion tasks, grant the minimum workspace permissions needed, and confirm every page, database, block, and connection target before any write. <br>
Risk: Broad triggers and unrelated network diagnostics may cause the agent to run commands outside the intended Notion workflow. <br>
Mitigation: Do not run local diagnostics or unrelated shell commands unless the user specifically requests troubleshooting. <br>
Risk: The referenced global npm CLI package could not be confirmed in the public registry during security review. <br>
Mitigation: Verify the CLI package source before global installation and prefer a trusted package source or pinned reviewed artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notion-api-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Notion CLI commands and structured JSON-style results; write operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
