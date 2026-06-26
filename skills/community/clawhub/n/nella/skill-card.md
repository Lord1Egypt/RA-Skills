## Description: <br>
Nella provides codebase-aware search, indexing, context tracking, assumption management, and dependency checks for AI coding agents working in non-trivial repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pablomanjarres](https://clawhub.ai/user/pablomanjarres) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use Nella to ground repository questions in indexed code, find definitions and call sites, preserve session context, record assumptions, and check dependency drift before making or finalizing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository snippets, search results, and usage metadata may be sent to configured remote embedding, reranking, or hosted MCP services. <br>
Mitigation: Use local-only or tightly scoped provider settings for private repositories, and review remote service configuration before indexing sensitive code. <br>
Risk: Tokens and persistent session context may be stored locally or written into agent configuration files. <br>
Mitigation: Avoid broad credentials, rotate API keys if they are written to config files, and restrict local credential storage to trusted workspaces. <br>
Risk: Self-hosted server mode can require sensitive service-role credentials and may expose an HTTP MCP endpoint if bound broadly. <br>
Mitigation: Use service-role credentials only for deliberate self-hosting, keep hosted servers bound to localhost unless intentional, and pin the npm package version. <br>


## Reference(s): <br>
- [ClawHub Nella release page](https://clawhub.ai/pablomanjarres/nella) <br>
- [Nella README](README.md) <br>
- [Nella skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, command examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce repository search results, session context summaries, recorded assumptions, dependency status, and setup guidance.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
