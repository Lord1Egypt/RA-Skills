## Description:

Browse and inspect Postman collections, requests, and environments from the terminal using pmctl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbingli](https://clawhub.ai/user/wbingli)

### License/Terms of Use:


## Use Case:

Developers and API engineers use this skill to discover Postman workspace endpoints, inspect request details, resolve environment variables, and build curl-oriented command workflows without opening the Postman GUI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides use of Postman API keys and may surface unmasked environment secrets.

Mitigation: Use a least-privilege Postman API key, avoid putting API keys directly in shell commands, and avoid full or JSON environment output unless secret exposure is acceptable.

Risk: The documented installation uses an unpinned third-party package.

Mitigation: Verify the pmctl package source and version before installing, use a virtual environment, and avoid running installation or commands as administrator.

Risk: The authoritative security verdict for this release is suspicious.

Mitigation: Review the skill before installation and deployment, following the provided security guidance.

## Reference(s):

- [ClawHub pmctl skill page](https://clawhub.ai/wbingli/skills/pmctl)
- [pmctl source repository](https://github.com/wbingli/pmctl)
- [Postman API key settings](https://go.postman.co/settings/me/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON-processing command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that access Postman collections, requests, workspaces, profiles, and environment values through pmctl.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
