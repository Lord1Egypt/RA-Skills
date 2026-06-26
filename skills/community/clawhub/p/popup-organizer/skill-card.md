## Description: <br>
Search and hire mobile vendors for events on PopUp, create event listings, send booking inquiries, and manage invoices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eliaskress](https://clawhub.ai/user/eliaskress) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Event organizers use this skill to search PopUp vendors, manage event listings and applications, send and update booking inquiries, review invoices, save vendors, and update organizer profile details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, cancel, delete, and respond to business records using an organizer API key. <br>
Mitigation: Use a revocable or least-privilege PopUp API key when available, and require the agent to summarize the exact event, vendor, inquiry, quote, amount, or profile change before account-changing calls. <br>
Risk: The security scan notes account-changing authority without built-in confirmation or privacy guidance. <br>
Mitigation: Require explicit approval for create, update, delete, cancellation, and quote-response actions, and avoid sending unnecessary personal or business data. <br>


## Reference(s): <br>
- [PopUp Organizer Skill Page](https://clawhub.ai/eliaskress/popup-organizer) <br>
- [PopUp Login](https://usepopup.com/login) <br>
- [PopUp Organizer API Base URL](https://usepopup.com/api/v1/organizer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with JSON API payloads and HTTP endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POPUP_API_KEY; PopUp list endpoints return JSON data with pagination.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
