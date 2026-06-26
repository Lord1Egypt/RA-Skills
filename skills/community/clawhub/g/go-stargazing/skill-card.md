## Description: <br>
Lightweight regional stargazing and astrophotography planning skill for tonight or a specified date, scanning China nationally or by province/city, coarse-filtering by cloud cover, refining with real weather, and returning nightly recommendations with weather details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clhwbd](https://clawhub.ai/user/clhwbd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify China regions that are likely suitable for stargazing or astrophotography on a given night or across several nights. It supports regional planning and weather review, not exact shooting-location selection or site-level safety decisions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Real-weather lookups send queried stargazing coordinates to Open-Meteo. <br>
Mitigation: Use the skill only where sharing those coordinates with Open-Meteo is acceptable, or disable real-weather workflows in restricted environments. <br>
Risk: Python dependencies are listed without pinned versions. <br>
Mitigation: Pin and review dependency versions before deployment in controlled or production environments. <br>
Risk: The tool can read user-supplied JSON boundary files when explicitly provided. <br>
Mitigation: Review polygon file paths and contents before execution, and restrict file access in sensitive environments. <br>
Risk: Recommendations are regional and do not verify exact shooting positions, measured seeing, measured light pollution, or local obstruction. <br>
Mitigation: Treat results as planning guidance, then verify the chosen site, weather, access, and safety conditions before travel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clhwbd/go-stargazing) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Chinese natural-language recommendations or structured JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes regional recommendations, backups, weather indicators, astronomy windows, risk notes, and data completeness notes.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
