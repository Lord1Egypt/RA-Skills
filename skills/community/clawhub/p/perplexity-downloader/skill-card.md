## Description:

Download and save Perplexity.ai conversations as individual Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to archive Perplexity.ai conversations from a single thread, a list of URLs, or a full account history into local Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and permanently save a user's Perplexity conversations, including full account history.

Mitigation: Use explicit thread URLs when possible, review content for sensitive details before processing, and decide where to store or delete generated archives.

Risk: Login-gated pages or pasted history content may expose private account information to the agent workflow.

Mitigation: Avoid pasting logged-in home pages unless needed for full-history export; provide only the minimum thread URLs or page text required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/perplexity-downloader)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)
- [Perplexity.ai](https://www.perplexity.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown files plus progress and completion messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves one Markdown file per thread under ~/perplexity-downloader/outputs/ and creates an index file for bulk or history exports.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
