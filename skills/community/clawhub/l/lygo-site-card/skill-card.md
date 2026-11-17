## Description:

Turns a public HTTPS URL or local HTML file into a compact JSON identity card covering page metadata, security headers, security.txt and robots.txt companions, SHA-256, and ALIGNED/DRIFT/SHADOW yield.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers, operators, and agents use this skill to check public page liveness, CSP/HSTS and other security header posture, companion files, and drift between staging and production URLs, or to parse local HTML without network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public-URL network boundary has a server-identified SSRF weakness.

Mitigation: Run the skill only against public sites you are authorized to inspect, and do not treat it as a hard SSRF boundary for adversarial URLs until DNS pinning or equivalent connection validation is fixed.

Risk: The install instructions use a mutable npx package reference.

Mitigation: Prefer a pinned and verified installer or release package before commercial deployment.

## Reference(s):

- [Security Reference](references/SECURITY.md)
- [SkillSpector Audit Notes](references/SKILLSPECTOR_AUDIT.md)
- [Quickstart](examples/quickstart.md)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-site-card)
- [OpenClaw Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-site-card)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Files]

**Output Format:** [Pretty-printed JSON to stdout, with optional JSON file output when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports card, headers, and compare reports; optional writes require --write with --i-consent; page bodies are capped at 400 KB.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
