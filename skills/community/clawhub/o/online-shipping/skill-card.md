## Description:

Compares courier shipping quotes in China and helps users book pickups, manage shipments, and handle support requests through xdccy.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdccycom](https://clawhub.ai/user/xdccycom)

### License/Terms of Use:

MIT-0

## Use Case:

Customers shipping packages within China can compare estimated courier prices, prepare and confirm pickup orders, view or cancel eligible shipments, and submit or track support requests.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Live account tokens and shipping contact details require careful handling.

Mitigation: Prefer manual browser login to sharing passwords in chat; protect and periodically clear locally stored credentials.

Risk: Submitting an order can incur charges; cancellations and support requests can have irreversible effects.

Mitigation: Review the preview and require explicit user confirmation before each billable or irreversible action.

Risk: The published package contains an unexpected duplicate project and hidden development-memory files.

Mitigation: Review the package before installation; the publisher should remove these files before distribution.

## Reference(s):

- [Shipping price guide](references/price_guide.md)
- [Address recognition guide](references/addr_recognition.md)
- [Ordering guide](references/order_guide.md)
- [Shipment management guide](references/manage_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [Sorted shipping quotes, order and support status in text or Markdown; optional JSON/CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Orders, cancellations, and support requests are previewed before explicit confirmation.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; bundled SKILL.md lists 6.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
