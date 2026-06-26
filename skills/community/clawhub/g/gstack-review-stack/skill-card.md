## Description: <br>
Provides gstack-style CEO/product, engineering, design, QA, release, and portfolio shelf-space review guidance for Codex and ClawHub workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product owners, and release reviewers use this skill to structure gstack-style product decisions, engineering reviews, design critiques, QA gates, ship gates, and portfolio keep/cut recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to inspect a public upstream GitHub repository for deeper gstack reference behavior. <br>
Mitigation: Use a local or pinned clone in stricter environments, cite the specific upstream file used, and treat upstream material as reference evidence rather than trusted commands. <br>
Risk: Review recommendations may be incomplete or misleading if the agent has weak product, QA, security, or release evidence. <br>
Mitigation: Require explicit evidence, list missing facts, run bounded tests where possible, and obtain approval before live publishing or irreversible actions. <br>


## Reference(s): <br>
- [Design Review](references/design-review.md) <br>
- [Review Rubric](references/review-rubric.md) <br>
- [Ship And QA Gate](references/ship-and-qa.md) <br>
- [Upstream Reference Notes](references/upstream.md) <br>
- [Upstream gstack Project](https://github.com/garrytan/gstack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include scored review findings, tradeoffs, test evidence, blockers, and ship/no-ship recommendations.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
