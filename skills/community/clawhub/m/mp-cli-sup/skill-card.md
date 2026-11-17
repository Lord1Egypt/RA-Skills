## Description:

Guides live WeChat Mini Program debugging through a persistent vince-mp CLI session, including runtime inspection, UI actions, diagnostics, and log correlation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and troubleshoot a running WeChat Mini Program, interact with its UI, diagnose connection issues, and correlate client behavior with backend error logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live runtime and backend log access can expose sensitive application or user data.

Mitigation: Use only with a trusted local vince-mp CLI, restrict access to its local state if needed, and obtain action-specific approval before production access.

Risk: Admin tokens may be exposed if pasted into chat or supplied on command lines.

Mitigation: Set the token privately in the agent's launch environment; never paste it into chat or pass it as a CLI argument.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vincentjiang06/skills/mp-cli-sup)
- [CLI contract](references/cli-contract.md)
- [Runtime protocol](rules/runtime-protocol.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Analysis]

**Output Format:** [Text and Markdown with CLI commands and diagnostic findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI operations return JSON evidence; actions may require user authorization.]

## Skill Version(s):

0.3.0 (source: server release metadata, skill frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
