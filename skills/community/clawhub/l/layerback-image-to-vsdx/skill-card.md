## Description:

Convert diagram images into fully editable Visio VSDX files with the official LayerBack web app and API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toplocalai](https://clawhub.ai/user/toplocalai)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and diagram authors use this skill to convert screenshots, flowcharts, architecture diagrams, UML, ER diagrams, organization charts, network diagrams, and whiteboard photos into editable Visio files through LayerBack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README install command uses an unpinned latest/global npx invocation.

Mitigation: Prefer a pinned installer version or a locally reviewed install before deployment.

Risk: A custom LayerBack API base URL can receive both uploaded diagrams and the API key.

Mitigation: Use the default LayerBack endpoint unless the custom endpoint is fully trusted.

Risk: Conversion uploads the source image to LayerBack and consumes credits.

Mitigation: Confirm the source file, size, destination, requested format, upload destination, and credit cost before starting conversion.

Risk: Uploaded diagrams may contain confidential or sensitive information.

Mitigation: Do not upload sensitive diagrams without explicit user authorization.

## Reference(s):

- [LayerBack Image to Visio](https://layerback.com/image-to-visio)
- [LayerBack API Documentation](https://layerback.com/docs/api)
- [LayerBack OpenAPI Specification](https://layerback.com/openapi.yaml)
- [LayerBack MCP Server](https://github.com/TopLocalAI/layerback-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and generated local artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce VSDX, PPTX, draw.io, SVG, IR, or preview files after user-confirmed LayerBack conversion.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
