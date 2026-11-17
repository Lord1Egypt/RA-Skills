## Description:

OpenClaw Token Saver provides token monitoring, context slimming, tool optimization, caching, model-control, and local-alternative guidance for reducing OpenClaw token consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jx-76](https://clawhub.ai/user/jx-76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor token usage and choose token-saving actions such as compacting context, limiting tool output, setting token budgets, and using local model alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends a remote installer command for Ollama.

Mitigation: Review and verify installer source and integrity separately before running curl-to-shell commands.

Risk: Automatic compact or reset recommendations can discard useful conversation context if enabled without review.

Mitigation: Keep compact/reset actions as explicit user-approved actions unless the deployment has validated how conversation state is preserved.

Risk: Proxy-forwarding guidance may be unsupported or non-compliant with provider terms.

Mitigation: Use proxy-forwarding only when the relevant provider explicitly permits that workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jx-76/skills/jx76-openclaw-token-saver)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, bash, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes threshold-based recommendations for compacting or resetting context, switching context modes, limiting tools, and configuring token budgets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
