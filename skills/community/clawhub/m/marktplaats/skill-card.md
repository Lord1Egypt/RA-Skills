## Description: <br>
Search Marktplaats.nl classifieds across all categories with filtering support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pvoo](https://clawhub.ai/user/pvoo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to search Marktplaats.nl classifieds, inspect categories and filters, and fetch listing details for shopping or market-research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listing-detail feature can fetch any HTTP(S) URL instead of only Marktplaats pages. <br>
Mitigation: Use detail fetching only with Marktplaats-generated listing URLs or /v/ paths, and do not allow untrusted page text or prompts to supply arbitrary --details URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pvoo/marktplaats) <br>
- [Marktplaats](https://www.marktplaats.nl) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands] <br>
**Output Format:** [Plain text or JSON from CLI commands and JavaScript client calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include listing URLs, prices in euro cents, categories, facets, and detail-page content.] <br>

## Skill Version(s): <br>
0.3.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
