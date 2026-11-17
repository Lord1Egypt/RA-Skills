## Description:

Analyzes a target company's technology stack and AI compute needs to produce a customer technical profile for AI compute sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Sales engineers and technical account teams use this skill to profile a target company's public technology signals, estimate GPU demand, and prepare sales entry recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching can be directed at unintended internal targets.

Mitigation: Use only trusted public company domains and avoid running the skill where localhost, private-network services, or cloud metadata endpoints are reachable.

Risk: Advertised data-source coverage may be overstated.

Mitigation: Treat the reported source coverage cautiously until the documentation or implementation is corrected.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain text, JSON, or Markdown company technical profile]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write the generated profile to a file when an output path is provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
