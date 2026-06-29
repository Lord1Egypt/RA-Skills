## Description: <br>
ILA East Coast port labor disruption signal - strike probability, inventory buffer, rerouting options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External procurement and logistics agents use this skill to evaluate ILA-covered US East and Gulf Coast port labor disruption risk and decide whether to pre-position inventory, book early sailings, reroute freight, or continue monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EVM private key for x402 paid API calls. <br>
Mitigation: Use a dedicated low-balance wallet or scoped payment setup rather than a wallet holding broad funds. <br>
Risk: The documented $5 tier may be charged automatically when signal probability exceeds 0.65. <br>
Mitigation: Review payment expectations before deployment and monitor usage where logistics agents can trigger calls automatically. <br>


## Reference(s): <br>
- [ILA Labor Signal Homepage](https://datasig.ai/signals/ila-labor) <br>
- [ILA Labor Signal API Example](https://datasig.ai/signals/ila-labor?port=USNYK) <br>
- [Accuracy Ledger](https://datasig.ai/accuracy/stats) <br>
- [Berth Congestion Related Signal](https://datasig.ai/signals/berth-congestion) <br>
- [Blank Sailing Related Signal](https://datasig.ai/signals/blank-sailing) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON response from a GET endpoint with labor risk scores, signal vocabulary, and routing or inventory recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payments; the documented higher tier may fire automatically when probability exceeds 0.65.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
