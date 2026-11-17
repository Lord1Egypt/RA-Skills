## Description:

Use AMap to search and read location data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other AMap users can search places, look up addresses and coordinates, check weather, and plan routes using an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run downloaded CLI software that has not been verified.

Mitigation: Review the CLI installation and use a verified release before allowing automatic setup.

Risk: The oo CLI may make startup changes to agent skill directories.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before running oo if those startup writes are unwanted.

Risk: Mapping requests send supplied location or IP information through OOMOL to AMap.

Mitigation: Provide only the location or IP information needed for the requested lookup.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [AMap](https://www.amap.com)
- [AMap Web Service API documentation](https://lbs.amap.com/api/webservice/guide/create-project/get-key)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require the oo CLI and an active AMap connection.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
