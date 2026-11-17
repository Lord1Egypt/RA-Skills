## Description:

Read a Housecall Pro estimate or invoice your contractor sent you, including line items, totals, tax, amounts still owed, and company details, from a shell with plain curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Homeowners and other customers can use the skill to read a contractor-sent Housecall Pro estimate or invoice and inspect its charges and company details from a shell. They can also decline an estimate option after checking it; approval must be completed in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A document link is a bearer credential that can expose the estimate or invoice and allow a decline.

Mitigation: Keep document links, tokens, and downloaded JSON private; do not put them in shared transcripts or commit them.

Risk: Declining an estimate option notifies the contractor and is not reversible through this workflow.

Mitigation: Read the estimate and verify the exact option before submitting a decline.

Risk: Approving an estimate commits to a quoted price.

Mitigation: Complete approval in the browser and do not try to script it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chrischall/skills/housecallpro-mcp)
- [Housecall Pro consumer API recipes](artifact/references/recipes.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a contractor-sent document link; invoice responses do not include line items.]

## Skill Version(s):

1.3.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
