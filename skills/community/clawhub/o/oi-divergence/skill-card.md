## Description: <br>
Open interest divergence from price; detects smart-money positioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request a real-time open-interest divergence signal before directional crypto trades or when comparing smart-money and retail positioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a live EVM private key and can initiate paid x402 requests. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit confirmation before any spending request, and monitor call pricing before use. <br>
Risk: Automatic payment authorization could spend funds without the user noticing each call. <br>
Mitigation: Configure the agent workflow to pause for approval before each paid request and reject repeated or background calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/oi-divergence) <br>
- [APEX Runner OI divergence signal](https://apexrunner.ai/signals/oi-divergence) <br>
- [APEX Runner pricing status](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response from an x402-authenticated GET request, with Markdown usage guidance in the skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and a funded wallet for paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
