## Description:

Install and use the public beta jd-drama CLI to operate JianDan short-drama projects, scripts, uploaded imports, assets, storyboards, videos, brands, material libraries, and task diagnostics from Codex, Code, OpenClaw, or other agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyengine-ai](https://clawhub.ai/user/flyengine-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to let an agent operate JianDan short-drama projects through the jd-drama CLI while keeping production writes behind dry-run previews and explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through actions against JianDan production projects and real quotas.

Mitigation: Install only when production operation is intended, review each dry-run output, and approve live commands only when the exact action is acceptable.

Risk: Creation, parsing, generation, upload, and edit workflows may affect real project data or consume credits.

Mitigation: Keep write actions gated by --dry-run followed by explicit user approval with --confirm.

Risk: Credentials, authorization codes, tokens, or local configuration contents could be exposed if provided to the agent.

Mitigation: Use browser authorization and do not provide passwords, tokens, authorization codes, or config-file contents to the agent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyengine-ai/skills/jd-drama)
- [JianDan Service](https://jiandan.flyengine.cn/)
- [JianDan API Endpoint](https://jiandan.flyengine.cn/api)
- [Skill Workflow](SKILL.md)
- [README](README.md)
- [NOTICE](NOTICE)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing instructions for jd-drama CLI workflows; live write actions require dry-run review and explicit confirmation.]

## Skill Version(s):

1.0.0-beta.6 (source: changelog, released 2026-09-17; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
