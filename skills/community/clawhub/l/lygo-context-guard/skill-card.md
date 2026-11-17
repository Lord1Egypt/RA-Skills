## Description:

LYGO Context Guard provides local pre-flight token budgeting, secret redaction, and deterministic context compaction for AI agents before model calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and AI agent operators use this skill to estimate token usage, redact credential-like patterns, compact large tool outputs or logs, and check budget fit before passing content to a model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads user-selected files and may print redacted or compacted content to stdout.

Mitigation: Run it only on intended inputs, route output to trusted destinations, and inspect results before reusing them in model context.

Risk: Secret redaction is best-effort pattern matching and is not a compliance guarantee.

Mitigation: Treat it as a guardrail, not a replacement for secret scanning, data loss prevention, or human review of sensitive material.

Risk: Token estimates are heuristic and may not match a model's exact tokenizer or billing counts.

Mitigation: Use the estimates for budgeting with margin, and reduce or split content when reports approach the target context budget.

Risk: Installing from an unpinned latest release can change the reviewed code over time.

Mitigation: Install a pinned and trusted ClawHub version when supply-chain reproducibility matters.

## Reference(s):

- [Security reference](references/SECURITY.md)
- [Quickstart example](examples/quickstart.md)
- [Project homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-context-guard)
- [ClawHub skill listing](https://clawhub.ai/deepseekoracle/skills/lygo-context-guard)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON reports and redacted or compacted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local processing; budget checks can return a nonzero exit code when content remains over budget.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
