## Description:

Analyzes form fields on a live webpage using browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evalgithub](https://clawhub.ai/user/evalgithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and operators use this skill to inspect a provided webpage URL and summarize the visible form field types and counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent opens user-provided URLs in a browser to inspect page structure.

Mitigation: Only analyze pages the user trusts or intentionally wants inspected.

Risk: Authenticated, private-network, localhost, admin, banking, or similarly sensitive pages can expose page structure during analysis.

Mitigation: Avoid those pages unless the user specifically intends their structure to be inspected.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with concise notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser observations and guidance when authentication, dynamic loading, hidden sections, or multi-section pages affect field counting.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
