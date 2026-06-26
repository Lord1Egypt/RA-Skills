## Description: <br>
Location Service helps agents geocode addresses and coordinates, parse Google Maps links, calculate distances, and prepare location inputs for weather lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jakah2551](https://clawhub.ai/user/jakah2551) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and external users use this skill to turn addresses, coordinates, or Google Maps URLs into location data, distances, and weather-ready coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location inputs can include sensitive addresses, coordinates, or map links that are sent to third-party geocoding or URL-resolution services. <br>
Mitigation: Use the skill only with location data you are comfortable sharing with those services. <br>
Risk: Short Google Maps links can trigger unintended network requests during redirect resolution. <br>
Mitigation: Avoid untrusted short links until exact allowed hostnames, HTTPS-only resolution, redirect limits, and private-network blocking are enforced. <br>


## Reference(s): <br>
- [OpenStreetMap Nominatim API](references/nominatim_api.md) <br>
- [Location Service Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jakah2551/location-service) <br>
- [Publisher Profile](https://clawhub.ai/user/jakah2551) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include coordinates, addresses, distance values, weather-ready coordinate strings, or error messages from geocoding and URL parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
