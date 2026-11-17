## Description:

Httpstat provides readable HTTP response statistics with a timing waterfall for checking URL response time, debugging slow requests, measuring TTFB, and viewing HTTP timing breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run HTTP timing checks, inspect DNS, TCP, TLS, TTFB, transfer timings, and compare text or JSON response statistics while diagnosing URL performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redirect following can pass supplied tokens or request bodies to another site.

Mitigation: Use the skill only against trusted URLs, avoid passing secrets in headers or request bodies, and be cautious with --follow until redirect handling strips credentials across origins and enforces real limits.

Risk: The security verdict requires review before installation.

Mitigation: Review and scan the skill before deployment, following the server-provided security guidance.

## Reference(s):

- [Httpstat ClawHub Skill Page](https://clawhub.ai/rogue-agent1/skills/httpstat)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus terminal text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports DNS, TCP, TLS, TTFB, transfer, total timing, selected headers, body size, status, and optional redirect information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
