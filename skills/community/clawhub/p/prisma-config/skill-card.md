## Description: <br>
Generates Prisma Access configurations for Strata Cloud Manager (SCM), including security policies, NAT rules, decryption policies, URL filtering profiles, GlobalProtect configurations, and other SCM objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leesandao](https://clawhub.ai/user/leesandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security engineers and developers use this skill to draft SCM API-compatible JSON payloads for Prisma Access configuration objects before reviewing and applying them in their own Strata Cloud Manager workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Prisma Access JSON can materially affect connectivity and access controls if applied without review. <br>
Mitigation: Review generated policies, NAT rules, decryption settings, and GlobalProtect configuration before applying them, and test changes in a staging tenant when possible. <br>
Risk: SCM API credentials could be exposed if users paste secrets into prompts or use overly broad deployment credentials. <br>
Mitigation: Keep credentials out of prompts and use least-privilege SCM API credentials in deployment tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leesandao/prisma-config) <br>
- [Skill homepage](https://github.com/leesandao/prismaaccess-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration, Guidance] <br>
**Output Format:** [SCM API-compatible JSON payloads with endpoint paths and required parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the target API endpoint path, required folder parameter, and query parameters when needed.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
