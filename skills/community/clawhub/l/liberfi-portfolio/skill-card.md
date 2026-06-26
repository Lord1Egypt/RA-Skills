## Description: <br>
Analyze wallet portfolios on supported blockchains, including token holdings, transaction activity, PnL statistics, total net worth, and authenticated LiberFi TEE wallet portfolio data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombmod](https://clawhub.ai/user/bombmod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect public wallet portfolio data or, after explicit authentication, review the user's own LiberFi TEE wallet holdings, activity, PnL, and net worth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and use a global LiberFi CLI, and the security verdict marks this release as suspicious. <br>
Mitigation: Install only from a trusted source, prefer a pinned or sandboxed install, and require explicit approval before installing or running the CLI. <br>
Risk: Authenticated `me` commands can access private LiberFi wallet portfolio data. <br>
Mitigation: Use authenticated commands only after confirming the user intends to access their own portfolio, and verify how login tokens are stored, revoked, or removed. <br>


## Reference(s): <br>
- [LiberFi homepage](https://liberfi.io) <br>
- [ClawHub release page](https://clawhub.ai/bombmod/liberfi-portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with CLI commands and portfolio summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON CLI responses as source material for human-facing portfolio reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
