## Description:

Builds pet-care and dog-training shortlists from public Rover listings accessed through Crawlora, preserving price units and limits on availability and qualification claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents comparing local pet sitters, walkers, or dog trainers use this skill to shortlist public profiles by service, starting rate, location, and attributed experience while identifying questions to confirm before booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location or sensitive pet and household details may be shared with Crawlora during searches.

Mitigation: Use only the location needed for the search and avoid unnecessary home, medical, or account details.

Risk: Public provider claims, starting prices, and sampled reviews may not establish qualifications, safety, total cost, or date availability.

Mitigation: Attribute claims to their listings and ask the provider to confirm qualifications, care needs, full pricing, and availability before deciding.

## Reference(s):

- [Rover endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/pet-care-provider-shortlisting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown provider shortlist and requirement matrix]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, rate units, attributed claims, and unresolved availability and care questions; does not book services.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
