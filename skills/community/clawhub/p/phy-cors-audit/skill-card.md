## Description: <br>
CORS (Cross-Origin Resource Sharing) misconfiguration auditor that probes live API endpoints with crafted Origin headers, scans common web stacks for insecure CORS middleware patterns, and generates stack-specific CORS configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit CORS behavior on live API endpoints, scan source code for insecure CORS patterns, and produce safer configuration examples for common web frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's CORS audit output and generated configuration are advisory and may be incomplete or incorrect for a specific production environment. <br>
Mitigation: Review generated findings and configuration before use, and validate them against the application's authentication, origin, method, header, and credentials requirements. <br>
Risk: Evidence notes one unsafe CORS example in the skill content. <br>
Mitigation: Treat examples as audit demonstrations unless explicitly marked as fixes, and ensure preflight handling uses the same explicit policy as normal CORS middleware. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-cors-audit) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code blocks, audit findings, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before applying generated CORS changes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
