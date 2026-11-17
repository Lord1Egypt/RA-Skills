## Description:

MiroPRISM is an adversarial two-round review protocol that runs specialist reviewers independently, broadcasts a sanitized Round 1 digest, and requires evidence-backed agreement, disagreement, or uncertainty before synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremyknows](https://clawhub.ai/user/jeremyknows)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use MiroPRISM to review architecture decisions, security-sensitive changes, open source releases, and other high-stakes artifacts where consensus drift is a risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow spawns multiple reviewers over the user's project and writes review records under analysis/miroprism.

Mitigation: Install only in environments where this review activity and local artifact writing are acceptable.

Risk: Untrusted artifact and reviewer text can be reused in later agent prompts.

Mitigation: Treat outputs as advisory, use the digest-review pause for sensitive work, and run only with strong prompt-injection isolation and least-privilege limits when reviewing hostile artifacts.

## Reference(s):

- [Post-Launch Metrics Reference](references/post-launch-metrics.md)
- [MiroPRISM ClawHub Skill Page](https://clawhub.ai/jeremyknows/skills/miroprism)
- [jeremyknows ClawHub Publisher Profile](https://clawhub.ai/user/jeremyknows)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance, Files]

**Output Format:** [Markdown review synthesis with digest logs, metrics, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes review artifacts under analysis/miroprism, including Round 1 outputs, sanitized digests, Round 2 outputs, archived syntheses, and optional metrics.]

## Skill Version(s):

1.4.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
