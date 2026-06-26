## Description: <br>
Guides engineering researchers through reproducible academic literature surveys with initial-survey or daily-reading modes, user checkpoints, IEEE citations, and structured research briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gao-tech1](https://clawhub.ai/user/Gao-tech1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and engineering teams use this skill to survey defined engineering research topics, track recent academic progress, and produce reproducible paper briefs with screening criteria, paper tables, IEEE citations, and method appendices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive research topics may be exposed through external academic searches or optional memory use. <br>
Mitigation: Avoid confidential topics in normal runs, or instruct the agent not to store memory for sensitive research. <br>
Risk: Paywalls or login barriers can limit paper analysis and lead to abstract-only interpretations. <br>
Mitigation: Provide authorized full-text content when available, or explicitly skip inaccessible papers and label abstract-only analysis. <br>
Risk: Generated literature summaries may contain incomplete or incorrect interpretations of papers. <br>
Mitigation: Review cited sources, paper lists, and the method appendix before relying on the brief for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gao-tech1/paper-briefing-assistant) <br>
- [Artifact README](artifact/README.md) <br>
- [Quick reference](artifact/quickref.md) <br>
- [Example workflow](artifact/example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research brief with tables, IEEE citations, appendices, and checkpoint prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paper lists, code and data links, abstract-only notices, and reproducibility details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
