## Description:

Publish podcast episodes from RSS + Notion to Substack with reliable Apple Podcasts embedding and image extraction, then generate LinkedIn-ready companion posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

Podcast publishers and content operators use this skill to turn RSS and Notion episode material into Substack posts with working Apple Podcasts embeds and LinkedIn-ready companion copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public publishing actions can distribute incorrect or unapproved episode content.

Mitigation: Require a human review and explicit approval before publishing to Substack or posting LinkedIn copy.

Risk: Runtime package installation can change the execution environment unexpectedly.

Mitigation: Run the skill in an environment where dependencies are pre-provisioned and runtime package installation is disabled.

Risk: Notion-provided image URLs are downloaded during episode export.

Mitigation: Constrain network egress and use the --no-download option unless the Notion sources are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielfoch/skills/podcast-to-substack)
- [Substack Embed Playbook](references/substack-embed-playbook.md)
- [LinkedIn Playbook](references/linkedin-playbook.md)
- [Apple Podcasts show URL](https://podcasts.apple.com/ca/podcast/the-canadian-real-estate-investor/id1634197127)
- [Notion API](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated text copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON episode data, downloaded image files, Substack publishing steps, and LinkedIn post text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
