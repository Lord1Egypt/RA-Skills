## Description: <br>
Structured runbooks and Python examples help teams detect, contain, recover from, and learn from AI agent commerce incidents involving spending loops, escrow abuse, identity compromise, service degradation, and cascade failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operations teams use this guide to prepare response playbooks and automation patterns for commerce-agent incidents. It focuses on detection signals, containment actions, recovery checks, forensics, and post-incident learning for systems that can affect budgets, escrows, reputation, webhooks, and credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide is non-executing, but its examples call live GreenHelix APIs that can change financial state for budgets, escrows, webhooks, or reputation data. <br>
Mitigation: Review the examples before use, start with sandbox or limited-scope test credentials, and add dry-run mode plus explicit confirmations before allowing changes to production resources. <br>
Risk: The skill requires a GREENHELIX_API_KEY and covers workflows involving wallet-like balances and sensitive agent operations. <br>
Mitigation: Use restricted credentials, store keys outside prompts and source files, rotate keys after incident exercises, and limit permissions to the specific read or write actions being tested. <br>
Risk: Automated containment patterns can freeze budgets or cancel escrows if detection thresholds or incident classification are wrong. <br>
Mitigation: Set conservative thresholds, require human approval for production containment until tested, log every action, and maintain rollback steps for budget restoration and false-positive recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-incident-response) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API documentation](https://api.greenhelix.net/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python code examples and inline operational commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied GREENHELIX_API_KEY for examples that call GreenHelix services.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
