## Description:

ORF fetches German ORF news items, formats a non-sport digest, and generates a cartoon ZiB studio image reflecting the selected stories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpojer](https://clawhub.ai/user/cpojer)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to request a concise German ORF news digest focused on Austrian and international politics, excluding sports. It returns individual headline messages with age and source link, then produces a related ZiB-style generated image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts ORF RSS endpoints and a Google/Gemini image-generation service.

Mitigation: Review and document external network use before installation or deployment.

Risk: The image-generation script reads a Gemini API key from GEMINI_API_KEY or OpenClaw configuration.

Mitigation: Use scoped credentials, keep keys out of shared logs and files, and confirm the configured account is approved for this use.

Risk: The setup script downloads unpinned Python packages when first run.

Mitigation: Pin and review package versions before use in controlled or commercial environments.

## Reference(s):

- [ClawHub ORF skill page](https://clawhub.ai/cpojer/skills/orf)
- [ORF News](https://news.orf.at/)
- [ORF RSS feeds](https://rss.orf.at/)
- [ORF News RSS](https://rss.orf.at/news.xml)
- [ORF Austria RSS](https://rss.orf.at/oesterreich.xml)

## Skill Output:

**Output Type(s):** [text, shell commands, image file, guidance]

**Output Format:** [Individual plain-text news messages followed by an image file/media response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default count is 5 items, maximum count is 15, with optional inland or ausland focus.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
