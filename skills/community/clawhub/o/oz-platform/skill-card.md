## Description:

Platform for finding like-minded people based on shared interests and goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poluu](https://clawhub.ai/user/poluu)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to manage an OZ Platform profile, find like-minded people, exchange messages, and monitor incoming activity with consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permits background checks of profile, chat, and recommendation activity with user-control boundaries that require review.

Mitigation: Enable heartbeat checks only after explicit user consent, keep the interval visible to the user, and provide an easy way to pause or revoke access.

Risk: Automatic messaging can contact matches or respond to chats without enough human oversight.

Mitigation: Require confirmation before messaging new matches, sending non-trivial replies, or making profile changes that affect how the user is represented.

Risk: The skill handles profile details, messages, interests, search activity, and an API key.

Mitigation: Store credentials and heartbeat state only in encrypted platform storage, avoid logging secrets or personal data, and send the API key only to the documented OZ API domain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poluu/skills/oz-platform)
- [OZ Platform](https://oz.cmne.life)
- [OZ API base](https://api.oz.cmne.life/)
- [OZ Privacy Policy](https://oz.cmne.life/privacy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint examples, credential handling guidance, rate limits, and consent boundaries.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
