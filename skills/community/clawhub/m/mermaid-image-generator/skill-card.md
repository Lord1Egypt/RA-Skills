## Description: <br>
Generate PNG/SVG images from Mermaid diagram syntax using mermaid.ink API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincent-ng](https://clawhub.ai/user/vincent-ng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to turn Mermaid diagram source into shareable PNG or SVG images for documentation, presentations, and technical communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mermaid diagram text is sent to the external mermaid.ink rendering service. <br>
Mitigation: Do not use this skill for confidential architecture, credentials, customer data, or other sensitive diagrams; use a local Mermaid renderer for those cases. <br>
Risk: Rendering requires network access to mermaid.ink. <br>
Mitigation: Confirm internet connectivity before use, or choose a local renderer when offline operation is required. <br>


## Reference(s): <br>
- [Mermaid image rendering service](https://mermaid.ink) <br>
- [Mermaid Live Editor](https://mermaid.live) <br>
- [ClawHub skill page](https://clawhub.ai/vincent-ng/mermaid-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/vincent-ng) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [PNG or SVG image files generated from Mermaid source, with concise command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports file input or stdin; output format is selected from the requested .png or .svg extension.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
