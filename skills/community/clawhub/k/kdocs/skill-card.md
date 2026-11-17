## Description:

Kdocs helps agents retrieve and summarize titles, authors, update times, links, and key content from public Kingsoft Docs shares, templates, and product pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to organize visible information from public Kingsoft Docs document shares, template listings, and product pages into concise summaries with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may provide a private or sensitive Kingsoft Docs link and expose visible document content to the agent session.

Mitigation: Use the skill only with public pages or documents the user is comfortable sharing in the agent session.

Risk: Dynamic page loading may produce incomplete summaries if visible page content is collected too early.

Mitigation: Wait for public pages to finish loading, preserve source links, and review extracted titles, timestamps, and summaries before relying on them.

Risk: Repeated access to public pages can create unnecessary load or conflict with platform expectations.

Mitigation: Apply frequency controls and avoid repeated visits when summarizing public shares, templates, or product pages.

## Reference(s):

- [Kingsoft Docs homepage](https://www.kdocs.cn/)
- [ClawHub Kdocs skill page](https://clawhub.ai/codekungfu/skills/kdocs)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain-text summaries with extracted public-page metadata and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include titles, authors, update times, paragraph summaries, tags, template names, product features, version information, and source URLs.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
