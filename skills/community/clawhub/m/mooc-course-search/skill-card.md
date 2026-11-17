## Description:

Searches China University MOOC courses and turns results into course recommendations based on the user's learning goal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acse-yz219](https://clawhub.ai/user/acse-yz219)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and agents use this skill to search for MOOC courses, compare candidate classes, and produce practical course-selection advice for goals such as exams, employment, personal interest, or changing fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Course topics entered by users may be sent to Youdao's MOOC search service.

Mitigation: Avoid including private personal details in course queries and keep shared query terms limited to what is needed for course search.

Risk: Course recommendations may be incomplete when search results are sparse or too broad.

Mitigation: Show the queryList used, explain recommendation rationale, and provide refined follow-up search terms when results are insufficient.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/acse-yz219/skills/mooc-course-search)
- [Youdao MOOC course search endpoint](https://mcp.study.youdao.com/public/mm-course/course/search)
- [Youdao MOOC course detail endpoint](https://mcp.study.youdao.com/public/mm-course/course/detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown course recommendations with query lists, course summaries, rationale, and optional course detail notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the actual queryList used for search and refined follow-up search terms when results are insufficient.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
