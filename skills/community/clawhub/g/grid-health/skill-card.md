## Description: <br>
Monitors real-time grid bot performance including fill rate, inventory levels, and status across trading pairs on multiple exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and trading-system operators use this skill to request live grid bot health metrics before adjusting grid parameters or diagnosing fill-rate and inventory issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated use can spend wallet funds on paid x402 requests. <br>
Mitigation: Use a dedicated low-balance wallet or spending controls, verify the per-call cost before automated use, and avoid wallets that hold significant funds. <br>


## Reference(s): <br>
- [ClawHub Grid Health listing](https://clawhub.ai/kynto2001-ctrl/skills/grid-health) <br>
- [APEX Runner Grid Health signal](https://apexrunner.ai/signals/grid-health) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes an x402-authenticated GET request that requires EVM_PRIVATE_KEY and returns paid JSON signal data from APEX Runner.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
