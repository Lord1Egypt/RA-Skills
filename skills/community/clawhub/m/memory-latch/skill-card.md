## Description: <br>
Detect and recover from context resets, memory/index outages, and cache clears with deterministic, trust-preserving reconstruction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OtherPowers](https://clawhub.ai/user/OtherPowers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use memory-latch to recover continuity after context resets, memory outages, or cache clears by separating known from unknown state and moving forward one verified step at a time. The skill also guides explicit confirmation before irreversible actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write continuity state to local .memory-latch files, which could expose sensitive context if users store secrets or unnecessary personal data there. <br>
Mitigation: Keep .memory-latch files free of secrets and sensitive personal data, and review or replace the bundled manifest before relying on it. <br>
Risk: Optional HMAC or wallet-backed consent modes add configuration and signing dependencies that may fail or be misapplied if enabled casually. <br>
Mitigation: Leave optional HMAC and wallet modes disabled unless the required secret storage or signer verification has been intentionally configured. <br>
Risk: Continuity recovery can overstate prior context if unverifiable memories are treated as facts. <br>
Mitigation: Use the skill's known versus unknown reconstruction flow and require one verified next step before continuing risky work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OtherPowers/memory-latch) <br>
- [Skill definition](artifact/skill.md) <br>
- [Bundled manifest example](artifact/manifest.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured state summaries, confirmation prompts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; produces local continuity and consent workflow guidance rather than executable code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
