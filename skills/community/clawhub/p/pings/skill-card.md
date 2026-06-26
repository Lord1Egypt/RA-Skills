## Description: <br>
Fetches the latest Wink Pings news and can use a user-provided email as the user_id for personalized subscription results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ully](https://clawhub.ai/user/ully) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request recent AI or Wink Pings news, optionally personalize results with their Wink/Pings email, and present returned articles in a consistent Markdown list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send a user email to Wink Pings as user_id and store it locally in plain text for reuse. <br>
Mitigation: Use only an email the user provides, explain why it is needed before saving it, and delete skills/pings/pings-user-email when the user no longer wants automatic reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ully/pings) <br>
- [Wink Pings latest news API](https://wink.run/api/pings/latest) <br>
- [Artifact API reference](artifact/reference.md) <br>
- [Artifact usage examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown news list with optional curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write a local single-line email configuration file when the user consents.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
