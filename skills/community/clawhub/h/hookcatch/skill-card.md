## Description: <br>
Test webhooks and expose local services using HookCatch, a developer-friendly webhook testing tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HookCatch](https://clawhub.ai/user/HookCatch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to create webhook bins, inspect captured requests, replay webhook traffic, and expose local services through HookCatch during integration testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook payloads and HookCatch API tokens can contain sensitive data. <br>
Mitigation: Treat captured payloads and HOOKCATCH_API_KEY as sensitive, use test data where possible, and prefer private or password-protected bins for sensitive testing. <br>
Risk: Tunnel, replay, delete, and token commands can expose local services or alter HookCatch resources. <br>
Mitigation: Confirm tunnel, replay, delete, and token commands before running them, then stop tunnels or delete bins when testing is complete. <br>


## Reference(s): <br>
- [HookCatch](https://hookcatch.dev) <br>
- [HookCatch documentation](https://docs.hookcatch.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the HookCatch CLI and HOOKCATCH_API_KEY for authenticated operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
