## Description:

Sends LinkedIn connection requests to a list of people through browser automation, handles profile-discovery fallbacks, and tracks connection status in a CSV or TSV file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10madh](https://clawhub.ai/user/10madh)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to send LinkedIn connection requests from a prepared recipient list while recording per-person outcomes. It is intended for browser-mediated outreach workflows that need profile URL fallback, connection-status detection, and incremental CSV or TSV progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates bulk LinkedIn outreach from a real logged-in account and can send actual connection requests.

Mitigation: Review each recipient list before use, keep batches small, and require confirmation before sending requests when account impact matters.

Risk: The security evidence flags anti-detection behavior and recommends careful review.

Mitigation: Use the skill only when the user accepts the account-risk tradeoff, avoid accounts already warned for automation, and stop before exceeding the documented session cap.

Risk: The skill can modify CSV or TSV tracking files and create a progress sidecar file.

Mitigation: Confirm the input file path and columns before running, and keep a backup of the tracking file before automated updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/10madh/skills/linkedin-bulk-connect)
- [LinkedIn Connect Browser Automation Workflow](artifact/references/browser-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser commands, Python snippets, JSON examples, and CSV or TSV status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify the user's tracking file by adding or updating connection-status fields and may maintain a linkedin_progress.json sidecar file.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
