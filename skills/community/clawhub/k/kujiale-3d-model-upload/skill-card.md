## Description:

Validates and runs the complete 5-step Kujiale OpenAPI 3D model upload flow: STS credentials, OSS upload, model parse trigger, parse status polling, and model submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violalulu](https://clawhub.ai/user/violalulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to test, troubleshoot, or automate 3D model ZIP uploads into a Kujiale tenant through the Kujiale OpenAPI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real run can create and submit assets in the configured Kujiale tenant.

Mitigation: Use dry-run first and install or run the skill only when remote model asset creation is intended.

Risk: Kujiale app credentials are required for real uploads.

Mitigation: Provide credentials through environment variables, avoid passing app secrets on the command line, and rotate credentials if exposure is suspected.

Risk: Default category and location values may not match every tenant or catalog tree.

Mitigation: Verify or override category and location settings before submitting production assets.

Risk: Omitting a ZIP path can cause the script to create and use a placeholder test ZIP.

Mitigation: Provide an explicit ZIP path for real uploads and confirm it matches Kujiale's model package requirements.

Risk: Real execution depends on outbound access to Kujiale OpenAPI and the returned OSS endpoint.

Mitigation: Run in an environment with intentional network access and pin the requests and oss2 dependencies in the execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/violalulu/skills/kujiale-3d-model-upload)
- [Manycore OpenAPI documentation](https://www.manycoreapis.com/openapi/index)
- [Manycore OpenAPI key console](https://www.manycoreapis.com/openapi/console/keys)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON run results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Real runs use Kujiale OpenAPI credentials and return uploadTaskId, filePath, previewImg, and brandGoodId.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
