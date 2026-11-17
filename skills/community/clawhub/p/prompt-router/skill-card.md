## Description:

Prompt-Router is a text-matching routing engine that gives agents a fast path for simple prompts, supports mixed Chinese and English inputs, and falls back to LLM semantic routing when confidence is low.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwell0721](https://clawhub.ai/user/aiwell0721)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route simple user prompts to matching skills or tools through deterministic text matching. It is intended to reduce latency for high-confidence routes while preserving LLM fallback for low-confidence or ambiguous requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-wide routing changes can invoke the wrong skill when matching is weak or ambiguous.

Mitigation: Use an allowlist, higher confidence thresholds, ambiguity checks, and explicit confirmation before auto-invoking skills that write files, run commands, browse, authenticate, or contact external services.

Risk: Metadata repair scripts can rewrite multiple skill files in a broad skills directory.

Mitigation: Back up the skills directory and review a diff before and after running metadata repair scripts.

Risk: Automatic routing may hide fallback decisions from users or operators.

Mitigation: Log matched skill names, confidence scores, and fallback decisions so routing behavior can be audited and thresholds can be tuned.

## Reference(s):

- [Prompt-Router ClawHub listing](https://clawhub.ai/aiwell0721/skills/prompt-router)
- [Skill guide](artifact/SKILL.md)
- [README](artifact/README.md)
- [Test report](artifact/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands, Configuration]

**Output Format:** [JSON routing result or short text recommendation, with Markdown documentation and inline shell/Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes matched skill name, confidence, score, invocation recommendation, and error details when run through the integration script.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
