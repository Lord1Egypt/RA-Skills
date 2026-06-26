## Description: <br>
This skill helps agents parse GPX or KML track files and generate static JPG route maps or interactive HTML route visualizations with elevation profiles and route statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziemen](https://clawhub.ai/user/ziemen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and external users can use this skill to convert recorded GPS tracks into route maps, elevation profiles, and statistics for running, cycling, hiking, or GIS-style review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles a real-looking route sample and local personal file path that may expose precise location or personal context. <br>
Mitigation: Review or remove bundled route samples before installation, sharing, or reuse, and avoid preserving source filenames when processing sensitive tracks. <br>
Risk: Interactive HTML maps can make external tile requests when opened. <br>
Mitigation: Open generated HTML only when external map tile requests are acceptable for the route being visualized. <br>
Risk: Generated outputs can preserve filenames and precise coordinates from trusted GPX or KML inputs. <br>
Mitigation: Use trusted input files and redact or avoid sharing generated outputs that contain sensitive route locations. <br>


## Reference(s): <br>
- [KML / GPX File Format Reference](references/formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, JPG, or HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces parsed track JSON, static route images, or interactive HTML maps depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
