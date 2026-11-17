## Description:

Guides agents through applying a Nexus2 sports prediction pipeline fix for pandas Timestamp JSON serialization failures and stale fixture ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tktk-ai](https://clawhub.ai/user/tktk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining Nexus2 sports prediction deployments use this skill to understand and apply fixes for JSON serialization crashes and stale fixture ingestion that can cause phantom predictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package describes the intended Nexus2 fixes but does not include the actual patched `publishing/publisher.py` and `nexus.py` files.

Mitigation: Review the publisher's actual patched files before copying them into a Nexus2 installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tktk-ai/skills/nexus2-pipeline-fix)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown with inline file paths and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Descriptive guidance only; the release evidence does not include the patched source files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
