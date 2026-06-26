## Description: <br>
Use this skill when onboarding a new agent or operator into Nervix, verifying live federation prerequisites, enrolling through the Nervix flow, and preparing or publishing the related skill bundle to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DansiDanutz](https://clawhub.ai/user/DansiDanutz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to verify Nervix federation access, enroll or validate agent identities, prepare publishable skill bundles, and publish them to ClawHub when credentials are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide persistent Nervix agent enrollment and heartbeat activity without complete lifecycle guidance. <br>
Mitigation: Confirm the target agent name, roles, token storage location, heartbeat stop procedure, and credential revocation or rotation plan before enrollment. <br>
Risk: The skill can guide ClawHub publishing or auto-bump publishing. <br>
Mitigation: Require explicit user approval and a configured ClawHub token before publishing or changing a published bundle. <br>


## Reference(s): <br>
- [Nervix Federation Reference](references/nervix-federation.md) <br>
- [Nervix Site](https://nervix.ai) <br>
- [Nervix tRPC API Root](https://nervix.ai/api/trpc) <br>
- [ClawHub Skill Page](https://clawhub.ai/DansiDanutz/nervix-onboarding) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/DansiDanutz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce enrollment, readiness, publishing, and troubleshooting steps; publishing requires an authorized ClawHub token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
