## Description: <br>
OpenCage lets agents run forward, reverse, and GeoJSON geocoding through an OOMOL-connected OpenCage account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to geocode addresses or places, reverse geocode coordinates, and request GeoJSON geocoding results through their connected OpenCage account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL/OpenCage account and sends geocoding inputs through that integration. <br>
Mitigation: Install only when OpenCage access through OOMOL is intended, and avoid submitting sensitive location data unless the user accepts that service flow. <br>
Risk: The artifact can install and invoke the oo CLI when the command is missing or authentication fails. <br>
Mitigation: Review the oo CLI installation path and only run setup steps after an auth or connection failure. <br>
Risk: Forward geocoding is tagged as a write action in the artifact even though the described behavior is geocoding lookup. <br>
Mitigation: Inspect the live connector schema and confirm the exact payload and expected effect before running tagged actions. <br>


## Reference(s): <br>
- [OpenCage homepage](https://opencagedata.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub OpenCage release](https://clawhub.ai/oomol/oo-opencage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector responses that include data and metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
