## Description:

Helps an agent browse and summarize public OSChina project pages and technical articles for lightweight information gathering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical analysts use this skill to gather concise summaries of public OSChina open source project pages, search results, and technical articles. It supports individual page review, project metadata extraction, article key-point summaries, and tag-based trend summaries while avoiding bulk collection or access-control bypass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be misused to request bulk collection, access-control bypass, or automated handling of human checks on OSChina.

Mitigation: Keep requests specific to public pages, control request frequency, require manual handling where human checks appear, and refuse bypass or bulk collection requests.

Risk: Summaries of public project or article pages may omit context or reflect stale page content.

Mitigation: Include source links in outputs and review extracted facts against the current public page before relying on them.

## Reference(s):

- [OSChina Home](https://www.oschina.net/)
- [OSChina Projects](https://www.oschina.net/project)
- [OSChina Search](https://www.oschina.net/search)
- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/oschina)
- [ClawHub Publisher Profile](https://clawhub.ai/user/codekungfu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or concise text summaries with extracted metadata fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project names, languages, stars when shown, licenses, maintenance status, article titles, authors, publish times, tags, engagement counts, links, and trend distributions.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
