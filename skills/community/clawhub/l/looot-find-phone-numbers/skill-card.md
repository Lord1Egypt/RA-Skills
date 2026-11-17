## Description:

Find a phone number. Use when the user says things like "find the mobile number for this LinkedIn profile", "get a phone number for Jane Doe at example.com" or "what is the direct line for this person". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to look up a person's phone number from a LinkedIn profile URL, email address, or name and company domain. The agent reports a match with its line type and confidence, or says when nothing matched.

### Deployment Geography for Use:

Global; provider coverage varies by region.

## Known Risks and Mitigations:

Risk: A phone lookup can expose a person's contact details, and a successful provider call may incur a fee.

Mitigation: Use the lookup for an authorized purpose, inspect and disclose the price, obtain the user's approval before running it, and retain any do-not-call flag with the result.

## Reference(s):

- [looot setup instructions](https://looot.ai/skill.md)
- [Find phone numbers on looot](https://looot.ai/agent-skills/find-phone-numbers)
- [ClawHub release page](https://clawhub.ai/walidboulanouar/skills/looot-find-phone-numbers)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown instructions with shell commands; lookup results as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a phone number when matched, with line type, country code or format, carrier, and match confidence; otherwise reports no match. Coverage varies by region.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
