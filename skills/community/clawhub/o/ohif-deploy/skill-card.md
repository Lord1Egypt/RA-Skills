## Description: <br>
Deploy OHIF medical imaging viewer with Docker and configure DICOMweb data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and imaging platform operators use this skill to deploy an OHIF viewer with Docker and connect it to DICOMweb-compatible sources such as Orthanc, DCM4CHEE, AWS S3, or custom services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment helper hard-codes external DICOMweb endpoints, which could send viewer traffic to unintended services. <br>
Mitigation: Replace the default DICOMweb URLs with the intended server endpoints before using the deployment around medical data. <br>
Risk: The documented SSL and domain flags are not implemented by the script, so users may assume protections that are not configured. <br>
Mitigation: Verify the generated Docker, NGINX, and OHIF configuration manually and configure TLS/domain handling outside the script when needed. <br>
Risk: The script uses unpinned Docker images and writes deployment files in the working directory. <br>
Mitigation: Review and pin container images, run from a dedicated directory, and check generated files before starting the stack. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and deployment configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Docker Compose, NGINX, and OHIF hosting configuration files when its deployment script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
