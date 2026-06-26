## Description: <br>
Diagnose mobile PDP and cart friction where the add-to-cart (ATC) control is hard to see or reach, simulate scroll paths and thumb zones, flag text-stacked dead zones and tap blind spots, and propose minimal UI refactors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rijoyai](https://clawhub.ai/user/rijoyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce, UX, product, and conversion teams use this skill to diagnose mobile product-page add-to-cart visibility problems, especially when mobile conversion is roughly 50% or more below desktop. It produces structured recommendations for above-fold CTA visibility, button placement, copy density, scroll behavior, and tap blind spots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Illustrative visibility scores can be mistaken for measurements when no page evidence is supplied. <br>
Mitigation: Label simulated or hypothetical scores clearly and request screenshots, URLs, viewport sizes, and mobile-vs-desktop conversion data for page-specific conclusions. <br>
Risk: UX recommendations may be applied without validation against the actual storefront, device viewport, or conversion funnel. <br>
Mitigation: Review proposed layout changes with product and engineering owners and test them on target mobile breakpoints before rollout. <br>


## Reference(s): <br>
- [Mobile ATC visibility playbook](artifact/references/mobile_atc_playbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/rijoyai/mobile-atc) <br>
- [Publisher profile](https://clawhub.ai/user/rijoyai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with scores, tables, bullet lists, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include illustrative scoring when no screenshots, URLs, viewport sizes, or conversion data are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
