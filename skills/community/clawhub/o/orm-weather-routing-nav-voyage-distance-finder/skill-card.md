## Description: <br>
Calculates voyage distance in nautical miles between global ports using the NavOptima platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy-gaoyue](https://clawhub.ai/user/andy-gaoyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marine operations, chartering, weather-routing, and customer quote teams use this skill to look up port-to-port or multi-port voyage distances, timing estimates, and route-map outputs from NavOptima. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes a shared NavOptima password. <br>
Mitigation: Remove and rotate the exposed credential before installation, and require user-provided or managed secrets instead. <br>
Risk: The workflow forces screenshot sharing without clear per-use consent or recipient checks. <br>
Mitigation: Change screenshot sharing to explicit opt-in and confirm the recipient before sending route outputs. <br>
Risk: The current version is not appropriate for sensitive voyage, customer, or account data. <br>
Mitigation: Do not use it with sensitive operational data until the credential and screenshot-sharing issues are fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy-gaoyue/orm-weather-routing-nav-voyage-distance-finder) <br>
- [Publisher profile](https://clawhub.ai/user/andy-gaoyue) <br>
- [Ocean Right Marine](https://ormwx.com) <br>
- [NavOptima voyage distance](https://nop.ormwx.com/voyage/distance) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown report with voyage distance tables, timing estimates, and route screenshot references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route screenshots and contact details in the response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
