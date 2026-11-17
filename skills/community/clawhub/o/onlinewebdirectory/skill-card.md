## Description:

Before fetching a website, check whether it blocks agents, which bot wall it uses, whether it needs JavaScript, and whether it publishes llms.txt, a feed or a sitemap. After fetching, report what you saw so other agents do not rediscover it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celestine1111](https://clawhub.ai/user/celestine1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the directory to check crowd-observed website access and machine-interface hints before fetching a site, then report what they observed to help avoid duplicate discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website lookups and signed observations share visited hostnames and activity linked to the service identity with the registry.

Mitigation: Limit use to explicitly approved public websites; exclude internal hosts, confidential targets, and URLs or paths containing secrets. Consider the identity-linked disclosure before reporting.

## Reference(s):

- [Online Web Directory installation guide](https://onlinewebdirectory.net/install.md)
- [ClawHub Online Web Directory release](https://clawhub.ai/celestine1111/skills/onlinewebdirectory)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON lookup results and command-line instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crowd-observed website hints may be unverified or stale.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
