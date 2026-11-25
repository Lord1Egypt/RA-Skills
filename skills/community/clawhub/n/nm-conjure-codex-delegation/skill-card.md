## Description:

Delegates to the OpenAI Codex CLI (codex exec)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when delegation-core selects Codex, routing a coding or analysis task to the OpenAI Codex CLI for a delegated result or second opinion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File contents included in a delegation may be sent to OpenAI.

Mitigation: Review the prompt and selected files before delegation, and exclude sensitive content you do not want sent to that service.

Risk: Delegation depends on Codex credentials and an external CLI, which may use account quota or incur costs.

Mitigation: Check credential handling and use a suitably scoped credential; confirm the CLI account, quota, and costs are acceptable before running it, especially with untrusted repository code.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conjure-codex-delegation)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Markdown delegation report; Codex CLI text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The result depends on the delegated prompt and supplied files; delegation reports are saved as timestamped Markdown files.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
