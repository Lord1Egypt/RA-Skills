## Description:

Turn user-supplied public policy digest points into one policy digest still per page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, office staff, and communications teams use this skill to turn already-approved public policy digest points into one still per named page or step. It helps plan, submit, review, and recover Beatra image-generation work without inventing missing policy facts or official document marks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend Beatra credits through paid image-generation tasks.

Mitigation: Require the user to approve the current production card before each paid request, use one opaque client_request_id per page, and report billing.net_charged_credits from the returned task.

Risk: The skill stores a reusable Beatra Device Token locally and the token can authorize broader Beatra tools than this policy-digest workflow needs.

Mitigation: Review the Beatra approval before installation, keep the token only in the protected Beatra credential file, and uninstall or disconnect through the bundled removal workflow when access is no longer needed.

Risk: Silent automatic updates are enabled by default.

Mitigation: Use the documented update controls to disable automatic checks when required, and rely on the bundled updater's package, checksum, and rollback checks for accepted updates.

Risk: Generated policy digest stills may contain unreadable or incorrect small text.

Mitigation: Review visible printed lines against the confirmed page list and treat unreadable text as a review item rather than a certified official notice.

## Reference(s):

- [Policy Digest Workflow](references/workflow.md)
- [Installation and Authentication](references/installation-and-auth.md)
- [Installation Registration](references/installation-registration.md)
- [Tasks and Results](references/tasks-and-results.md)
- [Billing, Errors, and Recovery](references/billing-errors-and-recovery.md)
- [MCP Connection](references/mcp-connection.md)
- [Automatic Updates and Safety](references/automatic-updates-and-safety.md)
- [Uninstall and Disconnect](references/uninstall-and-disconnect.md)
- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/policy-digest-set)
- [Beatra Skill Homepage](https://beatra.ai/skills/policy-digest-set)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown/text planning guidance plus returned image artifacts, task IDs, dimensions, formats, and billing credits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one page still per named page or step, normally as one approved paid Beatra request per page.]

## Skill Version(s):

0.1.2 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
