## Description:

Provides Git-like version control tools for ArcGIS web maps, enabling branch management, commits, diffs, and sync with ArcGIS Portal using the gitmap CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[14-tr](https://clawhub.ai/user/14-tr)

### License/Terms of Use:


## Use Case:

Developers and GIS engineers use this skill to inspect, version, compare, commit, and synchronize ArcGIS web map changes through GitMap-backed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local server can run credential-bearing map changes without authentication or clear safeguards.

Mitigation: Run it only in a trusted local environment and avoid exposing the localhost service while sensitive repositories or production Portal content are reachable.

Risk: Portal credentials may be supplied through environment variables or tool parameters.

Mitigation: Use least-privilege ArcGIS credentials or scoped tokens, and avoid passing passwords as tool parameters.

## Reference(s):

- [ClawHub Git-Map skill page](https://clawhub.ai/14-tr/skills/gitmap)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON tool responses containing CLI text and lightly structured map or commit data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gitmap-core and ArcGIS Portal credentials; most operations require a local GitMap repository working directory.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
