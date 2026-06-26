## Description: <br>
Read-only access to current German public warnings via the official NINA / warnung.bund.de API for NINA alerts, civil protection alerts, weather warnings, flood warnings, Katwarn-style checks, and active warnings for German cities, districts, or ARS region codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolf128058](https://clawhub.ai/user/wolf128058) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check current public warnings for German locations, districts, ARS codes, or nationwide warning feeds. It can return concise human-readable summaries or JSON enriched with warning details and GeoJSON when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts make outbound HTTPS requests to warnung.bund.de and may send German place names or ARS codes for warning lookup. <br>
Mitigation: Use the skill only where outbound access to warnung.bund.de and location or ARS lookup are acceptable. <br>
Risk: Warning results depend on the public NINA API response and may be incomplete, unavailable, or change over time. <br>
Mitigation: Present results as current API output, avoid overstating certainty, and include detail links or JSON when users need source-level context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wolf128058/nina-warnings) <br>
- [NINA public API base](https://warnung.bund.de/api31) <br>
- [Bundled ARS code cache](references/ars-codes.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Plain text or Markdown summaries, with optional JSON output from the helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include warning count, resolved region, normalized ARS code, sender, severity, effective time, expiry, detail links, descriptions, instructions, and GeoJSON feature counts when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
