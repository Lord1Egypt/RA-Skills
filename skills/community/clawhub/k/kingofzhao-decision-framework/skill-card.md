## Description: <br>
KingOfZhao Decision Framework helps agents structure decisions around knowns, unknowns, confidence-weighted trade-offs, red-line checks, and decision memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to compare options, surface unknowns, apply risk-weighted scoring, and record decision rationale for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision-memory records or heartbeat reviews may persist sensitive decision context when agent memory or workspace persistence is enabled. <br>
Mitigation: Review the skill's memory and recordkeeping behavior before installation, and store only the decision details intended for the active workspace. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046) <br>
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) <br>
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text with decision rankings, red-line checks, recommendations, and decision records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local decision-memory records when the agent is configured to persist them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
