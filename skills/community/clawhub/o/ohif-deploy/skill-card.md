## Description:

Deploy OHIF medical imaging viewer with Docker and configure DICOMweb data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and deployment engineers use this skill to deploy the OHIF medical imaging viewer with Docker and configure DICOMweb data sources for medical imaging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment configuration includes hardcoded external DICOMweb endpoints for medical imaging data.

Mitigation: Replace the endpoints with approved DICOMweb servers and do not use real patient or regulated medical data until the endpoints are verified and intentionally accepted.

Risk: Generated Docker Compose and JSON configuration can affect the runtime environment for the viewer.

Mitigation: Pin reviewed container images and inspect generated docker-compose.yml and config/hosting.json before starting containers.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker Compose and OHIF DICOMweb configuration details.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
