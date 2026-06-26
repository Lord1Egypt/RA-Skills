## Description: <br>
Navil Audit guides an agent through OpenClaw security audits covering installed skills, MCP servers, agent configuration, attack simulations, and remediation reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanpantheon](https://clawhub.ai/user/ivanpantheon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit OpenClaw skills, MCP servers, and agent configuration, run safe attack simulations, and generate remediation-oriented security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad security prompts may trigger local scans or pentest-style commands against sensitive OpenClaw and MCP configuration. <br>
Mitigation: Run the skill only for explicit audit tasks, provide exact config paths, and avoid broad home-directory scans. <br>
Risk: The skill depends on the external navil pip package. <br>
Mitigation: Install only when you trust that package and the intended local audit workflow. <br>
Risk: VirusTotal-related checks or generated reports may expose sensitive details if shared without review. <br>
Mitigation: Confirm what any external reputation check sends and redact generated reports before sharing. <br>


## Reference(s): <br>
- [Navil GitHub Repository](https://github.com/navilai/navil) <br>
- [Navil CI/CD Integration Guide](https://github.com/navilai/navil#cicd-integration) <br>
- [ClawHub Skill Page](https://clawhub.ai/ivanpantheon/navil-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON or SARIF scan output, and optional report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security findings are severity-ranked and may include remediation steps and CI/CD-compatible SARIF output.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, server release metadata, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
