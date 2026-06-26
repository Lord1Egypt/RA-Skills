## Description: <br>
High-performance Node.js implementation for monitoring Vietnamese Air Quality Indexes with localized city mapping, WAQI data retrieval, and AQI health interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guchigangz](https://clawhub.ai/user/guchigangz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to look up air quality for Vietnamese cities and return current AQI, weather, pollutant, and health-level data from WAQI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City names are sent to WAQI for lookup. <br>
Mitigation: Use only city inputs that are appropriate to share with the WAQI service. <br>
Risk: The skill uses an embedded shared WAQI token that could be revoked, rate-limited, or tied to the publisher's provider account. <br>
Mitigation: Monitor failures and replace the token with an approved service credential before relying on the skill in operational workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guchigangz/js-hanoi-air) <br>
- [Project homepage](https://github.com/picoclaw-skill/aqi-hanoi) <br>
- [WAQI API](https://api.waqi.info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Pretty-printed JSON written to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes success and error objects with city, AQI, level, weather, pollutant, and update timestamp fields when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
