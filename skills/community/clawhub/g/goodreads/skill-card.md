## Description: <br>
Search for books, get book details and reviews, discover personalized recommendations, and manage reading lists on Goodreads through browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surajssd](https://clawhub.ai/user/surajssd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Readers and book-focused assistants use this skill to search Goodreads, summarize book pages and reviews, discover recommendations, and help manage reading-list actions when the user is logged in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Goodreads in a browser and may change shelves, reading status, or ratings when the user is logged in. <br>
Mitigation: Review Goodreads actions before confirming account changes, and use manual login rather than sharing credentials with the agent. <br>
Risk: Goodreads pages can block, challenge, or change browser automation flows. <br>
Mitigation: Use fresh browser snapshots after navigation, handle authentication or verification prompts explicitly, and provide manual fallback steps when automation is blocked. <br>


## Reference(s): <br>
- [Goodreads Skill Instructions](artifact/SKILL.md) <br>
- [Goodreads Error Handling](artifact/assets/error-handling.md) <br>
- [Goodreads Workflows](artifact/references/WORKFLOWS.md) <br>
- [Goodreads Page Structure and Selectors](artifact/references/SELECTORS.md) <br>
- [Goodreads URL Patterns](artifact/references/URLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown responses with browser action guidance and concise book or shelf-action summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require the user to be logged into Goodreads for recommendations, shelf changes, and ratings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
