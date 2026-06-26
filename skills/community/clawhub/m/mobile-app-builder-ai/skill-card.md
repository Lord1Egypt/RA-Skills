## Description: <br>
Build full-stack web and mobile apps from a text description, including project creation, feature planning, and background Quick Start builds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VersaceXcodes](https://clawhub.ai/user/VersaceXcodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and builders use this skill to create, iterate, deploy, and publish web or Expo mobile app projects through LaunchPulse from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run live deployment, app-store publishing, domain, database, billing, environment-file, and payment-secret workflows. <br>
Mitigation: Require explicit user approval before those commands and review payload files, SQL, environment variables, and secret values before sending them. <br>
Risk: The skill stores or accepts LaunchPulse authentication tokens and may handle credentials for related services. <br>
Mitigation: Use only trusted API endpoints, protect the stored auth token, prefer scoped credentials where possible, and clear stored auth when access is no longer needed. <br>


## Reference(s): <br>
- [LaunchPulse homepage](https://launchpulse.ai) <br>
- [ClawHub skill page](https://clawhub.ai/VersaceXcodes/mobile-app-builder-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns project and session context, preview URLs, feature counts, billing context when applicable, and deployment or publishing status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
