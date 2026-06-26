## Description: <br>
Security best practices for Mapbox access tokens, including scope management, URL restrictions, rotation strategies, and protecting sensitive data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to choose appropriate Mapbox token types, scopes, URL restrictions, storage practices, rotation steps, and incident response actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may apply token rotation, revocation, scope, or URL restriction changes to live Mapbox environments incorrectly. <br>
Mitigation: Verify scopes and URL restrictions before applying changes, stage rotations with a monitoring window, and make dashboard or API changes deliberately. <br>
Risk: Real secret tokens could be pasted into chat during troubleshooting. <br>
Mitigation: Avoid sharing real secret tokens unless explicitly necessary and approved; prefer redacted examples. <br>


## Reference(s): <br>
- [Token Rotation & Monitoring](references/rotation-monitoring.md) <br>
- [Incident Response & Common Mistakes](references/incident-response.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with code, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no executable automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
