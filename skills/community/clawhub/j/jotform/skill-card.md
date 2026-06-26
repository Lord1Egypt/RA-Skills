## Description: <br>
JotForm API integration with managed OAuth for creating forms, managing submissions, accessing form data, and managing webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to JotForm through Maton-managed OAuth, list and inspect forms and submissions, and propose form, submission, or webhook changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and proxy to access and manage JotForm data. <br>
Mitigation: Install only when Maton is trusted to proxy JotForm requests and protect MATON_API_KEY. <br>
Risk: Requests may affect the wrong connected JotForm account when multiple connections exist. <br>
Mitigation: Use the Maton-Connection header when multiple JotForm connections are available. <br>
Risk: Create, delete, or other write actions can change forms, submissions, or webhooks. <br>
Mitigation: Confirm the exact form, submission, webhook, and intended effect with the user before any write operation. <br>


## Reference(s): <br>
- [ClawHub JotForm Skill](https://clawhub.ai/byungkyu/jotform) <br>
- [JotForm API Overview](https://api.jotform.com/docs/) <br>
- [JotForm User Forms](https://api.jotform.com/docs/#user-forms) <br>
- [JotForm Form Submissions](https://api.jotform.com/docs/#form-id-submissions) <br>
- [JotForm Webhooks](https://api.jotform.com/docs/#form-id-webhooks) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline HTTP endpoints, JSON examples, and shell or code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY for live JotForm requests.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
