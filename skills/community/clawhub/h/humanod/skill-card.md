## Description:

Give your AI agent hands in the real world. Hire verified humans for physical tasks, data collection, and physical verification via the Humanod network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[armandobrazil](https://clawhub.ai/user/armandobrazil)

### License/Terms of Use:


## Use Case:

External users and developers use Humanod to delegate paid real-world verification, photography, inspection, and local data-collection tasks through the Humanod API. The skill helps create tasks, review applicants and submitted proof, approve or reject work, cancel tasks, and check wallet balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create paid real-world tasks, hire workers, approve submissions, change task details, and cancel tasks.

Mitigation: Require explicit user confirmation before creating tasks, hiring workers, approving or rejecting submissions, changing prices, or canceling tasks; confirm budget and wallet impact before action.

Risk: The security evidence flags API-key handling in URLs as a concern.

Mitigation: Use a restricted, rotatable Humanod API key where available, avoid sharing keys in chat or URLs where possible, and rotate any key that may have been exposed.

Risk: Physical-world tasking can be misused for surveillance, trespass, harassment, or unauthorized collection of personal or sensitive data.

Mitigation: Decline tasks involving private people, restricted property, harassment, or sensitive data collection unless the user demonstrates authorization, consent, and lawful purpose.

Risk: Approving a submission may release payment for incomplete or incorrect work.

Mitigation: Compare submitted proof against the stated validation criteria before approval; provide specific feedback and request revision or rejection when proof is insufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/armandobrazil/skills/humanod)
- [Humanod App](https://www.humanod.app)
- [Humanod Documentation](https://docs.humanod.app)
- [Humanod Developer Keys](https://www.humanod.app/developer/keys)
- [Humanod API Server](https://humanod-api.onrender.com)

## Skill Output:

**Output Type(s):** [API calls, Text, Configuration, Guidance]

**Output Format:** [API requests and JSON responses with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HUMANOD_API_KEY and explicit user confirmation before paid or state-changing actions.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
