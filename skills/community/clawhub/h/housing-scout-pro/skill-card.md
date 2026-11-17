## Description:

Find and monitor housing listings for buying or renting, apply practical filters, compare candidates, run comps, and manage subscription-style alerts in supported regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junyij](https://clawhub.ai/user/junyij)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search sale or lease housing listings, filter and rank candidates, compare comparable properties, and manage listing alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public listing URLs and fetched page content can be sent to the third-party r.jina.ai fetch proxy.

Mitigation: Use only public real-estate URLs that are acceptable to share with an external fetch service.

Risk: Internal, private, credential-bearing, or tokenized URLs could expose sensitive data if passed into listing fetch flows.

Mitigation: Do not pass localhost, private network, cloud metadata, intranet, credential-bearing, or private query-parameter URLs.

Risk: Profiles, caches, subscriptions, and alert destinations are stored in the skill data directory.

Mitigation: Keep the data directory private, review stored chat IDs and subscriptions, and prune profiles, caches, and alert destinations when they are no longer needed.

Risk: Subscription notifications can send listing data outside the local runtime.

Mitigation: Verify notification channels and recipients before enabling subscriptions, and remove outbound targets when they are no longer approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junyij/skills/housing-scout-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with executable shell command examples and JSON notification payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local JSON state for profiles, queries, subscriptions, snapshots, and provider caches.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
