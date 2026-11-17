## Description:

A skill collection for AI programming assistants that indexes GIS, CAD, C#, AI, and IoT project guidance so agents can load targeted domain context for code generation, API usage, troubleshooting, and workflow advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[znlgis](https://clawhub.ai/user/znlgis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select and load focused guidance for geospatial, CAD, .NET, AI agent, and IoT tasks. It helps agents produce commands, code snippets, configuration, and troubleshooting advice for the relevant open-source tool instead of loading the whole collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some examples direct agents toward unverified installers.

Mitigation: Do not run the BillionMail curl-to-bash installer as written; use a pinned release or Docker Compose flow after inspecting the code.

Risk: Some guidance involves powerful administrative or destructive actions.

Mitigation: Require explicit confirmation and backups before recursive deletes or other destructive operations.

Risk: GeoServer examples may expose services with default credentials.

Mitigation: Change default credentials before any network exposure and restrict access to trusted networks.

Risk: OpenClaw-style desktop or shell automation can execute local actions.

Mitigation: Sandbox OpenClaw or disable shell access by default, and require approval for privileged operations.

Risk: Geocoding, RAG uploads, webhooks, and API calls can send sensitive data to external services.

Mitigation: Review data flows, redact secrets and sensitive inputs, and use only approved external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/znlgis/skills/opengis-skills)
- [opengis-skills repository](https://github.com/znlgis/opengis-skills)
- [znlgis upstream blog](https://znlgis.github.io/)
- [GeoPipeAgent pipeline schema](gis/geopipe-agent/reference/pipeline-schema.md)
- [GeoPipeAgent steps reference](gis/geopipe-agent/reference/steps-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, configuration snippets, and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The collection is intended for selective loading of the most relevant one to three skill files.]

## Skill Version(s):

1.0.0 (source: server release evidence and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
