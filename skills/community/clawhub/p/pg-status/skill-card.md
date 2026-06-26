## Description: <br>
Use when checking ProxyGate status, including balance, usage, listings, tunnel health, earnings, seller profile, or job status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwelten](https://clawhub.ai/user/jwelten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ProxyGate buyers and sellers use this skill to check account, usage, settlement, listing, tunnel, seller profile, and job status. It helps agents propose read-oriented ProxyGate CLI and SDK status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled command reference includes fund movement, proxy request, listing administration, tunnel, job lifecycle, logout, and skill-install commands that go beyond status checks. <br>
Mitigation: Allow read-only commands such as balance, usage, settlements, listings list/docs, and jobs list/get by default; require explicit user request and consequence confirmation before higher-impact commands. <br>
Risk: Status checks may expose account balances, usage history, settlements, listings, or job details. <br>
Mitigation: Review outputs before sharing them and avoid exposing sensitive account or operational details outside the intended session. <br>


## Reference(s): <br>
- [ProxyGate CLI Command Reference](references/commands.md) <br>
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs) <br>
- [ClawHub Pg Status Release Page](https://clawhub.ai/jwelten/pg-status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline bash and TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should emphasize read-only ProxyGate status commands unless the user explicitly asks for a higher-impact action.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
