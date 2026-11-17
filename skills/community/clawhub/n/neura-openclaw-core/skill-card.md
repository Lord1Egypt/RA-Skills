## Description:

Use when an OpenClaw-style or local autonomous computer-use agent needs a single Neura Relay preflight workflow for messages, file changes, browser submits, shell commands, package or publisher changes, workflow state, memory writes, or data exports before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neurarelay](https://clawhub.ai/user/neurarelay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare refs-only Action Cards and interpret Relay Decision Receipts before consequential local agent actions. It is intended for external and developer-facing workflows that need a governed checkpoint before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on the user environment trusting the Neura Relay package and route.

Mitigation: Confirm the selected package, route, publisher handle, and local policy before operational use.

Risk: The skill is a community example and could be mistaken for an official OpenClaw or ClawHub integration.

Mitigation: Preserve the no-official-claim boundary and require explicit authority refs for package, publisher, and ClawHub-facing actions.

Risk: Consequential actions could expose private payloads if raw content is placed in an Action Card.

Mitigation: Use refs-only Action Cards and omit message bodies, file contents, raw commands, credentials, customer data, secrets, tokens, passwords, and private payloads.

## Reference(s):

- [Neura Relay OpenClaw Scenario Corpus](references/scenario-corpus.md)
- [ClawHub skill page](https://clawhub.ai/neurarelay/skills/neura-openclaw-core)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text with refs-only Action Card fields and Decision Receipt interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute local actions; returns developer-owned next steps and missing refs.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
