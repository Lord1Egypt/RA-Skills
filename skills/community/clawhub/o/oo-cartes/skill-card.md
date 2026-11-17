## Description:

Operate Cartes.io to read, create, update, and delete maps, markers, and user data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Cartes.io account can ask an agent to find public maps and markers or manage their maps and markers. The skill guides the agent to check each action's schema and requires user confirmation before writes or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may install persistent skills for other agents without clear disclosure, affecting agent behavior beyond Cartes.io.

Mitigation: Review the CLI installation and automatic skill synchronization before setup; consider OO_SKILLS_SYNC_DISABLED, use a reviewed CLI release, and retain approval requirements for skill changes and deletions.

Risk: The remote CLI installer is unverified.

Mitigation: Review the installer and use a reviewed CLI release before allowing setup.

## Reference(s):

- [Cartes.io](https://cartes.io/)
- [Cartes.io API documentation](https://docs.cartes.io/developers/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Text]

**Output Format:** [JSON API responses and concise text summaries; shell commands invoke the oo CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change or delete data require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
