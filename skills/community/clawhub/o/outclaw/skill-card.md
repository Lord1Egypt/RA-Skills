## Description: <br>
Outclaw is a B2B outreach orchestrator that routes outreach setup, research, planning, campaign status, reply handling, and opt-out requests through guarded specialist skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milstan](https://clawhub.ai/user/milstan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users and sales operators use Outclaw to plan and manage guarded B2B outreach workflows, including lead pulls, target research, personalized draft generation, campaign dashboards, reply handling, and opt-outs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run local scripts and can change OpenClaw configuration automatically. <br>
Mitigation: Inspect the installed pack, shared scripts, and sibling skills before use, and run it only in a trusted workspace where configuration changes are acceptable. <br>
Risk: The skill can involve OAuth-protected channels, sensitive credentials, and paid contact-purchase behavior. <br>
Mitigation: Confirm OAuth scopes and purchase settings before connecting accounts, and withhold or limit credentials until the operator approves the intended workflow. <br>
Risk: Prospect and lead data may be written to temporary files and displayed in chat. <br>
Mitigation: Avoid shared machines or shared chat surfaces for sensitive outreach data, and review where memory, KB logs, and temporary lead files are stored and deleted. <br>


## Reference(s): <br>
- [Outclaw ClawHub page](https://clawhub.ai/milstan/outclaw) <br>
- [Outclaw homepage](https://github.com/leadbay/outclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, draft outreach content, command-oriented operational steps, and status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outbound messages require review and explicit per-touchpoint approval before sending.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter reports 2.1.33) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
