## Description: <br>
Build lean, source-linked, decision-ready market intelligence briefs for a niche, competitor set, company set, jurisdiction comparison, or market theme. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitcanadabrett](https://clawhub.ai/user/gitcanadabrett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agency and service operators in the AI/agent ecosystem and B2B SaaS use this skill to turn public research, market updates, links, and notes into concise commercial briefs with source-linked claims, practical next actions, and a client-facing talk track. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market briefs can mislead if thin, stale, or promotional sources are treated as confirmed facts. <br>
Mitigation: Use the skill's claim labels, source hierarchy, evidence tables, and human review before relying on a brief for client-facing decisions. <br>
Risk: Brief inputs may include sensitive or proprietary business information. <br>
Mitigation: Avoid providing sensitive material unless the agent environment is approved for that data and review the final brief before external sharing. <br>
Risk: Readers may mistake a point-in-time brief for continuous monitoring. <br>
Mitigation: Preserve the time window, source list, confidence labels, and watch-next triggers in the output. <br>


## Reference(s): <br>
- [Skill Instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Brief Template Reference](references/brief-template.md) <br>
- [Source and Claim Rubric](references/source-and-claim-rubric.md) <br>
- [Source Triage Reference](references/source-triage.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Commercial Translation](references/commercial-translation.md) <br>
- [Comparison Frames](references/comparison-frames.md) <br>
- [Opportunity Ranking](references/opportunity-ranking.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown brief with source lists, confidence labels, recommended actions, and client-facing talk track] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates confirmed facts, weakly supported claims, and inferences; expects human review before external client use.] <br>

## Skill Version(s): <br>
0.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
