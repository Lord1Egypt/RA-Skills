## Description: <br>
Uniswap API (uniswap.org). Use this skill for ANY Uniswap API request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Uniswap connector schemas, request quotes, check ERC-20 approval requirements, and create swap transaction calldata through the OOMOL oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare crypto swap transaction calldata after receiving wallet, token pair, amount, and quote inputs. <br>
Mitigation: Confirm the exact swap payload and expected effect with the user before running the write action. <br>
Risk: The skill depends on the OOMOL oo CLI and server-side credentials for access to the Uniswap connector. <br>
Mitigation: Install and use it only when the user trusts OOMOL and has intentionally connected Uniswap API credentials. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/oomol/oo-uniswap-api) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Uniswap API homepage](https://uniswap.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, json] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads; swap creation is a write action requiring user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
