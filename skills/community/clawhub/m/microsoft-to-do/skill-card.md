## Description: <br>
Microsoft To Do API integration with managed OAuth for managing task lists, tasks, checklist items, and linked resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to read and manage Microsoft To Do lists, tasks, checklist items, and linked resources through a Maton-managed Microsoft OAuth connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MATON_API_KEY is a sensitive credential used with a Maton-managed Microsoft To Do OAuth connection. <br>
Mitigation: Keep MATON_API_KEY private, store it in the environment, and install the skill only if Maton is trusted to broker the OAuth connection. <br>
Risk: Create, update, and delete operations can modify or remove Microsoft To Do data. <br>
Mitigation: Confirm the target list, task, checklist item, or linked resource and the intended effect before approving any write or delete request. <br>
Risk: When multiple Microsoft To Do connections exist, a request may target the wrong account. <br>
Mitigation: Use the Maton-Connection header to select the intended connection when more than one account is connected. <br>


## Reference(s): <br>
- [Microsoft To Do API Overview](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview) <br>
- [todoTaskList Resource](https://learn.microsoft.com/en-us/graph/api/resources/todotasklist) <br>
- [todoTask Resource](https://learn.microsoft.com/en-us/graph/api/resources/todotask) <br>
- [checklistItem Resource](https://learn.microsoft.com/en-us/graph/api/resources/checklistitem) <br>
- [linkedResource Resource](https://learn.microsoft.com/en-us/graph/api/resources/linkedresource) <br>
- [Microsoft To Do Skill on ClawHub](https://clawhub.ai/byungkyu/microsoft-to-do) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, HTTP examples, and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Microsoft To Do OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
