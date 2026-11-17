## Description:

Instagram carousel skill: plan, write, design and post Instagram carousels that people save and send, for an app, SaaS, product or personal brand. Picks a proven format (step-by-step, listicle, myth vs fact, framework, case study, tweet-card thread, photo story), writes the cover and a slide 2 that works on its own, renders native-looking 1080x1350 JPEG slides locally (Python + Pillow, bundled open-source fonts, no browser, no paid API), writes alt text and a keyword-first caption, then posts the carousel to one or many Instagram accounts with WoopSocial after you approve it, and reads the results back. Use when someone says "instagram carousel," "make a carousel," "carousel post," "carousel for my app," "turn this into a carousel," "educational carousel," "swipe post," "carousel template," or "post a carousel to instagram." Never invents results, reviews or stories, confirms before anything posts. Standalone: needs no other skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT

## Use Case:

Social media creators, marketers, and small teams use this skill to plan and produce Instagram carousels for a brand or product. It creates slide copy, images, alt text, and captions, and can prepare and publish posts through WoopSocial after the user reviews and approves them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft slide images may be uploaded before publication approval, including confidential screenshots.

Mitigation: Preview drafts locally and get explicit permission before uploading them; use OAuth for the connection.

Risk: The optional API-key-in-URL connection method can expose an account credential.

Mitigation: Use OAuth instead of the API-key-in-URL fallback.

Risk: A post could go to the wrong account or use an incorrect caption or schedule.

Mitigation: Review the account, caption, and schedule before approving publication.

## Reference(s):

- [Carousel formats](references/carousel-formats.md)
- [Design rules](references/design-rules.md)
- [Instagram platform guidance](references/instagram-2026.md)
- [WoopSocial connection and publishing](references/woopsocial.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, JSON, API Calls]

**Output Format:** [Carousel slide copy, captions, and alt text as text; 1080x1350 JPEG slide files; structured carousel JSON; and publication or metrics summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Carousel drafts can include up to 20 slides. Publishing requires user review and approval; the skill reads back available post metrics.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
