## Description: <br>
TPSCheck lets agents check UK phone numbers against TPS and CTPS and retrieve TPSCheck account usage through OOMOL's oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run TPSCheck phone-number screening and account-credit lookups through an OOMOL-connected TPSCheck account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive TPSCheck credentials through an OOMOL-connected account. <br>
Mitigation: Install only when comfortable connecting TPSCheck through OOMOL, and approve account connection steps intentionally. <br>
Risk: First-time setup includes remote oo CLI installation commands and account or billing links. <br>
Mitigation: Review install commands before running them, and use setup or billing steps only after an auth, connection, or credit failure. <br>


## Reference(s): <br>
- [TPSCheck homepage](https://www.tpscheck.uk) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
