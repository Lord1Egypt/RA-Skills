## Description:

Formats ORF.at news, sport, and science RSS headlines into source-separated Markdown sections with exact article links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximedogawa](https://clawhub.ai/user/maximedogawa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and format ORF headlines from news, sport, and science RSS feeds, with source-separated sections and exact article links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Austria-news prompts may cause the agent to use ORF when the user intended another source.

Mitigation: Ask users to name the desired source explicitly when they want a specific non-ORF news provider.

Risk: ORF headline responses depend on the availability and current contents of public ORF RSS feeds.

Mitigation: Report feed failures or missing sections clearly and do not invent headlines when a feed cannot be loaded.

## Reference(s):

- [ORF RSS overview](https://rss.orf.at/)
- [ORF news RSS feed](https://rss.orf.at/news.xml)
- [ORF sport RSS feed](https://rss.orf.at/sport.xml)
- [ORF science RSS feed](https://rss.orf.at/science.xml)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with section headings, numbered headlines, and inline article links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public ORF RSS feed items and preserves source-specific news, sport, and science sections.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
