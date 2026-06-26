## Description: <br>
OW Seller helps seller agents configure product catalogs, search buyer requests across supported platforms, match opportunities, prepare bid materials, and submit or publish seller content with external shop links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qutongyuan](https://clawhub.ai/user/qutongyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and their agents use this skill to configure inventory, monitor buyer requests, assess matches, prepare bids, and route winning buyers to external shops for transaction completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit bids and publish seller content externally with inconsistent confirmation, endpoint, trigger, and retention controls. <br>
Mitigation: Review high-impact automation paths before installation, keep auto-bidding disabled unless automatic bid submission is intended, and preview destinations and content before broad publishing. <br>
Risk: A configurable OW_API_URL or optional platform endpoint could route product, shop, or bid data to an unintended service. <br>
Mitigation: Verify OW_API_URL and any optional endpoint configuration before use, and prefer trusted HTTPS endpoints. <br>
Risk: Local state files can contain seller contact details, product catalogs, shop links, opportunities, bids, and other business data. <br>
Mitigation: Apply local access and retention controls before storing sensitive contact, business, payment, or buyer data in state files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qutongyuan/ow-seller) <br>
- [Bid preparation pattern](artifact/patterns/bid-preparation.md) <br>
- [Fulfillment pattern](artifact/patterns/fulfillment.md) <br>
- [Media scoring pattern](artifact/patterns/media-scoring.md) <br>
- [Platform search configuration](artifact/patterns/platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance, CLI text output, JSON state/configuration files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local state under state/ and may post bids or seller content to configured HTTPS endpoints.] <br>

## Skill Version(s): <br>
2.5.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
