## Description: <br>
Get mobility route options worldwide, including fare estimates, ETA, and deeplinks to open supported ride apps through the KLO Mobility A2A agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ubunyod574-max](https://clawhub.ai/user/ubunyod574-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer ride estimate, trip cost, ETA, and route option questions between two places or coordinates. It provides discovery and quote guidance, not booking or payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route queries may include precise coordinates and are sent to a disclosed third-party mobility agent. <br>
Mitigation: Install only if this data sharing is acceptable for the intended users and routes. <br>
Risk: Returned fares and ETAs are estimates and may differ from live provider pricing or availability. <br>
Mitigation: Label estimated values clearly and ask users to confirm fare, ETA, and provider details before booking elsewhere. <br>
Risk: Deeplinks can open third-party ride or route applications. <br>
Mitigation: Review deeplink destinations before opening them or handing them to users. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ubunyod574-max/mobility-quote) <br>
- [A2A Registry Entry](https://a2aregistry.org/?agent=80386a0c-03c9-4bde-b93a-f9e6082937cd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summaries with structured A2A JSON response fields and deeplinks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented HTTPS JSON-RPC example; route queries may include coordinates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
