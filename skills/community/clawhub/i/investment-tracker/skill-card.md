## Description: <br>
Investment portfolio management assistant that can query and update holdings, cash, diary entries, equity curves, and import holdings from screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[20czy](https://clawhub.ai/user/20czy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal investors use this skill to manage a local investment tracker through API calls, including holdings review, cash and diary updates, equity-curve tracking, benchmark comparison, and screenshot-assisted portfolio import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Investment Tracker API quick reference](references/api-docs.md) <br>
- [ClawHub skill page](https://clawhub.ai/20czy/investment-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with curl commands and structured summaries of API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, a local service at http://localhost:8000, and DASHSCOPE_API_KEY for screenshot analysis. Review every proposed write, rollback, or deletion before execution; protect API keys and redact account identifiers from screenshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
