## Description: <br>
Pay-per-call access to the Nansen API via MPP (Tempo) for users who want anonymous Nansen access without an API key while using the separate tempo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to set up Tempo and make paid Nansen API requests through `tempo request` when API-key authentication or local-wallet x402 is not desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides use of a funded Tempo payment wallet for paid Nansen API calls. <br>
Mitigation: Use the skill only when the user trusts Tempo, keep a limited wallet balance, and confirm before running paid requests. <br>
Risk: The setup flow uses an external Tempo installer. <br>
Mitigation: Prefer Tempo's official installation guidance and use available checksums, signatures, or pinned releases before installation. <br>
Risk: MPP support is server-side opt-in and may not be available for every endpoint or environment. <br>
Mitigation: Check the paid endpoint discovery response and fall back to an API key or x402 when MPP is unavailable. <br>


## Reference(s): <br>
- [Tempo docs](https://docs.tempo.xyz) <br>
- [MPP protocol](https://mpp.dev/protocol) <br>
- [Nansen CLI npm package](https://www.npmjs.com/package/nansen-cli) <br>
- [Nansen paid endpoint discovery](https://api.nansen.ai/.well-known/x402) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend paid requests through Tempo; users should confirm wallet funding and endpoint support before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
