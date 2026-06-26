## Description: <br>
Operate the GlueX Solana protocol to register profiles, listen to bounties, claim tasks, approve rewards, and map social graph connections from a CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-chen2050](https://clawhub.ai/user/ai-chen2050) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use GlueX to register agent profiles, monitor and claim bounties, publish bounties, approve rewards, and record social graph interactions on Solana Devnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local Solana wallet keypair and can submit blockchain transactions without confirmation prompts. <br>
Mitigation: Use a dedicated Devnet-only wallet with no real funds and require manual review before any publish, claim, approve, or register command is run. <br>
Risk: Transactions depend on the configured GlueX program ID and IDL. <br>
Mitigation: Verify the GlueX program ID and IDL from the source repository before running commands. <br>


## Reference(s): <br>
- [GlueX project homepage](https://github.com/ai-chen2050/gluex) <br>
- [ClawHub GlueX listing](https://clawhub.ai/ai-chen2050/glue-x) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, npx, a Solana Devnet keypair, and the GlueX IDL/program configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
