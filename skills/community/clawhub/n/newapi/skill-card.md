## Description: <br>
NewAPI helps agents manage a New API gateway account, including models, groups, balance, tokens, and secure token use in config files or shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Calcium-Ion](https://clawhub.ai/user/Calcium-Ion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage New API gateway accounts from an agent session. It supports querying account state, managing tokens, and applying token keys to downstream tools while reducing accidental secret exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has sensitive token-management power for New API accounts. <br>
Mitigation: Install only when the publisher is trusted, prefer exported NEWAPI_* environment variables, keep .env files minimal, and avoid exposing raw token values in chat, files, logs, or command arguments. <br>
Risk: The exec-token action can run a shell command after substituting a real token key. <br>
Mitigation: Prefer apply-token for config-file updates, and review any exec-token command carefully before it runs. <br>
Risk: scan-config redaction is best-effort and may miss secrets in some file formats. <br>
Mitigation: Treat sanitized scans as risk reduction rather than proof that a file contains no secrets, and avoid direct reads of secret-bearing config files. <br>


## Reference(s): <br>
- [ClawHub NewAPI skill page](https://clawhub.ai/Calcium-Ion/newapi) <br>
- [New API project](https://github.com/QuantumNous/new-api) <br>
- [New API website](https://www.newapi.ai) <br>
- [New API API reference index](https://apifox.newapi.ai/llms.txt) <br>
- [New API product documentation index](https://www.newapi.ai/llms.txt) <br>
- [QuantumNous skills repository](https://github.com/QuantumNous/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables and inline shell commands; helper scripts return sanitized text or JSON-derived summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholder-based token handling and best-effort redaction for secret-bearing outputs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
