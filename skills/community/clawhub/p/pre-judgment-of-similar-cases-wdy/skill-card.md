## Description: <br>
This skill helps agents retrieve legal provisions and similar case examples through the Wendaoyun/Wintaocloud API, then summarize legal consequences and possible next steps for dispute scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rose-develop](https://clawhub.ai/user/rose-develop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to support legal research for disputes such as fraud, debts, contract breaches, injuries, and litigation questions. It retrieves relevant laws and similar cases, formats the results, and can provide optional risk points and suggested next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User dispute summaries are sent to the third-party Wendaoyun/Wintaocloud API and may contain personal or sensitive case facts. <br>
Mitigation: Avoid unnecessary names, ID numbers, addresses, account details, and private case facts before using the skill. <br>
Risk: The skill supports legal research but its responses may be mistaken for professional legal advice. <br>
Mitigation: Treat responses as research support and have users consult qualified legal professionals for legal decisions. <br>
Risk: The skill depends on a bearer API key for the Wendaoyun/Wintaocloud API. <br>
Mitigation: Keep WENDAOYUN_API_KEY private and revoke or rotate it if disclosure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rose-develop/skills/pre-judgment-of-similar-cases-wdy) <br>
- [Wintaocloud open platform](https://open.wintaocloud.com/home) <br>
- [Wintaocloud get-laws API endpoint](https://h5.wintaocloud.com/prod-api/api/invoke/get-laws) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with legal provisions, similar case summaries, optional analysis, and inline shell commands for setup examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WENDAOYUN_API_KEY; default top_k is 3 and maximum top_k is 5.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
