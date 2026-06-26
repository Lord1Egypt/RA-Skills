## Description: <br>
Open Food Facts API helps agents search packaged foods by name or barcode and retrieve readable product, ingredient, allergen, Nutri-Score, NOVA, and nutrition details from Open Food Facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to look up packaged food products, compare search results, or retrieve nutrition and ingredient details from barcode-backed Open Food Facts records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Open Food Facts is crowd-sourced, so product data can be incomplete or inaccurate. <br>
Mitigation: Treat returned nutrition, ingredient, allergen, Nutri-Score, and NOVA details as informational and verify important dietary or safety decisions against product packaging or another trusted source. <br>
Risk: The scripts call a public external API and can be rate limited. <br>
Mitigation: Keep requests within the documented lookup and search limits, and retry later when the API reports rate limiting. <br>
Risk: The available security evidence notes pending VirusTotal telemetry. <br>
Mitigation: Review runtime behavior before deployment and avoid sharing sensitive files or credentials with the skill. <br>


## Reference(s): <br>
- [API Coverage](references/api-coverage.md) <br>
- [Open Food Facts API v2](https://world.openfoodfacts.org/api/v2) <br>
- [ClawHub Release Page](https://clawhub.ai/patello/openfoodfacts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted terminal output from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; output is read-only product lookup and search information from Open Food Facts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
