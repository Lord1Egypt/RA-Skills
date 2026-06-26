## Description: <br>
A CEO/executive-mode decision workflow for challenging premises, diagnosing problems, and producing definitive strategies for product, growth, market, technology, organization, and resource-allocation decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, executives, product leaders, and strategy teams use this skill to pressure-test strategic choices, select an analysis mode, compare alternatives, assess risks, and produce a decision summary with implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local decision-history files may contain confidential strategic, hiring, financing, product, or market information. <br>
Mitigation: Review or delete ~/.strategic-decisions as needed, and avoid using persistence-heavy modes for confidential work unless local storage is acceptable. <br>
Risk: The optional office-hours handoff depends on a local office-hours skill outside this artifact. <br>
Mitigation: Use the default jump-straight-in path unless the local office-hours skill is trusted and appropriate for the decision context. <br>
Risk: Strategy recommendations can be incomplete or wrong if the provided facts, assumptions, or market signals are weak. <br>
Mitigation: Require evidence for major claims, review recommendations with accountable stakeholders, and validate critical assumptions before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaisersong/kai-strategic-decision) <br>
- [Cognitive Patterns](artifact/references/cognitive-patterns.md) <br>
- [Decision Frameworks](artifact/references/decision-frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown narrative with decision tables, interactive questions, shell command snippets, and optional persisted Markdown decision summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AGGRESSIVE and SELECTIVE modes may create local Markdown decision records under ~/.strategic-decisions; the workflow also reads that folder to surface related prior decisions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
