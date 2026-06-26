## Description: <br>
Runs the full Dawn CLI strategy lifecycle from authentication and funding through strategy creation, launch, monitoring, and termination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[njdawn](https://clawhub.ai/user/njdawn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and prediction-market strategy authors use this skill to install or check the Dawn CLI, authenticate, create and revise strategies, launch paper or live runs, monitor positions and logs, and stop active runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live prediction-market trading and account operations. <br>
Mitigation: Use paper mode by default and require explicit user approval before login, funding, rule approval, strategy upload, or any live launch. <br>
Risk: A live run may spend real funds or continue operating without adequate oversight. <br>
Mitigation: Confirm budget, duration, account, monitoring plan, and stop status before launch, then monitor status, positions, and logs during operation. <br>


## Reference(s): <br>
- [Dawn](https://dawn.ai) <br>
- [ClawHub skill page](https://clawhub.ai/njdawn/prediction-market-bot-dawn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns conversationId, strategyId when launched, run mode, monitoring summary, and the exact next or last Dawn command.] <br>

## Skill Version(s): <br>
1.0.8 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
