## Description:

Helps agents prepare PowPow posts and manage login, publishing, image uploads, digital-human creation, and post deletion, with previews before confirmed write actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users of PowPow skills use this shared CLI to draft and preview posts, look up images and digital humans, and manage account actions after user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A confirmed action can publish a public post or upload an image.

Mitigation: Review the dry-run preview and obtain user approval before adding --confirm.

Risk: Creating a public digital human costs badges; deleting a post is irreversible.

Mitigation: Check the target and consequences in the preview before confirming either action.

Risk: An account session remains accessible on a shared machine.

Mitigation: Only install when you trust PowPow with your account session, and run logout when finished.

## Reference(s):

- [PowPow CLI release on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Text and Markdown with shell commands and local draft/preview files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions show a dry-run preview and require --confirm to execute.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
