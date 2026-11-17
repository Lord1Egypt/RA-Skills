## Description:

Control Google Nest devices (thermostats, cameras, doorbells) via the Google Smart Device Management API using curl and jq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mitchellbernstein](https://clawhub.ai/user/mitchellbernstein)

### License/Terms of Use:


## Use Case:

External developers and smart-home administrators use this skill to set up Google Smart Device Management API access and generate commands and configuration for listing and controlling Google Nest thermostats, cameras, doorbells, speakers, and displays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe global CLI installation instructions could link an unreviewed or missing helper into a system-wide command path.

Mitigation: Do not run the global ln -sf command as written; install only reviewed included helper files and prefer a user-local path.

Risk: OAuth client secrets and access tokens can expose smart-home devices if stored or shared insecurely.

Mitigation: Use a dedicated Google account or least-privilege project and store tokens in a protected credential store or a 0600 file.

Risk: Commands can change device state or access camera snapshots and streams.

Mitigation: Require explicit user confirmation before changing thermostat, fan, speaker, camera, or doorbell state or accessing camera media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mitchellbernstein/skills/google-home)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google Nest device registration](https://nests.google.com/frame/register-user)
- [Google OAuth token endpoint](https://www.googleapis.com/oauth2/v4/token)
- [Google Smart Device Management devices endpoint](https://smartdevicemanagement.googleapis.com/v1/enterprises/YOUR_PROJECT_ID/devices)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; outputs may include Google Smart Device Management API calls that require OAuth credentials and device permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
