## Description:

Huo15 Skills is a ClawHub/OpenClaw skill bundle for enterprise Word and PDF document generation, knowledge-base workflows, learning support, multi-agent coordination, memory curation, planning, verification, exploration, web scraping, SearXNG deployment, and presentation generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this bundle to add document generation, knowledge-base maintenance, local search deployment, web scraping, multi-agent coordination, and structured planning or verification workflows to an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submitted artifact includes more than the office-document generator, including credential-using, Docker, NotebookLM, scraper, knowledge-base, and agent-configuration workflows.

Mitigation: Review the whole bundle before installation and remove unrelated nested skills when only Word or PDF output is needed.

Risk: The security summary identifies under-disclosed credential use and agent-configuration persistence.

Mitigation: Run configuration-generating scripts only in a reviewed or disposable workspace, and inspect generated files before merging them into an active OpenClaw workspace.

Risk: The security guidance flags an Odoo TLS verification issue before use with stored Odoo credentials.

Mitigation: Do not use stored Odoo credentials with the document scripts until TLS verification is corrected and confirmed.

Risk: Docker, NotebookLM, scraper, and knowledge-base commands can change local services, send requests, or write local files.

Mitigation: Inspect each script and required permission before running it, especially install, sync, scrape, and compile commands.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaobod1/skills/huo15-skills)
- [Artifact README](artifact/README.md)
- [Office document skill definition](artifact/SKILL.md)
- [State Administration for Market Regulation model contract text library](https://htsfwb.samr.gov.cn/)
- [SearXNG documentation](https://docs.searxng.org/)
- [Qichacha MCP service](https://agent.qcc.com/mcp)
- [WeCom developer documentation example](https://developer.work.weixin.qq.com/document/path/91756)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, generated documents or presentations, and script-produced files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows can run local scripts, call APIs, write workspace configuration, sync an Obsidian vault, or deploy a local Docker service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
