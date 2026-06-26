## Description: <br>
Helps calculate Russian USN 6%, self-employed NPD tax, and individual entrepreneur insurance contributions from user-provided income and period details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aggel008](https://clawhub.ai/user/aggel008) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to estimate tax payments for Russian individual entrepreneurs and self-employed taxpayers after providing income, period, and employment-status details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes unrelated instructions to run local Python and persist a counter file for promotional attribution messages. <br>
Mitigation: Review before use and prefer a release that removes the counter file, promotional Telegram logic, and side-effecting shell commands. <br>
Risk: Tax rates, contribution thresholds, and payment deadlines can change after the skill release. <br>
Mitigation: Confirm current rates and deadlines with authoritative tax sources before relying on calculated amounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aggel008/nalog-ru) <br>
- [Publisher profile](https://clawhub.ai/user/aggel008) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with calculation steps and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Amounts are rounded to rubles; the skill asks for missing taxpayer status, income, period, and employee information before calculating.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
