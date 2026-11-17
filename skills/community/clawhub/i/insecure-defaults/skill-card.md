## Description:

Detects fail-open insecure defaults, including hardcoded secrets, weak authentication, and permissive security settings that allow applications to run insecurely in production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlas-secint](https://clawhub.ai/user/atlas-secint)

### License/Terms of Use:


## Use Case:

Developers, security engineers, and reviewers use this skill to audit production-reachable code and configuration for insecure defaults such as fallback secrets, default credentials, disabled authentication, weak cryptography, permissive access, and exposed debug behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests unrestricted shell access, which can be risky in sensitive workspaces or untrusted repositories.

Mitigation: Review the skill before installation and remove or tightly restrict shell access unless shell-backed analysis is explicitly needed and the target repositories are trusted.

Risk: Insecure-default searches can produce misleading findings when matches are in tests, examples, documentation, development-only tooling, or fail-secure code paths.

Mitigation: Apply the documented verification workflow: trace runtime behavior, confirm production reachability, and skip explicitly scoped non-production or fail-secure patterns.

## Reference(s):

- [Insecure Defaults Examples and Counter-Examples](artifact/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/atlas-secint/skills/insecure-defaults)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with search patterns, verification steps, and finding reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on production-reachable findings and distinguishes fail-open defaults from fail-secure behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
