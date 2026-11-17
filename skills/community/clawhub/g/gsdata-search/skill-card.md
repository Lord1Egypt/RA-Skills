## Description:

Searches the projects-databus.gsdata.cn API with a project ID, API signature, keywords, and time filters, returning filtered news result fields as JSON-compatible data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urhd528](https://clawhub.ai/user/urhd528)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query GS Data search results for keywords over a time range when they have valid GS Data project credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API signatures, project IDs, keywords, and time filters are sent to a hardcoded plaintext HTTP endpoint.

Mitigation: Use only non-sensitive credentials and data unless a reviewed HTTPS-capable version is available.

Risk: The command-line interface can expose credentials through shell history or process listings.

Mitigation: Prefer secret-management workflows or environment-based credential handling instead of passing secrets directly on the command line.

Risk: Python dependencies are not pinned reproducibly across artifact files.

Mitigation: Review and pin dependency versions before deployment in controlled environments.

## Reference(s):

- [ClawHub gsdata-search skill page](https://clawhub.ai/urhd528/skills/gsdata-search)
- [GS Data API endpoint](http://projects-databus.gsdata.cn:7777/api-project/service)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and JSON-compatible search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a list of dictionaries containing selected news fields such as title, UUID, media name, post time, emotion, URL, and digest.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact package metadata declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
