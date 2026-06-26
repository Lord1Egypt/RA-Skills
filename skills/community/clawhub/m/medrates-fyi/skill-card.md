## Description: <br>
Query US hospital price transparency data via the MedRates REST API to search medical procedure prices, compare hospitals, and filter by insurance plan and location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimaosipa](https://clawhub.ai/user/dimaosipa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer questions about US hospital procedure costs, compare hospital prices, and narrow results by payer, plan, billing code, or location. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Queries may send sensitive procedure, insurance plan, or location details to a third-party service. <br>
Mitigation: Use only the minimum needed information, avoid names or identifiers, prefer coarse location when possible, and confirm before sending sensitive health-related queries. <br>
Risk: The skill covers US hospital price transparency data only and may omit lower-cost non-hospital alternatives. <br>
Mitigation: State the hospital-only scope when presenting results and note that independent imaging centers, ambulatory surgery centers, clinics, or other providers may have different prices. <br>
Risk: Medical price data can be incomplete, outdated, or vary by payer and plan details. <br>
Mitigation: Present results as estimates or published rates, include relevant payer and plan filters, and advise users to confirm final costs with the provider or insurer. <br>


## Reference(s): <br>
- [MedRates website](https://medrates.fyi) <br>
- [MedRates API base URL](https://data.medrates.fyi) <br>
- [ClawHub skill page](https://clawhub.ai/dimaosipa/medrates-fyi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include hospital price comparisons, API request guidance, and links for follow-up exploration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
