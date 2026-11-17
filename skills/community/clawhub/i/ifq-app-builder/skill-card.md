## Description:

IFQ App Builder turns short app ideas into verified, build-ready prompt bundles across desktop, mobile, local web, PWA, and CLI modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peixl](https://clawhub.ai/user/peixl)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to convert a brief app request into a platform-routed prompt bundle with acceptance, packaging, security, i18n, and verification details. It is intended for Tier 0 prompt-bundle generation and handoff, not silent SDK installation, signing, or store submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompt bundles can contain scaffold commands that a downstream coding agent may execute.

Mitigation: Review scaffold commands, pin package versions where practical, and run installs in an isolated workspace or container without unrelated secrets.

Risk: The skill's generated app surfaces may include the IFQ colophon and attribution.

Mitigation: Use the skill only when the project can accept the disclosed IFQ attribution, or rebrand downstream forks according to the artifact license notice.

Risk: Tier 0 output is a prompt bundle, not a built or signed application.

Mitigation: Do not provide signing certificates, store tokens, or production credentials until a separate implementation, build, signing, and deployment step is explicitly requested and verified.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/peixl/skills/ifq-app-builder)
- [Project homepage](https://github.com/peixl/ifq-app-builder)
- [Quickstart](README.en.md#first-run)
- [Agent Compatibility](references/agent-compatibility.md)
- [Mode Routing](references/modes.md)
- [Platform Matrix](references/platform-matrix.md)
- [Quality Bar](references/quality-bar.md)
- [Security Baseline](references/security-baseline.md)
- [Verification](references/verification.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prompt bundle with verification commands and structured handoff details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local *.prompt.md build bundle with mode route, template id, assumptions, verification result, and caveats.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, package.json, clawhub.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
