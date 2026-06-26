## Description: <br>
Planit generates AI-optimized travel itineraries from natural-language trip requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use Planit to turn a short trip request into an itinerary with transportation options, hotel recommendations, daily attraction schedules, and cost estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel requests, user identifiers, context, skill configuration, and action telemetry are sent to the Planit backend. <br>
Mitigation: Install only when the backend is trusted, avoid submitting sensitive trip details, and review whether telemetry handling meets the deployment's privacy requirements. <br>
Risk: The release evidence reports a hard-coded plain-HTTP backend and notes that the privacy disclosures do not match the code. <br>
Mitigation: Configure a trusted HTTPS backend before setting PLANIT_SECRET, and treat SECURITY.md telemetry claims as unverified until the implementation and disclosures are reconciled. <br>


## Reference(s): <br>
- [Planit on ClawHub](https://clawhub.ai/yoborlon-alpha/planit) <br>
- [Security Policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Structured itinerary response with human-readable travel recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return itinerary, clarification, help, or error responses depending on the request and backend result.] <br>

## Skill Version(s): <br>
2.0.8 (source: release metadata, package.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
