## Description:

Search and retrieve LightSpeed VT courses, locations, and users through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and support teams can search or retrieve courses, locations, and users from a connected LightSpeed VT account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run remote installers without verified integrity or clear limits on local changes.

Mitigation: Prefer an independently installed, integrity-verified oo CLI; review setup behavior and any installation or update of other skills before proceeding.

Risk: Requests and credentials are handled through the OOMOL connector.

Mitigation: Connect only the intended LightSpeed VT account and consider OOMOL's role in handling requests and credentials.

## Reference(s):

- [LightSpeed VT API documentation](https://lightspeedvt.readme.io/reference/overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [LightSpeed VT](https://lightspeedvt.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with oo CLI commands and JSON request payloads; retrieved data is returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves courses, locations, and users; checks each action's live input schema before making a request.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
