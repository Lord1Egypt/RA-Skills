## Description: <br>
Access Finnish sports club events, invoices, notifications, and RSVP on myclub.fi for AI agents and parents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jannemakela](https://clawhub.ai/user/jannemakela) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, athletes, and agents assisting authorized MyClub users use this skill to retrieve Finnish sports club events, invoices, notifications, RSVP status, participants, comments, and calendar subscriptions from myclub.fi. <br>

### Deployment Geography for Use: <br>
Finland <br>

## Known Risks and Mitigations: <br>
Risk: MyClub credentials, notifications, child or member details, invoices, and generated calendar links may expose sensitive family or schedule data. <br>
Mitigation: Install only if the maiklubi npm package is trusted, use authorized family or club accounts only, avoid sharing sensitive command output in public chats or logs, and clear saved account access when it is no longer needed. <br>
Risk: Club-internal details such as team assignments, line-ups, event comments, and schedule changes may be incomplete or misleading if answered from public web sources. <br>
Mitigation: Use the skill's MyClub notification, event, participant, and summary commands for authorized account data, then review the returned details before acting. <br>


## Reference(s): <br>
- [Maiklubi on ClawHub](https://clawhub.ai/jannemakela/maiklubi-myclub) <br>
- [maiklubi npm package](https://www.npmjs.com/package/maiklubi) <br>
- [myclub.fi](https://myclub.fi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the maiklubi CLI and a configured MyClub account; command outputs may contain private member, invoice, notification, event, and calendar data.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
