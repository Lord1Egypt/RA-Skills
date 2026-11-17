## Description:

Use when searching public content on a Halo site with Halo CLI, especially for keyword search, site URL based search, result limits, or search without authenticated console access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruibaby](https://clawhub.ai/user/ruibaby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents in running Halo CLI search commands against public Halo sites or profile-selected Halo targets, including keyword searches, result limits, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Omitting `--url` can cause Halo CLI to use an active or selected local profile to choose the search target.

Mitigation: Use `--url` for unauthenticated public-site search, and confirm the selected profile before profile-based searches.

Risk: Search results intended for downstream tooling may be hard to parse if emitted as human-readable text.

Mitigation: Use `--json` when another tool needs to parse Halo search results.

## Reference(s):

- [Halo public website](https://www.halo.run)
- [Halo CLI shared skill reference](../halo-cli-shared)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command options when downstream tools need parseable search results.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
