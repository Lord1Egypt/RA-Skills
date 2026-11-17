## Description:

Manage Linkhut bookmarks and inspect tags through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage Linkhut bookmarks and inspect tags through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote code without separate approval.

Mitigation: Review and verify the CLI installation before allowing setup.

Risk: The CLI may have broader effects on installed agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invocation, as described in the CLI command reference.

Risk: Bookmark creation, updates, or deletion can change the user's Linkhut data.

Mitigation: Confirm the exact change before write actions and explicitly approve the target before deletion.

## Reference(s):

- [Linkhut](https://ln.ht)
- [Linkhut API documentation](https://docs.linkhut.org/)
- [oo CLI command reference and environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses are returned as JSON.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
