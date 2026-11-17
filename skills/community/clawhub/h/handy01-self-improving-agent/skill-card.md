## Description:

Self-improving agent system that analyzes conversation quality, identifies improvement opportunities, and continuously optimizes response strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handy01](https://clawhub.ai/user/handy01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to analyze conversation quality, log improvement notes, generate weekly improvement summaries, and suggest response-strategy updates for OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation feedback or improvement notes may include secrets, personal data, or proprietary content in the local improvement log.

Mitigation: Avoid logging sensitive content and periodically review or delete the local improvement log.

Risk: Heuristic analysis and suggested strategy updates may produce low-confidence or misleading guidance.

Mitigation: Review generated reports and suggested behavior updates before applying them to agent configuration or personality files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/handy01/skills/handy01-self-improving-agent)
- [Project Homepage](https://github.com/xiucheng/self-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reports, JSON-like analysis dictionaries, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append improvement notes to a local markdown log in the configured workspace.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
