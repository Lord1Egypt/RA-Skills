## Description: <br>
Compares static April 2026 GPU instance pricing and specifications across AWS, GCP, Azure, Volcengine, and Alibaba Cloud, with filters for GPU model, cloud provider, and region. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales engineers, cloud buyers, and AI infrastructure teams use this skill to compare GPU instance prices and specs across major cloud providers and export filtered results for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static pricing data may be mistaken for current cloud-provider quotes. <br>
Mitigation: Treat results as reference data and verify prices against official provider pricing pages before business decisions. <br>
Risk: Exporting to a chosen output path can replace an existing file at that path. <br>
Mitigation: Choose output paths deliberately and review exported CSV or text files before sharing. <br>


## Reference(s): <br>
- [GPU Pricing Reference Data](references/gpu_pricing.md) <br>
- [ClawHub release page](https://clawhub.ai/dashiming/pans-competitor-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code] <br>
**Output Format:** [Console table, JSON, or CSV; optional file export when an output path is supplied.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses static April 2026 pricing reference data and does not fetch live cloud-provider prices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
