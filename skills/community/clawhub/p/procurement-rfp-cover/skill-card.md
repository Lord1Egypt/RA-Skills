## Description:

Turn seller-supplied tender facts into one RFP cover still per project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and procurement support teams use this skill to turn confirmed project and tender notes into RFP cover stills. It plans a free card list first, then submits one approved Beatra image-generation task per project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Beatra account powers for a narrow cover-image workflow.

Mitigation: Install and authorize it only when those account powers are acceptable for the user and environment.

Risk: The Beatra device token is stored locally and shared across Beatra skills.

Mitigation: Keep the credential file private, avoid exposing tokens in chat or logs, and revoke the Beatra device if trust changes.

Risk: Silent automatic package updates are enabled by default.

Mitigation: Disable auto-updates with the documented command when reviewed code must remain fixed.

Risk: Paid generation tasks can consume Beatra credits and may settle at measured usage rather than the prepaid estimate.

Mitigation: Show the live model card and cost estimate before billable work, use one request identity per project, and report returned net charged credits.

## Reference(s):

- [RFP cover workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Installation registration](artifact/references/installation-registration.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [MCP connection](artifact/references/mcp-connection.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/procurement-rfp-cover)
- [Beatra skill homepage](https://beatra.ai/skills/procurement-rfp-cover)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and JSON payloads; generated stills are returned as image files or artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default delivery is 4 to 8 stills, with one paid image-generation task per project.]

## Skill Version(s):

0.1.3 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
