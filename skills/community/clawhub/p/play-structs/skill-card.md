## Description: <br>
Guides agents through starting Structs by choosing a guild, creating an account, building initial mining infrastructure, and refining Alpha Matter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and operators use this skill to onboard into the Structs game, configure a wallet-backed player account, and begin mining and refining Alpha Matter on the testnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires wallet setup or recovery and can involve sensitive mnemonics or signing keys. <br>
Mitigation: Use a dedicated testnet or low-value wallet, keep valuable mnemonics out of the agent transcript, and approve key recovery steps deliberately. <br>
Risk: Structs transaction commands are final once submitted, and documented long-running compute commands use -y to auto-submit completion. <br>
Mitigation: Load the referenced safety guidance, verify guild and reactor endpoints, and approve any long-running -y transaction before launch. <br>
Risk: Long-running mining and refining jobs can continue across sessions or fail silently, and concurrent jobs with one signing key can conflict. <br>
Mitigation: Use one signing key for one job at a time and follow the async reconnection flow before starting new work. <br>


## Reference(s): <br>
- [Play Structs on ClawHub](https://clawhub.ai/abstrct/play-structs) <br>
- [Structs SOUL](https://structs.ai/SOUL) <br>
- [Structs Safety Guide](https://structs.ai/SAFETY) <br>
- [Structs Commander Guide](https://structs.ai/COMMANDER) <br>
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [Structs Onboarding Skill](https://structs.ai/skills/structs-onboarding/SKILL) <br>
- [Structs Tools Configuration](https://structs.ai/TOOLS) <br>
- [Structs Guild Directory](https://public.testnet.structs.network/structs/guild) <br>
- [Structs Async Operations](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and external links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet/key-handling guidance, transaction commands, and long-running compute workflows.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
