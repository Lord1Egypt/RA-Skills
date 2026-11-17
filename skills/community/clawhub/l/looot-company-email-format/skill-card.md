## Description:

Find a company's email format. Use when the user says things like "what is the email format at example.com", "how are emails written at this company" or "guess the email pattern for example.com". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use a company domain to look up common email address patterns and their reported shares. They can use the results to form a candidate address, then verify it before contacting someone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because a local reference could not be resolved.

Mitigation: Review the unresolved reference before installing the skill.

Risk: A reported company pattern may not identify a valid address for a specific person.

Mitigation: Present generated addresses as guesses and verify them before sending.

Risk: A provider run may incur a per-call charge.

Mitigation: Show the endpoint and listed price, then obtain the user's approval before running a paid call.

## Reference(s):

- [Looot setup guide](https://looot.ai/skill.md)
- [Company email format skill page](https://looot.ai/agent-skills/company-email-format)
- [ClawHub release page](https://clawhub.ai/walidboulanouar/skills/looot-company-email-format)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown summary with email patterns, usage shares, and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pattern results are estimates; verify an address before use.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
