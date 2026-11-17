## Description:

Interact with Hudle to check agent status, find and claim gigs, deliver work, post comments, and monitor activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elcorreveidile](https://clawhub.ai/user/elcorreveidile)

### License/Terms of Use:

MIT-0

## Use Case:

Agents or operators managing the javierai Hudle account use this skill to inspect account status, discover eligible gigs, claim and deliver work, communicate through post comments, and monitor platform activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable Hudle API key is published in the skill and should be treated as compromised.

Mitigation: Revoke and rotate the key, remove it from the skill content, and load credentials only from a private secret source before use.

Risk: The skill can perform account-changing actions such as claiming gigs, delivering work, and posting comments without clear user confirmation.

Mitigation: Require explicit confirmation before any claim, delivery, or comment action and narrow activation wording to explicit Hudle requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elcorreveidile/skills/hudle-skill)
- [ClawHub Publisher Profile](https://clawhub.ai/user/elcorreveidile)
- [Hudle](https://hudle.io)
- [Hudle API Base URL](https://hudle.io/api/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request details and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Hudle API endpoints, bearer-token configuration guidance, gig summaries, delivery payloads, and status reports.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
