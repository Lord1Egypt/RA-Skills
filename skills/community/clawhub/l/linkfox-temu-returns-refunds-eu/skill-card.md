## Description:

Temu EU returns/refunds and after-sales API access through LinkFox, covering after-sales list and detail lookup, return logistics, return addresses, return-label preparation and upload, signatures, and carrier lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Temu EU sellers use this skill to call Temu Partner EU Returns & Refunds APIs through LinkFox for return, refund, and after-sales workflows. It helps retrieve after-sales records, return logistics, return addresses, carrier data, signatures, and return-label preparation or upload results.

### Deployment Geography for Use:

Europe (Temu EU seller workflows)

## Known Risks and Mitigations:

Risk: Broad Temu proxying may permit calls beyond the intended returns/refunds workflow.

Mitigation: Install only after confirming broad Temu proxying is acceptable, and prefer the fixed returns/refunds scripts over generic proxy scripts where possible.

Risk: LinkFox and Temu tokens, merchant data, and customer/business response data may be exposed through chat logs, shell history, plaintext token storage, or saved response files.

Mitigation: Keep tokens out of chat logs and shell history, secure or avoid plaintext token storage, and review saved response files for sensitive data.

Risk: Repeated calls may have billing or credit impact.

Mitigation: Verify actual billing and credit behavior before running repeated calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-returns-refunds-eu)
- [API reference](references/api.md)
- [Partner EU returns/refunds catalog](references/partner-eu-catalog.md)
- [Temu access token authorization](references/access-token.md)
- [Returns & Refunds API document index](references/apis/README.md)
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; scripts emit JSON responses and saved response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a linkfox session data directory; small responses print JSON, while large responses print summaries unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
