## Description: <br>
Analyzes an industry's opportunity landscape across demand scenarios, customer pain points, policy opportunities, and future developments, then produces a four-section Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents in an industry-analysis workflow use this skill to create the opportunity section of an industry report from session state, covering scenarios, pain points, policy opportunities, and future trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local report files and lightweight session state in its working area, which can overwrite or add files under the configured output path. <br>
Mitigation: Run it in a project folder where generated files are expected, and check for existing output files before use when preservation matters. <br>


## Reference(s): <br>
- [行业机会 4 维度框架](references/opportunity-dimensions.md) <br>
- [ClawHub release page](https://clawhub.ai/zrxparley/industry-analyzer-opportunity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown report plus session.json state update] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/{industry-slug}/04-opportunity.md and updates output/{industry-slug}/session.json when used in the industry-analysis workflow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
