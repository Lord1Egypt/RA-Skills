## Description:

Search and hire mobile vendors for events on PopUp, including vendor discovery, event listings, booking inquiries, and invoice management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliaskress](https://clawhub.ai/user/eliaskress)

### License/Terms of Use:


## Use Case:

External organizers and event teams use this skill to search PopUp vendors, create and manage event listings, send or update vendor inquiries, track invoices, save vendors, and maintain organizer profile details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or cancel live events, inquiries, saved vendors, invoices, and organizer profile data, including actions that may notify vendors.

Mitigation: Use a least-privilege PopUp API key when available and require explicit confirmation after showing the exact event, inquiry, or profile details before mutating account data.

Risk: The README shows an unpinned npx @latest publishing workflow and examples that place live tokens directly in shell commands.

Mitigation: Pin CLI versions for publishing workflows and provide tokens through environment variables or a secret manager instead of inline shell arguments.

## Reference(s):

- [PopUp login and API key setup](https://usepopup.com/login)
- [PopUp Organizer API base URL](https://usepopup.com/api/v1/organizer)
- [ClawHub skill page](https://clawhub.ai/eliaskress/skills/popup-organizer)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with HTTP API details and JSON request or response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the POPUP_API_KEY environment variable for authenticated PopUp organizer API requests.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
