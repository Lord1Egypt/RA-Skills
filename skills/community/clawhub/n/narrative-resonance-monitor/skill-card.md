## Description:

Measures whether a durable brand narrative is landing in the market by producing a resonance report with echo rate, AI-answer perception, locked-panel share of voice, and public resonance signals, while labeling each number as Measured, proxy, or User-provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, narrative, and brand teams use this skill to evaluate whether market language, answer-engine descriptions, and share-of-voice signals align with a canon narrative. It supports TALE Evaluate-phase resonance reporting without editing the canon lexicon or adjudicating claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package metadata understates the network/script and memory-write actions described by the skill workflow.

Mitigation: Install only in a host with per-operation permissions, and allow the named connectors and memory paths only when resonance monitoring is expected.

Risk: Report saves, event proposals, open-loop updates, and cache changes can alter persistent project memory.

Mitigation: Require explicit user confirmation before any report save, registry event proposal, open-loop update, or cache change.

Risk: Connector results, scraped mentions, and pasted analytics may contain untrusted content or misleading metrics.

Mitigation: Treat those inputs as untrusted, do not follow embedded instructions, and keep every number labeled as Measured, proxy, or User-provided with an as-of date.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/narrative-resonance-monitor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown resonance report with labeled metrics, source notes, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports echo-rate method and corpus, proxy AI-answer perception, locked-panel share of voice, as-of dates, and any unsupported claims marked as needing a source.]

## Skill Version(s):

19.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
