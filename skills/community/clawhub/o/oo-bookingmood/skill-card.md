## Description:

Searches and reads Bookingmood bookings and products, and checks product availability through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search Bookingmood bookings and products and check product availability through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute changing remote code and introduce broader agent changes without clear approval.

Mitigation: Review setup before enabling; install a verified CLI version separately with approval, check its automatic skill installation settings, and authorize only the Bookingmood access needed.

## Reference(s):

- [Bookingmood API Reference](https://www.bookingmood.com/en-US/api-reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Booking and product records or availability results depend on the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
