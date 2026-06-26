## Description: <br>
Help first-time inverter UPS buyers calculate load, battery Ah, and VA rating based on their appliances, usage hours, and power situation, with region-aware, brand-neutral guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbazex](https://clawhub.ai/user/arbazex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External buyers use this skill to collect appliance load, backup duration, battery, waveform, grid quality, installation, and regional context, then receive calculated inverter UPS specifications and product-research starting points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product suggestions can become outdated or fail to match local certifications, warranty terms, or availability. <br>
Mitigation: Treat product suggestions as starting points and verify current model specs, safety certifications, local availability, warranty terms, and installation requirements before buying. <br>
Risk: Sizing guidance depends on user-provided appliance wattage, backup duration, grid quality, and installation details. <br>
Mitigation: Ask targeted follow-up questions when inputs are incomplete and recalculate recommendations when measured load or usage assumptions change. <br>
Risk: Lead-acid battery recommendations can involve ventilation and maintenance constraints. <br>
Mitigation: Confirm installation ventilation and maintenance preference before recommending flooded batteries, and warn against closed unventilated placement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arbazex/inverter-ups-buying-consultant) <br>
- [Artifact homepage](https://github.com/arbazex/power-energy-buying-consultants/tree/master/inverter-ups-buying-consultant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown consultation with calculations, prioritized specification lists, and product suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external APIs, runtime dependencies, or environment variables are required; product suggestions should be verified for current specs, certifications, availability, and warranty before purchase.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
