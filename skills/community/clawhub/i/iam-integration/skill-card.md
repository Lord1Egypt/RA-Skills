## Description: <br>
Use when integrating a new service with the IAM (Identity and Access Management) system - covers gRPC client setup, JWT token validation, permission checks, and REST API usage for the changyuanfeilun platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effort02](https://clawhub.ai/user/effort02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when integrating services with an IAM system through gRPC clients or REST APIs. It helps them validate JWT tokens, check permissions, retrieve account information, configure required headers, and avoid common multi-tenancy mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JWT validation, token rotation, or gateway-provided headers could be implemented incorrectly for a specific IAM deployment. <br>
Mitigation: Verify JWT validation and rotation against the deployed IAM configuration, and ensure gateway-set headers cannot be spoofed by clients. <br>
Risk: Service-to-service IAM access could be broader than required. <br>
Mitigation: Use least-privileged IAM client credentials and restrict service-to-service network access before implementing the examples. <br>
Risk: IAM client dependencies may come from untrusted or unexpected repositories. <br>
Mitigation: Confirm dependency sources and versions before adding the referenced IAM clients to a service. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with Java, XML, YAML, REST API, and data model examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable behavior or hidden installation steps were identified by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
