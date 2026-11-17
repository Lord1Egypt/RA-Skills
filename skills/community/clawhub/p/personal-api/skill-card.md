## Description:

Turn an Obsidian vault into an AI-readable personal identity layer for ME.md, AGENT.md, agent adapters, and an optional Knowledge Palace v2 scaffold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beiyuii](https://clawhub.ai/user/beiyuii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, and individual knowledge workers use this skill to scaffold an Obsidian vault so agents can read identity, behavior, project context, and knowledge-management conventions. It supports full vault setup, identity-only setup, agent onboarding, vault maintenance, and release validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filled-in ME.md and AGENT.md may contain private identity, preference, and collaboration information.

Mitigation: Install only into the intended Obsidian vault, review generated identity files before agent use, and keep filled-in vault content out of public repositories.

Risk: Default setup creates a broader 30.knowledge scaffold than an identity-only user may expect.

Mitigation: Use --minimal when only the lightweight identity layer and basic navigation are wanted.

Risk: Agents could alter human-owned identity or behavior contracts without sufficient authorization.

Mitigation: Keep ME.md and deep identity files human-owned, require explicit authorization for identity changes, and review AGENT.md behavior-rule edits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beiyuii/skills/personal-api)
- [README](artifact/README.md)
- [Architecture](artifact/references/architecture.md)
- [Vault Layout](artifact/references/vault-layout.md)
- [Operation Boundaries](artifact/references/operation-boundaries.md)
- [Maintenance](artifact/references/maintenance.md)
- [Release Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, vault templates, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Obsidian vault scaffolding and template files; full mode creates the 30.knowledge structure, while --minimal creates only the identity layer and basic navigation.]

## Skill Version(s):

2.0.2 (source: server release metadata and target metadata; artifact frontmatter shows 2.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
