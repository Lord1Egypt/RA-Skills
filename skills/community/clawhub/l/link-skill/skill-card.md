## Description: <br>
Universal API integration skill for enterprise platforms. Connect to any platform using Swagger/OpenAPI discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use LinkSKILL to discover Swagger/OpenAPI endpoints, configure authentication, and run repeatable API requests against internal or external platforms from a CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles enterprise credentials and authenticated API requests. <br>
Mitigation: Use least-privilege, non-production credentials where possible and review each configured API target before use. <br>
Risk: Token-output commands and local token cache files can expose secrets in logs or on disk. <br>
Mitigation: Avoid running token-output commands in logged environments and delete scripts/.token_cache.json after use. <br>
Risk: Combining a platform configuration with arbitrary full URLs can send credentials to unintended API targets. <br>
Mitigation: Keep platform configs scoped to trusted gateways and avoid mixing configured authentication with arbitrary full URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/link-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local token and Swagger cache JSON files during authenticated API workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
