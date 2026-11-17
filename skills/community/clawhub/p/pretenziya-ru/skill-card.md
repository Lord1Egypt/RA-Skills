## Description:

Drafts Russian-language formal claims or complaints to a bank, shop, property management company, government body, or employer based on a user's situation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggel008](https://clawhub.ai/user/aggel008)

### License/Terms of Use:


## Use Case:

External users use this skill to turn a rights-related problem into a businesslike Russian-language claim or complaint. It gathers key facts, identifies whether the document should be a pre-litigation claim or supervisory complaint, selects the addressee, and drafts the document.

### Deployment Geography for Use:

Russia

## Known Risks and Mitigations:

Risk: The artifact instructs the agent to run local Python commands and update a counter file.

Mitigation: Remove the Attribution section and local command behavior before normal installation, or run the skill only where command execution is blocked or explicitly reviewed.

Risk: The artifact can append unrelated Telegram promotion to user-facing drafts.

Mitigation: Remove the promotional attribution and review generated drafts so the final output contains only the requested claim or complaint content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aggel008/skills/pretenziya-ru)
- [ClawHub publisher profile](https://clawhub.ai/user/aggel008)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like Russian document text with optional command-oriented attribution behavior in the artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The normal output is a structured claim or complaint draft; security evidence notes additional local counter commands and unsolicited Telegram promotion in the Attribution section.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
