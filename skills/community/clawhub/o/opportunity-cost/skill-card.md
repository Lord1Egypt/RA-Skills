## Description: <br>
Helps an agent guide opportunity-cost analysis by identifying the next-best alternative, estimating financial and non-financial tradeoffs, and comparing the chosen option against what is foregone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and decision-makers use this skill to evaluate scarce-resource choices involving money, time, attention, or staffing. It is most useful when an agent needs to surface realistic alternatives, estimate the value of the best unchosen option, and present a concise markdown opportunity-cost analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opportunity-cost examples may contain sensitive financial, staffing, or personal decision details if users add real cases to reusable examples. <br>
Mitigation: Keep sensitive decision details out of reusable skill examples unless retention and sharing are intentional. <br>
Risk: The skill can produce misleading guidance if alternatives or value estimates are incomplete. <br>
Mitigation: Require 3-5 realistic alternatives, include the do-nothing option, and label confidence before relying on the analysis. <br>


## Reference(s): <br>
- [Opportunity Cost Sources](references/sources.md) <br>
- [Bastiat's Broken Window Example](examples/bastiats-broken-window-1850.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deciqai/skills/opportunity-cost) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown opportunity-cost analysis with tables and concise decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only; no code execution, tool calls, or hidden data access indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
