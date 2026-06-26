## Description: <br>
Securely fetch credentials from LastPass vault via lpass CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitchrisqueen](https://clawhub.ai/user/gitchrisqueen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to retrieve specific credentials from a local LastPass vault through lpass for deployments, API calls, or logins that require secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose LastPass vault secrets directly to agent output, terminal output, transcripts, logs, or agent context. <br>
Mitigation: Install only when agent access to LastPass secrets is required, keep requests scoped to specific entries and fields, and treat returned values as confidential. <br>
Risk: Raw or notes retrieval can return more sensitive material than the immediate task requires. <br>
Mitigation: Prefer the narrowest needed field, such as password or username, and avoid sending secret output to unrelated tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitchrisqueen/lastpass-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text returned from lpass CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may contain sensitive secrets from LastPass and should be handled as confidential.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
