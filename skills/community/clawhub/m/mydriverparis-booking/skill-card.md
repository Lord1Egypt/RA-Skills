## Description:

Get instant quotes and book private chauffeur rides in Paris and across Europe with MyDriverParis, including airport and train station transfers, hourly hire, day trips, and VIP airport Meet & Greet through a public MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skatch](https://clawhub.ai/user/skatch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request prices and book private chauffeur rides with pickup or drop-off in France. It supports airport and train station transfers, city-to-city rides, hourly chauffeur service, private day trips, cancellation policy lookup, and VIP airport Meet & Greet.

### Deployment Geography for Use:

Global, for trips with pickup or drop-off in France

## Known Risks and Mitigations:

Risk: The skill relies on a mutable remote MCP service that handles passenger and itinerary details and generates booking payment links.

Mitigation: Only provide passenger and itinerary details when intentionally requesting a quote or booking, and review the remote service before installation.

Risk: Payment-link destination validation is not shown in the artifact.

Mitigation: Verify the payment link domain and merchant details before paying, and do not treat a ride as confirmed until payment is complete.

## Reference(s):

- [MyDriverParis homepage](https://www.mydriverparis.com)
- [MyDriverParis agent documentation](https://www.mydriverparis.com/llms-full.txt)
- [MyDriverParis public MCP endpoint](https://mcp-mydriverparis.mydriverparis.workers.dev/mcp)
- [ClawHub skill page](https://clawhub.ai/skatch/skills/mydriverparis-booking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quote options, passenger-detail prompts, cancellation-policy guidance, and Stripe payment links returned by the remote MCP service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
