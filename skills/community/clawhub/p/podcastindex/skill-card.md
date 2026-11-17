## Description:

Searches Podcast Index for podcasts and episodes, retrieves podcast and episode details, and summarizes authenticated Podcast Index API results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comicstrip](https://clawhub.ai/user/comicstrip)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to search Podcast Index, look up podcast or episode metadata, explore trending or recent podcasts, and turn API responses into concise user-facing summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podcast Index API credentials may be exposed if pasted into prompts, messages, or logs.

Mitigation: Store credentials in environment or configuration storage and avoid including secrets in conversation text.

Risk: Podcast search terms are sent to Podcast Index and may reveal sensitive interests or research topics.

Mitigation: Avoid sensitive private search terms and review queries before sending authenticated requests.

## Reference(s):

- [Podcast Index API Documentation](https://podcastindex.org/api/docs)
- [ClawHub PodcastIndex Skill](https://clawhub.ai/comicstrip/skills/podcastindex)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries with API request guidance and JSON-derived podcast or episode details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Podcast Index API credentials supplied through PODCASTINDEX_API_KEY and PODCASTINDEX_API_SECRET.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
