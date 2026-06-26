## Description: <br>
Registers .nad names on the Monad blockchain via Nad Name Service, including availability checks, pricing lookup, dry runs, and transaction registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check .nad name availability, estimate registration costs, and register or list names on Monad through Nad Name Service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet private keys and can submit irreversible blockchain transactions. <br>
Mitigation: Use a dedicated low-balance wallet, prefer dry-run first, and avoid exposing a primary wallet private key. <br>
Risk: Some lookup results may be simulated or overstated as reliable. <br>
Mitigation: Independently verify availability, ownership, pricing, and transaction details through official NNS sources before spending MON. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daaab/nadname-agent) <br>
- [Nad Name Service documentation](https://docs.nad.domains) <br>
- [Nad Name Service app](https://app.nad.domains) <br>
- [Monad Explorer](https://explorer.monad.xyz) <br>
- [Monad Bridge](https://bridge.monad.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration notes, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction steps, dry-run recommendations, wallet setup guidance, and verification warnings.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
