## Description: <br>
Handle customer service, bills, reservations, and more via Pine AI - negotiate, cancel, dispute, book, and resolve from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bojieli](https://clawhub.ai/user/bojieli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use Pine Assistant to delegate customer-service calls, billing negotiations, cancellations, reservations, disputes, and account follow-up through Pine's CLI while keeping each task in its own session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pine can act on sensitive accounts, payments, reservations, cancellations, and disputes. <br>
Mitigation: Use narrow instructions, avoid unnecessary PINs and account details, and personally review payments or destructive actions before they proceed. <br>
Risk: Pine credentials are stored locally at ~/.pine/config.json. <br>
Mitigation: Protect the local credential file and remove or revoke Pine credentials when the integration is no longer needed. <br>
Risk: Broad session lookup and raw event relay can expose task details or lead to confusing follow-up actions. <br>
Mitigation: Keep session IDs separate, use session lookup only to resolve the user's request, and relay unfamiliar events for user review before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/bojieli/pine-assistant) <br>
- [Pine Assistant Homepage](https://pineclaw.com) <br>
- [Pine AI](https://19pine.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the pine CLI, JSON flags, session URLs, and local credential storage at ~/.pine/config.json.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
