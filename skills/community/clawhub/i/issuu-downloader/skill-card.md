## Description:

Downloads public Issuu documents as high-quality PDFs with proxy support and retry behavior for access reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zykqyer](https://clawhub.ai/user/zykqyer)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user provides a public Issuu URL and needs a local PDF copy for legitimate access, review, or archival workflows. Users remain responsible for complying with Issuu terms and copyright requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound web requests to URLs supplied through the agent.

Mitigation: Run it in a network-restricted environment and provide only legitimate public Issuu document URLs.

Risk: The skill automatically tests common local proxy ports before downloading.

Mitigation: Disable or avoid automatic proxy detection where possible, and supply an explicit trusted proxy only when needed.

Risk: The skill saves downloaded PDF output to local storage.

Mitigation: Use a dedicated working directory and review saved files before sharing or retaining them.

Risk: The skill depends on external Python packages for HTTP requests and PDF conversion.

Mitigation: Review and pin dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zykqyer/skills/issuu-downloader)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [PDF file saved locally with a returned path or status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes downloaded content to a local downloads directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
