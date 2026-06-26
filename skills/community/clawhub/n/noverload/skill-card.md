## Description: <br>
Give your agent a searchable knowledge brain - semantic search, topic synthesis, and action tracking across your saved YouTube videos, articles, Reddit threads, X posts, and PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drewautomates](https://clawhub.ai/user/drewautomates) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users connect an agent to their Noverload account to search saved content, retrieve source details, synthesize topics, extract frameworks, and manage action items. The skill is intended for knowledge retrieval and organization across saved videos, articles, Reddit threads, X posts, and PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a third-party MCP package and authenticates with a personal Noverload access token. <br>
Mitigation: Install only if Noverload and the noverload-mcp npm package are trusted, use a revocable token, and do not commit or share the token. <br>
Risk: Retrieved library content may be exposed to the agent's working context. <br>
Mitigation: Review what account content the agent can access and keep the default readOnly:true mode unless saving or task updates are required. <br>


## Reference(s): <br>
- [Noverload OpenClaw Integration](https://noverload.com/openclaw) <br>
- [Noverload MCP Documentation](https://noverload.com/docs/mcp) <br>
- [ClawHub Skill Listing](https://clawhub.ai/drewautomates/noverload) <br>
- [Publisher Profile](https://clawhub.ai/user/drewautomates) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline prompts and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can retrieve account content into the agent context and can optionally save or update content when configured with readOnly:false.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
