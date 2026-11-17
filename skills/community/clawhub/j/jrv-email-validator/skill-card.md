## Description:

Validate email addresses with syntax checks (RFC 5322), MX record verification, disposable/temporary email detection, and common typo suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to validate individual email addresses or batches of addresses before signups, data cleanup, deliverability checks, or disposable-address screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DNS/MX checks may disclose queried email domains to configured DNS infrastructure.

Mitigation: Use --no-dns for sensitive lists or run DNS checks only in environments approved for the data.

Risk: Batch validation can process files containing sensitive email addresses.

Mitigation: Use only files the operator intentionally selects and handle validation output under the same data controls as the source list.

Risk: Terminal output from untrusted email-list content may be unsafe to display directly.

Mitigation: Prefer JSON output for review workflows or sanitize untrusted input before displaying terminal-formatted results.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text or JSON validation results, with command examples in Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read email addresses from a user-selected file, perform DNS/MX lookups unless disabled, and return a nonzero exit code when any address is invalid.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
