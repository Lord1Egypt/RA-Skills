## Description:

猫眼电影票购票助手 helps users search Maoyan movies and cinemas, choose showtimes and seats, create ticket orders, open payment links, and check ticket status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoyan-tech](https://clawhub.ai/user/maoyan-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent to complete a Maoyan movie-ticket workflow: finding movies and cinemas, comparing showtimes, selecting seats, creating an order, paying, and checking ticket issuance.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles Maoyan session tokens and stores an AuthKey locally.

Mitigation: Install only when the user is comfortable granting Maoyan session access; avoid exposing token values and prefer safer credential storage or authorization before broader deployment.

Risk: The skill can create ticket orders after user confirmations.

Mitigation: Require explicit user confirmation for seats and order details before order creation, and keep payment as a user-directed link or QR step.

Risk: Some workflows return generated shell command strings for message delivery.

Mitigation: Validate channel and target identifiers and replace returned shell strings with structured shell-free execution before production use.

## Reference(s):

- [Scripts API Reference](references/scripts-api.md)
- [Error Codes Reference](references/error-codes.md)
- [Maoyan Mobile Site](https://m.maoyan.com/)
- [ClawHub Skill Page](https://clawhub.ai/maoyan-tech/skills/maoyan-ticket-booking)
- [Publisher Profile](https://clawhub.ai/user/maoyan-tech)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown conversation responses with JSON-driven shell command examples and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May display movie, cinema, showtime, seat-map, payment, and ticket-status information returned by Maoyan scripts.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
