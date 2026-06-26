## Description: <br>
Query China Happy 8 (KL8) lottery historical data for the latest draw, a specific issue, recent draws, and number frequency analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect a local snapshot of China Happy 8 lottery draw data, including latest issue lookup, recent issue listing, and simple frequency analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stale hardcoded March-April 2026 KL8 data and does not fetch current draw results. <br>
Mitigation: Treat results as historical examples unless the KL8_DATA dictionary is manually updated from an authoritative source. <br>
Risk: The artifact documentation contains unrelated Bilibili notes and broad trigger phrases that may confuse users or agents. <br>
Mitigation: Clean the README content and narrow trigger phrases before relying on the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/kl8-data) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [kl8_data.py](artifact/kl8_data.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python function calls and console text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local python binary; data is a hardcoded March-April 2026 snapshot.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
