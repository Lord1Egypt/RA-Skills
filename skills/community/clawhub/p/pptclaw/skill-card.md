## Description:

Create and edit presentations by writing slide JSON files directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pptclaw](https://clawhub.ai/user/pptclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, edit, validate, and open presentation decks by manipulating PPTClaw deck JSON files and invoking the pptclaw CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global pptclaw package.

Mitigation: Use a pinned, project-local pptclaw install before allowing the agent to run CLI commands.

Risk: The skill can start a background local editor service.

Mitigation: Approve server startup explicitly and stop or remove the background service when the presentation workflow is complete.

Risk: The skill modifies deck files directly and can download image assets.

Mitigation: Review file changes, validate the deck, and approve image downloads before they are added to project assets.

## Reference(s):

- [PPTClaw Skill Page](https://clawhub.ai/pptclaw/skills/pptclaw)
- [Publisher Profile](https://clawhub.ai/user/pptclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deck file guidance, slide JSON structures, CLI commands, and validation steps for PPTClaw presentation workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
