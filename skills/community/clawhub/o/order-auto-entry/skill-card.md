## Description:

Automates purchase order intake by reading local files or Feishu email attachments, extracting order data with Laiye ADP, writing records and source files to Feishu Base, and notifying reviewers about exceptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

MIT-0

## Use Case:

Supply chain, sales operations, and implementation teams use this skill to process purchase orders from local documents or Feishu mailbox attachments into a Feishu Base review workspace. It helps reviewers focus on item matching, pricing, currency, and new-customer exceptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process mailbox attachments and upload customer order documents to cloud services.

Mitigation: Use it only with explicit per-run consent for mailbox access and customer document uploads.

Risk: The release evidence reports a suspicious security verdict because the described automation performs broad email processing, cloud uploads, Feishu writes, and notifications with limited confirmation.

Mitigation: Review the workflow carefully before installation and require human approval before running it on real orders.

Risk: The artifact contains only SKILL.md while the skill references scripts, configuration, and demo files needed to run the automation.

Mitigation: Require the publisher to include and verify the referenced implementation files before trusting the automation.

Risk: The workflow depends on the Laiye ADP CLI or API for document extraction.

Mitigation: Pin and verify the ADP CLI dependency or API configuration before use.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/Laiye-ADP/adp-skills/tree/main/order-auto-entry-skill-shareable/order-auto-entry)
- [Laiye ADP](https://adp.laiye.com/)
- [ClawHub skill listing](https://clawhub.ai/laiye-adp/skills/order-auto-entry)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve per-run mailbox access, customer document uploads, Feishu Base writes, file uploads, and reviewer notifications.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
