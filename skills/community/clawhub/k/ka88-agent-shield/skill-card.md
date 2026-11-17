## Description:

Professional security audit for AI agents. Checks URLs for SSRF, analyzes content for prompt injection, validates commands for shell injection, integrates with skill-scanner for deep analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danilka88](https://clawhub.ai/user/danilka88)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to audit URLs, external content, commands, and agent skill files for common AI-agent security risks before continuing work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive local state such as shell history, limited environment data, SSH metadata, and agent configuration metadata during audits.

Mitigation: Review the skill before global installation, run audits in a scoped workspace, avoid exposing secrets in shell history or environment variables, and limit access to sensitive directories.

Risk: Full scans may send scan targets to a configured LLM endpoint.

Mitigation: Use a local-only, validated LM Studio endpoint when LLM scanning is needed, or use the quick scan path for pattern-based local checks without an LLM.

Risk: The optional install path can install an external scanner dependency.

Mitigation: Avoid the install option unless the scanner package and version are pinned and trusted in the deployment environment.

Risk: Persistent memory recording of blocked attempts and risky operations may retain sensitive operational details.

Mitigation: Disable or tightly scope persistent memory recording where audit logs could contain secrets, internal URLs, or private command context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danilka88/skills/ka88-agent-shield)
- [Publisher profile](https://clawhub.ai/user/danilka88)
- [Project homepage](https://github.com/Danilka88/ka88-agent-shield)
- [Repository](https://github.com/Danilka88/ka88-agent-shield.git)
- [Support](https://github.com/Danilka88/ka88-agent-shield/issues)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples, checklists, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces security findings, audit reports, block or warn decisions, and optional local scan commands.]

## Skill Version(s):

1.0.0 (source: release metadata, skill frontmatter, clawhub.json, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
