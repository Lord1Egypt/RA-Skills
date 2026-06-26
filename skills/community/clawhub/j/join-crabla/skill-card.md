## Description: <br>
Recruit and orient a new AI agent into Guild KC (Crabla) on the Structs blockchain, including guild signup, substation connection, the first mine-refine-infuse cycle, strategic guidance, and daily human reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to join Guild KC in the Structs blockchain game, perform initial setup, and plan the first gameplay cycle with human approval for wallet transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain wallet actions can alter game state or expose funds if transactions are signed without review. <br>
Mitigation: Use a separate low-value wallet, inspect every transaction before signing, require explicit human approval, and avoid automatic signing. <br>
Risk: Ongoing gameplay automation or event-stream responses can continue beyond the user's intended scope. <br>
Mitigation: Set operating hours, a stop condition, and a reporting cadence before automation; keep event streams informational unless explicit action rules are approved. <br>
Risk: Proof-of-work mining can consume local compute resources. <br>
Mitigation: Start with low difficulty and get human approval before increasing CPU usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abstrct/join-crabla) <br>
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [Structs onboarding skill](https://structs.ai/skills/structs-onboarding/SKILL) <br>
- [Structs mining skill](https://structs.ai/skills/structs-mining/SKILL) <br>
- [Structs energy skill](https://structs.ai/skills/structs-energy/SKILL) <br>
- [Structs building skill](https://structs.ai/skills/structs-building/SKILL) <br>
- [Structs streaming skill](https://structs.ai/skills/structs-streaming/SKILL) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human review before signing blockchain transactions.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
