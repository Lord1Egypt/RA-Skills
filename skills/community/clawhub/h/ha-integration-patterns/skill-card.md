## Description: <br>
Home Assistant custom integration patterns and architectural decisions. Use when building HACS integrations, custom components, or API bridges for Home Assistant. Covers service response data, HTTP views, storage APIs, and integration architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usimic](https://clawhub.ai/user/usimic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when designing Home Assistant custom integrations, HACS components, or API bridges that need service responses, HTTP views, storage patterns, and release-aware implementation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Home Assistant code based on the examples could expose data or behave incorrectly if HTTP authentication, service response handling, or storage behavior is changed without review. <br>
Mitigation: Review generated code before deployment, require authentication for HTTP views, test service responses with return_response, and use Home Assistant public storage APIs. <br>
Risk: Home Assistant APIs and integration requirements can change across versions. <br>
Mitigation: Check the target Home Assistant version's breaking changes and documentation before implementing or releasing an integration. <br>


## Reference(s): <br>
- [Home Assistant integration basics](https://developers.home-assistant.io/docs/creating_integration_index) <br>
- [Home Assistant service calls](https://developers.home-assistant.io/docs/dev_101_services) <br>
- [Home Assistant HTTP views](https://developers.home-assistant.io/docs/api/webserver) <br>
- [Home Assistant blog](https://www.home-assistant.io/blog/) <br>
- [HACS publishing guidelines](https://hacs.xyz/docs/publish/start) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, bash, JSON, and checklist examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated Home Assistant code should be reviewed before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
