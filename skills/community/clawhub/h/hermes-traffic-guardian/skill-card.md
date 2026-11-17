## Description:

Hermes runtime traffic monitoring baseline for opt-in proxy inspection, egress detection, and attestation-aware traffic posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill as a Hermes traffic-monitoring specification baseline for implementing opt-in HTTP/HTTPS inspection, exfiltration and injection detection, redacted local findings, and attestation posture export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future implementations may add proxy behavior or HTTPS inspection beyond this beta scaffold.

Mitigation: Review any implementation before enabling it, keep HTTPS inspection opt-in, and scope proxy and CA trust to the intended Hermes process.

Risk: Traffic monitoring could expose sensitive request or response data if logging is implemented carelessly.

Mitigation: Preserve the documented redaction requirements and verify that snippets are redacted before logs, summaries, or attestation-linked outputs are written.

## Reference(s):

- [Hermes Traffic Guardian ClawHub page](https://clawhub.ai/davida-ps/skills/hermes-traffic-guardian)
- [ClawSec homepage](https://clawsec.prompt.security)
- [README](README.md)
- [Specification](SPEC.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON schemas and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a specification baseline only; the inspected package does not include active proxy runtime behavior.]

## Skill Version(s):

0.0.1-beta2 (source: server release, SKILL.md frontmatter, skill.json, CHANGELOG released 2026-05-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
