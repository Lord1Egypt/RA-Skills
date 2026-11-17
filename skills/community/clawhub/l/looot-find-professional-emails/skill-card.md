## Description:

Find a professional email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to find a person's work email using their full name and company domain. The agent reports the address with its verification status and confidence score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid provider runs incur a per-call charge.

Mitigation: Show the endpoint and list price, then get user approval before running it.

Risk: A provider may return an unverified address or a low-confidence result.

Mitigation: Report the verification status and confidence, and never present an unverified address as confirmed.

Risk: The security scan had incomplete coverage because a referenced local path could not be resolved.

Mitigation: Review the unavailable path and complete the scan before relying on its clean verdict.

## Reference(s):

- [Looot skill setup instructions](https://looot.ai/skill.md)
- [Find professional emails on Looot](https://looot.ai/agent-skills/find-professional-emails)
- [ClawHub release page](https://clawhub.ai/walidboulanouar/skills/looot-find-professional-emails)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [One line with the email, verification status, and confidence score]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unverified addresses must not be presented as confirmed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
