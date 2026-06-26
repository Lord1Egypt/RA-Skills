## Description: <br>
Guides developers in creating Claude Code hooks with security-first design for validation and enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to design, validate, test, and scope Claude Code and Claude Agent SDK hooks for security enforcement, observability, context injection, automation, and performance-sensitive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook examples can log sensitive tool inputs or outputs if copied without adaptation. <br>
Mitigation: Use metadata-only audit records where possible, and redact secrets before writing logs. <br>
Risk: HTTP hook examples can send hook payloads to external services. <br>
Mitigation: Use only trusted endpoints and minimize or redact payloads before transmission. <br>
Risk: Broad hook scopes can affect more sessions or projects than intended. <br>
Mitigation: Prefer project or plugin scope over global scope unless the hook is intentionally universal. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-abstract-hook-authoring) <br>
- [Source Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks) <br>
- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-agent-sdk) <br>
- [Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings) <br>
- [Hook Types Overview](artifact/modules/hook-types.md) <br>
- [Testing Hooks](artifact/modules/testing-hooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples should be reviewed and adapted before use.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata and target metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
