## Description:

Real-time arrival information for Hong Kong Green Mini Buses (GMB), with fuzzy stop name matching and multi-region route lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenho1394](https://clawhub.ai/user/stevenho1394)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Hong Kong GMB routes and retrieve upcoming arrivals for a route, direction, stop name, and region.

### Deployment Geography for Use:

Global deployment; transit coverage is Hong Kong.

## Known Risks and Mitigations:

Risk: The skill contacts public transit data hosts and writes local cache files.

Mitigation: Use a runtime that enforces the declared domain allowlist and restricts cache reads and writes to the skill cache directory.

Risk: Command safety depends on the platform honoring shell:false argument-array execution.

Mitigation: Invoke the Python tool with shell execution disabled and pass validated arguments as an argument array.

Risk: One route metadata fetch may download up to about 10MB despite smaller limits stated elsewhere in the documentation.

Mitigation: Enforce response-size limits at runtime and reject oversized route metadata responses before caching or parsing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stevenho1394/skills/hk-gmb-arrival)
- [Hong Kong Transport Department GMB ETA API](https://data.etagmb.gov.hk)
- [HK Bus Route Fare List](https://hkbus.github.io/hk-bus-crawling/routeFareList.min.json)
- [Security Audit Remediation](references/security-audit.md)
- [Route 481 Stops and Test Results](references/route-481-stops.md)

## Skill Output:

**Output Type(s):** [JSON, Transit arrival data, Guidance]

**Output Format:** [JSON objects returned by command-line tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Route search returns matching regions or suggestions; arrival lookup returns stop ID, stop name, and up to three HKT arrival times or a bounded error message.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
