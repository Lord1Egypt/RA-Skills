## Description: <br>
OpenClaw Ticket Assistant analyzes customer-support screenshots, identifies customer and issue details, and helps create tickets in an internal ticketing system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mskmz](https://clawhub.ai/user/mskmz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Support engineers use this skill to convert customer conversation screenshots into confirmed ticket fields, guide login when needed, and submit tickets through the internal ticket system after user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in browser session to create tickets in an internal system. <br>
Mitigation: Install it only for that workflow and review the filled ticket form before confirming submission. <br>
Risk: Customer screenshots may contain sensitive or unrelated information. <br>
Mitigation: Provide only relevant screenshots and verify the extracted customer, UID, handler, platform, and problem details before confirming submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mskmz/openclaw-ticket-assistant) <br>
- [Domain Account Login Guide](references/login-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text confirmation prompts and ticket summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes extracted customer, feedback contact, platform, problem description, and ticket number when creation succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
