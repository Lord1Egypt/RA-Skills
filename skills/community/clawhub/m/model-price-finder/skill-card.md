## Description: <br>
Simple tool to fetch and view model pricing from TokenRouter, with optional account registration for extended access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yb98k999](https://clawhub.ai/user/yb98k999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect current TokenRouter model prices, compare provider costs, and optionally add selected models to an OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts palebluedot.ai to retrieve public pricing data. <br>
Mitigation: Install only if this network access is acceptable for the environment. <br>
Risk: The enable command edits the local OpenClaw configuration. <br>
Mitigation: Review the generated backup and configuration changes if model behavior changes unexpectedly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yb98k999/model-price-finder) <br>
- [TokenRouter pricing API](https://www.palebluedot.ai/openIntelligence/api/pricing) <br>
- [PaleBlueDot AI](https://www.palebluedot.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown tables and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write OpenClaw configuration when the enable command is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
