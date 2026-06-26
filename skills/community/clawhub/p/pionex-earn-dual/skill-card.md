## Description: <br>
Helps agents answer Pionex Dual Investment questions, browse products, check rates and balances, review investment history, and prepare invest, revoke, or collect commands through the Pionex CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pibrandon](https://clawhub.ai/user/pibrandon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Pionex Dual Investment workflows through guided CLI commands, including product discovery, yield checks, balance review, investment submission, revocation, and collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help perform real crypto earn actions when Pionex API credentials are configured. <br>
Mitigation: Use a dedicated least-privilege API key, require Earn permission only where needed, and get explicit user confirmation before invest, revoke, or collect actions. <br>
Risk: Credentialed commands may submit unintended investment, revoke, or collect requests if command details are wrong. <br>
Mitigation: Run write operations with --dry-run first, review the full payload with the user, and verify product IDs, client-dual IDs, order state, and current profit values before execution. <br>
Risk: The skill depends on an external npm CLI package for Pionex operations. <br>
Mitigation: Verify the npm package and publisher before installation and install only when the user wants agent assistance with Pionex Dual Investment. <br>


## Reference(s): <br>
- [Pionex](https://www.pionex.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/pibrandon/pionex-earn-dual) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run command payloads and confirmation steps for credentialed Pionex Dual Investment actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
