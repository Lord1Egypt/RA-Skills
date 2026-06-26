## Description: <br>
Provides geographic and geolocation API access, including Google Maps services, open geocoders, and IP-to-location lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and query Pilot Protocol geo service agents for address conversion, coordinates, routes, travel time, elevation, timezone, air quality, places, and IP-based location lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Geo queries can disclose sensitive IPs, WiFi or cell identifiers, precise coordinates, or personal addresses to remote agents and providers. <br>
Mitigation: Submit only data you are authorized to share, avoid sensitive location identifiers unless consent and policy allow it, and review requests before sending them. <br>
Risk: The skill delegates work to Pilot Protocol service agents and upstream map or geolocation providers, so routing, cost, availability, and result quality can vary. <br>
Mitigation: Use list-agents and /help to confirm the current agent contract before querying, and review returned JSON or prose before relying on it. <br>
Risk: Flight-tracking requests can be routed through a geo agent listed in the catalog even though a dedicated flights skill is the intended path. <br>
Mitigation: Use the dedicated Pilot service agents flights skill for flight tracking rather than the geo skill's opensky-bbox agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-geo) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON response envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and reachable service agents; responses depend on remote agents and upstream providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
