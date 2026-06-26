## Description: <br>
Generates professional LMP-format label JSON from natural language descriptions, saves labels locally by default, and can optionally create a cloud preview link when the user configures an API endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lams001](https://clawhub.ai/user/lams001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn plain-language product, shipping, asset, price tag, and regulated-label requests into printable LMP label files with layout, typography, barcode, QR code, and optional preview-link output. For compliance-style labels, it provides layout and field guidance that must be reviewed against final local regulations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated labels may contain names, addresses, product details, barcodes, or other sensitive content. <br>
Mitigation: Leave apiEndpoint empty for local-only use; if cloud preview is enabled, send labels only to a trusted HTTPS endpoint and avoid sensitive label content when possible. <br>
Risk: The skill writes generated .lmp files to the user's Downloads folder. <br>
Mitigation: Use sanitized filenames, avoid unsanitized user path input, and review saved files before sharing or uploading them. <br>
Risk: Compliance-style labels may not satisfy final legal requirements for a target market. <br>
Mitigation: Treat generated compliance labels as layout and style references, then verify the final label against local regulations and qualified review before market use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lams001/lmp-label-generator) <br>
- [LMP Protocol](https://github.com/lams001/lmp-protocol) <br>
- [LabelMake Pro](https://labelmakepro.com) <br>
- [Label compliance guide](COMPLIANCE.md) <br>
- [Asset label example](references/examples/asset-label.json) <br>
- [Product label example](references/examples/product-label.json) <br>
- [Shipping label example](references/examples/shipping-label.json) <br>
- [Support and issues](https://github.com/lams001/lmp-protocol/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Markdown, API Calls, Guidance] <br>
**Output Format:** [LMP JSON saved as a .lmp file, with Markdown response links and optional preview API request] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Always writes a local .lmp file to Downloads; optionally POSTs generated label content to a configured HTTPS preview endpoint.] <br>

## Skill Version(s): <br>
1.5.5 (source: frontmatter, ClawHub release metadata, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
