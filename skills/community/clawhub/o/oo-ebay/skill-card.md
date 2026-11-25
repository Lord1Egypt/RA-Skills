## Description:

Use this skill to read, create, and update eBay data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to retrieve eBay account, order, and shipping information and to record order fulfillment. It provides action guidance and runs through an already connected eBay account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run a remotely downloaded CLI installer, and the scanner could not assess its contents.

Mitigation: Before installing, verify the installer through a trusted CLI source and understand what it changes; the scan found no clear evidence of malicious intent but does not establish safety.

## Reference(s):

- [eBay Fulfillment API documentation](https://developer.ebay.com/develop/api/sell/fulfillment_api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [eBay](https://www.ebay.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can record shipping fulfillment; the skill requires confirmation of the exact payload and effect before write actions.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
