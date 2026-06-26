## Description: <br>
This skill fetches AI model pricing data from multiple API platforms, calculates model ratios, completion ratios, and group ratios with a unified pricing formula, and outputs standardized JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengmengkaizmk](https://clawhub.ai/user/zhengmengkaizmk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to gather pricing from configured AI API platforms, compute standardized pricing ratios, and compare current results with a saved snapshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches pricing from configured external API endpoints, so results depend on the trustworthiness and availability of those sources. <br>
Mitigation: Review references/pricing_urls.json before running and keep only pricing sources you trust. <br>
Risk: A normal run overwrites the bundled latest pricing snapshot. <br>
Mitigation: Use --no-snapshot when you do not want data/latest_snapshot.json updated. <br>
Risk: Providing an output directory can replace fixed result filenames in that directory. <br>
Mitigation: Choose --output-dir carefully and use a dedicated directory for generated pricing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhengmengkaizmk/model-pricing-calculator) <br>
- [Pricing rules](references/pricing_rules.md) <br>
- [Pricing URL configuration](references/pricing_urls.json) <br>
- [12AI pricing page](https://new.12ai.org/pricing) <br>
- [PackyAPI pricing page](https://www.packyapi.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus standardized JSON blocks and optional JSON snapshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can overwrite data/latest_snapshot.json unless --no-snapshot is used; can write model_ratios.json, completion_ratios.json, and group_ratios.json when --output-dir is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
