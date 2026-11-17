## Description:

Generates OCAX node passports that summarize local hardware, node identifiers, reputation scores, and supported task types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catcherintheroad-hub](https://clawhub.ai/user/catcherintheroad-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and compute-resource operators use this skill to inspect local node hardware and generate a passport-style summary for OCAX task suitability and reputation status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and displays detailed local hardware and node identity information.

Mitigation: Install only where this local profiling is expected, and review generated passport output before sharing it.

Risk: Generated passport output may expose host characteristics, node identifiers, and reputation data.

Mitigation: Avoid publishing full passport output publicly unless those details are intended to be disclosed.

Risk: Dependency versions are not fully pinned for reproducible installs.

Mitigation: Pin and review dependencies in controlled deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/catcherintheroad-hub/skills/ocax-passport)
- [Publisher Profile](https://clawhub.ai/user/catcherintheroad-hub)
- [Declared Repository](https://github.com/HKUDS/OCAX-Passport)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown summaries and JSON-compatible hardware passport data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are host-dependent and may include local hardware details, generated node identifiers, and computed task scores.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
