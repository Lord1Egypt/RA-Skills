## Description:

Opens arXiv in the user's Brave browser, reusing an existing arXiv tab when possible and verifying the destination before confirming success.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to have an agent open the arXiv homepage in Brave while reusing an existing matching tab or browser session when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusing an existing browser session can expose the user's current arXiv account state if they are already signed in.

Mitigation: Use the skill only to open arXiv; it stops at login, avoids credential handling, and should not be used to manage account settings or modify content.

Risk: Browser automation may open an unintended or duplicate tab if destination matching is not checked.

Mitigation: Reuse an existing matching arXiv tab when available, open only one destination tab otherwise, and verify the arXiv destination before reporting success.

## Reference(s):

- [arXiv homepage](https://arxiv.org/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-arxiv)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown status updates with browser automation steps when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens one arXiv destination tab when no matching tab exists, reuses an existing matching tab when possible, and stops at login pages instead of handling credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
