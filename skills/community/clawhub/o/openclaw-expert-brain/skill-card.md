## Description: <br>
OpenClaw Expert Brain lets agents query a curated OpenClaw NotebookLM knowledge base for installation, configuration, skills, troubleshooting, multi-agent, cron, security, and related guidance in Spanish or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[radelqui](https://clawhub.ai/user/radelqui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to ask documentation and operational questions about OpenClaw installation, configuration, custom skills, ClawHub, troubleshooting, multi-agent workflows, cron, security, MCP, and mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user questions to NotebookLM through the external nlm CLI and a Google/nlm session. <br>
Mitigation: Avoid sending secrets or private data in prompts, and install only where use of notebooklm-mcp-cli and NotebookLM is acceptable. <br>
Risk: Answers may include operational or security guidance that affects OpenClaw deployments. <br>
Mitigation: Verify important security or operational advice against primary OpenClaw sources before applying it. <br>


## Reference(s): <br>
- [OpenClaw Expert Brain on ClawHub](https://clawhub.ai/radelqui/openclaw-expert-brain) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown answers returned through the nlm CLI, with commands or configuration snippets when relevant.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent to NotebookLM through an external nlm CLI session and can answer in Spanish or English.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
