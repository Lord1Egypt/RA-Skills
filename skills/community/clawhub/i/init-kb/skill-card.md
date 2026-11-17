## Description:

Init Kb initializes or updates a project knowledge base by scraping websites and social profiles with Firecrawl, guiding the user through gap-filling questions, and producing structured on-demand markdown references for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevjade](https://clawhub.ai/user/kevjade)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to build or refresh a structured knowledge base for a business, project, or client. The generated KB gives downstream agents project context, voice guidance, business intelligence, guardrails, and on-demand source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle Firecrawl API keys through chat input or a local .firecrawl/api-key.txt file.

Mitigation: Prefer FIRECRAWL_API_KEY in the environment or a secret manager, avoid pasting secrets into shared chats, and keep .firecrawl out of version control.

Risk: The skill can append knowledge-base loading guidance to persistent agent configuration files.

Mitigation: Review proposed AGENTS.md or CLAUDE.md changes before accepting them, especially in shared or multi-project workspaces.

Risk: The skill sends provided URLs to Firecrawl and stores scraped content locally.

Mitigation: Scrape only public URLs you are comfortable sending to Firecrawl and retaining in local project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevjade/skills/init-kb)
- [Firecrawl API endpoint](https://api.firecrawl.dev/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with conversational guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a project knowledge-base directory, scraped page markdown, Firecrawl cache files, and optional AGENTS.md or CLAUDE.md integration snippets.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
