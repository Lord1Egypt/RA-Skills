## Description:

Turn user-supplied account-opening material checklist lines into a four-to-eight still KYC guide set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn an approved account-opening materials checklist into a consistent set of KYC guide stills, one still per supplied material. It supports planning, confirmation, generation, review, delivery, and recovery for Beatra image-generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a persistent shared Beatra Device Token that can spend credits and access broader media capabilities than this KYC image workflow requires.

Mitigation: Install only when that account access is acceptable, keep the token out of chat and logs, and revoke access from the Beatra Console when the workflow is no longer needed.

Risk: Billable image-generation calls can spend Beatra credits, and prepaid estimates may differ from final measured charges.

Mitigation: Require the production card before paid work, use one approved request per still, preserve request IDs for recovery, and report returned net charged credits.

Risk: Automatic package updates are silent by default.

Mitigation: Use the provided update control to disable automatic updates when review or change control is required.

Risk: Uploaded local files become available to Beatra and may contain sensitive reference material.

Mitigation: Upload only reference files that are truly needed, treat scans or photos as visual references only, and avoid using uploads to infer missing KYC requirements.

Risk: Generated stills may contain unreadable or inaccurate small text and should not be treated as legal or official KYC requirements.

Mitigation: Review visible printed text against the confirmed pack list, report unreadable text as a review item, and avoid presenting generated output as a certified legal opinion.

## Reference(s):

- [KYC Materials Guide Pack Workflow](references/workflow.md)
- [Installation and Authentication](references/installation-and-auth.md)
- [Installation Registration](references/installation-registration.md)
- [Tasks and Results](references/tasks-and-results.md)
- [Billing, Errors, and Recovery](references/billing-errors-and-recovery.md)
- [MCP Connection](references/mcp-connection.md)
- [Automatic Updates and Safety](references/automatic-updates-and-safety.md)
- [Uninstall and Disconnect](references/uninstall-and-disconnect.md)
- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/kyc-guide-set)
- [Beatra Skill Homepage](https://beatra.ai/skills/kyc-guide-set)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated image artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a free pack list before billable generation, then delivers image artifacts with task IDs, resolved models, observed formats and dimensions, and net charged credits.]

## Skill Version(s):

0.1.2 (source: server release evidence and packaged manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
