## Description:

Build structured AI agent personalities using OCEAN, DISC, and Jungian frameworks. Define traits, communication styles, guardrails, and compile to system prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcrowan3](https://clawhub.ai/user/jcrowan3)

### License/Terms of Use:


## Use Case:

Developers and agent builders use PersonaNexus to define YAML-based agent identities, validate them against a schema, and compile them into system prompts or platform-specific personality and configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity YAML files may contain sensitive persona, policy, or prompt material.

Mitigation: Use trusted identity files, avoid storing secrets in YAML, and write generated outputs only to private directories you control.

Risk: Unpinned dependency installs can change behavior across environments.

Mitigation: Use pinned or locked dependency versions before production use.

Risk: Generated prompts or configuration files can encode undesired agent behavior if source identities are incorrect.

Mitigation: Validate identity files and review compiled outputs before deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcrowan3/skills/personanexus-skill)
- [PersonaNexus repository](https://github.com/PersonaNexus/personanexus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, CLI commands, YAML templates, and generated prompt or configuration artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce plain-text prompts, OpenAI or Anthropic-oriented prompt text, OpenClaw personality JSON, SOUL.md and STYLE.md content, full identity JSON, validation messages, and scaffolded YAML identity files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
