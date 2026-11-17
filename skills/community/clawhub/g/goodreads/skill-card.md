## Description:

Searches for books, gets book details and reviews, discovers personalized recommendations, and manages reading lists on Goodreads through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surajssd](https://clawhub.ai/user/surajssd)

### License/Terms of Use:


## Use Case:

External users use this skill to operate Goodreads in a browser: searching for books, reading book details and reviews, getting recommendations, and managing shelves or ratings when authenticated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When the user is logged into Goodreads, the skill may read account-specific Goodreads pages.

Mitigation: Install only when browser-based Goodreads operation is intended, check authentication before account-specific workflows, and avoid handling user credentials.

Risk: Authenticated workflows can change Goodreads shelves or ratings.

Mitigation: Perform shelf and rating changes only for explicit user requests, then re-snapshot the page to confirm the resulting state.

Risk: Goodreads may block, rate-limit, or change page structure during browser automation.

Mitigation: Use the documented recovery steps: avoid unnecessary re-navigation, re-snapshot after navigation or page-changing actions, inspect screenshots when structure is unclear, and provide manual instructions when automation is blocked.

## Reference(s):

- [Goodreads Skill on ClawHub](https://clawhub.ai/surajssd/skills/goodreads)
- [Goodreads Browser Workflows](references/WORKFLOWS.md)
- [Goodreads Page Structure and Selectors](references/SELECTORS.md)
- [Goodreads URL Patterns](references/URLS.md)
- [Error Handling and Recovery](assets/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with browser-action guidance and concise Goodreads result summaries or confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include book metadata, community review excerpts, recommendation groups, authentication notices, and shelf-action confirmations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
