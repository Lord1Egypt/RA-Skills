## Description:

Real Chrome automation for AI agents - authenticated sessions, PII anonymization, sealed secrets, site adapters, session checkpoints, and video recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enreign](https://clawhub.ai/user/enreign)

### License/Terms of Use:

MIT

## Use Case:

Developers, power users, and automation engineers use this skill to guide agents through real Chrome workflows, including logged-in browser tasks, frontend verification, form filling, session recovery, secure handling of sensitive pages, and browser-session recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an MCP server access to real logged-in Chrome profiles and persistent browser sessions.

Mitigation: Use a dedicated agent Chrome profile, set strict allowed_domains, keep retention short, and enable anonymize:true for sensitive pages.

Risk: Credentials, webhook URLs, or sensitive values could be exposed through shared KV state or unsafe automation flows.

Mitigation: Use sealed secrets or a proper secret manager instead of storing secrets in shared KV, and review audit logs for sensitive workflows.

Risk: Included selector-debug scripts and scheduled automation examples can be unsafe when used with untrusted selectors or temporary scripts.

Mitigation: Avoid selector-debug scripts with untrusted selectors, do not schedule /tmp scripts in cron, and review scripts before use.

Risk: Registering an unverified Pagerunner binary as an MCP server can expand local automation risk.

Mitigation: Pin and verify the Pagerunner binary before registering it as an MCP server.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/enreign/skills/pagerunner-skill)
- [Repository (metadata)](https://github.com/Enreign/pagerunner-skill)
- [Quick Start Guide](SKILL.md)
- [Pagerunner Tools Reference](REFERENCE.md)
- [Security, Privacy, and Guardrails](SECURITY.md)
- [Advanced Topics](ADVANCED.md)
- [Video Recording Guide](RECORDING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, shell, JSON, and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs operational guidance for agent use of Pagerunner MCP tools; no model-generated media or structured dataset is produced by the skill itself.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
