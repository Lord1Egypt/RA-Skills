## Description:

Reduce MCP token costs by up to 94% and enforce least-privilege tool access by creating YAML policies that control which MCP tools each agent can see and call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanpantheon](https://clawhub.ai/user/ivanpantheon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reduce MCP tool-schema token overhead and create least-privilege tool access policies for agents. It provides guidance, commands, and YAML examples for checking, generating, applying, monitoring, and rolling back Navil policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Artifact checksums do not match the bundled release evidence.

Mitigation: Verify the release package and file hashes before installation, and do not rely on the bundled checksums until the mismatch is resolved.

Risk: Install guidance uses an unpinned pip package and may bypass system package protections.

Mitigation: Install Navil in an isolated environment such as pipx or a virtual environment, and pin and verify the package version before use.

Risk: Policy files can affect which MCP tools agents can see and call.

Mitigation: Review ~/.navil/policy*.yaml before enabling the policy engine for agent tool access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivanpantheon/skills/navil-policy)
- [Navil Homepage](https://github.com/navilai/navil)
- [Policy Documentation](https://github.com/navilai/navil#tool-scoping)
- [Community Policy Templates](https://github.com/navilai/navil/tree/main/policies)
- [Token Cost Guide](https://navil.ai/docs/token-costs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include policy recommendations, Navil CLI commands, and YAML snippets for agent tool scoping.]

## Skill Version(s):

1.0.2 (source: frontmatter, artifact/skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
