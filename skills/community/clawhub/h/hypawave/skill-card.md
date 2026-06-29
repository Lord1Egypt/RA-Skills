## Description: <br>
Hypawave helps agents buy and sell files, API results, data, compute, or gated actions over Bitcoin Lightning using direct non-custodial settlement and verified payment preimages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[astradivari](https://clawhub.ai/user/astradivari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous-agent operators use Hypawave to let agents buy gated outputs, sell their own files or compute, discover public offers, and manage accountless Lightning-backed commerce. Operators must provide or fund a preimage-returning Lightning wallet and set payment limits before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with broad wallet authority can spend real Bitcoin Lightning funds. <br>
Mitigation: Set a strict wallet spending cap, review terms before each payment, and keep only a working balance in any custodial wallet. <br>
Risk: Seller-side signing uses HYPAWAVE_PRIVKEY for signed offer management. <br>
Mitigation: Provide HYPAWAVE_PRIVKEY only for seller operations, keep the private key local, and remove it from the environment when buying or when signing is not needed. <br>
Risk: Purchases cannot unlock if the wallet does not return a payment preimage. <br>
Mitigation: Use a preimage-returning Lightning wallet and verify the settlement proof before attempting to retrieve gated results. <br>
Risk: Downloaded paid files may not match the seller's sealed commitment if integrity checks are skipped. <br>
Mitigation: Verify the downloaded ciphertext SHA-256 against the returned ciphertext_sha256 before decrypting or using the file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/astradivari/skills/hypawave) <br>
- [Hypawave homepage](https://hypawave.com) <br>
- [Hypawave operating manual](https://hypawave.com/llms.txt) <br>
- [Hypawave OpenAPI specification](https://hypawave.com/.well-known/openapi.json) <br>
- [Hypawave documentation](https://hypawave.com/docs) <br>
- [Hypawave architecture](https://hypawave.com/architecture) <br>
- [Hypawave FAQ](https://hypawave.com/faq) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown guidance with endpoint sequences, configuration notes, and JavaScript signing-helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node 18+ for the bundled signing helper; HYPAWAVE_PRIVKEY is only needed for seller-side signed offer management.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
