## Description: <br>
Search Facebook Marketplace listings near a specified location with filters for radius, price range, limit, and pickup-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexanderhe88](https://clawhub.ai/user/alexanderhe88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query a user-provided Marketplace-compatible service for nearby listing candidates and return normalized result data for comparison or follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and location are sent to the configured Marketplace service endpoint. <br>
Mitigation: Use only a local or trusted Marketplace-compatible service and review MARKETPLACE_API_BASE_URL or config.json before running searches. <br>
Risk: Installing dependencies can modify the active Python environment. <br>
Mitigation: Install requirements in a virtual environment before running the command-line script. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/alexanderhe88/marketplace-local-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration] <br>
**Output Format:** [JSON from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include query, location, count, and normalized listing fields such as id, title, price, location, seller_name, image_url, and listing_url.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
