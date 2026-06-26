## Description: <br>
Mapbox (mapbox.com). Use this skill for Mapbox requests including geocoding, routing, and travel matrix tasks through the OOMOL-connected Mapbox connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate Mapbox through an OOMOL-connected account for forward, reverse, and batch geocoding, directions, and travel time or distance matrices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting Mapbox through OOMOL, so prompts and action requests are sent to the OOMOL connector for Mapbox API actions. <br>
Mitigation: Install only when that connection model is acceptable and confirm the connected Mapbox account before use. <br>
Risk: First-time setup may involve running a CLI installer command. <br>
Mitigation: Review installer commands before execution and run setup steps only when an auth, connection, or missing-command error requires them. <br>
Risk: Write, destructive, billing-impacting, or bulk requests can change data or incur cost. <br>
Mitigation: Require explicit user confirmation for the exact payload and intended effect before running those requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-mapbox) <br>
- [Mapbox homepage](https://www.mapbox.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Mapbox icon](https://static.oomol.com/logo/third-party/Mapbox.svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce oo CLI commands and JSON request payloads based on the live connector schema.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
