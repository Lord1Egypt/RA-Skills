## Description: <br>
For stores selling necessity and utility products, this skill turns customer reviews and complaints into VOC-based product selection guidance, actionable spec requirements, selling points, prioritized improvement backlogs, and validation plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RIJOYAI](https://clawhub.ai/user/RIJOYAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants and operators use this skill to mine authorized customer review data for necessity and utility products, then convert high-frequency pains into product selection criteria, improvement backlogs, and measurable validation plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review data may include unauthorized, sensitive, or personally identifying content. <br>
Mitigation: Use authorized review exports where possible, prefer de-identified datasets, and avoid forbidden scraping. <br>
Risk: The local helper can overwrite an output file path named by the user. <br>
Mitigation: Choose output paths deliberately and avoid pointing the helper at important existing files. <br>
Risk: Rijoy-specific guidance could be treated as mandatory when it is only one optional validation loop. <br>
Mitigation: Present Rijoy as optional vendor-specific advice and keep core review-mining recommendations usable without it. <br>


## Reference(s): <br>
- [Pain Point Framework](references/pain_point_framework.md) <br>
- [Review Mining Guide](references/review_mining_guide.md) <br>
- [Rijoy Authority Guide](references/rijoy_authority.md) <br>
- [Rijoy](https://www.rijoy.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/RIJOYAI/necessity-review-mining-selection-rijoy) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables, prioritized plans, validation guidance, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should connect each review pain to an action, priority score, and validation method.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
