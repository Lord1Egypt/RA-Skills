## Description:

Query Indian mutual fund NAV data, scheme info, and history via the free MFapi.in REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanaksinghal](https://clawhub.ai/user/kanaksinghal)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to look up Indian mutual fund schemes, latest NAV values, NAV history, and scheme metadata through MFapi.in. It also supports resolving ISINs to scheme codes with a local cache before fetching latest NAV data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund search terms, scheme codes, and ISINs are sent to MFapi.in.

Mitigation: Install and use the skill only when sharing those lookup values with MFapi.in is acceptable.

Risk: The ISIN lookup script stores its scheme-list cache in /tmp, which can be inappropriate on shared or multi-user machines.

Mitigation: Use a private per-user cache directory before relying on ISIN lookup results in shared environments.

## Reference(s):

- [MFapi.in](https://www.mfapi.in)
- [MFapi.in REST API base URL](https://api.mfapi.in)
- [ClawHub skill page](https://clawhub.ai/kanaksinghal/skills/mfapi)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for CLI examples; the optional Python script caches the MFapi scheme list locally for ISIN lookup.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
