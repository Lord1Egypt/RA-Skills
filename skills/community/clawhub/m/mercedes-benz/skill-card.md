## Description: <br>
Locate Mercedes-Benz dealerships and search new, used, and certified pre-owned vehicle inventory across the United States using zip code-based filters and vehicle specifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaudata](https://clawhub.ai/user/kaudata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find Mercedes-Benz USA dealers and compare nearby vehicle inventory by zip code, model, price, mileage, year, color, fuel type, and other filters. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: This is an unofficial Mercedes-Benz USA integration, so users may mistake the results for an official MBUSA or NVIDIA service. <br>
Mitigation: Present the skill as third-party and unofficial, and verify critical dealer, price, availability, and vehicle details with Mercedes-Benz USA or the dealer before acting. <br>
Risk: Zip codes and search filters are sent to Mercedes-Benz USA services, and the optional REST server may expose search endpoints if reachable on an untrusted network. <br>
Mitigation: Avoid submitting sensitive location queries, and keep any REST server deployment on a trusted local network unless authentication and access controls are added. <br>


## Reference(s): <br>
- [Mercedes-Benz USA Utilities on ClawHub](https://clawhub.ai/kaudata/mercedes-benz) <br>
- [Artifact README](artifact/README.md) <br>
- [OpenClaw tool schema](artifact/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, API Calls] <br>
**Output Format:** [JSON strings containing dealer or vehicle records with URLs intended for Markdown link presentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns zip code-based dealer and inventory search results, including contact details, vehicle attributes, prices, mileage, availability, image URLs, dealer URLs, and service scheduling URLs when available.] <br>

## Skill Version(s): <br>
0.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
