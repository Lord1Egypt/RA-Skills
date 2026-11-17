## Description:

Hermes Guard monitors AI agent output quality with completion gating, missing-tool fallback, and correction-as-code feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lybang972314](https://clawhub.ai/user/lybang972314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Hermes Guard to audit AI agent outputs, block low-quality responses, create correction rules, and handle missing-tool situations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises automatic persistent changes to agent instruction files without clear approval, rollback, or scoping.

Mitigation: Use it first in a disposable or version-controlled project, inspect diffs, and require review before changes are applied to AGENTS.md or equivalent instruction files.

Risk: Generated tool stubs or registrations could expand agent behavior beyond the user's intended scope.

Mitigation: Review proposed tool definitions, registrations, and generated code before enabling them in production workflows.

Risk: Running the package in production repositories could modify files or expose sensitive workspace context.

Mitigation: Pin and verify the Python package version, avoid repositories containing credentials, and keep production use behind normal change-control gates.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/lybang972314/hermes-guard)
- [ClawHub skill page](https://clawhub.ai/lybang972314/skills/hermes-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with shell commands and Python or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose correction rules and tool stubs for review.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
