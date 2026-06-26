## Description: <br>
Plan and generate deep links for token swaps on PancakeSwap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan PancakeSwap token swaps, verify token details, and produce a prefilled PancakeSwap link for wallet review. It does not execute swaps or take custody of funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broader local file authority than the core swap-planning workflow appears to need. <br>
Mitigation: Limit local file tools during deployment unless a reviewed workflow requires them. <br>
Risk: The skill silently sends basic system metadata to PancakeSwap during initialization. <br>
Mitigation: Review or remove the startup ping if automatic telemetry is not acceptable for the deployment. <br>
Risk: Opening a prefilled swap page can lead users toward a financial transaction. <br>
Mitigation: Require user confirmation before opening any swap page and remind users to review the transaction in their wallet. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pcs-bot/pcs-swap-planner) <br>
- [PancakeSwap AI homepage](https://github.com/pancakeswap/pancakeswap-ai) <br>
- [PancakeSwap swap interface](https://pancakeswap.finance/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown with links and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces swap-planning guidance and a PancakeSwap deep link for user review; no transaction execution.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
