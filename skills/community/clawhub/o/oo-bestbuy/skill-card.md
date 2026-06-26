## Description: <br>
This skill lets an agent search and read Best Buy product, category, store, and review data through the OOMOL bestbuy connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with an OOMOL-connected Best Buy account use this skill to inspect action schemas and run read-only Best Buy lookup actions for products, categories, stores, and reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Best Buy account and can lead the agent through optional CLI installation or login setup. <br>
Mitigation: Install and use it only when the user wants an agent to query Best Buy, and run CLI install or login steps only when intentionally setting up that connection. <br>
Risk: The connector is described as read-only, but its results depend on live Best Buy and OOMOL service access. <br>
Mitigation: Review returned product, store, category, and review data before relying on it for purchasing or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-bestbuy) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Best Buy homepage](https://www.bestbuy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI; Best Buy credentials are handled through the user's OOMOL connection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
