## Description:

LYGO Skill Gate is a local pre-install risk scanner for OpenClaw and ClawHub skill packages that checks skill folders for subprocess, shell, network, secret, dynamic-code, webhook, and permission-claim mismatch signals without downloading, installing, or executing the scanned skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and operators use this skill to audit ClawHub or OpenClaw skill folders before installation or execution and to produce risk bands, findings, and permission-claim mismatch checks for review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned @latest ClawHub installer version, which can change between runs.

Mitigation: Review or pin the installer version before installation, as recommended by the authoritative security guidance.

Risk: Generated scan reports may contain snippets of secret-looking text from scanned packages.

Mitigation: Treat reports as sensitive review artifacts and avoid sharing them publicly.

Risk: Static heuristic scanning can miss unsafe behavior or flag legitimate operator tooling.

Mitigation: Use the risk report as a review gate, then inspect flagged code and SECURITY.md before trusting a third-party skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-skill-gate)
- [Publisher Profile](https://clawhub.ai/user/deepseekoracle)
- [Project Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-skill-gate)
- [Security Reference](references/SECURITY.md)
- [Quickstart](examples/quickstart.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance, files]

**Output Format:** [JSON and plain text risk reports, with optional report files written under state/ when consent is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes indicate clear or low risk, elevated risk, high or critical risk, or an invalid skill path.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, SKILL.md frontmatter, claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
