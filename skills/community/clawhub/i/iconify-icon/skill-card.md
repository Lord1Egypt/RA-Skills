## Description:

Provides Iconify icon collection browsing, search, and framework usage examples through the XiaoBenYang service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to browse Iconify icon sets, search for icons, retrieve icon set details, and obtain usage examples for frameworks such as React, Vue, and Svelte.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary marks the release suspicious because code behavior and credential handling are under-disclosed.

Mitigation: Review the skill before installation and use it only when the XiaoBenYang service and release publisher are trusted.

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a dedicated low-privilege key, avoid sharing or committing the workspace, and remove or rotate the key after use.

Risk: Tool calls depend on an external XiaoBenYang API origin.

Mitigation: Confirm the configured API origin before use and avoid overriding it in untrusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/iconify-icon)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP API origin](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown summaries of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key stored as XBY_APIKEY before tool calls can succeed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
