## Description:

Synchronize email activities and quotation events with OKKI CRM as follow-up trail records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to integrate email sending and quotation workflows with OKKI CRM so customer communications and quote events are recorded as follow-up trail records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CRM logging can write sensitive email excerpts and quotation details into OKKI and local files.

Mitigation: Install only with least-privileged OKKI credentials, confirm operator consent for automatic logging, and review what email and quotation fields are included before enabling writes.

Risk: Domain and vector-based customer matching can misfile communications or quotations under the wrong customer.

Mitigation: Require stronger confidence thresholds or human review before automatic trail creation, especially for public-domain addresses, partial matches, and vector-search matches.

Risk: Deduplication and unmatched-customer logs use shared temporary storage by default.

Mitigation: Move runtime records to controlled application storage with appropriate permissions, retention, and monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/okki-email-sync)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with JavaScript APIs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes OKKI CRM trail records and local deduplication or unmatched-customer log files when integrated and executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
