## Description:

Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyaryyj](https://clawhub.ai/user/hoyaryyj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch standard web pages, extract readable Markdown, and reduce page clutter before analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global latest-version npm install can change over time and may introduce unexpected package behavior.

Mitigation: Use a pinned or local Defuddle installation before relying on the skill in a managed environment.

Risk: Fetching private-network, localhost, credential-bearing, or sensitive internal URLs can expose content through the extraction workflow.

Mitigation: Use the skill only for web pages that are intentionally selected for fetching and summarization, preferably public pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoyaryyj/skills/kepano-defuddle)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers Defuddle markdown output with --md; can save extracted page content to a file or extract title, description, and domain metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
