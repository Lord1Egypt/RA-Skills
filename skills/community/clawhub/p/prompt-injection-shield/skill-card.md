## Description:

Scans untrusted text for English and Chinese prompt-injection patterns and returns a risk score, matched rules, and a recommended disposition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to screen web pages, emails, retrieved documents, and tool output before adding untrusted text to an AI context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic scanning can miss attacks or block harmless text.

Mitigation: Review the matched rules and recommended action before admitting or discarding content; do not treat a pass result as a safety guarantee.

Risk: WebFetch or WebSearch use may retrieve untrusted material beyond the intended scan.

Mitigation: Keep retrieval user-directed and review any web access before use.

Risk: The skill instructions describe flags that the bundled scanner does not accept.

Mitigation: Run the script with --text or --file, and use --json for machine-readable results; do not use --input or --mode.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/prompt-injection-shield)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain text or JSON risk report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a score from 0 to 100, matched rules, and a drop, quarantine, or pass recommendation.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
