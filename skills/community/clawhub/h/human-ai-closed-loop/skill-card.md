## Description:

Structures a recurring human-AI cognition loop where AI drafts checklists, humans test assumptions and add experiential input, and AI synthesizes updated outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to run iterative planning and problem-solving workflows that separate verified facts, falsifiable hypotheses, blind spots, human feedback, and updated recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feedback logs may contain sensitive project observations or private human input.

Mitigation: Keep loop_log-style records local and avoid placing sensitive data in feedback unless the runtime storage behavior is confirmed.

Risk: Closed-loop work can stall or drift if human feedback is delayed, confidence falls repeatedly, or checklists lack falsifiable assumptions.

Mitigation: Use heartbeat checks to identify stale sessions, falling confidence, missing assumptions, and pending feedback before continuing the loop.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kingofzhao/skills/human-ai-closed-loop)
- [Publisher Homepage](https://github.com/KingOfZhao/AGI_PROJECT)
- [artifact/README.md](artifact/README.md)
- [artifact/VERIFICATION_PROTOCOL.md](artifact/VERIFICATION_PROTOCOL.md)
- [artifact/HEARTBEAT.md](artifact/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text with checklist items, hypotheses, feedback categories, confidence notes, and synthesis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local loop_log-style records for tracking feedback rounds.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and README list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
